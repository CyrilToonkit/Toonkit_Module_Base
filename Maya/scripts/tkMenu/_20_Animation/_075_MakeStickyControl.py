import re

import maya.cmds as mc
import pymel.core as pc
import tkMayaCore as tkc

def createVolumeTransform(type=0, name="volume"):
    TYPES = ["Sphere", "Box", "Cone"]
    assert 0 <= type <=2,"Type should be : " + " or ".join([str(i) + " (" + TYPES[i] + ")" for i in range(len(TYPES))])
    
    volShape = mc.createNode("render" + TYPES[type], name=name+"Shape")
    parentT = mc.listRelatives(volShape, parent=True)
    return mc.rename(parentT, name)

def makeSticky(basename="sticky_01"):
    """
    TODO : namespace from meshes + global root (/ns) + set for sticky controllers (/ns)
    """
    USERMSG = "Please select at least one vertex, typically with soft selection in 'global' mode !"
    sel = pc.selected()
    assert len(sel) > 0 and isinstance(sel[0], pc.general.MeshVertex), USERMSG
    
    pinGeoT = sel[0].node().getParent()
    pinGeoShapes = pinGeoT.getShapes()
    pinGeoShape = pinGeoShapes[0]
    pinGeoOrigShape = pinGeoShapes[-1]
    
    hasDeformed = False
    for shape in pinGeoShapes:
        if shape.name().endswith("Deformed"):
            hasDeformed = True
        elif shape.name().endswith("Orig"):
            pinGeoOrigShape = shape
        else:
            pinGeoShape = shape

    softSel = tkc.getSoftSelections()
    #print("pinGeoOrigShape",pinGeoOrigShape)
    #print("pinGeoShape",pinGeoShape)
    #print("soft",softSel)
    
    #Create root
    root = pc.group(name= basename, empty=True)
    basename = root.name()
    
    #Find position for the pin
    pinPos = [0,0,0]
    posCnt = 0
    for selVert in sel:
        if not isinstance(selVert, pc.general.MeshVertex):
            continue
        pinPos += selVert.getPosition(space="world")
        posCnt += 1
    pinPos /= posCnt
    
    closestInfo = tkc.closestPoint(pinGeoT, pinPos)
    uvPin = pc.createNode("uvPin", name=basename + "_uvPin")
    
    nMesh = 0
    uvPin.coordinate[nMesh].coordinateU.set(closestInfo['u'])
    uvPin.coordinate[nMesh].coordinateV.set(closestInfo['v'])
    
    pinGeoOrigShape.worldMesh[0] >> uvPin.originalGeometry
    pinGeoShape.worldMesh[0] >> uvPin.deformedGeometry

    #Create pin and controls
    pinOffset = tkc.getNode(createVolumeTransform(type=1, name=basename + "_Buffer"))
    pinOffsetShape = pinOffset.getShape()
    pinOffsetShape.overrideEnabled.set(True)
    pinOffsetShape.overrideColor.set(7)
    root.addChild(pinOffset)
    uvPin.outputMatrix[nMesh] >> pinOffset.offsetParentMatrix
    
    ctrl = tkc.getNode(createVolumeTransform(type=0, name=basename + "_Ctrl"))
    ctrlShape = ctrl.getShape()
    ctrlShape.overrideEnabled.set(True)
    ctrlShape.overrideColor.set(14)
    pinOffset.addChild(ctrl)
    ctrl.t.set([0,0,0])
    ctrl.r.set([0,0,0])
    ctrl.s.set([1,1,1])

    pc.addAttr(ctrl, longName="ShowBuffer", attributeType="enum", en="False:True", keyable=True, defaultValue=0)
    ctrl.ShowBuffer >> pinOffsetShape.v
    
    pc.addAttr(ctrl, longName="Size", keyable=True, defaultValue=1.0)
    ctrl.Size >> ctrlShape.radius
    
    mult = pc.createNode("multDoubleLinear", name= ctrl.name() + "_sizeMul")
    mult.input2.set(2.0)
    ctrl.Size >> mult.input1
    mult.output >> pinOffsetShape.sizeX
    mult.output >> pinOffsetShape.sizeY
    mult.output >> pinOffsetShape.sizeZ
    
    #Before creating the cluster, disconnect all uvPins temporarily
    pinCons = []
    oldUvPins = pc.listConnections(pinGeoT.getShapes()[0], type="uvPin")

    for oldUvPin in oldUvPins:
        pinCons.append((
            oldUvPin,
            pc.listConnections(oldUvPin.originalGeometry, plugs=True)[0],
            pc.listConnections(oldUvPin.deformedGeometry, plugs=True)[0],
            ))
        pc.disconnectAttr(pinCons[-1][1], oldUvPin.originalGeometry)
        pc.disconnectAttr(pinCons[-1][2], oldUvPin.deformedGeometry)

    #Create the cluster
    selectedShapes = []
    selectedSoftSel = []
    for data in softSel:
        if pc.nodeType(data[0]) == "mesh" and not "Layer" in data[0]:
            selectedShapes.append(data[0])
            selectedSoftSel.append(data)
            
    softSel = selectedSoftSel

    cls, clsHandle = pc.cluster(selectedShapes, name=basename + "Cluster", after=not hasDeformed, before=hasDeformed)
    clsHandle.rp.set([0,0,0])
    clsHandle.sp.set([0,0,0])
    clsHandle.getShape().origin.set([0,0,0])
    clsHandle.v.set(False)
    root.addChild(clsHandle)
    
    #Connect the cluster
    ctrl.t >> clsHandle.t
    ctrl.r >> clsHandle.r
    ctrl.s >> clsHandle.s
    
    pinOffset.worldMatrix[0] >> cls.clusterXforms.preMatrix
    pinOffset.worldInverseMatrix[0] >> cls.clusterXforms.postMatrix 

    #Weight the cluster
    for shapeIndex, shape in enumerate(selectedShapes):
        if pc.nodeType(shape) != "mesh":
            continue

        pntCount = pc.polyEvaluate(shape, vertex=True)
        for pointIndex in range(pntCount):
            cls.weightList[shapeIndex].weights[pointIndex].set(softSel[shapeIndex][1].get(pointIndex, 0.0))
    
    #Reconnect UVPins
    for pin, origSource, deformedSource in pinCons:
        origSource >> pin.originalGeometry
        deformedSource >> pin.deformedGeometry
        
    

makeSticky()
"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Author : Cyril GIBAUD - Toonkit
    Copyright (C) 2014-2017 Toonkit
    http://toonkit-studio.com/

    Toonkit Module Lite is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Toonkit Module Lite is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Toonkit Module Lite.  If not, see <http://www.gnu.org/licenses/>
-------------------------------------------------------------------------------
"""

"""
    Geometry colors manager

    TODO :
    -Manage Transparencies
    -Manage shader types (lambert/blinn/phong)
    -Colors palettes/presets
    -Improve UI (thumbnail, selection perservation)
"""

import os
try:
    from itertools import izip as zip
except:
    pass

import pymel.core as pc
import maya.cmds as mc
import maya.mel as mel

import tkMayaCore as tkc

__author__ = "Cyril GIBAUD - Toonkit"

SHADERTYPES = mc.listNodeTypes('shader')

PREVIZ_COLORS = {}

EXCLUDED_COLOR = (-1,-1,-1)

def to0_255(inColor):
    return (int(inColor[0] * 255), int(inColor[1] * 255), int(inColor[2] * 255))

def to0_1(inColor):
    return (inColor[0] / 255.0, inColor[1] / 255.0, inColor[2] / 255.0)

def assignShader(inMaterial, inObj, inSG=None, inFaces=None):
    #print "assignShader(%s, %s, %s, %s)" % (str(inMaterial), str(inObj), str(inSG), str(inMultiUVs))
    #return None
    shape = inObj
    if mc.nodeType(inObj) == "transform":
        shapes = mc.listRelatives(inObj, shapes=True, fullPath=True)
        if not shapes is None and len(shapes) > 0:
            shape = shapes[0]
        else:
            mc.warning("Can't find any shapes on object %s" % inObj)

    shadingGroup = None

    if inSG != None:
        shadingGroup = inSG
    else:
        nodes = mc.listHistory(inMaterial, future=True, levels=1)
        
        for node in nodes:
            nodeType = mc.nodeType(node)
            if not "initialParticleSE" in node and (nodeType == "shadingEngine" or nodeType == "materialFacade"):
                shadingGroup = node
                break

        #No shading group ?
        if shadingGroup == None:
            shadingGroup = mc.sets(renderable=True, noSurfaceShader=True, empty=True, name=inMaterial+"SG")
            mc.connectAttr(inMaterial + ".outColor", shadingGroup + ".surfaceShader", force=True)

    if inFaces is None:
        mc.sets(shape, forceElement=shadingGroup)
    else:
        mc.sets(["{0}.{1}".format(shape, item) for item in inFaces], forceElement=shadingGroup)

    return shadingGroup

def getShaders(inObj, inFirstOnly=True):
    shaders = []
    shapes = [inObj]
    if mc.nodeType(inObj) == "transform":
        shapes = mc.listRelatives(inObj, shapes=True, fullPath=True)

    #Will store plugs where connections are coming from, to take only the first one into account
    managedPlugs = []

    for shape in shapes:
        shadingGroups = iter(mc.listConnections(shape, type="shadingEngine", connections=True) or [])
        if shadingGroups != None:
            for inputPlug, sGroup in zip(shadingGroups, shadingGroups):
                isPlugManaged = False

                if "initialParticleSE" in sGroup:
                    continue

                #if a connection exist on a parent plug, just skip
                for managedPlug in managedPlugs:
                    if inputPlug.startswith(managedPlug):
                        isPlugManaged = True
                        break

                if isPlugManaged:
                    continue

                #find the shader connected to shading group
                cons = mc.listConnections(sGroup, destination=False)
                for con in cons:
                    if mc.nodeType(con) in SHADERTYPES:
                        shaders.append(con)
                        managedPlugs.append(inputPlug)
                        if inFirstOnly:
                            return shaders
                        break

    return list(set(shaders))

""" PYMEL VERSION
def getShaderFaces(inObject, inShader):
    sgs = mc.listConnections(shaderNode, type="shadingEngine") 
    if len(sgs) > 0:
        cons = sgs[0].dagSetMembers.listConnections(plugs=True)
        for con in cons:
            if con.node() == objectNode:
                return con.objectGrpCompList.get()

    return None
"""

def getShaderFaces(inObject, inShader):
    faces = []

    sgs = mc.listConnections(inShader, type="shadingEngine")
    if len(sgs) > 0:
        attr = "{0}.{1}".format(sgs[0], "dagSetMembers")
        cons = mc.listConnections(attr, plugs=True)
        if cons is None:

            return faces

        for con in cons:
            if con.split(".")[0] == inObject and not ".comp" in con:
                faces.extend(mc.getAttr("{0}.{1}".format(con, "objectGrpCompList")))

    return faces

def gatorShaders(inObj, inRef):
    if inRef.type() == "transform":
        inRef = inRef.getShape()

    shaders = getShaders(inRef.name(), False)

    if len(shaders) == 1:
        assignShader(shaders[0], inObj.name())
        return

    baseShader = None
    faceShaders = [None] * inRef.numFaces()

    for shader in shaders:
        faces = tkc.deserializeComponents(getShaderFaces(inRef.name(), shader))

        if faces is None or len(faces) == 0:
            baseShader = shader
            continue

        for i in range(len(faces)):
            faceShaders[faces[i]] = shader

    sample = tkc.sampleGeometry(inObj, inRef)

    shaders_faces = {}

    totalFaces = 0

    for i in range(len(sample)):
        refPolygonIndex = sample[i]
        shader = faceShaders[refPolygonIndex]

        if shader in shaders_faces:
            shaders_faces[shader].append(i)
        else:
            shaders_faces[shader] = [i]

    for shader, faces in shaders_faces.items():
        assignShader(shader, inObj.name(), inFaces=tkc.serializeComponents(faces))

def roundColor(inColor):
    return (round(inColor[0], 2), round(inColor[1], 2), round(inColor[2], 2))

def getShaderName(inColor):
    return "pre_lambert_{0}_{1}_{2}".format(inColor[0], inColor[1], inColor[2])

def assignColor(inMesh, inColor, inFaces=None, inAddToDict=True):
    global PREVIZ_COLORS
    if inColor[0] == -1:
        return

    shaderName = getShaderName(inColor)

    if not mc.objExists(shaderName):
        mc.shadingNode("lambert", asShader=True, name=shaderName)
        mc.setAttr(shaderName + ".color", *[i / 255.0 for i in inColor])

    assignShader(shaderName, inMesh, inFaces=inFaces)

    if not inAddToDict:
        return

    if not inColor in PREVIZ_COLORS:
        PREVIZ_COLORS[inColor] = []

    shortName = inMesh.split(":")[-1]

    PREVIZ_COLORS[inColor].append(shortName)

    if EXCLUDED_COLOR in PREVIZ_COLORS and shortName in PREVIZ_COLORS[EXCLUDED_COLOR]:
        PREVIZ_COLORS[EXCLUDED_COLOR].remove(shortName)

def addColor(rgb, sel):
    global PREVIZ_COLORS

    if rgb[0] == -1:
        return

    selection = []
    object_faces = {}

    rawSelection = sel

    for selObj in rawSelection:
        soloObj = selObj
        if ".f" in selObj:
            soloObj = selObj.split(".")[0]
            if not soloObj in object_faces:
                object_faces[soloObj] = []
            object_faces[soloObj].append(selObj.split(".")[1])

        selection.append(soloObj)

    if not rgb in PREVIZ_COLORS:
        PREVIZ_COLORS[rgb] = []

    for selObj in selection:
        assignColor(selObj, rgb, object_faces.get(selObj))

        PREVIZ_COLORS[rgb].append(selObj)

        if EXCLUDED_COLOR in PREVIZ_COLORS and selObj in PREVIZ_COLORS[EXCLUDED_COLOR]:
            PREVIZ_COLORS[EXCLUDED_COLOR].remove(selObj)

    getFromScene(True)

def setColors():

    steps = 0
    for shd_color, meshes in PREVIZ_COLORS.items():
        steps += len(meshes)

    gMainProgressBar = None

    if mc.control("palProgressBar", exists=True):
        mc.control("palProgressBar", edit=True, visible=True)
        gMainProgressBar = "palProgressBar"
    else:
        gMainProgressBar = mc.mel.eval('$tmp = $gMainProgressBar')

    mc.progressBar( gMainProgressBar,
    edit=True,
    beginProgress=True,
    isInterruptable=True,
    status="Applying colors",
    maxValue=steps)

    notFound = []
    for shd_color, meshes in PREVIZ_COLORS.items():
        #print shd_color, meshes
        for mesh in meshes:
            mc.progressBar(gMainProgressBar, edit=True, step=1)

            faces = None
            meshName = mesh

            if "." in mesh:
                meshName, faces = meshName.split(".")
                faces = faces.split(";")

            if not mc.objExists(meshName):
                results = mc.ls("*:"+meshName)
                if len(results) > 0:
                    meshName = results[0]

            if mc.objExists(meshName):
                assignColor(meshName, shd_color, faces, False)
                pass
            else:
                notFound.append(mesh)
                mc.warning(mesh + " not found !")

    mc.progressBar(gMainProgressBar, edit=True, endProgress=True)

    if gMainProgressBar == "palProgressBar":
        mc.control("palProgressBar", edit=True, visible=False)

    if len(notFound) > 0:
        mc.warning("Some meshes were not found :\n" + ",".join(notFound))

def colorCommand(inColor):
    global PREVIZ_COLORS
    selection = [n.name() for n in pc.selected()]

    print ("selection",selection)

    if len(selection) == 0:
        mc.warning("Please select some objects to color")
        return

    opaqueColor = (inColor[1], inColor[2], inColor[3])
    opaqueColor = to0_255(roundColor(to0_1(opaqueColor)))

    addColor(opaqueColor, selection)

    mc.select(selection)

def getFromScene(inManagedOnly=False):
    global PREVIZ_COLORS

    excluded = PREVIZ_COLORS.get(EXCLUDED_COLOR, [])

    managed = []

    if inManagedOnly:
        for shd_color, meshes in PREVIZ_COLORS.items():
            for mesh in meshes:
                managed.append(mesh.split(".")[0])
        managed = list(set(managed))

    PREVIZ_COLORS = {}

    meshes = pc.ls(type="mesh")

    for mesh in meshes:
        if mesh.intermediateObject.get():
            continue

        shortName = mesh.getParent().name().split(":")[-1]

        if inManagedOnly and not shortName in managed:
            continue

        if shortName in excluded:
            if not EXCLUDED_COLOR in PREVIZ_COLORS:
                PREVIZ_COLORS[EXCLUDED_COLOR] = []
            PREVIZ_COLORS[EXCLUDED_COLOR].append(shortName)
            continue

        shaders = getShaders(mesh.name(), False)
        if len(shaders) > 0:
            if len(shaders) > 1:
                #print "Multiple shaders",mesh,shaders
                for shader in shaders:
                    faces = getShaderFaces(mesh.name(), shader)
                    if len(faces) == 0:
                        mc.warning("Can't get shader faces from {0} on {1}".format(shader, mesh.name()))
                        continue
                    color = to0_255(mc.getAttr(shader + ".color")[0])
                    if not color in PREVIZ_COLORS:
                        PREVIZ_COLORS[color] = []

                    PREVIZ_COLORS[color].append("{0}.{1}".format(shortName, ";".join(faces)))
            else:
                shader = shaders[0]
                color = to0_255(mc.getAttr(shader + ".color")[0])
                if not color in PREVIZ_COLORS:
                    PREVIZ_COLORS[color] = []

                PREVIZ_COLORS[color].append(shortName)
        else:
            mc.warning("Can't get any shader from {0} !".format(mesh.name()))

    initUI()
    tkc.deleteUnusedNodes()

def palNewClick(*args):
    sel = mc.ls(sl=True)

    if len(sel) == 0:
        mc.warning("Please select some objects to color")
        return

    mc.colorEditor()
    if mc.colorEditor(query=True, result=True):
        values = roundColor(mc.colorEditor(query=True, rgb=True))
        
        rgb = to0_255(values)

        addColor(rgb, sel)

    mc.select(sel)

def palExcludeClick(*args):
    global PREVIZ_COLORS

    sel = mc.ls(sl=True)

    if len(sel) == 0:
        mc.warning("Please select some objects to color")
        return

    selection = []
    object_faces = {}

    rawSelection = sel

    for selObj in rawSelection:
        soloObj = selObj.split(":")[-1]
        if ".f" in soloObj:
            soloObj = soloObj.split(".")[0]

        selection.append(soloObj)

    if not EXCLUDED_COLOR in PREVIZ_COLORS:
        PREVIZ_COLORS[EXCLUDED_COLOR] = []

    PREVIZ_COLORS[EXCLUDED_COLOR].extend(selection)

    getFromScene(True)

    mc.select(sel)

def palEditClick(*args):
    global PREVIZ_COLORS

    sel = mc.textScrollList("tkPalManagedLB", query=True, selectItem=True)

    if sel == None:
        mc.warning("Please select a color set in the list")
        return

    oldColor = eval("("+sel[0].split(" : ")[0]+")")

    values = to0_1(oldColor)

    mc.colorEditor(rgb=values)

    if mc.colorEditor(query=True, result=True):
        values = roundColor(mc.colorEditor(query=True, rgb=True))
        
        rgb = to0_255(values)

        objects = PREVIZ_COLORS[oldColor]
        del PREVIZ_COLORS[oldColor]
        PREVIZ_COLORS[rgb] = objects

        for mesh in objects:
            faces = None
            meshName = mesh

            if "." in mesh:
                meshName, faces = meshName.split(".")
                faces = faces.split(";")

            if not mc.objExists(meshName):
                results = mc.ls("*:"+meshName)
                if len(results) > 0:
                    meshName = results[0]

            assignColor(meshName, rgb, faces, False)

        initUI()

def palApplyClick(*args):
    global PREVIZ_COLORS

    selection = []
    object_faces = {}

    rawSelection = mc.ls(sl=True)

    if len(rawSelection) == 0:
        mc.warning("Please select some objects to color")
        return

    for selObj in rawSelection:
        soloObj = selObj
        if ".f" in selObj:
            soloObj = selObj.split(".")[0]
            if not soloObj in object_faces:
                object_faces[soloObj] = []
            object_faces[soloObj].append(selObj.split(".")[1])

        selection.append(soloObj)

    sel = mc.textScrollList("tkPalManagedLB", query=True, selectItem=True)

    if sel == None:
        mc.warning("Please select a color set in the list")
        return

    color = eval("("+sel[0].split(" : ")[0]+")")
    #rawObjects = sel[0].split(" : ")[1].split(",")

    for selObj in selection:
        assignColor(selObj, color, object_faces.get(selObj))

    getFromScene(True)

def palTodoChanged(*args):
    sel = mc.textScrollList("tkPalTodoLB", query=True, selectItem=True)
    mc.select(sel)

def palManagedChanged(*args):
    sync = mc.checkBox("tkPalAutoSelectCB", query=True, value=True)

    if sync:
        sel = []
        rawSel = mc.textScrollList("tkPalManagedLB", query=True, selectItem=True)
        
        for selPatterns in rawSel:
            selPatterns = selPatterns.split(" : ")[1].split(",")
            for selPattern in selPatterns:
                objs = []
                if "." in selPattern:
                    selObj, selFaces = selPattern.split(".")
                    objSolos = mc.ls(["*:"+selObj, selObj], transforms=True)
                    for objSolo in objSolos:
                        objs.extend(["{0}.{1}".format(objSolo, face) for face in selFaces.split(";")])
                else:
                    objs = mc.ls(["*:"+selPattern, selPattern], transforms=True)
                sel.extend(objs)

        if len(sel) == 0:
            mc.select(clear=True)
        else: 
            mc.select(sel)

def palLoadClick(*args):
    global PREVIZ_COLORS

    choosenFile = mc.fileDialog2(caption="Select your palette file", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=1)

    if choosenFile != None and len(choosenFile) > 0:
        choosenFile = choosenFile[0]

        content = None

        with open(choosenFile) as f:
            content = f.read()

        if content != None:
            PREVIZ_COLORS = eval(content)
            initUI()

def palSaveClick(*args):
    choosenFile = mc.fileDialog2(caption="Save your palette file", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=0)

    if choosenFile != None and len(choosenFile) > 0:
        choosenFile = choosenFile[0]

        with open(choosenFile, "w") as f:
            f.write(str(PREVIZ_COLORS))

def palApplyAllClick(*args):
    setColors()
    tkc.deleteUnusedNodes()

def palGetFromSceneClick(*args):
    getFromScene()

def palRefreshClick(*args):
    initUI()

def connectControls():
    mc.button("tkPalLoadBT", edit=True, c=palLoadClick)
    mc.button("tkPalSaveBT", edit=True, c=palSaveClick)
    mc.button("tkPalApplyAllBT", edit=True, c=palApplyAllClick)

    mc.button("tkPalGetFromSceneBT", edit=True, c=palGetFromSceneClick)
    mc.button("tkPalRefreshBT", edit=True, c=palRefreshClick)

    mc.button("tkPalNewBT", edit=True, c=palNewClick)
    mc.button("tkPalEditBT", edit=True, c=palEditClick)
    mc.button("tkPalApplyBT", edit=True, c=palApplyClick)
    mc.button("tkPalExcludeBT", edit=True, c=palExcludeClick)

    mc.textScrollList("tkPalManagedLB", edit=True, sc=palManagedChanged)
    mc.textScrollList("tkPalTodoLB", edit=True, sc=palTodoChanged)

def initUI(*args):
    meshesT=[]
    meshes = pc.ls(type="mesh")

    for mesh in meshes:
        if mesh.intermediateObject.get():
            continue

        meshesT.append(mesh.getParent().name())

    list(set(meshesT))

    managedMeshes = []
    mc.textScrollList("tkPalManagedLB", edit=True, removeAll=True)

    for shd_color, meshes in PREVIZ_COLORS.items():
        if shd_color[0] == -1:
            continue

        mc.textScrollList("tkPalManagedLB", edit=True, append="{0},{1},{2} : {3}".format(shd_color[0], shd_color[1], shd_color[2], ",".join(meshes)))
        for mesh in meshes:
            for meshT in meshesT:
                if meshT.split(":")[-1] == mesh.split(".")[0]:
                    managedMeshes.append(meshT.split(":")[-1])
                    break

    mc.textScrollList("tkPalTodoLB", edit=True, removeAll=True)
    for meshT in meshesT:
        if not meshT.split(":")[-1] in managedMeshes:
            mc.textScrollList("tkPalTodoLB", edit=True, append=meshT)

def showUI():
    if (mc.window('tkPaletteUI', q=True, exists=True)):
        mc.deleteUI('tkPaletteUI')

    dirname, filename = os.path.split(os.path.abspath(__file__))
    ui = mc.loadUI(uiFile=os.path.join(dirname, "UI", "tkPalette.ui"))

    mc.showWindow(ui)

    #add menu

    connectControls()

    initUI()

    mc.control("palProgressBar", edit=True, visible=False)
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

import re
import math

import maya.api.OpenMaya as api
import pymel.core as pc

import tkMayaCore as tkc
import tkNodeling as tkn

"""
DEFAULT_PRESET = {
    "inPrimary":0,
    "inPrimaryNegate":False,
    "inSecondary":2,
    "inSecondaryType":0,
    "inSecondaryData":[0.0, 0.0, 1.0],
    "inSecondaryNegate":False
}

LEFT_ARM_IK_PRESET_0 = {
    "inSecondaryType":2,
    "inSecondaryNegate":True
}

LEFT_ARM_IK_PRESET_1 = {
    "inSecondaryType":3,
    "inSecondaryNegate":True
}

RIGHT_ARM_IK_PRESET_0 = {
    "inPrimaryNegate":True,
    "inSecondaryType":2,
    "inSecondaryNegate":True
}

RIGHT_ARM_IK_PRESET_1 = {
    "inPrimaryNegate":True,
    "inSecondaryType":3,
    "inSecondaryNegate":True
}

FINGER_PRESET_0 = {
    "inSecondary":1,
    "inSecondaryType":2
}

FINGER_PRESET_1 = {
    "inSecondary":1,
    "inSecondaryType":3
}

LEG_IK_PRESET_0 = {
    "inPrimary":1,
    "inPrimaryNegate":True,
    "inSecondaryType":2,
}

LEG_IK_PRESET_1 = {
    "inPrimary":1,
    "inPrimaryNegate":True,
    "inSecondaryType":3
}

FOOT_PRESET = {
    "inPrimary":2,
    "inPrimaryNegate":False,
    "inSecondary":1,
    "inSecondaryData":[0.0, 1.0, 0.0],
}

tkj.writePreset(pc.PyNode("Character1_Hips"), inPrimaryChild="Character1_Spine")
tkj.writePreset(pc.PyNode("Character1_Spine2"), inPrimaryChild="Character1_Neck")

tkj.writePreset(pc.PyNode("Character1_LeftArm"), **LEFT_ARM_IK_PRESET_0)
tkj.writePreset(pc.PyNode("Character1_LeftForeArm"), **LEFT_ARM_IK_PRESET_1)
tkj.writePreset(pc.PyNode("Character1_LeftHand"), inPrimaryChild="Character1_LeftHandMiddle1")

fingers = [
        ["Character1_LeftHandThumb1", "Character1_LeftHandThumb2", "Character1_LeftHandThumb3"],
        ["Character1_LeftHandIndex1", "Character1_LeftHandIndex2", "Character1_LeftHandIndex3"],
        ["Character1_LeftHandMiddle1", "Character1_LeftHandMiddle2", "Character1_LeftHandMiddle3"],
        ["Character1_LeftHandRing1", "Character1_LeftHandRing2", "Character1_LeftHandRing3"],
        ["Character1_LeftHandPinky1", "Character1_LeftHandPinky2", "Character1_LeftHandPinky3"]
    ]

for finger in fingers:
    i = 0
    for digit in finger:
        tkj.writePreset(pc.PyNode(digit), **(FINGER_PRESET_0 if i < 2 else FINGER_PRESET_1))
        i += 1

tkj.writePreset(pc.PyNode("Character1_RightArm"), **RIGHT_ARM_IK_PRESET_0)
tkj.writePreset(pc.PyNode("Character1_RightForeArm"), **RIGHT_ARM_IK_PRESET_1)
tkj.writePreset(pc.PyNode("Character1_RightHand"), inPrimaryChild="Character1_RightHandMiddle1")

fingers = [
        ["Character1_RightHandThumb1", "Character1_RightHandThumb2", "Character1_RightHandThumb3"],
        ["Character1_RightHandIndex1", "Character1_RightHandIndex2", "Character1_RightHandIndex3"],
        ["Character1_RightHandMiddle1", "Character1_RightHandMiddle2", "Character1_RightHandMiddle3"],
        ["Character1_RightHandRing1", "Character1_RightHandRing2", "Character1_RightHandRing3"],
        ["Character1_RightHandPinky1", "Character1_RightHandPinky2", "Character1_RightHandPinky3"]
    ]

for finger in fingers:
    i = 0
    for digit in finger:
        tkj.writePreset(pc.PyNode(digit), **(FINGER_PRESET_0 if i < 2 else FINGER_PRESET_1))
        i += 1

tkj.writePreset(pc.PyNode("Character1_LeftUpLeg"), **LEG_IK_PRESET_0)
tkj.writePreset(pc.PyNode("Character1_LeftLeg"), **LEG_IK_PRESET_1)
tkj.writePreset(pc.PyNode("Character1_LeftFoot"), **FOOT_PRESET)

tkj.writePreset(pc.PyNode("Character1_RightUpLeg"), **LEG_IK_PRESET_0)
tkj.writePreset(pc.PyNode("Character1_RightLeg"), **LEG_IK_PRESET_1)
tkj.writePreset(pc.PyNode("Character1_RightFoot"), **FOOT_PRESET)

tkj.orientJointPreset(pc.PyNode("Character1_Hips"), DEFAULT_PRESET)
"""

"""
inPrimary : 0=x, 1=y, 2=z
inSecondary : 0=x, 1=y, 2=z
"""
def aim(inTransform,  inPrimary=0, inPrimaryDirection=None, inPrimaryPoint=None, inPrimaryNegate=False, inSecondary=1, inSecondaryDirection=None, inSecondaryPoint=None, inSecondaryNegate=False, inPreserveChildren=False):
    #print "aim", inTransform, "inPrimary=", inPrimary, "inPrimaryDirection=", inPrimaryDirection, "inPrimaryPoint=", inPrimaryPoint, "inPrimaryNegate=", inPrimaryNegate, "inSecondary=", inSecondary, "inSecondaryDirection=", inSecondaryDirection, "inSecondaryPoint=", inSecondaryPoint, "inSecondaryNegate=", inSecondaryNegate, "inPreserveChildren=", inPreserveChildren

    if inPrimaryDirection is None and inPrimaryPoint is None:
        raise ValueError("inPrimaryDirection and inPrimaryPoint can't both be null !")

    if inSecondaryDirection is None and inSecondaryPoint is None:
        raise ValueError("inSecondaryDirection and inPrimaryPoint can't both be null !")

    origPos = inTransform.getTranslation(space='world')
    
    #Calculate axis vectors

    if inPrimary == 2:
        if inSecondary == 0:
            inPrimary = 1
            inSecondary = 2
        else:
            inPrimaryNegate = not inPrimaryNegate
    elif inPrimary == 1:
        if inSecondary == 2:
            inPrimary = 2
            inSecondary = 0
        
    primaryAxis = pc.datatypes.Vector(inPrimaryDirection) if not inPrimaryDirection is None else pc.datatypes.Vector(inPrimaryPoint) - origPos
    primaryAxis.normalize()
    if inPrimaryNegate:
        primaryAxis = primaryAxis * -1

    secondaryDirection = pc.datatypes.Vector(inSecondaryDirection) if not inSecondaryDirection is None else pc.datatypes.Vector(inSecondaryPoint) - origPos
    secondaryDirection.normalize()
    if (inSecondary == 2 or (inPrimary != 1 and inSecondary == 0)) and not inSecondaryNegate:
        secondaryDirection = secondaryDirection * -1

    lastAxis = primaryAxis.cross(secondaryDirection)
    lastAxis.normalize()

    secondaryAxis = lastAxis.cross(primaryAxis)
    if inSecondaryNegate:
        secondaryAxis = secondaryAxis * -1

    #Build axis list
    axis = [primaryAxis, secondaryAxis, lastAxis]
    possibleLast = range(3)
    possibleLast.remove(inPrimary)
    possibleLast.remove(inSecondary)

    #Build matrix
    mat = pc.datatypes.Matrix(axis[inPrimary], axis[inSecondary], axis[possibleLast[0]])
    mat.a30 = origPos.x#- xAxis.dot(origPos) ? 
    mat.a31 = origPos.y#- yAxis.dot(origPos) ?
    mat.a32 = origPos.z#- zAxis.dot(origPos) ?
    mat.a33 = 1

    #toEuler
    q = api.MQuaternion(mat.rotate)
    eulerAngles = map(math.degrees, q.asEulerRotation())
    
    rotateOrder = pc.xform(inTransform, rotateOrder=True, query=True)
    if rotateOrder != "xyz":
        pc.xform(inTransform, rotateOrder="xyz", preserve=True)

    #pc.xform(inTransform, matrix=mat, worldSpace=True)
    pc.rotate(inTransform, eulerAngles, absolute=True, worldSpace=True, preserveChildPosition=inPreserveChildren)
    #inTransform.setRotation(mat.rotate, space='world', preserveChildPosition=inPreserve)

    if rotateOrder != "xyz":
        pc.xform(inTransform, rotateOrder=rotateOrder, preserve=True)

def getPoleVector(inStartPoint, inMiddlePoint, inEndPoint, inDistance=1.0, inDistanceAsFactor=False):
    inStartPoint = pc.datatypes.Vector(inStartPoint)
    inMiddlePoint = pc.datatypes.Vector(inMiddlePoint)
    inEndPoint = pc.datatypes.Vector(inEndPoint)
    
    factor = 1.0
    
    midToStart = inStartPoint - inMiddlePoint
    midToEnd = inEndPoint - inMiddlePoint
    
    if inDistanceAsFactor:
        factor = 0.0
        factor += midToStart.length()
        factor += midToEnd.length()
        factor /= 2
        
    midToStart.normalize()
    midToEnd.normalize()

    return inMiddlePoint + (midToStart + midToEnd) * -1 * inDistance * factor

"""
inPrimaryType : 0 = World vector, 1 = World point, 2 = towards child
inSecondaryType : 0 = World vector, 1 = World point, 2 = UpVChildren, 3 = UpVParent, 4 = UpVParentParent, 5 = towards parent
"""
def orientJoint(inTransform, inPrimary=0, inPrimaryType=2, inPrimaryData=[1.0, 0.0, 0.0], inPrimaryNegate=False, inPrimaryChild=None, inSecondary=1, inSecondaryType=0, inSecondaryData=[0.0, 1.0, 0.0], inSecondaryNegate=False, inOrientChildren=False):
    #print "inPrimaryType",inPrimaryType
    #print "inPrimaryData",inPrimaryData

    cns = tkc.storeConstraints([inTransform], inRemove=True)

    cons = tkc.getNodeConnections(inTransform, "t", "r", "s", inSource=True, inDestination=False)
    consIter = cons[:]
    for con in consIter:
        dest, source = con
        #print " -source",source,"dest",dest
        source.disconnect(dest)

    inTransform = pc.PyNode(inTransform.name())

    childTrans = [1,0,0]
    primaryIsDirection = True

    childObj = None
    children = inTransform.getChildren(type="joint")

    ns = str(inTransform.namespace())

    if not inPrimaryChild is None and inPrimaryChild != "":
        if pc.objExists(ns + inPrimaryChild.split(":")[-1]):
            childObj = pc.PyNode(ns + inPrimaryChild.split(":")[-1])
        else:
            if pc.objExists(inPrimaryChild):
                childObj = pc.PyNode(inPrimaryChild)
            else:
                pc.warning("Given primary child cannot be found ({0}) !".format(inPrimaryChild))

    elif len(children) > 0:
        childObj = children[0]
    
    #Calculations for inPrimary "Point" (child direction, or inverse parent direction)
    if not childObj is None:
        childTrans = childObj.getTranslation(space='world')
        primaryIsDirection = False
    else:
        parent = inTransform.getParent()
        if not parent is None:
            childTrans = parent.getTranslation(space='world')
            primaryIsDirection = False
            inPrimaryNegate = not inPrimaryNegate

    firstPoint = inTransform.getTranslation(space="world")
    secondPoint = childTrans
    thirdPoint = None
    #Calculations for UpVs
    if inSecondaryType > 1:
        if inSecondaryType == 5:
            thirdPoint = inTransform.getParent().getTranslation(space='world')
        elif len(children) > 0 or inSecondaryType > 3:
            if inSecondaryType > 2:
                if inSecondaryType > 3:
                    parent = inTransform.getParent()
                    if not parent is None:
                        parentParent = parent.getParent()
                        if not parentParent is None:
                            thirdPoint = firstPoint
                            secondPoint = parent.getTranslation(space='world')
                            firstPoint = parentParent.getTranslation(space='world')
                else:
                    parent = inTransform.getParent()
                    if not parent is None:
                        thirdPoint = secondPoint
                        secondPoint = firstPoint
                        firstPoint = parent.getTranslation(space='world')
            else:
                childChildren = children[0].getChildren()
                if len(childChildren) > 0:
                    thirdPoint = childChildren[0].getTranslation(space="world")

    primaryPoint = childTrans
    if inPrimaryType != 2:
        primaryPoint = inPrimaryData
        primaryIsDirection = inPrimaryType == 0

    #print "primaryPoint",primaryPoint

    if primaryIsDirection:
        if inSecondaryType == 0:
            aim(inTransform,  inPrimary=inPrimary, inPrimaryDirection=primaryPoint, inPrimaryNegate=inPrimaryNegate, inSecondary=inSecondary, inSecondaryDirection=inSecondaryData, inSecondaryNegate=inSecondaryNegate, inPreserveChildren=True)
        elif inSecondaryType == 1:
            aim(inTransform,  inPrimary=inPrimary, inPrimaryDirection=primaryPoint, inPrimaryNegate=inPrimaryNegate, inSecondary=inSecondary, inSecondaryPoint=inSecondaryData, inSecondaryNegate=inSecondaryNegate, inPreserveChildren=True)
        elif not thirdPoint is None:#Upvs
            if inSecondaryType == 5:
                aim(inTransform,  inPrimary=inPrimary, inPrimaryDirection=primaryPoint, inPrimaryNegate=inPrimaryNegate, inSecondary=inSecondary, inSecondaryPoint=thirdPoint, inSecondaryNegate=inSecondaryNegate, inPreserveChildren=True)
            else:
                upV = getPoleVector(firstPoint, secondPoint, thirdPoint)
                aim(inTransform,  inPrimary=inPrimary, inPrimaryDirection=primaryPoint, inPrimaryNegate=inPrimaryNegate, inSecondary=inSecondary, inSecondaryPoint=upV, inSecondaryNegate=inSecondaryNegate, inPreserveChildren=True)
    else:
        if inSecondaryType == 0:
            aim(inTransform,  inPrimary=inPrimary, inPrimaryPoint=primaryPoint, inPrimaryNegate=inPrimaryNegate, inSecondary=inSecondary, inSecondaryDirection=inSecondaryData, inSecondaryNegate=inSecondaryNegate, inPreserveChildren=True)
        elif inSecondaryType == 1:
            aim(inTransform,  inPrimary=inPrimary, inPrimaryPoint=primaryPoint, inPrimaryNegate=inPrimaryNegate, inSecondary=inSecondary, inSecondaryPoint=inSecondaryData, inSecondaryNegate=inSecondaryNegate, inPreserveChildren=True)
        elif not thirdPoint is None:#Upvs
            if inSecondaryType == 5:
                aim(inTransform,  inPrimary=inPrimary, inPrimaryPoint=primaryPoint, inPrimaryNegate=inPrimaryNegate, inSecondary=inSecondary, inSecondaryPoint=thirdPoint, inSecondaryNegate=inSecondaryNegate, inPreserveChildren=True)
            else:
                upV = getPoleVector(firstPoint, secondPoint, thirdPoint)
                aim(inTransform,  inPrimary=inPrimary, inPrimaryPoint=primaryPoint, inPrimaryNegate=inPrimaryNegate, inSecondary=inSecondary, inSecondaryPoint=upV, inSecondaryNegate=inSecondaryNegate, inPreserveChildren=True)

    pc.makeIdentity(inTransform, apply=True)
    """
    try:
        #makeIdentity will fail sooner or later because it wat to act on children...
        pc.makeIdentity(inTransform, apply=True)
    except Exception as e:
        pc.warning(e)
    """
    if len(cns) > 0:
        tkc.loadConstraints(cns, inMaintainOffset=True)

    if len(cons) > 0:
        tkc.setNodeConnections(inTransform, cons)

    if inOrientChildren:
        for child in childen:
            if child.type() == "joint":
                orientJoint(child,  inPrimary=inPrimary, inPrimaryNegate=inPrimaryNegate, inSecondary=inSecondary, inSecondaryType=inSecondaryType, inSecondaryData=inSecondaryData, inSecondaryNegate=inSecondaryNegate, inOrientChildren=True)

def addAttr(inTransform, inName, inValue, inEnumValues=None):
    attType = type(inValue).__name__
    #print "attType",attType
    
    if attType == "int":
        attType = "long"
    elif attType == "str":
        attType = "string"
    elif attType in ['list', 'tuple']:
        subType = type(inValue[0]).__name__
        
        #print "subType",subType
        
        if subType == "int":
            attType = "Int32Array"
        if subType == "float":
            attType = "doubleArray"
    #print "final attType",attType

    if pc.attributeQuery(inName, node=inTransform, exists=True):
        pc.deleteAttr(inTransform, at=inName)

    if "Array" in attType or attType == "string":
        pc.addAttr(inTransform, longName=inName, dt=attType)
        inTransform.attr(inName).set(inValue)
    elif attType == "long" and not inEnumValues is None:
        pc.addAttr(inTransform, longName=inName, attributeType="enum", en=inEnumValues, defaultValue=inValue)
    else:
        pc.addAttr(inTransform, longName=inName, attributeType=attType, defaultValue=inValue)

DEFAULT_PRESET = {
    "inPrimary":0,
    "inPrimaryType":2,
    "inPrimaryData":[1.0, 0.0, 0.0],
    "inPrimaryNegate":False,
    "inPrimaryChild":"",
    "inSecondary":1,
    "inSecondaryType":0,
    "inSecondaryData":[0.0, 1.0, 0.0],
    "inSecondaryNegate":False
}

def writePreset(inTransform, inClearDict=DEFAULT_PRESET, **inPreset):
    if not inClearDict is None:
        for key, value in inClearDict.iteritems():
            if pc.attributeQuery(key, node=inTransform, exists=True):
                pc.deleteAttr(inTransform, at=key)

    for key, value in inPreset.iteritems():
        addAttr(inTransform, key, value)

def readPreset(inTransform):
    preset = {}

    for key in DEFAULT_PRESET.keys():
        if pc.attributeQuery(key, node=inTransform, exists=True):
            preset[key] = inTransform.attr(key).get()

    return preset
"""
writePreset(pc.selected()[0], **DEFAULT_PRESET)
print readPreset(pc.selected()[0])
"""

def orientJointPreset(inTransform, inDefaultPreset=DEFAULT_PRESET, inOrientChildren=True, inSkipPrefix=None, inSkipIfFound=None):
    if not inSkipPrefix is None and inTransform.stripNamespace().startswith(inSkipPrefix):
        return

    preset = inDefaultPreset.copy()
    preset.update(readPreset(inTransform))

    orientJoint(inTransform, **preset)

    if inOrientChildren and inSkipIfFound != inTransform.stripNamespace():
        for child in inTransform.getChildren(type="joint"):
            orientJointPreset(child, inDefaultPreset=inDefaultPreset, inOrientChildren=True, inSkipPrefix=inSkipPrefix, inSkipIfFound=inSkipIfFound)

def createSymmetry(inObjects=None, inPrimaryPattern=".*Left.*", inSecondaryPattern=".*Right.*", inRotate=True, inLockCenter=0, inConsiderHierarchy=True, invertX=True, invertY=False, invertZ=False):
    if inObjects is None:
        inObjects = pc.selected()
    elif not isinstance(inObjects, (list, tuple)):
         inObjects = [inObjects]

    if inConsiderHierarchy:
        inRoots = inObjects[:]

        for root in inRoots:
            inObjects.extend(root.getChildren(allDescendents=True, type="joint"))

        inObjects = list(set(inObjects))

    for obj in inObjects:
        print "obj",obj
        if re.match(inPrimaryPattern, obj.name()):
            continue

        if re.match(inSecondaryPattern, obj.name()):
            otherSide = obj.name().replace(inSecondaryPattern.strip(".*^&"), inPrimaryPattern.strip(".*^&"))
            if pc.objExists(otherSide):
                otherNode = pc.PyNode(otherSide)
                
                obj.tx.disconnect(destination=False)
                obj.ty.disconnect(destination=False)
                obj.tz.disconnect(destination=False)

                if invertX:
                    tkn.mul(otherNode.tx, -1.0) >>  obj.tx
                else:
                    otherNode.tx >>  obj.tx

                if invertY:
                    tkn.mul(otherNode.ty, -1.0) >>  obj.ty
                else:
                    otherNode.ty >>  obj.ty

                if invertZ:
                    tkn.mul(otherNode.tz, -1.0) >>  obj.tz
                else:
                    otherNode.tz >>  obj.tz


                if inRotate:
                    obj.rx.disconnect(destination=False)
                    obj.ry.disconnect(destination=False)
                    obj.rz.disconnect(destination=False)

                    if invertX and not invertY and not invertZ:
                        otherNode.rx >>  obj.rx
                        
                        tkn.mul(otherNode.ry, -1.0) >>  obj.ry
                        
                        tkn.mul(otherNode.rz, -1.0) >>  obj.rz
                    else:
                        otherNode.rx >>  obj.rx
                        otherNode.ry >>  obj.ry
                        otherNode.rz >>  obj.rz
        else:
            attrs = ["tx", "ty", "tz"]
            for attr in attrs:
                obj.attr(attr).setLocked(False)

            if not inLockCenter is None:
                obj.attr(attrs[inLockCenter]).setLocked(True)

#createSymmetry()

def disconnectSymmetry(inObjects=None, inPrimaryPattern=".*Left.*", inSecondaryPattern=".*Right.*", inConsiderHierarchy=True):
    if inObjects is None:
        inObjects = pc.selected()
    elif not isinstance(inObjects, (list, tuple)):
         inObjects = [inObjects]

    if inConsiderHierarchy:
        inRoots = inObjects[:]

        for root in inRoots:
            inObjects.extend(root.getChildren(allDescendents=True, type="joint"))

        inObjects = list(set(inObjects))

    for obj in inObjects:
        if re.match(inPrimaryPattern, obj.name()):
            continue

        if re.match(inSecondaryPattern, obj.name()):
            obj.tx.disconnect(destination=False)
            obj.ty.disconnect(destination=False)
            obj.tz.disconnect(destination=False)

            obj.rx.disconnect(destination=False)
            obj.ry.disconnect(destination=False)
            obj.rz.disconnect(destination=False)
        else:
            obj.tx.setLocked(False)
            obj.ty.setLocked(False)
            obj.tz.setLocked(False)

    tkc.deleteUnusedNodes()
#disconnectSymmetry()

def UIVisChanged(args):
    #Defer the execution in case hidiung is temporary (docking/undocking)
    pc.evalDeferred(cleanIfHidden)

def cleanIfHidden():
   if not pc.control(UINAME+"DockControl", query=True, visible=True):
        if pc.window(UINAME, q=True, exists=True):
            pc.deleteUI(UINAME)
        pc.deleteUI(UINAME+"DockControl")

UINAME = "tkJointOrientUI"

def showUI(*inArgs):
    if (pc.window(UINAME, q=True, exists=True)):
        pc.deleteUI(UINAME)

    mainWindow = pc.mel.eval("$tmp = $gMainPane")
    dockLayout = pc.paneLayout(configuration='single', parent=mainWindow)
    dockName = pc.dockControl(UINAME+"DockControl", allowedArea='all', area='top', floating=False, content=dockLayout, label="Dev' Mate", vcc=UIVisChanged)
 
    dirname, filename = os.path.split(os.path.abspath(__file__))
    ui = pc.loadUI(uiFile=dirname + "\\UI\\tkJointOrient.ui")
    pc.showWindow(ui)

    pc.control(ui, e=True, parent=dockLayout)
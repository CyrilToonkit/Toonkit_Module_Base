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
import os

import maya.api.OpenMaya as api
import pymel.core as pc

import OscarZmqMayaString as ozms
import tkMayaCore as tkc
import tkNodeling as tkn

try: basestring
except: basestring=str

"""
import tkJointOrient as tkj
reload(tkj)

SKELETAL_PREFIX = ""

DEFAULT_PRESET = {
    "inPrimary":1,#Y
    "inPrimaryType":2,#towards child
    "inPrimaryData":[0.0, 1.0, 0.0],
    "inPrimaryNegate":False,

    "inSecondary":2,#Z
    "inSecondaryType":0,#World vector
    "inSecondaryData":[0.0, 0.0, -1.0],
    "inSecondaryNegate":False
}

LEFT_SHOULDER_PRESET_0 = {
    "inPrimary":0,#X
    "inSecondaryData":[0.0, 0.0, 1.0],
}

RIGHT_SHOULDER_PRESET_0 = {
    "inPrimary":0,#X
    "inPrimaryNegate":True,
    "inSecondaryData":[0.0, 0.0, 1.0],
}

LEFT_ARM_IK_PRESET_0 = {
    "inPrimary":0,#X
    "inSecondaryType":2,#UpVChildren
    "inSecondaryNegate":True
}

LEFT_ARM_IK_PRESET_1 = {
    "inPrimary":0,#X
    "inSecondaryType":3,#UpVParent
    "inSecondaryNegate":True
}

LEFT_HAND_PRESET_0 = {
    "inPrimary":0,#X
    "inSecondaryType":4,#UpVParentParent
    "inSecondaryNegate":True,
    "inPrimaryChild":SKELETAL_PREFIX + "LeftHandMiddle1",
}

RIGHT_HAND_PRESET_0 = {
    "inPrimary":0,#X
    "inPrimaryNegate":True,
    "inSecondaryType":4,#UpVParentParent
    "inSecondaryNegate":True,
    "inPrimaryChild":SKELETAL_PREFIX + "RightHandMiddle1",
}

RIGHT_ARM_IK_PRESET_0 = {
    "inPrimary":0,#X
    "inPrimaryNegate":True,
    "inSecondaryType":2,#UpVChildren
    "inSecondaryNegate":True
}

RIGHT_ARM_IK_PRESET_1 = {
    "inPrimary":0,#X
    "inPrimaryNegate":True,
    "inSecondaryType":3,#UpVParent
    "inSecondaryNegate":True
}

LEFT_FINGER_PRESET_0 = {
    "inPrimary":0,#X
    "inSecondary":1,
    "inSecondaryType":2#UpVChildren
}

LEFT_FINGER_PRESET_1 = {
    "inPrimary":0,#X
    "inSecondary":1,
    "inSecondaryType":3#UpVParent
}

RIGHT_FINGER_PRESET_0 = {
    "inPrimary":0,#X
    "inPrimaryNegate":True,
    "inSecondary":1,
    "inSecondaryType":2#UpVChildren
}

RIGHT_FINGER_PRESET_1 = {
    "inPrimary":0,#X
    "inPrimaryNegate":True,
    "inSecondary":1,
    "inSecondaryType":3#UpVParent
}

LEG_IK_PRESET_0 = {
    "inPrimary":1,#Y
    "inPrimaryNegate":True,
    "inSecondaryType":2,#UpVChildren
    "inSecondaryNegate":True,
}

LEG_IK_PRESET_1 = {
    "inPrimary":1,#Y
    "inPrimaryNegate":True,
    "inSecondaryType":3,#UpVParent
    "inSecondaryNegate":True,
}

FOOT_PRESET = {
    "inPrimary":2,#Z
    "inPrimaryNegate":False,
    "inSecondary":1,
    "inSecondaryData":[0.0, 1.0, 0.0],
}

tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "Hips"), inPrimaryChild=SKELETAL_PREFIX + "Spine")
tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "Spine3"), inPrimaryChild=SKELETAL_PREFIX + "Neck")

tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "Head"), inPrimaryChild=SKELETAL_PREFIX + "Neck")

tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "LeftShoulder"), **LEFT_SHOULDER_PRESET_0)

tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "LeftArm"), **LEFT_ARM_IK_PRESET_0)
tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "LeftForeArm"), **LEFT_ARM_IK_PRESET_1)
tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "LeftHand"), **LEFT_HAND_PRESET_0)

fingers = [
        [SKELETAL_PREFIX + "LeftHandThumb1", SKELETAL_PREFIX + "LeftHandThumb2", SKELETAL_PREFIX + "LeftHandThumb3"],
        [SKELETAL_PREFIX + "LeftHandIndex1", SKELETAL_PREFIX + "LeftHandIndex2", SKELETAL_PREFIX + "LeftHandIndex3"],
        [SKELETAL_PREFIX + "LeftHandMiddle1", SKELETAL_PREFIX + "LeftHandMiddle2", SKELETAL_PREFIX + "LeftHandMiddle3"],
        [SKELETAL_PREFIX + "LeftHandRing1", SKELETAL_PREFIX + "LeftHandRing2", SKELETAL_PREFIX + "LeftHandRing3"],
        [SKELETAL_PREFIX + "LeftHandPinky1", SKELETAL_PREFIX + "LeftHandPinky2", SKELETAL_PREFIX + "LeftHandPinky3"]
    ]

for finger in fingers:
    i = 0
    for digit in finger:
        tkj.writePreset(pc.PyNode(digit), **(LEFT_FINGER_PRESET_0 if i < 2 else LEFT_FINGER_PRESET_1))
        i += 1

tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "RightShoulder"), **RIGHT_SHOULDER_PRESET_0)

tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "RightArm"), **RIGHT_ARM_IK_PRESET_0)
tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "RightForeArm"), **RIGHT_ARM_IK_PRESET_1)
tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "RightHand"), **RIGHT_HAND_PRESET_0)

fingers = [
        [SKELETAL_PREFIX + "RightHandThumb1", SKELETAL_PREFIX + "RightHandThumb2", SKELETAL_PREFIX + "RightHandThumb3"],
        [SKELETAL_PREFIX + "RightHandIndex1", SKELETAL_PREFIX + "RightHandIndex2", SKELETAL_PREFIX + "RightHandIndex3"],
        [SKELETAL_PREFIX + "RightHandMiddle1", SKELETAL_PREFIX + "RightHandMiddle2", SKELETAL_PREFIX + "RightHandMiddle3"],
        [SKELETAL_PREFIX + "RightHandRing1", SKELETAL_PREFIX + "RightHandRing2", SKELETAL_PREFIX + "RightHandRing3"],
        [SKELETAL_PREFIX + "RightHandPinky1", SKELETAL_PREFIX + "RightHandPinky2", SKELETAL_PREFIX + "RightHandPinky3"]
    ]

for finger in fingers:
    i = 0
    for digit in finger:
        tkj.writePreset(pc.PyNode(digit), **(RIGHT_FINGER_PRESET_0 if i < 2 else RIGHT_FINGER_PRESET_1))
        i += 1

tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "LeftUpLeg"), **LEG_IK_PRESET_0)
tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "LeftLeg"), **LEG_IK_PRESET_1)
tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "LeftFoot"), **FOOT_PRESET)

tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "RightUpLeg"), **LEG_IK_PRESET_0)
tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "RightLeg"), **LEG_IK_PRESET_1)
tkj.writePreset(pc.PyNode(SKELETAL_PREFIX + "RightFoot"), **FOOT_PRESET)

tkj.orientJointPreset(pc.PyNode(SKELETAL_PREFIX + "Hips"), DEFAULT_PRESET)

"""

def checkOrients(inRootName, inRootNs, inRefNs, inRecursively=True, inDelta=tkc.CONST_DELTA):
    faulty = []

    faults = []

    inRoot = tkc.getNode(inRootNs + inRootName)
    inRefRoot = tkc.getNode(inRefNs + inRootName)
    
    exists = False

    if inRoot is None or inRefRoot is None:
        if inRoot is None:
            pc.warning("Target {0} cannot be found !".format(inRootName))
        if inRefRoot is None:
            pc.warning("Reference {0} cannot be found !".format(inRootName))

        faults.append('objects not found')
    else:
        exists = True

        if not tkc.listsBarelyEquals(inRoot.t.get(), inRefRoot.t.get(), delta=inDelta):
            faults.append('translations')
        if not tkc.listsBarelyEquals(inRoot.r.get(), inRefRoot.r.get(), delta=inDelta):
            faults.append('rotations')
        if not tkc.listsBarelyEquals(inRoot.s.get(), inRefRoot.s.get(), delta=inDelta):
            faults.append('scalings')

        if pc.hasAttr(inRoot, "jointOrient", False) and pc.hasAttr(inRefRoot, "jointOrient", False):
            if not tkc.listsBarelyEquals(inRoot.jointOrient.get(), inRefRoot.jointOrient.get(), delta=inDelta):
                faults.append('jointOrients')

    if len(faults) > 0:
        faulty.append("{0} do not match {1} ({2}).".format(inRoot, inRefRoot,",".join(faults)))

    if exists and inRecursively:
        for child in inRoot.getChildren():
            faulty.extend(checkOrients(str(child.stripNamespace()), inRootNs, inRefNs, inRecursively=True, inDelta=inDelta))

    return faulty 

def bakeOrientJoint(inJoints=None):
    inJoints = inJoints or [j for j in pc.selected() if j.type() == "joint"]
    
    for joint in inJoints:
        joint.rx.set(joint.rx.get() + joint.jointOrientX.get())
        joint.jointOrientX.set(0.0)
        
        joint.ry.set(joint.ry.get() + joint.jointOrientY.get())
        joint.jointOrientY.set(0.0)
        
        joint.rz.set(joint.rz.get() + joint.jointOrientZ.get())
        joint.jointOrientZ.set(0.0)
        
def resetOrientJoint(inJoints=None):
    inJoints = inJoints or [j for j in pc.selected() if j.type() == "joint"]
    
    for joint in inJoints:
        joint.jointOrientX.set(joint.jointOrientX.get() + joint.rx.get())
        joint.rx.set(0.0)
        
        joint.jointOrientY.set(joint.jointOrientY.get() + joint.ry.get())
        joint.ry.set(0.0)
        
        joint.jointOrientZ.set(joint.jointOrientZ.get() + joint.rz.get())
        joint.rz.set(0.0)

"""
Axis:
---------------------------
inPrimary : 0=x, 1=y, 2=z
inSecondary : 0=x, 1=y, 2=z
---------------------------

"""
def aim(inTransform,  inPrimary=0, inPrimaryDirection=None, inPrimaryPoint=None, inPrimaryNegate=False, inSecondary=1, inSecondaryDirection=None, inSecondaryPoint=None, inSecondaryNegate=False, inPreserveChildren=False):
    #print "aim", inTransform, "inPrimary=", inPrimary, "inPrimaryDirection=", inPrimaryDirection, "inPrimaryPoint=", inPrimaryPoint, "inPrimaryNegate=", inPrimaryNegate, "inSecondary=", inSecondary, "inSecondaryDirection=", inSecondaryDirection, "inSecondaryPoint=", inSecondaryPoint, "inSecondaryNegate=", inSecondaryNegate, "inPreserveChildren=", inPreserveChildren

    if inPrimary == inSecondary:
        raise ValueError("inPrimary and inSecondary can't be the same axis '{0}' ({1})!".format(["x", "y", "z"][inPrimary], inTransform))

    if inPrimaryDirection is None and inPrimaryPoint is None:
        raise ValueError("inPrimaryDirection and inPrimaryPoint can't both be null ({0}) !".format(inTransform))

    if inSecondaryDirection is None and inSecondaryPoint is None:
        raise ValueError("inSecondaryDirection and inPrimaryPoint can't both be null ({0}) !".format(inTransform))

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
    possibleLast = list(range(3))
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

def makeIdentity(inObj):
    attrs = {}
    for channel in tkc.CHANNELS:
        attr = inObj.attr(channel)
        attrs[channel] = (attr.isLocked(), attr.isKeyable(), attr.isInChannelBox())
        attr.setLocked(False)

    children = inObj.getChildren()
    if len(children) > 0:
        dupe = pc.duplicate(inObj, parentOnly=True)[0]
        pc.makeIdentity(dupe, apply=True)

        inObj.rotate.set(dupe.rotate.get())
        inObj.jointOrient.set(dupe.jointOrient.get())

        pc.delete(dupe)
    else:
        pc.makeIdentity(inObj, apply=True)

    for channel, info in attrs.items():
        attr = inObj.attr(channel)
        attr.setLocked(info[0])

    """
    inObj.jointOrientX.set(inObj.rotateX.get() + inObj.jointOrientX.get())
    inObj.jointOrientY.set(inObj.rotateY.get() + inObj.jointOrientY.get())
    inObj.jointOrientZ.set(inObj.rotateZ.get() + inObj.jointOrientZ.get())
    
    attrs = {}
    for channel in tkc.CHANNELS:
        attr = inObj.attr(channel)
        attrs[channel] = (attr.isLocked(), attr.isKeyable(), attr.isInChannelBox())
        attr.setLocked(False)

    inObj.rotate.set([0.0,0.0,0.0])
    tkc.compensateCns(inObj)

    for channel, info in attrs.items():
        attr = inObj.attr(channel)
        attr.setLocked(info[0])
    """

def getFirstOrientedChild(inTransform):
    children = inTransform.getChildren()

    if len(children) == 0:
        return None

    if len(children) == 1:
        return children[0]

    for child in children:
        if len(readPreset(child)) > 0:
            return child

    return children[0]


"""
inPrimaryType : 0 = World vector, 1 = World point, 2 = towards child, 3 = towards parent, 5 = matched
inSecondaryType : 0 = World vector, 1 = World point, 2 = UpVChildren, 3 = UpVParent, 4 = UpVParentParent, 5 = towards parent, 6 = External UpV

TODO : same options for Primary and Secondary !
TODO : tackle last aiming bugs (for instance Spine needs to point [0,0,-1] to point [0,0,1]) !
"""
def orientJoint(inTransform,
                inPrimary=0,
                inPrimaryType=2,
                inPrimaryData=[1.0, 0.0, 0.0],
                inPrimaryNegate=False,
                inPrimaryChild=None,
                inSecondary=1,
                inSecondaryType=0,
                inSecondaryData=[0.0, 1.0, 0.0],
                inSecondaryNegate=False,
                inOrientChildren=False,
                inIdentity=False,
                ):

    attrs = {}
    for channel in tkc.CHANNELS:
        attr = inTransform.attr(channel)
        attrs[channel] = (attr.isLocked(), attr.isKeyable(), attr.isInChannelBox())
        attr.setLocked(False)

    cns = tkc.storeConstraints([inTransform], inRemove=True)

    cons = tkc.getNodeConnections(inTransform, "t", "r", "s", inSource=True, inDestination=False)
    consIter = cons[:]
    for con in consIter:
        dest, source = con
        #print " -source",source,"dest",dest
        dest.disconnect(source)

    inTransform = pc.PyNode(inTransform.name())

    childTrans = [1,0,0]
    primaryIsDirection = True

    childObj = None
    children = inTransform.getChildren(type="joint")

    ns = str(inTransform.namespace())

    if inPrimaryType == 5:
        childObj = tkc.getNode(ns + inPrimaryChild.split(":")[-1])
        if childObj is None:
            childObj = tkc.getNode(inPrimaryChild)

        matchObj = None
        if not childObj is None:
            if not tkc.listsBarelyEquals(inPrimaryData, [0.0,0.0,0.0]):
                matchObj = pc.group(empty=True, name="tmp")
                childObj.addChild(matchObj)
                matchObj.t.set([0.0,0.0,0.0])
                matchObj.r.set(inPrimaryData)
                childObj = matchObj

            pc.rotate(inTransform, ozms.getPymelRotation(childObj, space="world"), absolute=True, worldSpace=True, preserveChildPosition=True)

            if not matchObj is None:
                pc.delete(matchObj)
    else:
        if not inPrimaryChild is None and inPrimaryChild != "":
            if not isinstance(inPrimaryChild, (list, tuple)):
                inPrimaryChild = [inPrimaryChild]

            for childName in inPrimaryChild:
                if pc.objExists(ns + childName.split(":")[-1]):
                    childObj = pc.PyNode(ns + childName.split(":")[-1])
                else:
                    if pc.objExists(childName):
                        childObj = pc.PyNode(childName)
                    else:
                        pc.warning("Given primary child cannot be found ({0}) !".format(childName))

        else:
            if inPrimaryType == 2 and len(children) > 0:
                childObj = getFirstOrientedChild(inTransform)
            elif inPrimaryType == 3:
                childObj = inTransform.getParent()

        #Calculations for inPrimary "Point" (child direction, or inverse parent direction)
        if not childObj is None:
            childTrans = [0,0,0]
            if not isinstance(childObj, (list, tuple)):
                childObj = [childObj]

            for child in childObj:
                childTrans += child.getTranslation(space='world')

            childTrans /= len(childObj)

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
                    childChild = getFirstOrientedChild(getFirstOrientedChild(inTransform))
                    if not childChild is None:
                        thirdPoint = childChild.getTranslation(space="world")

        primaryPoint = childTrans
        if inPrimaryType != 2 and inPrimaryType != 3:
            primaryPoint = inPrimaryData
            primaryIsDirection = inPrimaryType == 0

        #print "primaryPoint",primaryPoint
        if isinstance(inSecondaryData, (tuple, list)) and isinstance(inSecondaryData[0], basestring):
            inSecondaryData = eval(inSecondaryData[0] + "({})".format(",".join(["\"{}\"".format(d) if isinstance(d, basestring) else str(d) for d in inSecondaryData[1:]])))
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
    """
    print "orientJoint({}, inPrimary={}, inPrimaryType={}, inPrimaryData={}, inPrimaryNegate={}, inPrimaryChild={}, inSecondary={}, inSecondaryType={}, inSecondaryData={}, inSecondaryNegate={}, inOrientChildren={}, inIdentity={}, CHILD={})".format(
            inTransform, inPrimary, inPrimaryType, inPrimaryData, inPrimaryNegate, inPrimaryChild, inSecondary, inSecondaryType, inSecondaryData, inSecondaryNegate, inOrientChildren, inIdentity, childObj)
    """
    if inIdentity:
        makeIdentity(inTransform)
    else:
        bakeOrientJoint([inTransform])

    if len(cns) > 0:
        tkc.loadConstraints(cns, inMaintainOffset=True)

    if len(cons) > 0:
        tkc.setNodeConnections(cons, inTransform)

    for channel, info in attrs.items():
        attr = inTransform.attr(channel)
        attr.setLocked(info[0])

    if inOrientChildren:
        for child in childen:
            if child.type() == "joint":
                orientJoint(child,  inPrimary=inPrimary, inPrimaryNegate=inPrimaryNegate, inSecondary=inSecondary, inSecondaryType=inSecondaryType, inSecondaryData=inSecondaryData, inSecondaryNegate=inSecondaryNegate, inOrientChildren=True)

def getUpVPos(inTopRef, inMiddleRef, inEndRef):
    upVector = pc.group(empty=True)
    resPlan = tkc.createResPlane(target=upVector, topRef = tkc.getNode("::"+inTopRef), middleRef = tkc.getNode("::"+inMiddleRef), endRef = tkc.getNode("::"+inEndRef))
    poses = upVector.translate.get()
    pc.delete(resPlan)
    pc.delete(upVector)
    return list(poses)

def addAttr(inTransform, inName, inValue, inEnumValues=None):
    attType = type(inValue).__name__
    #print inTransform, inName, inValue, " : attType",attType
    
    if attType == "int":
        attType = "long"
    elif attType == "str":
        attType = "string"
    elif attType in ['list', 'tuple']:
        if isinstance(inValue, tuple):
            inValue = list(inValue)
        subType = type(inValue[0]).__name__
        
        #print "subType",subType
        
        if subType == "int":
            attType = "Int32Array"
        if subType == "float":
            attType = "doubleArray"
        if subType == "str":
            attType = "stringArray"

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
        for key, value in inClearDict.items():
            if pc.attributeQuery(key, node=inTransform, exists=True):
                pc.deleteAttr(inTransform, at=key)

    for key, value in inPreset.items():
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

def orientJointPreset(inTransform, inDefaultPreset=DEFAULT_PRESET, inOrientChildren=True, inSkipPrefix=None, inSkipIfFound=None, inIdentity=False, inOrientPresettedOnly=False):
    if not inSkipPrefix is None and inTransform.stripNamespace().startswith(inSkipPrefix):
        return

    preset = inDefaultPreset.copy()
    actualPreset = readPreset(inTransform)
    if len(actualPreset) > 0 or not inOrientPresettedOnly:
        preset.update(actualPreset)
        preset["inIdentity"] = inIdentity
        orientJoint(inTransform, **preset)

    if inOrientChildren and inSkipIfFound != inTransform.stripNamespace():
        for child in inTransform.getChildren(type="joint"):
            orientJointPreset(child, inDefaultPreset=inDefaultPreset, inOrientChildren=True, inSkipPrefix=inSkipPrefix, inSkipIfFound=inSkipIfFound, inIdentity=inIdentity)

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
        print ("obj",obj)
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
    ui = pc.loadUI(uiFile=os.path.join(dirname, "UI", "tkJointOrient.ui"))
    pc.showWindow(ui)

    pc.control(ui, e=True, parent=dockLayout)
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

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  _____ _    ____  _       
 |_   _| | _|  _ \(_) __ _ 
   | | | |/ / |_) | |/ _` |
   | | |   <|  _ <| | (_| |
   |_| |_|\_\_| \_\_|\__, |
                     |___/ 

    Maya Toonkit Rigging/animation library
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

import os
import copy
import json
import re
import math
import operator

import pymel.core as pc
import maya.cmds as mc
import pymel.core.system as pmsys
from maya.OpenMaya import MVector
import OscarZmqMayaString as ozms

import tkMayaCore as tkc
import tkSIGroups
import PAlt as palt
import tkNodeling as tkn
import tkExpressions
import tkProjects.tkContext as context

__author__ = "Cyril GIBAUD - Toonkit"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
   ____                _              _       
  / ___|___  _ __  ___| |_ __ _ _ __ | |_ ___ 
 | |   / _ \| '_ \/ __| __/ _` | '_ \| __/ __|
 | |__| (_) | | | \__ \ || (_| | | | | |_\__ \
  \____\___/|_| |_|___/\__\__,_|_| |_|\__|___/
                                             
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

RIG_ROOT_NAME = "TKRig"
ELEMENT_INFO_NAME = "TK_OSCAR_ElementInfo"

CONST_LEFTPREFIXES = ["^L_", "^Left_", ":L_", ":Left_","_L_", "_Left_"]
CONST_RIGHTPREFIXES = ["^R_", "^Right_",":R_", ":Right_","_R_", "_Right_"]

CONST_LEFTPREFIXES = ["Left_"]
CONST_RIGHTPREFIXES = ["Right_"]

CONST_TRANSMARKER = [["posx", "posy", "posz"],["rotx", "roty", "rotz"],["sclx", "scly", "sclz"]]

ELEMSINDICES = {0:"Model", 1:"Root", 2:"Input", 3:"Output", 4:"Null", 5:"Control", 6:"Deform", 7:"PlaceHolder"}

ALLOWED_GEOMETRIES = ["mesh"]

CONST_BAKERSUFFIX = "_tkBaker"

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
   ___                          _    ____ ___ 
  / _ \ ___  ___ __ _ _ __     / \  |  _ \_ _|
 | | | / __|/ __/ _` | '__|   / _ \ | |_) | | 
 | |_| \__ \ (_| (_| | |     / ___ \|  __/| | 
  \___/|___/\___\__,_|_|    /_/   \_\_|  |___|
                                             
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def OscarGetRoot(ns=""):
    if pc.objExists(ns+RIG_ROOT_NAME):
        return pc.PyNode(ns+RIG_ROOT_NAME)
    return None

def OscarGetNodes(ns="*", parent=None):
    nodes = []

    if parent != None:
        rigs = [parent]
    else:
        pattern = None
        if ns == "*":
            pattern = ["*:"+RIG_ROOT_NAME, RIG_ROOT_NAME]
        else:
            if not ":" in ns:
                ns = ns + ":"
            pattern = [ns+RIG_ROOT_NAME]

        rigs = pc.ls(pattern)

    for rig in rigs:
        children = rig.getChildren()

        #don't forget the "root" Control
        if parent == None:
            rigParent = rig.getParent()
            children.extend([n for n in rigParent.getChildren() if n.name().endswith("_Root")])

        for child in children:
            if child.name().endswith("Root"):
                nodes.append(child)
            else:
                nodes.extend(OscarGetNodes(ns, child))

    return nodes

def OscarGetElements(ns="*", types=None):
    pattern = None
    if ns == "*":
        pattern = ["*:*_"+ELEMENT_INFO_NAME, "*_"+ELEMENT_INFO_NAME]
    else:
        if not ":" in ns:
            ns = ns + ":"
        pattern = [ns+"*_"+ELEMENT_INFO_NAME]

    elemProps = pc.ls(pattern)

    if types == None:
        return [n.getParent() for n in elemProps]
    
    elems = []
    currentType = ""
    if isinstance(types, basestring):
        types = [types]
    for elemProp in elemProps:
        currentType = ELEMSINDICES[elemProp.tk_type.get()]
        if currentType in types:
            elem = elemProp.getParent()
            if currentType != "Control" or (not "_Buffer" in elem.name() and len(pc.listConnections(elem, type="constraint", destination=False)) == 0):
                elems.append(elem)
            
    return elems
     
def OscarGetAllControls():
    return OscarGetElements(types=["Control"])

def OscarFilterPosed(inObjects):
    movedControls = []

    for nControl in inObjects:
        if not tkc.listsBarelyEquals(nControl.getTranslation(), [0.0,0.0,0.0]):
            movedControls.append(nControl)
            continue
        if not tkc.listsBarelyEquals(ozms.getPymelRotation(nControl), [0.0,0.0,0.0]):
            movedControls.append(nControl)
            continue
        if not tkc.listsBarelyEquals(nControl.getScale(), [1.0,1.0,1.0]):
            movedControls.append(nControl)
            continue

    return movedControls
    
def OscarGetMovedControls():
    return OscarFilterPosed(OscarGetAllControls())

def OscarGetOpposite(inObjs):
    #pre-compile regexes
    leftregexes = []
    rightregexes = []
    for prefixIndex in range(len(CONST_LEFTPREFIXES)):
        leftPrefix = CONST_LEFTPREFIXES[prefixIndex]
        rightPrefix = CONST_RIGHTPREFIXES[prefixIndex]

        leftregexes.append([re.compile(leftPrefix), rightPrefix.replace("^", "")])
        rightregexes.append([re.compile(rightPrefix), leftPrefix.replace("^", "")])
    
    symSelection = []
    for selObj in inObjs:
        oppositeName = selObj.name()
        regexes = []
        for regexRule in leftregexes:
            if regexRule[0].search(oppositeName):
                regexes = leftregexes
                break
        if len(regexes) == 0:
            for regexRule in rightregexes:
                if regexRule[0].search(oppositeName):
                    regexes = rightregexes
                    break

        for regexRule in regexes:
            oppositeName = regexRule[0].sub(regexRule[1], oppositeName)
        if oppositeName != selObj.name() and pc.objExists(oppositeName):
            symSelection.append(pc.PyNode(oppositeName))
        
    return symSelection

def OscarMirrorSel():
    for selObj in pc.selected():
        opposites = OscarGetOpposite([selObj])
        if len(opposites) > 0:
            opposite = opposites[0]
            opposite.t.set(selObj.t.get())
            opposite.r.set(selObj.r.get())

def OscarHide(inControls, ns="*"):
    if isinstance(inControls, basestring):
        inControls = [inControls]
    
    for control in inControls:
        #find object
        pattern = control

        if ns != "*":
            if not ns.endswith(":"):
                ns = ns + ":"
    
            pattern = ns + pattern
        else:
            pattern = ["*:" + pattern, pattern]
    
        toHides = pc.ls(pattern)
    
        #find rigStuff
        for toHide in toHides:
            attrs = pc.ls(toHide.namespace() + "*.RigStuff")
            if len(attrs) > 0:
                #connect
                shape = toHide
                if shape.type() == "transform":
                    shape = toHide.getShape() or toHide
                attrs[0] >> shape.v

def OscarRemoveControls(inControls, inHide=True, ns="*"):
    if isinstance(inControls, basestring):
        inControls = [inControls]

    #find "KeySets" property
    pattern = "*" + tkc.CONST_KEYSETSPROP

    if ns != "*":
        if not ns.endswith(":"):
            ns = ns + ":"

        pattern = ns + pattern
    else:
        pattern = ["*:" + pattern, pattern]

    props = pc.ls(pattern, transforms=True)
    
    hidden = []

    for prop in props:
        attrs = tkc.getParameters(prop)
        
        for attr in attrs:
            modified = False                    
            value = prop.attr(attr).get()
            
            for control in inControls:
                foundValue = None
                candidate = "${0},".format(control)
                if candidate in value:
                    foundValue = candidate
                else:
                    candidate = ",${0}".format(control)
                    if candidate in value:
                        foundValue = candidate
                
                if not foundValue is None:
                    modified = True
                    value = value.replace(foundValue, "")

                    if inHide and not control in hidden:
                        OscarHide(control)
                        hidden.append(control)

            if modified:
                prop.attr(attr).set(value)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
   ____            _             _   _                              
  / ___|___  _ __ | |_ _ __ ___ | | | |    __ _ _   _  ___ _ __ ___ 
 | |   / _ \| '_ \| __| '__/ _ \| | | |   / _` | | | |/ _ \ '__/ __|
 | |__| (_) | | | | |_| | | (_) | | | |__| (_| | |_| |  __/ |  \__ \
  \____\___/|_| |_|\__|_|  \___/|_| |_____\__,_|\__, |\___|_|  |___/
                                                |___/               

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def connectThrough(sourceAttr, destAttr, blendAttr, blendAttr2=None):
    #print "connectThrough(sourceAttr %s, destAttr %s, blendAttr %s)" % (sourceAttr, destAttr, blendAttr)

    if blendAttr2 != None:
        blendNode2 = pc.shadingNode("multDoubleLinear", asUtility=True, name=destAttr.replace(".", "_") + "_LayerMBlend2")
        pc.connectAttr(blendAttr, blendNode2.name() + ".input1")
        pc.connectAttr(blendAttr2, blendNode2.name() + ".input2")

        blendAttr = blendNode2.name() + ".output"

    reverseName = blendAttr.replace(".", "_") + "_Reverse"
    if not pc.objExists(reverseName):
        reverseNode = pc.shadingNode("reverse", asUtility=True, name=reverseName)
        pc.connectAttr(blendAttr, reverseNode.name() + ".inputX")
    
    blendNode = pc.shadingNode("multDoubleLinear", asUtility=True, name=destAttr.replace(".", "_") + "_LayerMBlend")
    pc.connectAttr(sourceAttr, blendNode.name() + ".input1")
    pc.connectAttr(blendAttr, blendNode.name() + ".input2")

    blendNodeNeutral = pc.shadingNode("multDoubleLinear", asUtility=True, name=destAttr.replace(".", "_") + "_LayerNBlend")
    pc.setAttr(blendNodeNeutral.name() + ".input1", pc.getAttr(destAttr))
    pc.connectAttr(reverseName + ".output.outputX", blendNodeNeutral.name() + ".input2")
    
    blendAddNode = pc.shadingNode("addDoubleLinear", asUtility=True, name=destAttr.replace(".", "_") + "_LayerBlendAdd")
    pc.connectAttr(blendNode.name() + ".output", blendAddNode.name() + ".input1")
    pc.connectAttr(blendNodeNeutral.name() + ".output", blendAddNode.name() + ".input2")
    
    pc.connectAttr(blendAddNode.name() + ".output", destAttr)

def createControlLayer(inRefObj, inRigObj, considerPosition=False, considerRotation=False, localOnly=True, inAttrHolder=None, inAttrName="mocap", inGlobalBlendAttrName=None):
    parentObj = tkc.getParent(inRigObj)
    parentRef = tkc.getParent(inRefObj)
    
    buffered = inRigObj
    neutralPose = tkc.getNeutralPose(buffered)
    while(neutralPose != None):
        buffered = neutralPose
        neutralPose = tkc.getNeutralPose(buffered)

    buffer = tkc.addBuffer(buffered, inSuffix="CtrlLayer")
    
    parentMatcher = pc.group(name=inRigObj.name() + "_parentMatcher", empty=True, parent=parentRef)
    tkc.matchTRS(parentMatcher, parentObj)
    if not localOnly:
        tkc.constrain(parentMatcher, parentObj)

    localSpace = pc.group(name=inRigObj.name() + "_localSpace", empty=True, parent=inRefObj)
    tkc.matchTRS(localSpace, inRigObj)

    localMatcher = pc.group(name=inRigObj.name() + "_localMatcher", empty=True, parent=parentMatcher)
    tkc.matchTRS(localMatcher, inRigObj)
    
    if not pc.attributeQuery( inAttrName,node=inRigObj ,exists=True ):
        pc.addAttr(inRigObj, at="long", longName=inAttrName, keyable=True, defaultValue=1.0, minValue=0.0, maxValue=1.0, softMinValue=0.0, softMaxValue=1.0)
        pc.setAttr("{0}.{1}".format(inRigObj.name(), inAttrName), 1)

    cns = tkc.constrain(localMatcher, localSpace)
    if considerRotation:
        connectThrough(localMatcher.name() + ".rx", buffer.name() + ".rx", inRigObj.name() + "." + inAttrName, inGlobalBlendAttrName)
        connectThrough(localMatcher.name() + ".ry", buffer.name() + ".ry", inRigObj.name() + "." + inAttrName, inGlobalBlendAttrName)
        connectThrough(localMatcher.name() + ".rz", buffer.name() + ".rz", inRigObj.name() + "." + inAttrName, inGlobalBlendAttrName)
    else:
        pc.disconnectAttr(cns.name() + ".constraintRotateX", localMatcher.name() + ".rotateX")
        pc.disconnectAttr(cns.name() + ".constraintRotateY", localMatcher.name() + ".rotateY")
        pc.disconnectAttr(cns.name() + ".constraintRotateZ", localMatcher.name() + ".rotateZ")

    if considerPosition:
        connectThrough(localMatcher.name() + ".tx", buffer.name() + ".tx", inRigObj.name() + "." + inAttrName, inGlobalBlendAttrName)
        connectThrough(localMatcher.name() + ".ty", buffer.name() + ".ty", inRigObj.name() + "." + inAttrName, inGlobalBlendAttrName)
        connectThrough(localMatcher.name() + ".tz", buffer.name() + ".tz", inRigObj.name() + "." + inAttrName, inGlobalBlendAttrName)
    else:
        pc.disconnectAttr(cns.name() + ".constraintTranslateX", localMatcher.name() + ".translateX")
        pc.disconnectAttr(cns.name() + ".constraintTranslateY", localMatcher.name() + ".translateY")
        pc.disconnectAttr(cns.name() + ".constraintTranslateZ", localMatcher.name() + ".translateZ")
"""
Old version of the template, we will need more info to manage a whole rig
----------------------------
{mocapMarkerName:(ControllerName, considerPosition, considerRotation)}

template = {    "cha_GB_MOC_LEyebrowEnd":("Left_Eyebrow_Out", True, False),
                "cha_GB_MOC_LEyebrowMid":("Left_Eyebrow_Mid", True, False),
                "cha_GB_MOC_LEyebrowStart":("Left_Eyebrow_In", True, False),
                "cha_GB_MOC_REyebrowEnd":("Right_Eyebrow_Out", True, False),
                "cha_GB_MOC_REyebrowMid":("Right_Eyebrow_Mid", True, False),
                "cha_GB_MOC_REyebrowStart":("Right_Eyebrow_In", True, False),
                "cha_GB_MOC_LMouthCorner":("Left_MouthCorner", True, False),
                "cha_GB_MOC_RMouthCorner":("Right_MouthCorner", True, False),
                "cha_GB_MOC_RMouthCorner":("Right_MouthCorner", True, False),
                "cha_GB_MOC_LLipUpperBend":("Left_UpperLip_Inter", True, False),
                "cha_GB_MOC_RLipUpperBend":("Right_UpperLip_Inter", True, False),
                "cha_GB_MOC_LLipLowerBend":("Left_LowerLip_Inter", True, False),
                "cha_GB_MOC_RLipLowerBend":("Right_LowerLip_Inter", True, False),
                "cha_GB_MOC_LipLower":("UpperLip_Center", True, False),
                "cha_GB_MOC_LipUpper":("LowerLip_Center", True, False),
                "TK_cha_GB_MOC_jaw":("Jaw_Bone_Ctrl", True, True),
                "cha_GB_MOC_LPuffer":("Left_Cheek", True, False),
                "cha_GB_MOC_RPuffer":("Right_Cheek", True, False),
                "cha_GB_MOC_LEye":("Left_Eye", False, True),
                "cha_GB_MOC_REye":("Right_Eye", False, True)
            }

injectControlLayer("mocap_optical", "TK_Head_FK_Main_Deform", template)

New version (backward incompatible)
{ControllerName:(mocapMarkerName, considerPosition, considerRotation, localOnly matchingFunction, realMocapMarkers())}

localOnly is a boolean indicating if we need to use local offsets only from mocap template

matchingFunction is a function taking *args, a list of markers names, and outputs a "new marker" (a new object to be used for matching, named like "ControllerName" argument in the template)
matchingFunctions that will be usefull:
-aimMatcher
-poleMatcher

realMocapMarkers is a list of real Markers names, used by the matching function to create a new object (named like "ControllerName" argument in the template)

New version of the template
----------------------------
                #mocapMarkerName:(ControllerName, considerPosition, considerRotation, localOnly matchingFunction, realMocapMarkers)
template = {    #Spine/Head
                "WOLF_Hips":("Spine_01", True, True),
                "WOLF_Spine":("Spine_02", False, True),
                "WOLF_Spine1":("Spine_03", False, True),
                "WOLF_Spine2":("Spine_04", False, True),
                "WOLF_Neck":("Neck_01", False, True),
                "WOLF_Neck1":("Neck_03", False, True),
                "WOLF_Head":("Head", True, True),

                #Left fore leg
                #Left fore leg IK
                "WOLF_RightFingerBase":("Left_Fore_DogLeg_IK", True, True, False),
                "WOLF_RightForePoleVector":("Left_Fore_UpV", True, False, False, "poleMatcher", ("WOLF_RightArm", "WOLF_RightForeArm", "WOLF_RightHand")),
                "WOLF_RightHand":("Left_Fore_Reverse_03", False, True, False),
                "WOLF_RightHandMiddle1":("Left_Fore_FOOT_03", False, True),

                #Right fore leg
                #Right fore leg IK
                "WOLF_LeftFingerBase":("Right_Fore_DogLeg_IK", True, True, False),
                "WOLF_LeftForePoleVector":("Right_Fore_UpV", True, False, False, "poleMatcher", ("WOLF_LeftArm", "WOLF_LeftForeArm", "WOLF_LeftHand")),
                "WOLF_LeftHand":("Right_Fore_Reverse_03", False, True, False),
                "WOLF_LeftHandMiddle1":("Right_Fore_FOOT_03", False, True),

                #Left rear leg
                #Left rear leg IK
                "WOLF_RightToeBase":("Left_Rear_DogLeg_IK", True, True, False),
                "WOLF_RightRearPoleVector":("Left_Rear_UpV", True, False, False, "poleMatcher", ("WOLF_RightUpLeg", "WOLF_RightLeg", "WOLF_RightFoot")),
                "WOLF_RightFoot":("Left_Rear_Reverse_03", False, True, False),
                "WOLF_RightFootMiddle1":("Left_Rear_FOOT_03", False, True),

                #Right rear leg
                #Right rear leg IK
                "WOLF_LeftToeBase":("Right_Rear_DogLeg_IK", True, True, False),
                "WOLF_LeftRearPoleVector":("Right_Rear_UpV", True, False, False, "poleMatcher", ("WOLF_LeftUpLeg", "WOLF_LeftLeg", "WOLF_LeftFoot")),
                "WOLF_LeftFoot":("Right_Rear_Reverse_03", False, True, False),
                "WOLF_LeftFootMiddle1":("Right_Rear_FOOT_03", False, True),

                #Tail
                "WOLF_Tail1":("Tail_01", True, True),
                "WOLF_Tail2":("Tail_02", False, True),
                "WOLF_Tail3":("Tail_03", False, True),
                "WOLF_Tail4":("Tail_04", False, True),
                "WOLF_Tail5":("Tail_05", False, True)
           }

tkRig.injectControlLayer("Reference", "Local_COG", template)

Todo :  -Invert key/value     

"""
def injectControlLayer(inCLRootName, inRigRootName, inTemplate, inAttrHolder=None, inAttrName="mocap"):
    clRoot = pc.PyNode(inCLRootName)
    rigRoot = pc.PyNode(inRigRootName)
    
    clNS = clRoot.namespace()
    rigNS = rigRoot.namespace()
    
    tkc.constrain(clRoot, rigRoot, "Pose")
    
    for key in inTemplate.keys():
        templateObj = ""

        connectionData = inTemplate[key]
        rigObj = rigNS + key
        if not pc.objExists(rigObj):
            pc.warning("Can't find object for template key %s" % rigObj)
            continue

        if len(connectionData) >= 5:#Custom relation (using a custom function and list of source markers)
            func = connectionData[4]
            if isinstance(func, str):
                func = eval(func)
            #print "func", func

            args = [clNS, connectionData[0]]
            args.extend(connectionData[5])
            #print "args", args

            #execute matcher function
            matcher = func(*args)
            #print "matcher", matcher

            if matcher != None:
                templateObj = matcher
            else:
                pc.warning("Can't find custom object with function  %s(%s)" % (connectionData[4], str(args)))
                continue

        else:#Direct relation (getting position and/or rotation)
            templateObj = clNS + connectionData[0]
            if not pc.objExists(templateObj):
                pc.warning("Can't find object for template value %s" % templateObj)
                continue
        
        if templateObj != "":
            localOnly=True
            if len(connectionData) >= 4:
                localOnly=connectionData[3]
            
            globalAttr = None

            if inAttrHolder != None:
                if not pc.attributeQuery( inAttrName,node=inAttrHolder, exists=True):
                    pc.addAttr(inAttrHolder, at="long", longName=inAttrName, keyable=True, defaultValue=0.0, minValue=0.0, maxValue=1.0, softMinValue=0.0, softMaxValue=1.0)
                globalAttr = "{0}.{1}".format(inAttrHolder, inAttrName)

            createControlLayer(pc.PyNode(templateObj), pc.PyNode(rigObj), connectionData[1], connectionData[2], localOnly, inAttrHolder, inAttrName, globalAttr)

def poleMatcher(*args):
    ns = args[0]

    topObjName = ns+args[2]
    middleObjName = ns+args[3]
    downObjName = ns+args[4]

    target = pc.group(empty=True, parent=topObjName, name=ns+args[1])

    tkc.createResPlane(target, pc.PyNode(topObjName), pc.PyNode(middleObjName), pc.PyNode(downObjName))

    return target.name()

def alternateParent(*args):
    ns = args[0]

    objName = ns+args[2]
    parentName = ns+args[3]

    target = pc.group(empty=True, parent=parentName, name=ns+args[1])
    tkc.constrain(target, pc.PyNode(objName))

    return target.name()

def clusterize(inCurve):
    clusters=[]
    
    crvShape = inCurve
    if inCurve.type() =="transform":
        crvShape = inCurve.getShape()

    for i in range(crvShape.numCVs()):
        clusterComponents = pc.cluster(crvShape.name() + ".cv[%i]" % i,name=crvShape.name() + "_cluster_%02i" % i)
        clusters.append(clusterComponents[1])
        
    return clusters

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ____  _             _             
 |  _ \(_) __ _  __ _(_)_ __   __ _ 
 | |_) | |/ _` |/ _` | | '_ \ / _` |
 |  _ <| | (_| | (_| | | | | | (_| |
 |_| \_\_|\__, |\__, |_|_| |_|\__, |
          |___/ |___/         |___/ 

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def fuseDictionaries(sourceNs, destinationNs, dictPattern):
    sourceDictName = sourceNs + dictPattern
    sourceDictList = pc.ls(sourceDictName)
    sourceDict = None if len(sourceDictList) == 0 else sourceDictList[0]
    if sourceDict != None:
        destinationDictName = sourceDictName.replace(sourceNs, destinationNs)
        if pc.objExists(destinationDictName):
            params = tkc.getParameters(sourceDict)
            for param in params:
                if not pc.attributeQuery(param, node=destinationDictName, exists=True):
                    tkc.addParameter(pc.PyNode(destinationDictName), param, inType="string", default=pc.getAttr("{0}.{1}".format(sourceDict.name(), param)))
        else:
            pc.warning("Destination dictionary cannot be found ({0})".format(destinationDictName))
    else:
        pc.warning("Source dictionary cannot be found ({0})".format(sourceDictName))

def fuseRigs(inSourceTopNodeOrPath, inDestinationTopNodeOrPath, inSourceJointsMapping=None, inDestinationJointsMapping=None, inSourceReConstraints=None, inDestinationReConstraints=None, inMoveNodes=True, inCtrlSet=None, inDebug=True):
    if inDebug:
        print "Source",inSourceTopNodeOrPath,"Dest",inDestinationTopNodeOrPath,"SourceJointsMap",inSourceJointsMapping,"DestJointsMap",inDestinationJointsMapping,"ReConstraints",inSourceReConstraints

    # ! importFile ?
    sourceTopNode = inSourceTopNodeOrPath
    sourceNs = sourceTopNode.namespace()

    destinationTopNode = inDestinationTopNodeOrPath
    destinationNs = destinationTopNode.namespace()

    #Get rid of references
    if pc.referenceQuery(sourceTopNode, isNodeReferenced=True):
        refFile = pc.FileReference(namespace=sourceNs)
        refFile.importContents()

    if pc.referenceQuery(destinationTopNode, isNodeReferenced=True):
        refFile = pc.FileReference(namespace=destinationNs)
        refFile.importContents()

    canUseNamespaces = sourceNs != destinationNs

    #Geometries dictionary will help taking good decisions on skin fusion and on which Geometry to keep or drop, based on skinClusters and joints mapping
    #DataModel : {geoShortName:{sourceData:{geoNode:PyNode, skinNode:PyNode,influences:[PyNode,]}},{destinationData:{geoNode:PyNode, skinNode:PyNode,influences:[PyNode,]}}, fromSource:bool}
    GeometriesDict = {}

    #DataModel : {infShortName:infNode}
    SourceInfsDict = {}

    #DataModel : {infShortName:infNode}
    DestinationInfsDict = {}

    toDelete = []

    #Fuse skinClusters
    print ""
    print "Fuse skinClusters..."
    #First collect skinClusters and influences 
    skins = pc.ls(type="skinCluster")

    for skin in skins:
        geoNode = skin.getGeometry()[0]
        if not geoNode.type() in ALLOWED_GEOMETRIES:
            continue
        influences = pc.skinCluster(skin,query=True,inf=True)

        #First prune and remove unused so we're sure not to do inconsistent choices on skin complexity
        pc.skinPercent(skin, geoNode, pruneWeights=0.01 )
        removedInfs = tkc.removeUnusedInfs(skin, influences)
        for removedInf in removedInfs:
            removeInfNode = pc.PyNode(removedInf)
            if removeInfNode in influences:
                influences.remove(removeInfNode)

        shortName = str(geoNode.stripNamespace())
        fromSource = tkc.isChildOf(geoNode, sourceTopNode, canUseNamespaces)
        data = {"geoNode":geoNode, "skinNode":skin, "influences":influences}

        if not shortName in GeometriesDict:
            GeometriesDict[shortName] = {"fromSource":False}
        GeometriesDict[shortName][("sourceData" if fromSource else "destinationData")] = data

        if fromSource:
            GeometriesDict[shortName]["sourceData"] = data
            for infNode in influences:
                if not infNode.stripNamespace() in SourceInfsDict:
                    SourceInfsDict[infNode.stripNamespace()] = infNode
        else:
            GeometriesDict[shortName]["destinationData"] = data
            for infNode in influences:
                if not infNode.stripNamespace() in DestinationInfsDict:
                    DestinationInfsDict[infNode.stripNamespace()] = infNode

    if inDebug:
        debugDict = copy.deepcopy(GeometriesDict)
        for geoShortName, geoData in debugDict.iteritems():
            for key, value in geoData.iteritems():
                if key != "fromSource":
                    value["geoNode"] = value["geoNode"].name()
                    value["skinNode"] = value["skinNode"].name()
                    value["influences"] = ",".join([n.name() for n in value["influences"]])
        print ""
        print json.dumps(debugDict, sort_keys=True, indent=4)

    #Here we'll do the real skinCluster rebuild, and decide at last which geometry to use
    #Find PyNodes for the mapping
    sourceJointMapping = {}
    destJointMapping = {}

    if not inSourceJointsMapping is None:
        for key, value in inSourceJointsMapping.iteritems():
            if key == "":
                key = None
            else:
                if key in SourceInfsDict:
                    key = SourceInfsDict[key]
                else:
                    if inDebug:
                        print " - Source key {0} not found !".format(key)
                    key = None
            if value == "":
                value = None
            else:
                if isinstance(value, list):
                    realValue = []
                    for valueItem in value:
                        if valueItem == "*":
                            realValue.append(valueItem)
                        else:
                            if valueItem in DestinationInfsDict:
                                realValue.append(DestinationInfsDict[valueItem])
                            else:
                                if inDebug:
                                    print " - Source value {0} not found !".format(valueItem)
                    if len(realValue) > 0:
                        value = realValue
                    else:
                        value = None
                else:
                    if value == "*":
                        value = [value]
                    else:
                        if value in DestinationInfsDict:
                            value = [DestinationInfsDict[value]]
                        else:
                            if inDebug:
                                print " - Source value {0} not found !".format(destinationNs+value)
                            value = None
            if key != None or value != None:
                sourceJointMapping[key] = value

    if not inDestinationJointsMapping is None:
        for key, value in inDestinationJointsMapping.iteritems():
            if key == "":
                key = None
            else:
                if key in DestinationInfsDict:
                    key = DestinationInfsDict[key]
                else:
                    if inDebug:
                        print " - Destination key {0} not found !".format(key)
                    key = None
            if value == "":
                value = None
            else:
                if isinstance(value, list):
                    realValue = []
                    for valueItem in value:
                        if valueItem == "*":
                            realValue.append(valueItem)
                        else:
                            if valueItem in SourceInfsDict:
                                realValue.append(SourceInfsDict[valueItem])
                            else:
                                if inDebug:
                                    print " - Destination value {0} not found !".format(valueItem)
                    if len(realValue) > 0:
                        value = realValue
                    else:
                        value = None
                else:
                    if value == "*":
                        value = [value]
                    else:
                        if value in SourceInfsDict:
                            value = [SourceInfsDict[value]]
                        else:
                            if inDebug:
                                print " - Destination value {0} not found !".format(value)
                            value = None
            if key != None or value != None:
                destJointMapping[key] = value

    if inDebug:
        print "destJointMapping",destJointMapping
        print  "sourceJointMapping",sourceJointMapping

    for geoShortName, geoData in GeometriesDict.iteritems():
        if not "sourceData" in geoData:
            if inDebug:
                print "{0} only appears in destination".format(geoShortName)
            if pc.objExists(sourceNs+geoShortName):
                geoT = pc.PyNode(sourceNs+geoShortName).getParent()
                if not geoT in toDelete:
                    toDelete.append(geoT)
        elif not "destinationData" in geoData:
            geoData["fromSource"] = True
            if inDebug:
                print "{0} only appears in source".format(geoShortName)
            if pc.objExists(destinationNs+geoShortName):
                geoT = pc.PyNode(destinationNs+geoShortName).getParent()
                if not geoT in toDelete:
                    toDelete.append(geoT)
        else:
            sourceInfsCount = len(geoData["sourceData"]["influences"])
            destInfsCount = len(geoData["destinationData"]["influences"])

            geoData["sourceData"]["influencesReplacements"] = {}
            for infNode in geoData["sourceData"]["influences"]:
                if infNode in sourceJointMapping:
                    #print "in {0} Source, replacing".format(geoShortName), infNode, "by", sourceJointMapping[infNode]
                    replaced=False
                    for replacementJoint in sourceJointMapping[infNode]:
                        if replacementJoint == "*":
                            geoData["sourceData"]["influencesReplacements"][infNode]="*"
                            sourceInfsCount -= 1
                            replaced=True
                            break
                        else:
                            if replacementJoint in geoData["destinationData"]["influences"]:
                                geoData["sourceData"]["influencesReplacements"][infNode]=replacementJoint
                                sourceInfsCount -= 1
                                replaced=True
                                break
                    if not replaced:
                        if inDebug:
                            pc.warning("No replacement found for {0} in destination influences for {1}, replacing by default by {2}".format(geoData["sourceData"]["geoNode"].name(), infNode.name(), sourceJointMapping[infNode][0]))
                        sourceInfsCount -= 1
                        geoData["sourceData"]["influencesReplacements"][infNode]=sourceJointMapping[infNode][0]

            geoData["destinationData"]["influencesReplacements"] = {}
            for infNode in geoData["destinationData"]["influences"]:
                if infNode in destJointMapping:
                    #print "in {0} Destination, replacing".format(geoShortName), infNode, "by", destJointMapping[infNode]
                    replaced=False
                    for replacementJoint in destJointMapping[infNode]:
                        if replacementJoint == "*":
                            geoData["destinationData"]["influencesReplacements"][infNode]="*"
                            destInfsCount -= 1
                            replaced=True
                            break
                        else:
                            if replacementJoint in geoData["sourceData"]["influences"]:
                                if replacementJoint in sourceJointMapping and ("*" in sourceJointMapping[replacementJoint] or infNode in sourceJointMapping[replacementJoint]):
                                    if inDebug:
                                        print "Replacing {0} in destination skipped, as it exists as a source replacement !".format(infNode)
                                    replaced=True
                                    break
                                geoData["destinationData"]["influencesReplacements"][infNode]=replacementJoint
                                destInfsCount -= 1
                                replaced=True
                                break
                    if not replaced:
                        if inDebug:
                            pc.warning("No replacement found for {0} in source influences for {1}, replacing by default by {2}".format(geoData["destinationData"]["geoNode"].name(), infNode.name(), destJointMapping[infNode][0]))
                        destInfsCount -= 1
                        geoData["destinationData"]["influencesReplacements"][infNode]=destJointMapping[infNode][0]

            geoData["fromSource"] = sourceInfsCount > destInfsCount

            if inDebug:
                print ""
                print "{0} have most of its data in {1} ({2}/{3})".format(geoShortName,
                        "SOURCE" if geoData["fromSource"] else "DESTINATION",
                        sourceInfsCount, destInfsCount)

    #Fuse Geometries
    print ""
    print "Fuse Geometries"
    for geoShortName, geoData in GeometriesDict.iteritems():
        print " -{0} version used for : {1}".format("Source     " if geoData["fromSource"] else "Destination", geoShortName)
        dataName = "sourceData" if geoData["fromSource"] else "destinationData"
        if "influencesReplacements" in geoData[dataName] and len(geoData[dataName]["influencesReplacements"]) > 0:
            for k,v in geoData[dataName]["influencesReplacements"].iteritems():
                if v == "*":
                    otherDataName = "destinationData" if geoData["fromSource"] else "sourceData"
                    tkc.replaceDeformers([k],None,False,[geoData[dataName]["skinNode"]],[geoData[otherDataName]["skinNode"]])
                    print " - Fuse Deformers {0} => {1}".format(k.name(), geoData[otherDataName]["skinNode"].name())
                else:
                    tkc.replaceDeformers([k],v,False,[geoData[dataName]["skinNode"]])
                    print " - ReplaceDeformers {0} => {1}".format(k.name(), v.name())

        if geoData["fromSource"]:
            meshT = geoData["sourceData"]["geoNode"].getParent()
            if "destinationData" in geoData and pc.objExists(geoData["destinationData"]["geoNode"]):
                transform = geoData["destinationData"]["geoNode"].getParent()
                #Reparent
                tranformParent = transform.getParent()
                pc.delete(transform)
                pc.parent(meshT, tranformParent)
            else:
                #Reparent using a name match ?
                destMeshTName = meshT.getParent().name().replace(sourceNs, destinationNs)
                if pc.objExists(destMeshTName):
                    pc.parent(meshT, destMeshTName)
                else:
                    pc.warning("Can't reparent {0}, no valid candidate found in destination ({1}".format(meshT.name(), destMeshTName))
        else:
            if "sourceData" in geoData and pc.objExists(geoData["sourceData"]["geoNode"]):
                transform = geoData["sourceData"]["geoNode"].getParent()
                pc.delete(transform)

    rigStuffAttr = None
    rigStuffAttrs = pc.ls(destinationNs+"*.RigStuff")

    if len(rigStuffAttrs) > 0:
        rigStuffAttr = rigStuffAttrs[0]

    sourceExceptions = []
    destinationExceptions = []

    #reConstraints
    if not inSourceReConstraints is None:
        for source, target in inSourceReConstraints.iteritems():
            if pc.objExists(sourceNs+source) and pc.objExists(destinationNs+target):
                sourceNode = pc.PyNode(sourceNs+source)
                targetNode = pc.PyNode(destinationNs+target)
                tkc.removeAllCns(sourceNode)
                try:
                    tkc.constrain(sourceNode, targetNode)
                except:
                    pass
                try:
                    tkc.constrain(sourceNode, targetNode, "Scaling")
                except:
                    pass
                if tkc.isElement(sourceNode):
                    shapes = sourceNode.getShapes()
                    for shape in shapes:
                        if rigStuffAttr != None:
                            rigStuffAttr >> shape.overrideVisibility
                        else:
                            shape.overrideVisibility = 0
                    sourceExceptions.append(source)
                    if inCtrlSet != None and pc.objExists(sourceNs+inCtrlSet):
                        if pc.sets(sourceNs+inCtrlSet,im=sourceNode):
                            pc.sets(sourceNs+inCtrlSet,rm=sourceNode)
            else:
                pc.warning("Some objects can't be found for source constraints : {0} => {1}".format(sourceNs+source, destinationNs+target))
    if not inDestinationReConstraints is None:
        for source, target in inDestinationReConstraints.iteritems():
            if pc.objExists(destinationNs+source) and pc.objExists(sourceNs+target):
                sourceNode = pc.PyNode(destinationNs+source)
                targetNode = pc.PyNode(sourceNs+target)
                tkc.removeAllCns(sourceNode)
                try:
                    tkc.constrain(sourceNode, targetNode)
                except:
                    pass
                try:
                    tkc.constrain(sourceNode, targetNode, "Scaling")
                except:
                    pass
                if tkc.isElement(sourceNode):
                    shapes = sourceNode.getShapes()
                    for shape in shapes:
                        if rigStuffAttr != None:
                            rigStuffAttr >> shape.overrideVisibility
                        else:
                            shape.overrideVisibility = 0
                    destinationExceptions.append(source)
                    if inCtrlSet != None and pc.objExists(destinationNs+inCtrlSet):
                        if pc.sets(destinationNs+inCtrlSet,im=sourceNode):
                            pc.sets(destinationNs+inCtrlSet,rm=sourceNode)
            else:
                pc.warning("Some objects can't be found for destination constraints : {0} => {1}".format(sourceNs+source, destinationNs+target))

    #Fuse Rig elements
    if inMoveNodes:
        nodes = OscarGetNodes(sourceNs)

        for node in nodes:
            otherNodeName = node.name().replace(sourceNs, destinationNs)
            if pc.objExists(otherNodeName):
                #Rename and constrain
                if inDebug:
                    print "Rename and constrain",node.name()
                
                toRename = []
                otherNode = pc.PyNode(otherNodeName)
                children = node.getChildren(allDescendents=True, type='transform')
                for child in children:

                    if tkc.isElement(child):#3D Elements are constrained
                        if inDebug:
                            print " -child {0} is Element".format(child.name())
                        otherObjName = child.name().replace(sourceNs, destinationNs)
                        if pc.objExists(otherObjName):
                            otherObj = pc.PyNode(otherObjName)
                            tkc.removeAllCns(child)
                            tkc.constrain(child, otherObj)
                            try:
                                tkc.constrain(child, otherObj, "Scaling")
                            except:
                                pass
                        shapes = child.getShapes()
                        for shape in shapes:
                            if rigStuffAttr != None:
                                rigStuffAttr >> shape.overrideVisibility
                            else:
                                shape.overrideVisibility = 0
                        if inCtrlSet != None and pc.objExists(sourceNs+inCtrlSet):
                            if pc.sets(sourceNs+inCtrlSet,im=child):
                                pc.sets(sourceNs+inCtrlSet,rm=child)
                        params = tkc.getParameters(child)
                        for param in params:
                            if pc.getAttr(child.name() + "." + param, settable=True):
                                if not pc.attributeQuery(param, node=otherObj, exists=True):
                                    definition = tkc.getDefinition(child.name() + "." + param)
                                    #pc.warning(param + " definition !! " + str(definition))
                                    tkc.addParameter(otherObj, name=param, inType=definition[0], default=definition[1], min=definition[2], max = definition[3], softmin=definition[4], softmax=definition[5])
                                if inDebug:
                                    print child.name() + "." + param + " CONNECTED TO " + otherObj.name() + "." + param
                                pc.connectAttr(otherObj.name() + "." + param, child.name() + "." + param)
                    elif tkc.isProperty(child):#Parameters are linked
                        if child.name().endswith(tkc.CONST_ATTRIBUTES):
                            continue
                        if inDebug:
                            print " -child {0} is Property".format(child.name())
                        propertyParent = child.getParent()
                        otherParentName = propertyParent.name().replace(sourceNs, destinationNs)
                        if not pc.objExists(otherParentName):
                            pc.error("Can't find parent for source property ({0}) !".format(otherParentName))
                        otherParent = pc.PyNode(otherParentName)
                        otherObjName = child.name().replace(sourceNs, destinationNs)
                        otherObj = None
                        if pc.objExists(otherObjName):
                            otherObj = pc.PyNode(otherObjName)
                        else:
                            otherObj = pc.group(empty=True, name=otherObjName, parent=otherParent)
                        params = tkc.getParameters(child)
                        for param in params:
                            if pc.getAttr(child.name() + "." + param, settable=True):
                                if not pc.attributeQuery(param, node=otherObj, exists=True):
                                    definition = tkc.getDefinition(child.name() + "." + param)
                                    #pc.warning(param + " definition !! " + str(definition))
                                    tkc.addParameter(otherObj, name=param, inType=definition[0], default=definition[1], min=definition[2], max = definition[3], softmin=definition[4], softmax=definition[5])
                                if inDebug:
                                    print child.name() + "." + param + " CONNECTED TO " + otherObj.name() + "." + param
                                pc.connectAttr(otherObj.name() + "." + param, child.name() + "." + param)

                    toRename.append(child)
                toRename.append(node)

                for toRenameObj in toRename:
                    toRenameObj.rename(destinationNs+toRenameObj.name().replace(":", "__"))
                otherNode.getParent().addChild(node)
            else:
                #Simply move
                #Find/create first common parent
                print "Simply move",node.name()
                allParents = node.getAllParents()
                hierarchy=[]
                newParent=None
                for parent in allParents:
                    otherParentName = parent.name().replace(sourceNs, destinationNs)
                    if not pc.objExists(otherParentName):
                        hierarchy.append(otherParentName)
                    else:
                        newParent = pc.PyNode(otherParentName)
                        break

                for newChild in hierarchy:
                    newParent = pc.group(empty=True, name=newChild, parent=newParent)
                newParent.addChild(node)

                children = node.getChildren(allDescendents=True, type='transform')
                for child in children:
                    child.rename(child.name().replace(sourceNs, destinationNs))
                node.rename(node.name().replace(sourceNs, destinationNs))

        #Fuse Publish-Related data
        #Attributes (Synoptic)
        #maybe todo

        #TK_KeySets
        sourceKeySetsName = sourceNs + "*_TK_KeySets"
        sourceKeySetsList = pc.ls(sourceKeySetsName)
        sourceKeySets = None if len(sourceKeySetsList) == 0 else sourceKeySetsList[0]
        if sourceKeySets != None:
            destinationKeySetsName = sourceKeySets.name().replace(sourceNs, destinationNs)
            if pc.objExists(destinationKeySetsName):
                params = tkc.getParameters(sourceKeySets)
                for param in params:
                    valuesStr = pc.getAttr("{0}.{1}".format(sourceKeySets.name(), param))
                    valuesList = valuesStr.split(",")

                    #Remove source "Control" objects constrained by something else in destination
                    for objException in sourceExceptions:
                        if "$"+objException in valuesList:
                            valuesList.remove("$"+objException)

                    if not pc.attributeQuery(param, node=destinationKeySetsName, exists=True ):
                        tkc.addParameter(pc.PyNode(destinationKeySetsName), name=param, inType="string", default=",".join(valuesList))
                    else:
                        otherValuesList = pc.getAttr("{0}.{1}".format(destinationKeySetsName, param)).split(",")
                        for otherValue in otherValuesList:
                            if not otherValue in valuesList:
                                valuesList.append(otherValue)
                        pc.setAttr("{0}.{1}".format(destinationKeySetsName, param), ",".join(valuesList))

                if len(destinationExceptions) > 0:#Remove destination "Control" objects constrained by something else in source
                    params = tkc.getParameters(pc.PyNode(destinationKeySetsName))
                    for param in params:
                        valuesStr = pc.getAttr("{0}.{1}".format(destinationKeySetsName, param))
                        valuesList = valuesStr.split(",")
                        modified=False
                        for objException in destinationExceptions:
                            if "$"+objException in valuesList:
                                valuesList.remove("$"+objException)
                                modified=True
                        if modified:
                            pc.setAttr("{0}.{1}".format(destinationKeySetsName, param), ",".join(valuesList))
            else:
                pc.warning("!!! Destination KeySets cannot be found !!!")
        else:
            pc.warning("!!! Source KeySets cannot be found !!!")
        #Dictionaries
        #TK_CtrlsDic
        fuseDictionaries(sourceNs, destinationNs, "*_TK_CtrlsDic")
        #TK_CtrlsChannelsDic
        fuseDictionaries(sourceNs, destinationNs, "*_TK_CtrlsChannelsDic")
        #TK_ParamsDic
        fuseDictionaries(sourceNs, destinationNs, "*_TK_ParamsDic")
        
        #Other "rig root" objects (Reference ?)   
        #maybe todo

    #Fuse sets
    sets = [objSet for objSet in pc.ls(sourceNs + "*", sets=True) if tkc.isSimpleObjectSet(objSet.name())]
    for setNode in sets:
        otherSetName = setNode.name().replace(sourceNs, destinationNs)
        if pc.objExists(otherSetName):
            pc.sets(otherSetName, include=setNode.members())
            toDelete.append(setNode)
        else:
            setNode.rename(setNode.name().replace(sourceNs, destinationNs))

    if len(toDelete) > 0:
        if inDebug:
            print "Delete :\r\n", "\r\n".join([obj.name() for obj in toDelete])
        pc.delete(toDelete)

    #Move/Remove geometries with no skinCluster ?
    #maybe todo

def bake(inGeoNullName="Geometries", inJointsFilters=None, inToPreserve=None, inParents=None, inJointRadius=0.7, inJointPrefix="", inStart=None, inEnd=None):
    #collect skinned geometries and influences
    geosT = []
    allInfs = []
    createdJoints = []
    root = None

    toDelete = []

    if not pc.objExists(inGeoNullName):
        pc.warning("Given object for Geometry container ('{0}'') does not exists !".format(inGeoNullName))
        return createdJoints

    geometries = pc.PyNode(inGeoNullName)
    ns = geometries.namespace()

    if inToPreserve == None:
        inToPreserve = []

    #Resolve variables in parents dictionary
    if inParents == None:
        inParents = {"":DEFAULT_JOINT_PARENT}
    elif not "" in inParents:
        inParents[""] = DEFAULT_JOINT_PARENT

    parentsMapping = {}
    for key, value in inParents.iteritems():
        parentsMapping[key] = ns+value

    #Get rid of reference
    if pc.referenceQuery(geometries, isNodeReferenced=True):
        refFile = pc.FileReference(namespace=ns)
        refFile.importContents()

    skins = pc.ls(type="skinCluster")
    for skin in skins:
        geoT = skin.getGeometry()[0].getParent()
        isBaked=False
        if tkc.isVisibleAfterAll(skin.getGeometry()[0]):
            infs = pc.skinCluster(skin,query=True,inf=True)

            for inf in infs:
                if not inf in allInfs:
                    valid = False
                    if inJointsFilters == None:
                        valid=True
                    else:
                        for inJointsFilter in inJointsFilters:
                            if inf.name().startswith(inJointsFilter):
                                valid=True
                    if valid:
                        isBaked = True
                        allInfs.append(inf)
                else:
                    isBaked = True

            if isBaked and not geoT in geosT:
                geosT.append(geoT)

    if len(allInfs) == 0:
        pc.warning("No influences found !")
        return None

    root = tkc.getParent(allInfs[0], model=True)
    skins = tkc.storeSkins(geosT)

    pc.select(clear=True)
    createdJoints = []
    for inf in allInfs:
        origName = inf.name()
        inf.rename(origName+"_old")
        infDupe = pc.joint(name=origName, radius=inJointRadius)

        infParentName = parentsMapping[""] if not origName in parentsMapping else parentsMapping[origName]
        infParentObj = None
        if pc.objExists(infParentName):
            infParentObj = pc.PyNode(infParentName)
        else:
            infParentObj = pc.group(name=infParentName, empty=True, parent=root)
            inToPreserve.append(infParentObj)

        infParentObj.addChild(infDupe)
        tkc.constrain(infDupe, inf, "Position", False)
        tkc.constrain(infDupe, inf, "Orientation", False)
        connectScaling(infDupe,inf)
        createdJoints.append(infDupe)

    #Bake deformers animation
    if inStart == None:
        inStart = pc.playbackOptions(query=True, animationStartTime=True)
    if inEnd == None:
        inEnd = pc.playbackOptions(query=True, animationEndTime=True)
    
    mel.eval("paneLayout -e -manage false $gMainPane")
    pc.bakeResults(createdJoints, simulation=True, sampleBy=1, t=(inStart,inEnd), disableImplicitControl=True, preserveOutsideKeys=True, sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, bakeOnOverrideLayer=False, minimizeRotation=True, controlPoints=False, shape=False)
    mel.eval("paneLayout -e -manage true $gMainPane")

    pc.currentTime(inStart)
    for skin in skins:
        tkc.loadSkin(skin)

    if inJointPrefix != "":
        for createdJoint in createdJoints:
            createdJoint.rename(createdJoint.namespace() + inJointPrefix + createdJoint.stripNamespace())

    children = root.getChildren()

    for child in children:
        if not child in toDelete:
            toDelete.append(child)

    toPreserve = [geometries]

    #! need PyNodes here...
    if inToPreserve != None:
        toPreserve.extend(inToPreserve)

    for child in toDelete:
        if not child in toPreserve:
            print "DELETE " + child.name()
            #pc.delete(child)
        else:
            print "Skip deleting " + child.name()

    return createdJoints

"""

EXAMPLE USAGE OF fuseRigs AND bake to fuse and bake facial to body of Invisible Hours RigStuff

import tkRig

def resolveDictionary(inDict, inVariables):
    rebuilt = {}
    for key, value in inDict.iteritems():
        for search, replace in inVariables.iteritems():
            if search in key:
                key = key.replace(search, replace)
            if search in value:
                value = value.replace(search, replace)
        rebuilt[key] = value
    return rebuilt

def getStartEnd(inObjects):
    startEnd = [sys.maxint, -sys.maxint]
    for object in inObjects:
        curKeys = pc.keyframe(object, query=True)
        if curKeys != None and len(curKeys) > 0:
            if curKeys[0] < startEnd[0]:
                startEnd[0] = curKeys[0]
            if curKeys[-1] > startEnd[1]:
                startEnd[1] = curKeys[-1]

    return startEnd

def createInitKey(inObjects):
    for object in inObjects:
        tkc.resetTRS(object)
    pc.setKeyframe(inObjects)

#Debug selection = [pc.PyNode("florawhite_rgf_1_3:FL_char"), pc.PyNode("FL_char")]
HELP_TEXT = "You have to select two assets top nodes, first the rig to merge (rgf), then the destination rig (rgm)"

selection = pc.selected()

if len(selection) != 2:
    pc.error(HELP_TEXT)

assemblies = pc.ls(assemblies=True)

for selectionObj in selection:
    if not selectionObj in assemblies:
        pc.error(HELP_TEXT)

if selection[1].stripNamespace()[2:] != "_char":
    pc.warning("Beware, it seems your destination rig does not respect conventions (topNode = 'SHORTCODE(2 letters)'_Char)")

sourceTopNode = selection[0]
sourceNs = sourceTopNode.namespace()

destinationTopNode = selection[1]
destinationNs = destinationTopNode.namespace()

if sourceNs == destinationNs:
    pc.error("Source and destination rigs have the same namespace, the merge will work only with differnet namespaces")

prefix = selection[1].stripNamespace()[0:3]

#Merging rigs

variables = {"$PREFIX":prefix} 

sourceJointsMapping = {
                    "TK_Spine_0_Deform"             :"$PREFIXSpine3",
                    "TK_Neck_0_Deform"              :"$PREFIXNeck",
                    "TK_Head_Ctrl_Facial_0_Deform"  :"$PREFIXHead"
                }

destJointsMapping = {
                    "$PREFIXJaw":["TK_Jaw_0_Deform","TK_Bottom_Teeth_Main_Deform"],
                    "$PREFIXHead":["TK_Top_Teeth_Main_Deform","TK_Left_Eye_Main_Deform","TK_Right_Eye_Main_Deform"]
                }

reConstraints = {
                    "TK_GlobalSRT_Root"     :"$PREFIXHips",
                    "TK_Head_Ctrl_Root"     :"$PREFIXHead"
                }

sourceJointsMapping = resolveDictionary(sourceJointsMapping, variables)
destJointsMapping = resolveDictionary(destJointsMapping, variables)
reConstraints = resolveDictionary(reConstraints, variables)

#Create initialization frame and set time range
objects = pc.sets(sourceNs + prefix + "ctrls_set", query=True)

startEnd = getStartEnd(objects)

initFrame = startEnd[0]-1

pc.currentTime(startEnd[0])
pc.setKeyframe(objects)
pc.currentTime(initFrame)
createInitKey(objects)

pc.playbackOptions(ast=startEnd[0], min=startEnd[0],aet=startEnd[1], max=startEnd[1])

#Actually fuse rigs
tkRig.fuseRigs(sourceTopNode, destinationTopNode, inSourceJointsMapping=sourceJointsMapping, inDestinationJointsMapping=destJointsMapping, inSourceReConstraints=reConstraints)

#Clean Facial rig

sourceRigNode = pc.PyNode(sourceNs + prefix + "rig")
for child in sourceRigNode.getChildren():
    pc.parent(child, destinationNs + prefix + "rig")

pc.delete(sourceNs + prefix + "char")

pc.connectAttr(sourceNs+"Global_SRT.RigStuff",  sourceNs+"TK_LocalSRT_Root.visibility")
pc.connectAttr(sourceNs+"Global_SRT.RigStuff",  sourceNs+"TK_Spine_Root.visibility")
pc.connectAttr(sourceNs+"Global_SRT.RigStuff",  sourceNs+"TK_Neck_Root.visibility")
pc.connectAttr(sourceNs+"Global_SRT.RigStuff",  sourceNs+"TK_Head_Ctrl_Root.visibility")

#Change/remove namespace
tkc.renameDuplicates()

pc.namespace(setNamespace=":" if sourceNs == "" else sourceNs)
toRename = pc.namespaceInfo(listNamespace=True)
pc.namespace(setNamespace=":" if destinationNs == "" else destinationNs)
for obj in toRename:
    if pc.objExists(obj):
        locked = pc.lockNode(obj, query=True, lock=True)
        if len(locked) > 0 and locked[0]:
            continue
        pc.rename(obj, obj.replace(sourceNs, destinationNs), ignoreShape=True)

if sourceNs != "":
    try:
        pc.namespace(removeNamespace=sourceNs[0:-1], force=True)
    except:
        pass

#Bake facial deformers"

reParents=  {
                "":"$PREFIXHead"
            }

reParents = resolveDictionary(reParents, variables)

tkRig.bake(inGeoNullName=destinationNs+prefix+"geo_grp", inJointsFilters=[destinationNs+"TK_"], inToPreserve=None, inParents=reParents, inJointRadius=0.7, inJointPrefix=prefix, inStart=initFrame, inEnd=startEnd[1])

#Finish cleaning

toDeleteObjs = ["TK_GlobalSRT_Root","rig_OSCAR_Attributes","rig_TK_CtrlsDic","rig_TK_CtrlsChannelsDic","rig_TK_ParamsDic","rig_TK_KeySets","TKRig","mod_Root"]
for toDeleteObj in toDeleteObjs:
    if pc.objExists(destinationNs+toDeleteObj):
        pc.delete(destinationNs+toDeleteObj)

pc.currentTime(startEnd[0])

print ""
print "----------------------------------------------"
pc.warning("Assets merging and baking went OK !")
print "----------------------------------------------"
"""




'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  _     ___  ____  
 | |   / _ \|  _ \ 
 | |  | | | | | | |
 | |__| |_| | |_| |
 |_____\___/|____/ 
                   
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
def getRootName(inNodeName):
    return "TK_{0}_Root".format(inNodeName)

def getNodeName(inRootName):
    return inRootName[3:-5]

ATTRS = ["t{AXIS}", "r{AXIS}", "s{AXIS}", "v"]

VARIABLES = {
    "AXIS":["x", "y", "z"]
}

def lockAttrs(inObj, inLock=True):
    for attr in ATTRS:
        attrs = []
        
        isVar = False
        for variable, values in VARIABLES.iteritems():
            if variable in attr:
                isVar = True
                for value in values:
                    attrs.append(attr.format(**{variable:value}))
        
        if not isVar:
            attrs.append(attr)

        for subAttr in attrs:
            inObj.attr(subAttr).setLocked(inLock)

            if not inLock:
                inObj.attr(subAttr).setKeyable(True)
                #inObj.attr(subAttr).showInChannelBox(True)

def OscarSplitNodes(inNodesToKeep):
    #split nodes to remove/nodes to keep
    nodes = OscarGetNodes()

    allGivenNodes = inNodesToKeep[:]
    nodesRootToKeep = nodes[:]
    nodesRootToRemove = []

    for node in nodes:
        nodeName = getNodeName(node.name())
        if not nodeName in inNodesToKeep:
            nodesRootToRemove.append(node)
            nodesRootToKeep.remove(node)
        else:
            allGivenNodes.remove(nodeName)

    return (nodesRootToRemove, nodesRootToKeep, allGivenNodes)

def simplifyRig(inNodesToKeep, inAddDeformers=None, inReconstrain=None, inReskin=None, inDontReskin=None, inRemoveFollicles=True, inRemoveLattices=True, inRemoveClusters=True, inDeleteTags=None, inDeleteObjs=None, inReconstrainPost=None, inDebugFolder=None):
    debugCounter = 0

    if not inDebugFolder is None:
        if not os.path.isdir(inDebugFolder):
            os.makedirs(inDebugFolder)
        else:
            tkc.emptyDirectory(inDebugFolder)
        print "DEBUG MODE ACTIVATED ({})".format(inDebugFolder)
        tkc.capture(os.path.join(inDebugFolder, "{0:04d}_ORIGINAL.jpg".format(debugCounter)), start=1, end=1, width=1280, height=720)
        debugCounter = debugCounter + 1

    """
    #split nodes to remove/nodes to keep
    nodes = OscarGetNodes()

    allGivenNodes = inNodesToKeep[:]
    nodesRootToKeep = nodes[:]
    nodesRootToRemove = []

    for node in nodes:
        nodeName = getNodeName(node.name())
        if not nodeName in inNodesToKeep:
            nodesRootToRemove.append(node)
            nodesRootToKeep.remove(node)
        else:
            allGivenNodes.remove(nodeName)
    """
    nodesRootToRemove, nodesRootToKeep, allGivenNodes = OscarSplitNodes(inNodesToKeep)

    if len(allGivenNodes) > 0:
        pc.warning("Some given nodes cannot be found in the rig:\n" + "\n".join(allGivenNodes))

    #Add deformers
    #------------------------------------------
    if not inAddDeformers is None:
        visLinker = None
        visLinkers = pc.ls("*.Deformers")
        if len(visLinkers) > 0:
            visLinker = visLinkers[0]

        addedDefs = []

        for low_jnt in inAddDeformers:
            if not pc.objExists(low_jnt):
                pc.warning("Add low deformer skipped, can't find {0} !".format(low_jnt))
            else:
                newDef = tkc.createRigObject(refObject=pc.PyNode(low_jnt), name="$refObject_low_jnt", type="Deformer", mode="child", match=True)
                if not visLinker is None:
                    visLinker >> newDef.v
                addedDefs.append(newDef)

    deformersToReplace = {}
    #Find deformers to replace
    for nodeRoot in nodesRootToRemove:
        deformers = nodeRoot.getChildren(allDescendents=True, type='joint')

        for deformer in deformers:
            deformersToReplace[deformer.name()] = deformer.getTranslation(space="world")

    deformersRemaining = {}
    #Find remaining deformers 
    for nodeRoot in nodesRootToKeep:
        deformers = nodeRoot.getChildren(allDescendents=True, type='joint')

        for deformer in deformers:
            deformersRemaining[deformer.name()] = deformer.getTranslation(space="world")

    #Remove tags
    if not inDeleteTags is None:
        removedObjects = []
        tags = tkTagTool.getTags()
        for tag in inDeleteTags:
            if tag in tags:
                removedObjects.extend(tags[tag])

        removedObjects = list(set(removedObjects))
        if len(removedObjects) > 0:
            print "Remove tagged objects (with tags {0}) : {1}".format(inDeleteTags, removedObjects)
            pc.delete(removedObjects)
            if not inDebugFolder is None:
                tkc.capture(os.path.join(inDebugFolder, "{0:04d}_remove_TaggedObjects.jpg".format(debugCounter)), start=1, end=1, width=1280, height=720)
                debugCounter = debugCounter + 1

    #Remove complex dependencies (geometry constraints/follicles...)
    #---------------------------------------------------------------------------
    #Follicles
    if inRemoveFollicles:
        follicles = [s.getParent() for s in pc.ls(type="follicle")]
        for follicle in follicles:
            follicleParent = follicle.getParent()
            for follicleChild in follicle.getChildren(type="transform"):
                lockAttrs(follicleChild, inLock=False)
                follicleParent.addChild(follicleChild)
        if len(follicles) > 0:
            print "Remove follicles : {0}".format(follicles)
            pc.delete(follicles)
            if not inDebugFolder is None:
                tkc.capture(os.path.join(inDebugFolder, "{0:04d}_remove_Follicles.jpg".format(debugCounter)), start=1, end=1, width=1280, height=720)
                debugCounter = debugCounter + 1

    #Lattices ?
    if inRemoveLattices:
        lattices = [s.getParent() for s in pc.ls(type="lattice")]
        if len(lattices) > 0:
            print "Remove lattices : {0}".format(lattices)
            pc.delete(lattices)
            if not inDebugFolder is None:
                tkc.capture(os.path.join(inDebugFolder, "{0:04d}_remove_Lattices.jpg".format(debugCounter)), start=1, end=1, width=1280, height=720)
                debugCounter = debugCounter + 1

    #Clusters ?
    if inRemoveClusters:
        clusters = pc.ls(type="cluster")
        removedClusters = []
        for cluster in clusters:
            meshHistory = pc.listHistory(cluster, future=True, type="mesh")
            if len(meshHistory) > 0:
                removedClusters.append(cluster)
        if len(removedClusters) > 0:
            print "Remove clusters : {0}".format(removedClusters)
            pc.delete(removedClusters)
            if not inDebugFolder is None:
                tkc.capture(os.path.join(inDebugFolder, "{0:04d}_remove_Clusters.jpg".format(debugCounter)), start=1, end=1, width=1280, height=720)
                debugCounter = debugCounter + 1

    #Reconstrain
    #------------------------------------------
    if not inReconstrain is None:
        for old, new in inReconstrain.iteritems():
            if not pc.objExists(old):
                pc.warning("Forced reparenting : can't find child {0}".format(old))
                continue
            if not pc.objExists(new):
                pc.warning("Forced reparenting : can't find parent {0}".format(new))
                continue
            oldNode = pc.PyNode(old)
            newNode = pc.PyNode(new)

            tkc.removeAllCns(oldNode)
            tkc.constrain(oldNode, newNode)
            tkc.constrain(oldNode, newNode, "Scaling")

            print "Forced reparenting : reparent {0} to {1}".format(old, new)
            if not inDebugFolder is None:
                tkc.capture(os.path.join(inDebugFolder, "{0:04d}_reconstrain_{1}_TO_{2}.jpg".format(debugCounter, old, new)), start=1, end=1, width=1280, height=720)
                debugCounter = debugCounter + 1

    #'Live' blendshape targets
    #------------------------------------
    #If a "live" blendShape is found we will have two cases :
        #The live BS have more kept deformers than the "top level" mesh : transfer target skinning to "top level" mesh     
        #The live BS have less kept deformers than the "top level" mesh : ignore target skinning

    blendShapes = pc.ls(type="blendShape")
    for blendShape in blendShapes:
        if pc.objExists(blendShape):
            meshes = pc.listHistory(blendShape, future=True, type="mesh")
            if len(meshes) > 0:
                mesh = meshes[-1].getParent()
                cons = pc.listConnections(blendShape, source=True, destination=False, type="mesh")
                keptTopInfs = []
                skinTop = tkc.getSkinCluster(mesh)
                if not skinTop is None:
                    keptTopInfs = [inf for inf in skinTop.influenceObjects() if inf.name() in deformersRemaining]
                for con in cons:
                    skin = tkc.getSkinCluster(con)
                    if not skin is None:
                        BSinfs = skin.influenceObjects()
                        #Determine if most of the influences are kept or dropped
                        keptInfs = [inf for inf in BSinfs if inf.name() in deformersRemaining]

                        transfered = False
                        if len(keptInfs) > len(keptTopInfs):
                            transfered = True
                            print "We need to TRANSFER skinning from", con
                            tkc.gator([mesh], con, inCopyMatrices=True, inDirectCopy=True)
                        else:
                            print "We can DROP skinning from", con

                        pc.skinCluster(skin, edit=True, unbind=True)
                        if not inDebugFolder is None:
                            tkc.capture(os.path.join(inDebugFolder, "{0:04d}_liveBS_{1}_{2}.jpg".format(debugCounter, con, "transfered" if transfered else "dropped")), start=1, end=1, width=1280, height=720)
                            debugCounter = debugCounter + 1
                        #TODO ? We may have to do the same with blendShapes...

                    #tkc.freeze(con)
                    #pc.delete(con)

    skinningReplacements = {}
    #Find closest deformers for replacement
    for deformerToReplace, deformerToReplacePos in deformersToReplace.iteritems():

        if not inReskin is None and deformerToReplace in inReskin and pc.objExists(inReskin[deformerToReplace]):
            if pc.objExists(inReskin[deformerToReplace] + "_low_jnt"):
                closestJoint = pc.PyNode(inReskin[deformerToReplace] + "_low_jnt")
            else:
                closestJoint = pc.PyNode(inReskin[deformerToReplace])

            print "Reskin : forced replacement {0} => {1}".format(deformerToReplace, closestJoint)
            if not closestJoint in skinningReplacements:
                skinningReplacements[closestJoint] = [deformerToReplace]
            else:
                skinningReplacements[closestJoint].append(deformerToReplace)
        else:
            closestJoint = None
            closestDist = 1000000

            for deformerRemaining, deformerRemainingPos in deformersRemaining.iteritems():
                if not inDontReskin is None and deformerRemaining in inDontReskin:
                    continue
                dist = (deformerToReplacePos - deformerRemainingPos).length()

                if dist < closestDist:
                    closestJoint = deformerRemaining
                    closestDist = dist

            print "Reskin : proximity replacement {0} => {1}".format(deformerToReplace, closestJoint)
            if not closestJoint in skinningReplacements:
                skinningReplacements[closestJoint] = [deformerToReplace]
            else:
                skinningReplacements[closestJoint].append(deformerToReplace)

    #Actually replace deformers

    #Filter skinClusters that affects meshes
    skins = pc.ls(type="skinCluster")
    meshSkins = [skin for skin in skins if len(skin.getGeometry()) > 0 and skin.getGeometry()[0].type() == "mesh"]

    gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')

    pc.progressBar( gMainProgressBar,
    edit=True,
    beginProgress=True,
    isInterruptable=True,
    status="Replacing deformers",
    maxValue=len(skinningReplacements))

    for newDef, oldDefs in skinningReplacements.iteritems():
        pc.progressBar(gMainProgressBar, edit=True, step=1)
        tkc.replaceDeformers(tkc.getNodes(oldDefs), tkc.getNode(newDef), inSkins=meshSkins)

    pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

    reparentings = {}

    #Figure out reparentings to do
    for nodeRootToRemove in nodesRootToRemove:

        #Get constraints to deleted objects
        cons = tkc.getExternalConstraints(nodeRootToRemove)
        for con in cons:
            owners = tkc.getConstraintOwner(con)
            for owner in owners:
                root = tkc.getParent(owner, root=True)
                #If constraint applies to a kept object
                if root in nodesRootToKeep:
                    for target in tkc.getConstraintTargets(con):
                        #print "target.name()",target.name(),"reparented",reparented

                        targetRoot = tkc.getParent(target, root=True)

                        if targetRoot in nodesRootToKeep or target in reparentings:
                            continue

                        #print "! Reparent", target, "owner", owner, "cons",con
                        #Find the best candidate for reparenting
                        parents = tkc.getAllParents(target)
                        for parent in parents:
                            parentRoot = tkc.getParent(parent, root=True)
                            if parentRoot in nodesRootToKeep:
                                reparentings[target] = parent
                                break

    #Actually reparent
    for target, newParent in reparentings.iteritems():
        print "Automatic reparenting : reparent {0} to {1}".format(target, newParent)

        lockAttrs(target, False)

        #Create a copy
        targetName = target.name()
        target.rename(targetName + "_TKLOW")
        lowObj = pc.group(empty=True, name=targetName, world=True)
        tkc.matchTRS(lowObj, target)
        target.getParent().addChild(lowObj)
        for child in target.getChildren(type="transform"):
            lowObj.addChild(child)

        lockAttrs(lowObj, True)

        #Actually reparent
        newParent.addChild(target)
        if target in nodesRootToRemove:
            nodesRootToRemove.remove(target)
            nodesRootToRemove.append(lowObj)

        shapes = target.getShapes()
        if len(shapes) > 0:
            pc.delete(shapes)

        if not inDebugFolder is None:
            tkc.capture(os.path.join(inDebugFolder, "{0:04d}_autoReparent_{1}_TO_{2}.jpg".format(debugCounter, targetName, newParent)), start=1, end=1, width=1280, height=720)
            debugCounter = debugCounter + 1

    #Actually delete unwanted nodes
    if not inDebugFolder is None:
        for nodeRootToRemove in nodesRootToRemove:
            pc.delete(nodeRootToRemove)

            tkc.capture(os.path.join(inDebugFolder, "{0:04d}_deleteNode_{1}.jpg".format(debugCounter, nodeRootToRemove)), start=1, end=1, width=1280, height=720)
            debugCounter = debugCounter + 1
    else:
        pc.delete(nodesRootToRemove)

    if not inDeleteObjs is None:
        for toDelete in inDeleteObjs:
            if pc.objExists(toDelete):
                pc.delete(toDelete)
                if not inDebugFolder is None:
                    tkc.capture(os.path.join(inDebugFolder, "{0:04d}_deleteObj_{1}.jpg".format(debugCounter, toDelete)), start=1, end=1, width=1280, height=720)
                    debugCounter = debugCounter + 1
            else:
                print "Object {} to delete by name was not found".format(toDelete)

    tkc.deleteUnusedNodes()

    #ReconstrainPost
    #------------------------------------------
    if not inReconstrainPost is None:
        for old, new in inReconstrainPost.iteritems():
            oldNodes = pc.ls([old, old+"_TKLOW"])
            if len(oldNodes) == 0:
                pc.warning("Post reparenting : can't find child {0}".format(old))
                continue
            newNodes = pc.ls([new, new+"_TKLOW"])
            if len(newNodes) == 0:
                pc.warning("Post reparenting : can't find parent {0}".format(new))
                continue

            oldNode = oldNodes[0]
            newNode = newNodes[0]

            tkc.constrain(oldNode, newNode)
            tkc.constrain(oldNode, newNode, "Scaling")

            print "Post reparenting : reparent {0} to {1}".format(old, new)
            if not inDebugFolder is None:
                tkc.capture(os.path.join(inDebugFolder, "{0:04d}_postReparent_{1}_TO_{2}.jpg".format(debugCounter, old, new)), start=1, end=1, width=1280, height=720)
                debugCounter = debugCounter + 1



def cutSkinnedMeshes ( inObjList, inDeleteMesh = False, inFillHole = False, inNamePolyCombine = 'low_poly', inToJointParent=False, inDeleteJoints=False, inCombine=True):
    """Cut and combine the skinned meshes selected

        Input arguments:
        inObjList -- list of selected meshes
        inDeleteMesh -- delete the original meshes (default False)
        inFillHole -- close borders of creates meshes (default False)
        inNamePolyCombine -- name of the new combine meshes (default 'low_poly')
        inToJointParent -- new mesh parent of joint if True, child if false (default True) 
        inDeleteJoints -- delete the joints (default True)

        Return values:
        newObjList -- dictionary list of new objects by joint

    """
    if inToJointParent == False:
        inDeleteJoints == False

    kk=0
    #Dictionary List of ojects by influence (joint)
    copyObject = {}
    newObjList = {}

    #For each object selected
    for kk in range(len(inObjList)):
        
        #---INITIALIZATION---
        #Get skin cluster
        skin = tkc.getSkinCluster(inObjList[kk])        
        #Get number of vertices
        nVerts = pc.polyEvaluate(inObjList[kk], vertex=True)
        nFace = pc.polyEvaluate(inObjList[kk], face=True)

        #Get influences list
        inf = pc.skinCluster(skin,query=True,inf=True)      
        #Get skinCluster weights
        w = tkc.getWeights(inObjList[kk]) 
        #Dictionary list of {influence,weight_mean} by face
        d1 = {u: 1.0 for u in range(nFace)}
        #Dictionary list of {face,weight_mean} by influence
        d2 = {v: [] for v in inf}     
        i=0
        k=0
        moyenne = {k: 0.0 for k in inf}
        numberOfVerticeByFace = []        
        dicOfVerticeByFace = {k: [] for k in range(nFace)}        
        #Recover the dictionnary of vertices by faces
        for i in range(nFace):
            #dicOfVerticeByFace[i]= inObjList[kk].faces[i].getVertices()
            dicOfVerticeByFace[i]= inObjList[kk].getPolygonVertices(i)
            numberOfVerticeByFace.append(len(dicOfVerticeByFace[i]))  
        

        #FIND for each face the corresponding influence
        #For each polygon                        
        i=0
        while i < nFace :
            k=0
            #For each influence
            for k in range(len(inf)):
                #Compute arithmetic mean
                sum=0
                j=0
                #Compute the mean for all the vertex of the face
                while j < numberOfVerticeByFace[i] :
                    sum=sum+w[dicOfVerticeByFace[i][j]+nVerts*k]  
                    j+=1
                moyenne[inf[k]]=sum/numberOfVerticeByFace[i]
               
            m_max=max(moyenne.iteritems(), key=operator.itemgetter(1))[0]
            if m_max in d2.keys():
                d2[m_max].append([i, moyenne[m_max]])
            
            d1[i]={m_max:moyenne[m_max]}
            i+=1

        list = []
        for key, value in  d2.iteritems():
            #Duplicate object by influence
            nom1="{0}_{1}".format(key,inObjList[kk])
            duplicata=  pc.duplicate(inObjList[kk], name=nom1)
         
            cleanMesh(duplicata[0].name())

            #Create a dictionnary of objects by influence
            if key in copyObject.keys():
                copyObject[key].append(duplicata[0])
            else:
                copyObject[key]=[duplicata[0]]
            
            list = []          
            #Delete the unused faces
            for key2, value2 in d2.iteritems():
                if key != key2:
                    #list = []
                    for k in value2:
                        list.append("{0}.f[{1}]".format(duplicata[0], k[0]))                        
            pc.delete(list)
    
            #Unlock the Transforms
            attrs = ["tx","ty", "tz", "rx","ry","rz","sx","sy","sz"]
            for attr in attrs:
               duplicata[0].attr(attr).setLocked(False) 
            parentJoint = key.getParent(1)             
            if inToJointParent == False:
                pc.parent(duplicata[0], key, add=False)
            else:
                if parentJoint != None:               
                    pc.parent(duplicata[0], parentJoint, add=False)
                else:
                    pc.warning("Be careful, no parent defined !")
                    pc.parent(duplicata[0], key, add=False)

            #Fill the mesh if necessary
            if inFillHole == True:
                pc.polyCloseBorder(duplicata[0], ch=False)
             
        #Delete the original mesh if necessary  
        if inDeleteMesh ==  True:
            pc.delete(inObjList[kk])
                

    newObjList = copyObject.copy()
    if inCombine:
        #Combine objects with same influence (joint)    
        for key3, value3 in copyObject.iteritems():
            parentJoint = key3.getParent(1)
            if len(value3) > 1: #Check if object > 1
                del newObjList[key3]
                nom2="{0}_{1}".format(key3,inNamePolyCombine)
                combinedPoly = pc.polyUnite(value3, ch=False, mergeUVSets=True, centerPivot=True, name=nom2)[0]
                newObjList[key3]=[combinedPoly]
                if inToJointParent == False:
                    pc.parent(combinedPoly,key3, add=False)
                else:
                    if parentJoint != None:  
                        pc.parent(combinedPoly,parentJoint, add=False)
                    else:
                        pc.warning("Be careful, no parent defined !")
                        pc.parent(combinedPoly,key3, add=False)
            else:  
                continue
            
            if inDeleteJoints == True and parentJoint != None:
                pc.delete(key3)
            else:
                continue


    return newObjList


def jointsFromCurve(inCurve, inNbJoints=4, inSplineIK=False, inScl=False, inSquash=False, inClusters=False, inPrefix=None):
    
    crvShape = inCurve
    if inCurve.type() =="transform":
        crvShape = inCurve.getShape()

    namePrefix = inPrefix or crvShape.name() + "_"

    createdAssemblies = []

    #cvs = crvShape.getCVs()
    spans = pc.getAttr(crvShape.name() + ".spans")
    
    #create the joints
    joints = []
    jointSize = 0.5 * crvShape.length() / inNbJoints
    perc = crvShape.length() / float(inNbJoints)
    
    oldJoint = None

    rigRoot = pc.group(empty=True, name=namePrefix + "splineRig")
    
    pc.select(rigRoot, replace=True)

    for i in range(inNbJoints):
        param = crvShape.findParamFromLength(perc * i)
        curJoint = pc.joint(p=crvShape.getPointAtParam(param), name=namePrefix+"bone_%02i" % i, radius=jointSize)
        if oldJoint != None:
            pc.joint(oldJoint, edit=True, oj="xyz", sao="yup")
        oldJoint = curJoint
        joints.append(curJoint)
        
    #Effector
    param = crvShape.findParamFromLength(perc * inNbJoints)
    curJoint = pc.joint(p=crvShape.getPointAtParam(param), name=namePrefix+"bone_eff", radius=jointSize)
    if oldJoint != None:
        pc.joint(oldJoint, edit=True, oj="xyz", sao="yup")
            
    joints.append(curJoint)

    createdAssemblies.append(joints[0])
    
    if inClusters:
        clusters = clusterize(inCurve)
        pc.parent(clusters, rigRoot)
    
    if inSplineIK:
        ikComponents = pc.ikHandle(sol="ikSplineSolver", ccv=False, pcv=False, c=crvShape, sj=joints[0], ee=joints[-1], name=namePrefix+"SplineIK")
        ikComponents[1].rename(namePrefix+ikComponents[1].name())
        createdAssemblies.append(ikComponents[0])
        pc.parent(ikComponents[0], rigRoot)

        if inScl:
            crvInfo = None
            crvInfoName = namePrefix + "CrvInfo"
            if pc.objExists(crvInfoName):
                crvInfo = pc.PyNode(crvInfoName)
            else:
                crvInfo = pc.shadingNode("curveInfo", asUtility=True, n=crvInfoName);
                pc.connectAttr(crvShape.name() + ".worldSpace[0]", crvInfo.name() + ".inputCurve")
                
            length = pc.getAttr(crvInfo.name() + ".arcLength")
            #restlength stores the default curve length
            if not pc.attributeQuery("restLength", node=crvInfo, exists=True):
                pc.addAttr(crvInfo, sn="restLength")
            pc.setAttr(crvInfo.name() + ".restLength", length)

            #stretch attr indicates if we scale with the curve or not
            if not pc.attributeQuery("stretch", node=crvInfo, exists=True):
                pc.addAttr(crvInfo, sn="stretch", dv=1.0)
            pc.setAttr(crvInfo.name() + ".restLength", length)

            #factoir returns the current length in regard to rest length
            if not pc.attributeQuery("factor", node=crvInfo, exists=True):
                pc.addAttr(crvInfo, sn="factor")
                mulDiv = pc.shadingNode("multiplyDivide", asUtility=True, name=crvInfoName + "_MulDiv")
                pc.setAttr(mulDiv.name() + ".operation" , 2)
                pc.connectAttr(crvInfo.name() + ".arcLength", mulDiv.name() + ".input1X")
                pc.connectAttr(crvInfo.name() + ".restLength", mulDiv.name() + ".input2X")
                pc.connectAttr(mulDiv.name() + ".outputX", crvInfo.name() + ".factor")
            
            #scale attr outputs final scaling
            if not pc.attributeQuery("scale", node=crvInfo, exists=True):
                pc.addAttr(crvInfo, sn="scale")
                globScaleMul = pc.shadingNode("multDoubleLinear", asUtility=True, name=crvInfoName + "_GlobalScale_Mul")
                crvInfo.stretch >> globScaleMul.input1
                crvInfo.factor >> globScaleMul.input2

                globScaleReverse = pc.shadingNode("reverse", asUtility=True, name=crvInfoName + "_GlobalScale_Reverse")
                crvInfo.stretch >> globScaleReverse.inputX

                globScaleAdd = pc.shadingNode("addDoubleLinear", asUtility=True, name=crvInfoName + "_GlobalScale_Add")
                globScaleMul.output >> globScaleAdd.input1
                globScaleReverse.outputX >> globScaleAdd.input2

                globScaleAdd.output >> crvInfo.scale

            for curJoint in joints[1:]:
                sclMul = pc.shadingNode("multDoubleLinear", asUtility=True, name=curJoint.name() + "_Scale_Mul")
                sclMul.input2.set(curJoint.tx.get())
                crvInfo.scale >> sclMul.input1

                sclMul.output >> curJoint.tx
                    
            if inSquash:
                if len(joints) - 2 <= 0:
                    pc.warning("Too few joints to create squash rig, more than 2 expected !")
                    return joints

                clampScale = pc.shadingNode("clamp", asUtility=True, name=namePrefix +"Scale_Clamp")
                crvInfo.scale >> clampScale.inputR
                pc.setAttr(clampScale.name() + ".minR", 0.001)
                pc.setAttr(clampScale.name() + ".maxR", 1000)
                
                invertScale = pc.shadingNode("multiplyDivide", asUtility=True, name=namePrefix +"Scale_Invert")
                pc.setAttr(invertScale.name() + ".operation", 2)
                pc.setAttr(invertScale.name() + ".input1X", 1)
                pc.connectAttr(clampScale.name() + ".outputR", invertScale.name() + ".input2X")
                
                if not pc.attributeQuery("bulge_factor", node=crvInfo, exists=True):
                    pc.addAttr(crvInfo, sn="bulge_factor", dv=1.0)

                for i in range(len(joints)):
                    perc = i / (len(joints) - 1.0)

                    if perc > 0.0 and perc < 1.0:
                        sclMul = pc.shadingNode("multDoubleLinear", asUtility=True, name=joints[i].name() + "_Squash_Mul")
                        crvInfo.bulge_factor >> sclMul.input1
                        sclMul.input2.set(-math.pow((perc - 0.5) * 2,2)+1)

                        sclPow = pc.shadingNode("multiplyDivide", asUtility=True, name=joints[i].name() + "_Squash_Pow")
                        sclPow.operation.set(3)#Power
                        invertScale.outputX >> sclPow.input1X
                        sclMul.output >> sclPow.input2X

                        sclPow.outputX >> joints[i].sy
                        sclPow.outputX >> joints[i].sz
    return joints

"""
import motionPathRig as mp
reload(mp)

inCurve = None

sel = pc.selected()

if len(sel) > 0:
    inCurve = sel[0]

mp.motionPathRig(inCurve, inNb=10, inLength=10)
"""
def motionPathRig(inCurve, inNb=10, inLength=10, inName="motionPathRig"):
    """
    print "inCurve",inCurve
    print "inNb", inNb
    print "inLength",inLength
    """
    #Create the poleVector curve
    upVCurve = pc.duplicate(inCurve, name=inCurve.name() + "_UPV")[0]
    upVCurve.ty.set(2.0)
    tkc.freezeTransform(upVCurve)

    #upVCurveRebuilt = pc.rebuildCurve(upVCurve, ch=True, rpo=0, rt=0, end=1, kr=0, kcp=0, kep=1, kt=0, s=300, d=2, tol=0.01)[0]

    #Create the base spline rig (arbitrarily towards +Z)
    clusters = clusterize(inCurve)
    upVClusters = clusterize(upVCurve)

    container = pc.group(empty=True, world=True, name=inCurve.name() + "_Root")

    i = 0
    for cluster in clusters:
        ctrl = tkc.createRigObject(refObject=container, name=inCurve.name() + "_Ctrl1", type="Null", mode="child", match=False)

        ctrl.tx.set(cluster.rotatePivotX.get())
        ctrl.ty.set(cluster.rotatePivotY.get())
        ctrl.tz.set(cluster.rotatePivotZ.get())

        ctrl.ry.set(-90)

        ctrl.addChild(cluster)
        ctrl.addChild(upVClusters[i])

        i += 1

    #Create main control and attributes
    mainCtrl = tkc.createRigObject(refObject=None, name="Main_Ctrl", type="Null", mode="child", match=False)

    tkc.addParameter(inobject=mainCtrl, name="Follow", inType="int", default=0, min=0, max=1, softmin=0, softmax=1, nicename="", expose=True, containerName="", readOnly=False, booleanType=0, skipIfExists=True, keyable=True)
    tkc.addParameter(inobject=mainCtrl, name="Locomotion", inType="double", default=0, min=-1000000, max=1000000, softmin=-100, softmax=100, nicename="", expose=True, containerName="", readOnly=False, booleanType=0, skipIfExists=True, keyable=True)
    tkc.addParameter(inobject=mainCtrl, name="FromEnd", inType="int", default=0, min=0, max=1, softmin=0, softmax=1, nicename="", expose=True, containerName="", readOnly=False, booleanType=0, skipIfExists=True, keyable=True)
    tkc.addParameter(inobject=mainCtrl, name="Scale", inType="double", default=1.0, min=0.001, max=1000, softmin=.1, softmax=10, nicename="", expose=True, containerName="", readOnly=False, booleanType=0, skipIfExists=True, keyable=True)
    
    tkc.addParameter(inobject=mainCtrl, name="U", inType="double", default=0, min=None, max=None, softmin=None, softmax=None, nicename="", expose=True, containerName="", readOnly=False, booleanType=0, skipIfExists=True, keyable=True)
    tkc.addParameter(inobject=mainCtrl, name="Length", inType="double", default=inLength, min=None, max=None, softmin=None, softmax=None, nicename="", expose=True, containerName="", readOnly=False, booleanType=0, skipIfExists=True, keyable=True)
    tkc.addParameter(inobject=mainCtrl, name="Number", inType="int", default=inNb, min=None, max=None, softmin=None, softmax=None, nicename="", expose=True, containerName="", readOnly=False, booleanType=0, skipIfExists=True, keyable=True)
    
    mainCtrl.ty.set(5)

    #Extract curve Info and calculate U in "Follow" or "Locomotion" modes
    curveShape = inCurve.getShape()
    upVCurveShape = upVCurve.getShape()

    curveInfo = pc.createNode("curveInfo", name=inCurve.name() + "_info")
    curveShape.worldSpace[0] >> curveInfo.inputCurve

    #Prepare 'from end' condition
    fromEndCond = pc.createNode("condition", name=inCurve.name() + "_fromEnd_cond")
    fromEndCond.secondTerm.set(1)
    mainCtrl.FromEnd >> fromEndCond.firstTerm

    fromEnd_minus = pc.createNode("plusMinusAverage", name=inCurve.name() + "_fromEnd_minus")
    fromEnd_minus.operation.set(2)#substract
    curveInfo.arcLength >> fromEnd_minus.input1D[0]
    mainCtrl.Locomotion >> fromEnd_minus.input1D[1]

    fromEnd_minus.output1D >> fromEndCond.colorIfTrueR
    mainCtrl.Locomotion >> fromEndCond.colorIfFalseR

    scaleMul = pc.createNode("multDoubleLinear", name=mainCtrl.name() + "_scale_mul")
    mainCtrl.Scale >> scaleMul.input1
    fromEndCond.outColorR >> scaleMul.input2

    lengthDivide = pc.createNode("multiplyDivide", name=mainCtrl.name() + "_length_divide")
    lengthDivide.operation.set(2)
    scaleMul.output >> lengthDivide.input1X
    curveInfo.arcLength >> lengthDivide.input2X

    lengthDivide.outputX >> mainCtrl.U

    #sectionLength
    mainCtrl.Length >> lengthDivide.input1Y
    mainCtrl.Number >> lengthDivide.input2Y
    
    sectionDivide = pc.createNode("multiplyDivide", name=mainCtrl.name() + "_section_divide")
    sectionDivide.operation.set(2)
    lengthDivide.outputY >> sectionDivide.input1X
    curveInfo.arcLength >> sectionDivide.input2X

    #Create motion rig
    for i in range(inNb):

        up = pc.spaceLocator(name="{0}_Up_{1:02d}".format(inName, i))

        upCns = tkc.pathConstrain(up, upVCurve, tangent=True, parametric=False, addPercent=False)

        loc = pc.spaceLocator(name="{0}_Loc_{1:02d}".format(inName, i))

        locCns = tkc.pathConstrain(loc, inCurve, tangent=True, parametric=False, addPercent=False)
        locCns.frontAxis.set(0)#X
        locCns.upAxis.set(1)#Y

        locCns.worldUpType.set(1)#Object Up
        up.worldMatrix[0] >> locCns.worldUpMatrix

        #U value
        if i > 0:
            sectionMul = pc.createNode("multDoubleLinear", name=loc.name() + "_section_mul")
            sectionDivide.outputX >> sectionMul.input1
            sectionMul.input2.set(i)

            sectionAdd = pc.createNode("addDoubleLinear", name=loc.name() + "_section_add")
            mainCtrl.U >> sectionAdd.input1
            sectionMul.output >> sectionAdd.input2

            sectionAdd.output >> upCns.uValue
            sectionAdd.output >> locCns.uValue
        else:
            mainCtrl.U >> upCns.uValue
            mainCtrl.U >> locCns.uValue

"""
import SuperIK
reload(SuperIK)
SuperIK.createSuperIK(pc.selected()[0], pc.selected()[1], pc.selected()[2], pc.selected()[3])
"""

def createSuperIK(inCtrl, *args):
    if len(args) == 3:
        createSuperIKLink(inCtrl, args[0], inValue=1.0)
        createSuperIKLink(inCtrl, args[1], inValue=.75)
        createSuperIKLink(inCtrl, args[2], inValue=.25)
    elif len(args) == 4:
        createSuperIKLink(inCtrl, args[0], inValue=1.0)
        createSuperIKLink(inCtrl, args[1], inValue=.8)
        createSuperIKLink(inCtrl, args[2], inValue=.5)
        createSuperIKLink(inCtrl, args[3], inValue=.2)

def createSuperIKLink(inSuperIK, inCtrl, inValue=1.0, invertX=False, invertZ=False):
    neutral = inCtrl.getParent()
    root = inCtrl.getParent().getParent()

    orienterName = "{0}_{1}_Orienter".format(inSuperIK.name(), inCtrl.stripNamespace())

    if pc.objExists(orienterName):
        return

    orienter = pc.group(empty=True, world=True, name=orienterName)
    root.addChild(orienter)
    orienter.t.set([0,0,0])
    orienter.r.set([0,0,0])
    tkc.constrain(orienter, inSuperIK.getParent(), "Orientation")

    linkLocal = pc.group(empty=True, world=True, name="{0}_{1}_LinkLocal".format(inSuperIK.name(), inCtrl.stripNamespace()))
    orienter.addChild(linkLocal)
    inSuperIK.t >> linkLocal.t

    sensor = pc.group(empty=True, world=True, name="{0}_{1}_Sensor".format(inSuperIK.name(), inCtrl.stripNamespace()))
    root.addChild(sensor)
    sensor.t.set([0,0,0])
    tkc.constrain(sensor, linkLocal)

    output = sensor.t

    if inValue != 1.0:
        attenuate = pc.createNode("multiplyDivide", name="{0}_{1}_Attenuate".format(inSuperIK.name(), inCtrl.stripNamespace()))
        sensor.t >> attenuate.input1

        attenuate.input2X.set(inValue)
        attenuate.input2Y.set(inValue)
        attenuate.input2Z.set(inValue)

        output = attenuate.output

    neutralCons = pc.listConnections(neutral.t, source=True, destination=False)

    neutralMul = pc.createNode("multiplyDivide",  name="{0}_{1}_Active".format(inSuperIK.name(), inCtrl.stripNamespace()))

    neutralMul.output >> neutral.t

    neutralInput = neutralMul.input1

    if len(neutralCons) == 1:
        add = pc.createNode("plusMinusAverage", name="{0}_{1}_Add".format(inSuperIK.name(), inCtrl.stripNamespace()))
        neutralCons[0].output >> add.input3D[0]
        output >> add.input3D[1]

        add.output3D >> neutralInput
    else:
        neutralConsX = pc.listConnections(neutral.tx, source=True, destination=False)
        neutralConsY = pc.listConnections(neutral.ty, source=True, destination=False)
        neutralConsZ = pc.listConnections(neutral.tz, source=True, destination=False)

        if len(neutralConsX) == 1 or len(neutralConsY) == 1 or len(neutralConsZ) == 1:
            add = pc.createNode("plusMinusAverage", name="{0}_{1}_Add".format(inSuperIK.name(), inCtrl.stripNamespace()))

            if len(neutralConsX) == 1:
                neutralConsX[0].output >> add.input3D[0].input3Dx
                neutral.tx.disconnect()

            if len(neutralConsY) == 1:
                neutralConsY[0].output >> add.input3D[0].input3Dy
                neutral.ty.disconnect()

            if len(neutralConsZ) == 1:
                neutralConsZ[0].output >> add.input3D[0].input3Dz
                neutral.tz.disconnect()

            output >> add.input3D[1]

            add.output3D >> neutralInput
        else:
            output >> neutralInput

def applyDeltas(inDeltaPattern="{name}_delta.ma", inPattern="{type:[a-z]{2}}_{name}-{variation}_hig_v{version:[0-9]{3}}{suffix}.ma", inPath=None):
    filePath = inPath

    deltaPath = inDeltaPattern

    if not os.path.isfile(deltaPath):
        pc.warning("Can't find a delta scene '{0}' !".format(deltaPath))
        return False

    if inPath is None:
        #Save scene in a temporary file
        tmpFile = tempfile.NamedTemporaryFile(prefix='applyDeltas',suffix='.ma', delete=False)
        tmpFile.close()
        filePath = tmpFile.name
        pc.system.saveAs(filePath, force=True)

    #Open delta file
    pc.openFile(deltaPath, force=True, prompt=False, loadReferenceDepth='none')

    #load the good reference
    ref = None
    
    refs = pc.system.listReferences()
    if len(refs) > 0:
        ref = refs[0]
    else:
        pc.warning("Can't find a reference in the delta scene '{0}' !".format(deltaPath))
        return False
    
    ref.load(newFile=baseModPath)

    #import reference

    #Reset All ?

    #Mesh overrides to True

    #Deformer visibilities to False

    #LOD to high all ?

    #Delete orphans

    #Remove namespace

    #Delete temporary file
    if inPath is None:
        os.remove(tmpFileName)

    """
    if inPath is None:
        inPath = pc.system.sceneName()
    else:
        pass

    if inPath is None or "untitled" in inPath:
        pc.warning("No valid path given !")
        return

    folderPath, fileName = os.path.split(inPath) 

    print folderPath, fileName
    """
    
    return True


#Frequency = 0.075
#Length = 0.5

"""
import SnakeWaveLoc as sw
reload(sw)

import tkMayaCore as tkc
reload(tkc)

bottoms = [n for n in pc.ls("Bottom_*", type="transform") if not "NeutralPose" in n.name()]
ups = [n for n in pc.ls("Loc_*", type="transform") if not "NeutralPose" in n.name()]

actives = [n.active for n in ups]

crushPose = [ {'attr': u'ty', 'source': 'Loc_0', 'value': -0.5},
         {'attr': u'ty', 'source': 'Bottom_0', 'value': 0.5},
         {'attr': u'sx', 'source': 'Bottom_0', 'value': 1.5}]

crushPoses = []

for i in range(len(bottoms)):
    newPose = []
    for poseItem in crushPose:
        newPoseItem = poseItem.copy()
        newPoseItem["source"] = newPoseItem["source"].replace("Loc_0", ups[i].name()).replace("Bottom_0", bottoms[i].name())
        newPose.append(newPoseItem)
    
    crushPoses.append(newPose)

sw.createSnakeWaveLoc(bottoms, pc.PyNode("Global_SRT.WaveFrequency"), pc.PyNode("Global_SRT.WaveLength"),
    pc.PyNode("Global_SRT.Locomotion"), pc.PyNode("Global_SRT.WaveActive"), actives, crushPoses, pc.PyNode("Global_SRT.WaveUp"), pc.PyNode("Global_SRT.CrushOnGround"))
"""

def createSnakeWaveLoc(inObjects, inFrequencyAttr, inLengthAttr, inLocomotionAttr, inActiveAttr, inActiveAttrs=None, inCrushPoses=None, inUpAttr=None, inCrushAttr=None, inBaseOffset=10, inDestattr="tx", inCurvePath=os.path.join(os.path.dirname(__file__),"WaveCycle.ma"), inCurveUpPath=os.path.join(os.path.dirname(__file__),"UpCycle.ma"), inBaseName="SnakeWave"):
    baseOffset = 10000
    counter = 1

    frequencyAttr = pc.PyNode(inFrequencyAttr)
    lengthAttr = pc.PyNode(inLengthAttr)
    locomotionAttr = pc.PyNode(inLocomotionAttr)

    for obj in inObjects:
        offsetmul = pc.createNode("multDoubleLinear", name="{0}_OffsetMul_{1}".format(inBaseName, counter))
        lengthAttr >> offsetmul.input1
        offsetmul.input2.set(baseOffset)

        offsetadd = pc.createNode("addDoubleLinear", name="{0}_OffsetAdd_{1}".format(inBaseName, counter))
        locomotionAttr >> offsetadd.input1
        offsetmul.output >> offsetadd.input2

        freqmul = pc.createNode("multDoubleLinear", name="{0}_FreqMul_{1}".format(inBaseName, counter))
        offsetadd.output >> freqmul.input1
        frequencyAttr >> freqmul.input2

        animCurve = pc.system.importFile(inCurvePath, returnNewNodes=True)[0]
        animCurve.rename("{0}_animCurve_{1}".format(inBaseName, counter))
        freqmul.output >> animCurve.input

        upCurve = pc.system.importFile(inCurveUpPath, returnNewNodes=True)[0]
        upCurve.rename("{0}_upCurve_{1}".format(inBaseName, counter))
        freqmul.output >> upCurve.input

        finalmul = pc.createNode("multDoubleLinear", name="{0}_FinalMul_{1}".format(inBaseName, counter))
        animCurve.output >> finalmul.input1

        exprString = "{0} = ((({1} -(1/{2}))*1000000) % (3000000*(1/{2}))/1000000)".format(finalmul.input2.name(), offsetadd.output.name(), frequencyAttr.name())
        expr = pc.expression( s=exprString , name="{0}_Expr_{1}".format(inBaseName, counter))
        
        activeMul = pc.createNode("multDoubleLinear", name="{0}_GlobalActiveMul_{1}".format(inBaseName, counter))
        finalmul.output >> activeMul.input1
        inActiveAttr >> activeMul.input2

        output = activeMul.output
        crushAttr = inCrushAttr
        
        globalActiveUp = pc.createNode("multDoubleLinear", name="{0}_GlobalActiveUp_{1}".format(inBaseName, counter))
        upCurve.output >> globalActiveUp.input1
        inActiveAttr >> globalActiveUp.input2

        upAttr = globalActiveUp.output

        if not inActiveAttrs is None:
            activeAttr = inActiveAttrs[counter-1]
            activeNode = pc.createNode("multDoubleLinear", name="{0}_ActiveMul_{1}".format(inBaseName, counter))
            activeMul.output >> activeNode.input1
            activeAttr >> activeNode.input2

            output = activeNode.output

            crushActiveNode = pc.createNode("multDoubleLinear", name="{0}_CrushActiveMul_{1}".format(inBaseName, counter))
            crushAttr >> crushActiveNode.input1
            activeAttr >> crushActiveNode.input2

            crushAttr = crushActiveNode.output

        if not inUpAttr is None:
            upMul = pc.createNode("multDoubleLinear", name="{0}_UpMul_{1}".format(inBaseName, counter))
            inUpAttr >> upMul.input1
            upAttr >> upMul.input2
            upAttr = upMul.output

        reverseUp = pc.createNode("reverse", name="{0}_ReverseUp_{1}".format(inBaseName, counter))
        upAttr >> reverseUp.inputX
        upAttr = reverseUp.outputX

        crushMul = pc.createNode("multDoubleLinear", name="{0}_CrushMul_{1}".format(inBaseName, counter))
        crushAttr >> crushMul.input1
        upAttr >> crushMul.input2

        if not inCrushPoses is None:
            crushPose = inCrushPoses[counter-1]
            if isinstance(crushPose, (list,tuple)):#pose
                tkc.loadPoses(inCrushPoses[counter-1], inActivationAttr=crushMul.output)
            else:#attr
                crushMul.output >> crushPose

        thisInput = None

        if obj.type() == "transform":
            layerName = obj.name() + "_poseLayer"
            layerNode = obj.getParent()
            if not layerNode.name() == layerName:
                layerObj = pc.group(empty=True, name=layerName)
                layerNode.addChild(layerObj)
                layerObj.t.set([0,0,0])
                layerObj.r.set([0,0,0])
                layerObj.s.set([1,1,1])
                layerNode = layerObj
                layerNode.addChild(obj)

                thisInput = layerNode.attr(inDestattr)
        else:
            thisInput = obj

        output >> thisInput

        baseOffset += inBaseOffset
        counter += 1

def importRig(path, newName="", newRootName=""):
    pc.undoInfo(openChunk=True)
    objects = tkc.importFile(path, newName)

    #Include imported rig in provided rig
    if objects != None and newRootName != "":
        if pc.objExists(newRootName):
            newRoot = pc.PyNode(newRootName)
            rigName = tkc.getRigName(newRootName)

            #Move objects under an "ExtraRigs" root
            if len(objects[0]) > 0:
                extraRigsName = rigName + tkc.CONST_EXTRARIGSSUFFIX
                extraRigs = None

                if not pc.objExists(extraRigsName):
                    extraRigs = tkc.createRigObject(newRoot, extraRigsName)
                else:
                    extraRigs = pc.PyNode(extraRigsName)
                for obj in objects[0]:
                    pc.parent(obj, extraRigs)

                #Merge groups
                if len(objects[1]) > 0:
                    #Find the new rig Name
                    newRigName = ""
                    for obj in objects[0]:
                        if obj.name()[-len(tkc.CONST_ROOTSUFFIX):] == tkc.CONST_ROOTSUFFIX:
                            newRigName = obj.name()[:-len(tkc.CONST_ROOTSUFFIX)]
                    if newRigName != "":
                        tkSIGroups.merge(newRigName, rigName)
                    else:
                        pc.warning("Can't find rig Root from imported objects (%s), no groups merged !" % str(objects[0]))
        else:
            pc.warning("Can't find specified Root (%s)" % newRootName)
    pc.undoInfo(closeChunk=True)
    return objects

def plotRig(deleteTheRest=True):
    pc.undoInfo(openChunk=True)
    rigRoot = None
    root = None
    
    sel = pc.ls(sl=True)
    for selObj in sel:
        root = tkc.getParent(selObj, model=True)
        if root != None:
            rigRoot = root
            break

    if rigRoot == None:
        pc.warning("No rig selected !")
        pc.undoInfo(closeChunk=True)
        return root

    charName = rigRoot.stripNamespace()
    ns = rigRoot.namespace()
    
    #Geos
    geos = getGeometries(ns)
    
    #Deformers
    defs = tkc.getDeformers(geos)

    # - Create fbx rig
    #Create fbx root
    
    root = tkc.createRigObject(name=charName + "_FBX")
    
    #Reparent geometries
    for geo in geos:
        pc.setAttr(geo + ".tx", keyable=True, lock=False)
        pc.setAttr(geo + ".ty", keyable=True, lock=False)
        pc.setAttr(geo + ".tz", keyable=True, lock=False)
        pc.setAttr(geo + ".rx", keyable=True, lock=False)
        pc.setAttr(geo + ".ry", keyable=True, lock=False)
        pc.setAttr(geo + ".rz", keyable=True, lock=False)
        pc.setAttr(geo + ".sx", keyable=True, lock=False)
        pc.setAttr(geo + ".sy", keyable=True, lock=False)
        pc.setAttr(geo + ".sz", keyable=True, lock=False)
        pc.parent(geo, root)

    #Create deformers container
    deformersRoot = tkc.createRigObject(root, name=root.name() + "_Deformers")

    #Re-parent deformers
    for deform in defs:
        cns = tkc.getConstraints(deform)
        poseManaged = False
        scalingManaged = False
        for cn in cns:
            if cn.type() == "parentConstraint":
                poseManaged = True
            elif cn.type() == "scaleConstraint":
                scalingManaged = True
        
        if not poseManaged or not scalingManaged:
            ancestor = deform.getParent()
            if not poseManaged:
                tkc.constrain(deform, ancestor, "Pose")
            if not scalingManaged:
                tkc.constrain(deform, ancestor, "Scaling")

        pc.parent(deform, deformersRoot)

    #Bake deformers animation
    start = pc.playbackOptions(query=True, animationStartTime=True)
    end = pc.playbackOptions(query=True, animationEndTime=True)
    
    pc.bakeResults(defs, simulation=True, sampleBy=1, t=(start,end), disableImplicitControl=True, preserveOutsideKeys=True, sparseAnimCurveBake=False, removeBakedAttributeFromLayer=False, bakeOnOverrideLayer=False, minimizeRotation=True, controlPoints=False, shape=False)

    #If operation succeeded and deleteTheRest=True, remove useless items
    if deleteTheRest:
        pc.delete(rigRoot)
        pass

    pc.undoInfo(closeChunk=True)
    return root

def byPassNode(inObj, ancestor=None, removeNode=True, affect=True):
    newDef = None
    #Get Root
    root = tkc.getParent(inObj, root=True)

    #Get Members
    members = tkc.getChildren(root, True)
    
    #Get Controls/Deformers
    controls = []
    deformers = []
    for member in members:
        if member.type() == "joint":
            deformers.append(member)
        else:
            controls.append(member)
    
    #Get first Ancestor if not given
    if ancestor == None:
        ancestor = None
        #  - try from root
        cns = tkc.getConstraints(root)
        if len(cns) > 0:
            #print cns
            targets = tkc.getConstraintTargets(cns[0])
            if len(targets) > 0:
                ancestor = targets[0]
        
        #  - try with "controls"
        for control in controls:
            cns = tkc.getConstraints(root)
            if len(cns) > 0:
                #print cns
                targets = tkc.getConstraintTargets(cns[0])
                if len(targets) > 0:
                    ancestor = targets[0]
                    break

    if ancestor == None:
        pc.warning("Cannot find ancestor !")
        return
    else:
        print "Ancestor found " + str(ancestor)

    pc.undoInfo(openChunk=True)

    #Get Dependents and re-constrain to ancestor
    if removeNode:
        allControls = []
        allControls.append(root)
        allControls.extend(controls)
        
        dependents = []
        for control in allControls:
            cns = tkc.getConstraintsUsing(control)
            #print "Cons using " + str(control) + " : " + str(cns)
            for cn in cns:
                owner = tkc.getConstraintOwner(cn)
                for own in owner:
                    if not own in allControls and not own in dependents:
                        otherRoot = tkc.getParent(own, root=True)
                        if otherRoot != root:
                            dependents.append(own)
        if affect:
            for dependent in dependents:
                tkc.removeAllCns(dependent)
                tkc.constrain(dependent, ancestor, inType="Pose", inOffset=True)
                tkc.constrain(dependent, ancestor, inType="Scaling", inOffset=True)

    #Get deformers and replace with Ancestor deformer if needed and possible
    # - get a deformer
    if len(deformers) > 0:
        ancestorDeformer = None

        if ancestor.type() == "joint":
            ancestorDeformer = ancestor
        else:
            ancestorRoot = tkc.getParent(ancestor, root=True)
            ancestorMembers = tkc.getChildren(ancestorRoot, True)
            ancestorDeformer = None
            for member in ancestorMembers:
                if member.type() == "joint":
                    ancestorDeformer = member
                    break

        if ancestorDeformer == None:
            proxyName = root.name()[:-5] + "_PROXYDEFORMER"
            
            pc.warning("Cannot find ancestor deformer, create a proxy deformer : " + proxyName)
            if not pc.objExists(proxyName):
                pc.select(clear=True)
                ancestorDeformer = pc.joint(name=proxyName)
                newDef = ancestorDeformer
            else:
                ancestorDeformer = pc.PyNode(proxyName)
        else:
            print "Ancestor deformer found " + str(ancestorDeformer)

        if affect:
            tkc.replaceDeformers(deformers, ancestorDeformer)

    #Remove node
    if affect:
        if removeNode:
            pc.delete(root)
        else:
            if len(deformers) > 0:
                pc.delete(deformers)

    #TODO remove from KeySets/SelectionSets

    pc.undoInfo(closeChunk=True)

    return newDef

def safeByPassNode(ns, objStr, ancestorStr="", removeNode=False):
    inObj=None
    ancestor=None
    if ancestorStr != "" and pc.objExists(ns + ":" + ancestorStr):
        ancestor=pc.PyNode(ns + ":" + ancestorStr)

    if pc.objExists(ns + ":" + objStr):
        inObj=pc.PyNode(ns + ":" + objStr)

    if inObj != None:
        return byPassNode(inObj, ancestor, removeNode)

    pc.warning("Can't find object to bypass node (%s, %s)" % (ns, objStr))
    return None

def reachIteratively(inAttr, inRefAttrs, inRefValues, inIterations=100, inEpsilon=0.001, debug=False, inKnownMin=None, inKnownMax=None, inKnownRatio=None):
    if not isinstance(inRefAttrs, list):
        inRefAttrs = [inRefAttrs]

    if not isinstance(inRefValues, list):
        inRefValues = [inRefValues]

    pyAttr = pc.PyNode(inAttr)
    attrMax = inKnownMax if inKnownMax is not None else pyAttr.getMax()
    attrMin = inKnownMin if inKnownMax is not None else  pyAttr.getMin()

    maxIter = inIterations
    #pc.mel.eval("paneLayout -e -manage true $gMainPane")
    attrValue = pc.getAttr(inAttr)
    oldValues = []
    for inRefAttr in inRefAttrs:
        oldValues.append(pc.getAttr(inRefAttr))
    
    deltas = []
    counter = 0
    delta = 0
    for inRefValue in inRefValues:
        singleDelta = math.fabs(inRefValue - oldValues[counter])
        delta += singleDelta 
        deltas.append(singleDelta)
        counter += 1

    oldDeltas = list(deltas)
    
    first = True
    direction = 1 if delta > 0 else -1
    baseratio = 1.0 if inKnownRatio is None else inKnownRatio
    amount = delta * inKnownRatio
    
    minDelta = 180
    closestValue = 0
    while maxIter > 0:
        if math.fabs(delta) <= inEpsilon:
            if debug:
                print "returned {0} with delta {1}".format(math.fabs(inRefValue - oldValues[0]), delta)
            return

        value = attrValue + amount * direction
        if not attrMax is None and value > attrMax:
            value = attrMax
        if not attrMin is None and value < attrMin:
            value = attrMin

        pc.setAttr(inAttr, value)

        #pc.setAttr("IK3_SoftChain_TestGeneration:IK3_SoftChain_TestGeneration_IK_Ctrl.ty", pc.getAttr("IK3_SoftChain_TestGeneration:IK3_SoftChain_TestGeneration_IK_Ctrl.ty"))
        #pc.refresh()
        curValues = []
        for inRefAttr in inRefAttrs:
            curValues.append(pc.getAttr(inRefAttr))
        
        deltas = []
        stepDeltas = []
        stepDelta = 0
        delta = 0
        counter = 0
        for inRefValue in inRefValues:
            singleDelta = math.fabs(inRefValue - curValues[counter])
            delta += singleDelta 
            deltas.append(singleDelta)

            singleStepDelta = math.fabs(oldValues[counter] - curValues[counter])
            stepDelta += singleStepDelta 
            stepDeltas.append(singleStepDelta)

            counter += 1
        
        if delta < minDelta:
            #print "New best : delta : %s, minDelta : %s, closestValue : %s (%s => %s)" % (str(delta), str(minDelta), str(closestValue), str(curValues[0]), str(inRefValues[0]))
            minDelta = delta
            closestValue = value

        oldDelta = 0
        for singleDelta in oldDeltas:
            oldDelta += singleDelta

        if delta > oldDelta + inEpsilon:
            #value = value - amount * direction
            #pc.setAttr(inAttr, value)
            #print "delta : %s, oldDelta : %s" % (str(delta), str(oldDelta))
            direction *= -1
            if not first:
                amount *= .5
        else:
            if stepDelta == 0:
                direction *= -1
                amount *= .5

                stepDelta = 1
            amount *= delta / stepDelta

        first = False

        attrValue = value
        oldDeltas = list(deltas)
        oldValues = list(curValues)
        
        maxIter -= 1

        if debug:
            print "value : %s, oldValue : %s, oldDelta : %s, curValue : %s, curDelta : %s (amount : %s, stepDelta ! %s)" % (str(value), str(oldValues[0]), str(oldDeltas[0]), str(curValues[0]), str(delta), str(amount), str(stepDelta))

    pc.setAttr(inAttr, closestValue)
    if debug:
        print "exited after %i iterations" % (inIterations - maxIter)

""" DEPRECATED
def reachIterativelyOLD(inAttr, inRefAttr, inRefValue, inIterations=100, inEpsilon=0.0001, debug=True):
    maxIter = inIterations
    
    attrValue = pc.getAttr(inAttr)
    oldValue = pc.getAttr(inRefAttr)
    
    delta = math.fabs(inRefValue - oldValue)
    oldDelta = delta
    
    first = True
    direction = 1 if delta > 0 else -1
    amount = delta
    
    minDelta = 180
    closestValue = 0
    while maxIter > 0:
        if math.fabs(delta) <= inEpsilon:
            print "returned {0} with delta {1}".format(math.fabs(inRefValue - curValue), delta)
            return

        value = attrValue + amount * direction
        pc.setAttr(inAttr, value)
        
        curValue = pc.getAttr(inRefAttr)
        delta = math.fabs(inRefValue - curValue)
        stepDelta = math.fabs(oldValue - curValue)
        
        if delta < minDelta:
            minDelta = delta
            closestValue = value

        if delta > oldDelta + inEpsilon:
            #value = value - amount * direction
            #pc.setAttr(inAttr, value)
            print "delta : %s, oldDelta : %s" % (str(delta), str(oldDelta))
            direction *= -1
            if not first:
                amount *= .5
        else:
            amount *= delta / stepDelta

        first = False

        attrValue = value
        oldDelta = delta
        oldValue = curValue
        
        maxIter -= 1
    
        if debug:
            print "value : %s, oldValue : %s, oldDelta : %s, curValue : %s, curDelta : %s (amount : %s, stepDelta ! %s)" % (str(value), str(oldValue), str(oldDelta), str(curValue), str(delta), str(amount), str(stepDelta))

    print minDelta, closestValue
    pc.setAttr(inAttr, closestValue)
    if debug:
        print "exited after %i iterations" % (inIterations - maxIter)
"""

def plotRigAndExport(inPath):
    fbxRoot = plotRig()
    if fbxRoot != None:
        pmsys.exportAll(inPath, force=True, type="FBX export")

def getMeshesT(NS):
    refMeshes = pc.ls(NS + ":*", type="mesh")
    refMeshesT = []
    for mesh in refMeshes:
        if not mesh.getParent() in refMeshesT:
            refMeshesT.append(mesh.getParent())
    return refMeshesT

def copyUVs(inRef, inTarget):
    #print "inRef",inRef
    #print "inTarget",inTarget
    refMeshShape = inRef if inRef.type() != "transform" else inRef.getShape()
    targetTransform = inTarget if inTarget.type() == "transform" else inTarget.getParent()

    histo = pc.listHistory(targetTransform)

    for histoItem in histo:
        if histoItem.type() == "polyMapDel":
            pc.delete(histoItem)

    hasIntermediate = False
    shapes = targetTransform.getShapes()
    targetMeshShape = shapes[0]

    for shape in shapes:
        if shape.intermediateObject.get():
            hasIntermediate = True
            targetMeshShape = shape

    if hasIntermediate:
        targetMeshShape.intermediateObject.set(False)
        pc.polyTransfer(targetMeshShape, uvSets=True, alternateObject=refMeshShape)

        pc.select(targetMeshShape)
        pc.mel.eval("DeleteHistory")

        targetMeshShape.intermediateObject.set(True)
    else:
        targetMeshShape.clearUVs()
        targetMeshShape.setUVs(*refMeshShape.getUVs())
        targetMeshShape.assignUVs(*refMeshShape.getAssignedUVs())

def copyAssetUVs(*args):
    HELP_TEXT = "Please select two top nodes, the asset to match first, then the 'ref' asset to copy Uvs"

    sel = pc.selected()             

    if len(sel) != 2:
        pc.error(HELP_TEXT)

    refNs = sel[1].namespace()
    targetNs = sel[0].namespace()

    if refNs == targetNs:
        pc.error("Your top nodes needs to have different namespaces ! " + HELP_TEXT)

    refMeshes = pc.ls(refNs+"*", type="mesh")
    refMeshesT = []
    for refMesh in refMeshes:
        meshT = refMesh.getParent()
        if not meshT in refMeshesT:
            refMeshesT.append(meshT)

    for refMeshT in refMeshesT:
        targetMeshName = ""
        if refNs == "":
            targetMeshName = targetNs + refMeshT.name()
        else:
            targetMeshName = refMeshT.name().replace(refNs, targetNs)

        if pc.objExists(targetMeshName):
            copyUVs(refMeshT, pc.PyNode(targetMeshName))
        else:
            pc.warning("Can't find target mesh " + targetMeshName)

def copyMeshesUVs(*args):
    HELP_TEXT = "Please select two meshes, the mesh to match first, then the 'ref' mesh to copy Uvs"

    sel = pc.selected()

    if len(sel) != 2:
        pc.error(HELP_TEXT)

    refMesh = sel[1]
    refMeshShape = None
    if refMesh.type() == "transform":
        refMeshShape = refMesh.getShape()
        if refMeshShape.type() != "mesh":
            refMesh = None
    elif refMesh.type() == "mesh":
        refMesh = refMesh.getParent()
    else:
        refMesh = None

    targetMesh = sel[0]
    targetMeshShape = None
    if targetMesh.type() == "transform":
        targetMeshShape = targetMesh.getShape()
        if targetMeshShape.type() != "mesh":
            targetMesh = None
    elif targetMesh.type() == "mesh":
        targetMesh = targetMesh.getParent()
    else:
        targetMesh = None

    if refMesh == None or targetMesh == None:
        pc.error(HELP_TEXT)

    copyUVs(refMesh, targetMesh)

def transferShadings(refNS, targetNS, doTransfer=True, UVs=True, Shader=True):
    refMeshesT = getMeshesT(refNS)
    targetMeshesT = getMeshesT(targetNS)
    orphanMeshes = []
    
    for refMesh in refMeshesT:
        refMeshName = refMesh.stripNamespace()
        found = None
        for targetMesh in targetMeshesT:
            if targetMesh.stripNamespace() == refMeshName:
                found = targetMesh
                break
        if found != None:
            targetMeshesT.remove(found)
            if doTransfer:
                transferShading(refMesh, found, UVs, Shader)
        else:
            orphanMeshes.append(refMesh)

    if len(orphanMeshes) + len(targetMeshesT) > 0:
        if len(orphanMeshes) > 0:
            print "Cannot find TARGET equivalent of source meshes : " + str([o.name() for o in orphanMeshes])
        if len(targetMeshesT) > 0:
            print "Cannot find SOURCE equivalent of target meshes : " + str([o.name() for o in targetMeshesT])
        pc.error("Synchro problems found (see log for details) !")
    
def transferShading(refMesh, targetMesh, UVs=True, Shader=True):
    #Transfer UVS
    if UVs:
        #Search if object have 'orig' shape
        shapes = targetMesh.getShapes()
        downStackShape = shapes[len(shapes) - 1]
        #print "downStackShape " + downStackShape.name()
        intermediate = pc.getAttr(downStackShape.name() + ".intermediateObject")
        #print "Intermediate  ? " + str(intermediate)
        if intermediate:
            pc.setAttr(downStackShape.name() + ".intermediateObject", False)
        pc.transferAttributes(refMesh, downStackShape, transferUVs=2, sampleSpace=4)
        pc.delete(downStackShape, constructionHistory=True)
        if intermediate:
            pc.setAttr(downStackShape.name() + ".intermediateObject", True)

    #Assign shader
    if Shader:
        engine = pc.listConnections(refMesh.getShape(), type="shadingEngine")[0]
        shader = pc.listConnections(engine.name() + ".surfaceShader")[0]
        
        pc.select(targetMesh, replace=True)
        pc.hyperShade(assign = shader.name())

def updateShading(texturePath, uvPath, doTransfer=True):
    uvNS = os.path.basename(uvPath).split(".")[0]
    textNS = os.path.basename(texturePath).split(".")[0]
    
    pmsys.openFile(uvPath, force=True)
    pmsys.importFile(texturePath, namespace=textNS, mergeNamespacesOnClash=True, force=True)

    transferShadings(textNS, uvNS, doTransfer)

def updateShadingInPlace(doTransfer=True):
    sel = pc.ls(sl=True)
    if len(sel) == 2 and sel[0].namespace() != "" and sel[1].namespace() != "" and sel[0].namespace() != sel[1].namespace():
        uvNS = sel[0].namespace().split(":")[0]
        textNS = sel[1].namespace().split(":")[0]
        
        transferShadings(textNS, uvNS, doTransfer)
    else:
        pc.error("Selection is invalid, please select ref root first (texture), then target root (uvs) !")

def cleanMesh(inMesh):
    shapes = mc.listRelatives(inMesh, shapes=True)
    if shapes != None:
        for shape in shapes:
            if mc.getAttr("{0}.intermediateObject".format(shape)):
                mc.delete(shape)

def cleanSelectedMeshes(*args):
    sel = mc.ls(sl=True)
    for selObj in sel:
        pc.mel.eval("DeleteHistory " + selObj)
        cleanMesh(selObj)

def convertSkinningToCluster(*args):
    inVerbose=False

    HELP_TEXT = "You must select skinned meshes + any numbers of influences to convert as cluster deformers"

    createdClusters = []
    selection = pc.ls(sl = True, type='transform')
    if len(selection) == 0 :
        pc.warning("Nothing is selected")
        pc.warning(HELP_TEXT)
        return createdClusters
    
    #raw lists (filtering by type only)
    rawMeshesT = []
    rawJoints = []
    #data dictionaries (transform:[associated SkinClusters,...], filtered by usage)
    meshesT = {}
    joints = {}

    #filter selection
    for selItem in selection:
        if selItem.type() == "transform":
            shape = selItem.getShape()
            if shape != None and shape.type() == "mesh":
                rawMeshesT.append(selItem)

                skinClusterObj = tkc.getSkinCluster(selItem)
                if skinClusterObj != None:
                    meshesT[selItem] = [skinClusterObj]
                else:
                    pc.warning("The selected mesh don't have any skinCluster ({0})".format(selItem.name()))
        elif selItem.type() == "joint":
            rawJoints.append(selItem)

            skinClusterObjs = pc.listHistory(selItem, type="skinCluster", future=True)
            if len(skinClusterObjs) > 0:
                joints[selItem] = skinClusterObjs
            else:
                pc.warning("The selected joint is not associated to a skinCluster ({0})".format(selItem.name()))

    #Nothing consistent in selection ?
    if len(joints) == 0 and len(meshesT) == 0 :
        pc.warning("Your selection does not contains skinned meshes nor joints used as influence !")
        pc.warning(HELP_TEXT)
        return createdClusters

    if len(rawJoints) == 0:
        if inVerbose:
            print "No influences selected, add them from meshes"
        for meshT, skins in meshesT.iteritems():
            skinClusterObj = skins[0]
            infs = pc.skinCluster(skinClusterObj,query=True,inf=True)
            for inf in infs:
                if not inf in joints:
                    joints[inf] = [skinClusterObj]
                else:
                    joints[inf].append(skinClusterObj)
    elif len(rawMeshesT) == 0:
        if inVerbose:
            print "No meshes selected, add them from influences"
        for inf, skins in joints.iteritems():
            for skin in skins:
                meshes = skin.getGeometry()
                for mesh in meshes:
                    meshT = mesh.getParent()
                    if not meshT in meshesT:
                        meshesT[meshT] = [skin]
                    else:
                        meshesT[meshT].append(skin)

    if inVerbose:
        print len(meshesT), "meshes", meshesT
        print len(joints), "joints", joints

    if len(joints) == 0: #No consistent joints ?
        pc.warning("Your selection does not contains joints used as influence !")
        pc.warning(HELP_TEXT)
        return createdClusters
    elif len(meshesT) == 0: #No consistent meshes ?
        pc.warning("Your selection does not contains skinned meshes !")
        pc.warning(HELP_TEXT)
        return createdClusters

    #We have all we need, let's proceed

    #First reverse the mesh:skinClusters dictionary to skinCluster:meshes and create a lookup for pointCount
    skinsFromMeshes = {}
    pointCounts = {}
    for meshT, skins in meshesT.iteritems():
        if not skins[0] in skinsFromMeshes:
            skinsFromMeshes[skins[0]] = [meshT]
        else:
            skinsFromMeshes[skins[0]].append(meshT)

        pointCounts[meshT] = pc.polyEvaluate(meshT, vertex=True)

    #Here we go!

    gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')
    pc.progressBar( gMainProgressBar,
    edit=True,
    beginProgress=True,
    isInterruptable=True,
    status="Converting skinCluster to clusters",
    maxValue=len(joints))

    for joint, skins in joints.iteritems():
        #jointPosition = pc.xform(skinnedJoint, query=True, worldSpace=True, translation=True)
        meshes = []
        for skin in skins:
            if skin in skinsFromMeshes:
                meshes.extend(skinsFromMeshes[skin])
        #Create cluster
        createdCluster = pc.cluster(meshes, name = "TKCluster_"+joint.name(), relative = True)
        createdClusters.append(createdCluster[1])

        #Create cluster parent
        clusterGrp = pc.group(name = "Cluster_"+joint.name()+"_grp", empty=True, world=True)
        
        #Set positions (with local pivots)
        jointPosition = pc.xform(joint, query=True, worldSpace=True, translation=True)
        createdCluster[1].rotatePivot.set(jointPosition)
        createdCluster[1].scalePivot.set(jointPosition)
        clusterShape = createdCluster[1].getShape()
        clusterShape.originX.set(jointPosition[0])
        clusterShape.originY.set(jointPosition[1])
        clusterShape.originZ.set(jointPosition[2])
        clusterGrp.rotatePivot.set(jointPosition)
        clusterGrp.scalePivot.set(jointPosition)

        pc.parent(createdCluster[1], clusterGrp)

        #Set deform envelope maps
        for i in range(len(meshes)):
            mesh = meshes[i]
            skinClusterObj = meshesT[mesh][0]
            infs = pc.skinCluster(skinClusterObj,query=True,inf=True)
            jointIndex = infs.index(joint)
            jointWeights = list(skinClusterObj.getWeights(mesh, jointIndex))
            for x in range(pointCounts[mesh]):
                clusterWeight = jointWeights[x]
                skinClusterObj.weightList[x].weights[jointIndex].set(clusterWeight)
                createdCluster[0].weightList[i].weights[x].set(clusterWeight)

        pc.progressBar(gMainProgressBar, edit=True, step=1)

    pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

    return createdClusters

def convertClusterToSkinning(*args):
    inVerbose=False
    
    HELP_TEXT = "You must select meshes with clusters + any numbers of clusters to convert to skinning"

    createdSkins = []
    
    selection = pc.ls(sl = True, type='transform')
    if len(selection) == 0 :
        pc.warning("Nothing is selected")
        pc.warning(HELP_TEXT)
        return createdSkins
    
    #raw lists (filtering by type only)
    rawMeshesT = []
    rawClusters = []

    #data dictionaries (transform:[associated SkinClusters,...], filtered by usage)
    meshesT = {}
    clusters = {}

    #filter selection
    for selItem in selection:
        if selItem.type() == "transform":
            shape = selItem.getShape()
            print "shape.type()",shape.type()
            if shape != None and shape.type() == "mesh":
                rawMeshesT.append(selItem)

                meshClusters = pc.listHistory(type="cluster")

                if len(meshClusters) > 0:
                    meshesT[selItem] = meshClusters
                else:
                    pc.warning("The selected mesh don't have any clusters ({0})".format(selItem.name()))
            elif shape != None and shape.type() == "clusterHandle":
                meshCluster = pc.listHistory(shape, type="cluster", future=True)[0]
                rawClusters.append(meshCluster)
                meshes = pc.listHistory(meshCluster, type="mesh", future=True)
                if len(meshes) > 0:
                    clusters[meshCluster] = meshes
                else:
                    pc.warning("The selected cluster is not associated to a mesh ({0})".format(meshCluster.name()))
            else:
                pc.warning("The selection is not a mesh nor a cluster".format(selItem.name()))

    #Nothing consistent in selection ?
    if len(clusters) == 0 and len(meshesT) == 0 :
        pc.warning("Your selection does not contains clustered meshes nor clusters !")
        pc.warning(HELP_TEXT)
        return createdSkins

    if len(rawClusters) == 0:
        if inVerbose:
            print "No clusters selected, add them from meshes"
        for meshT, meshClusters in meshesT.iteritems():
            for cluster in meshClusters:
                if not cluster in clusters:
                    clusters[cluster] = [meshT.getShape()]
                else:
                    clusters[cluster].append(meshT.getShape())
    elif len(rawMeshesT) == 0:
        if inVerbose:
            print "No meshes selected, add them from clusters"
        for cluster, meshes in clusters.iteritems():
            for mesh in meshes:
                meshT = mesh.getParent()
                if not meshT in meshesT:
                    meshesT[meshT] = [cluster]
                else:
                    meshesT[meshT].append(cluster)

    if inVerbose:
        print len(meshesT), "meshes", meshesT
        print len(clusters), "clusters", clusters

    if len(clusters) == 0: #No consistent joints ?
        pc.warning("Your selection does not contains clusters !")
        pc.warning(HELP_TEXT)
        return createdSkins
    elif len(meshesT) == 0: #No consistent meshes ?
        pc.warning("Your selection does not contains clustered meshes !")
        pc.warning(HELP_TEXT)
        return createdSkins

    #We have all we need, let's proceed

    #Here we go!

    gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')
    pc.progressBar( gMainProgressBar,
    edit=True,
    beginProgress=True,
    isInterruptable=True,
    status="Converting clusters to skinning",
    maxValue=len(clusters))

    createdJoints = []
    jointsWeights = []
    meshesSkins = {}
    pointCounts = {}

    print "clusters",clusters

    for cluster, meshes in clusters.iteritems():
        clusterT = pc.listHistory(cluster, type="transform")[-1]
        clusterPosition = clusterT.rotatePivot.get()

        #Create joint
        pc.select(clear=True)

        shortName = cluster.stripNamespace()
        if shortName.startswith("TKCluster_"):
            shortName = shortName[10:]
        if shortName.endswith("Handle"):
            shortName = shortName[:-6]

        createdJoint = pc.joint(name = cluster.namespace() + cluster.stripNamespace()[10:-13])
        createdJoints.append(createdJoint)
        pc.xform(createdJoint, worldSpace=True, translation=clusterPosition)

        for i in range(len(meshes)):
            meshT = meshes[i].getParent()
            pointCounts[meshT] = pc.polyEvaluate(meshes[i], vertex=True)
            clusterWeight = []
            for x in range(pointCounts[meshT]):
                clusterWeight.append(cluster.weightList[i].weights[x].get())

            if not meshT in meshesSkins:
                meshesSkins[meshT] = {createdJoint:clusterWeight}
            else:
                meshesSkins[meshT][createdJoint] = clusterWeight

        pc.progressBar(gMainProgressBar, edit=True, step=1)

    #Add a TK_0_Deform if needed
    TK_0_Deform = None

    need0Deform = False
    for meshT, jointsDic in meshesSkins.iteritems():
        Zweights = [0 for i in range(pointCounts[meshT])]

        for i in range(pointCounts[meshT]):
            addedWeights = 0.0
            for joint, weights in jointsDic.iteritems():
                addedWeights += weights[i]
            if addedWeights < 1.0:
                need0Deform = True
                Zweights[i] = 1.0 - addedWeights
        if need0Deform:
            if TK_0_Deform == None:
                pc.select(clear=True)
                TK_0_Deform = pc.joint(name="TK_0_Deform")

            jointsDic[TK_0_Deform] = Zweights

    for meshT, jointsDic in meshesSkins.iteritems():
        joints = jointsDic.keys()

        skin = pc.animation.skinCluster(meshT,joints, name=meshT.name() + "_skinCluster", toSelectedBones=True)

        lenJoints = len(joints)
        weights = [0.0 for i in range(pointCounts[meshT] * lenJoints)]
        for i in range(pointCounts[meshT]):
            for x in range(lenJoints):
                weights[x + i*lenJoints] = jointsDic[joints[x]][i]

        print "meshT",meshT,weights
        skin.setWeights(skin.getGeometry()[-1], range(lenJoints), weights)
    
    pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

def hammerCenter(inObj, inThreshold=10.0):
    
    shape = inObj.getShape()
    
    if shape.type() != "mesh":
        return

    points = shape.getPoints()
    indices = []
    i=-1
    for point in points:
        i += 1
        if(point[0] < inThreshold and point[0] > -inThreshold and 
           point[1] < inThreshold and point[1] > -inThreshold and
           point[2] < inThreshold and point[2] > -inThreshold):
            indices.append(i)

    print "indices",len(indices),indices
    if len(indices) > 0:
        pc.select(["{0}.vtx[{1}]".format(inObj.name(), index) for index in indices])
        pc.mel.eval('weightHammerVerts;')

def isControl(inObj):
    prop = tkc.getProperty(inObj, "OSCAR_Attributes")
    return prop != None and (hasattr(prop,"RefObject") or hasattr(prop,"inversed_Axes"))

#Locators as groups
def simplifyTransforms(locators=True, nurbsCurves=False):
    cnt = 0
    trans = pc.ls(type="transform")
    
    for oTrans in trans:
        shapes = oTrans.getShapes()
        for shape in shapes:
            if locators and shape.type() == "locator":
                pc.delete(shape)
                cnt += 1
                continue
            if nurbsCurves and shape.type() == "nurbsCurve":
                cons = pc.listConnections(shape)
                for i in reversed(range(len(cons))):
                    if cons[i].type() == "hyperLayout":
                        cons.remove(cons[i])
                visCons = pc.listConnections([shape.overrideEnabled, shape.overrideVisibility, shape.visibility], plugs=True)
                for i in reversed(range(len(visCons))):
                    if ".overrideVisibility" in visCons[i].name():
                        visCons.remove(visCons[i])
                if len(cons) <= len(visCons):
                    if oTrans.getParent() != None and not isControl(oTrans):
                        pc.delete(shape)
                        cnt += 1

    print "Simplify transforms ok " + str(cnt) + " shapes deleted"

#Groups as locators
def addShape(inObj, inShapeType="locator"):
    shape = pc.createNode(inShapeType)
    transform = shape.getParent()
    pc.parent(shape, inObj, add=True, shape=True)
    pc.delete(transform)
    inObj.getShape().rename(inObj.name() + "Shape")

def bsTargetNameFromPose(inPoseName):
    if inPoseName.startswith("Left"):
        return inPoseName[5:] + "_Left"
    elif inPoseName.startswith("Right"):
        return inPoseName[6:] + "_Right"

    return inPoseName

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
   ___                       ____                     
  / _ \ ___  ___ __ _ _ __  |  _ \ ___  ___  ___  ___ 
 | | | / __|/ __/ _` | '__| | |_) / _ \/ __|/ _ \/ __|
 | |_| \__ \ (_| (_| | |    |  __/ (_) \__ \  __/\__ \
  \___/|___/\___\__,_|_|    |_|   \___/|___/\___||___/
                                                      
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''     
def connectOscarPoses(inPosesHolder, nodal=True, scaling=True):
    '''
    CALL

    reload(tkRig)

    ns = "Setup_C_Nerd_AN:"
    inPosesHolder = pc.PyNode(ns + "Oscar_Poses")
    tkRig.connectOscarPoses(inPosesHolder)

    pc.delete(inPosesHolder)

    ---------------------------

    reload(tkRig)

    ns = "Setup_C_Martin_AN:"
    inPosesHolder = pc.PyNode(ns + "Oscar_Poses")
    tkRig.connectOscarPoses(inPosesHolder)
    #pc.delete(inPosesHolder)
    '''

    allowedChannels = ()

    baseChannels = ( "tx", "translateX"  ,"ty", "translateY" , "tz", "translateZ",
                    "rx", "rotateX"     ,"ry", "rotateY"    ,"rz", "rotateZ")

    scalings = ("sx", "scaleX","sy", "scaleY","sz", "scaleZ")

    
    if not scaling:
        allowedChannels = tuple(list(baseChannels)[:])
    else:
        channelsList = list(baseChannels)[:]
        channelsList.extend(list(scalings)[:])
        allowedChannels = tuple(channelsList)

    failedPosesContainer = None
    failedPosesHolders = {}

    poses = tkc.getChildren(inPosesHolder, False, False, False)
    ns = inPosesHolder.namespace()
    #params = tkc.getParameters(inParamHolder)
    #print " *** PARAMS :"
    #for param in params:
        #print "PARAM : '" + param + "'"

    paramsDic = {}

    posesData = []
    #order/filter
    for pose in poses:
        #poseName is of form :   [NAMESPACE]:TKPose_[(eventually)Left/Right_][PoseName]_TKParam_[Attribute, "." replaced by "__"]_TKParam_[Priority]
        splitName = pose.stripNamespace().split("_TKParam_")
        poseName = splitName[0][7:]
        attributeName = splitName[1].replace("__",".")
        priority = int(splitName[2])
        ignorePrio = False
        if len(splitName) > 3 and splitName[3] == "True":
            ignorePrio = True
        parameters = tkc.getParameters(pose)

        posesData.append((pose, poseName, attributeName, priority, parameters, ignorePrio))
    posesData.sort(key=lambda x: x[3], reverse=True)

    prioritaryAttributes = {}#animChannel:{priority,poseChannel}, )
    ignoredPriority = {}#animChannel:{ignored,poseChannel}, )
    correctivesDic  = {}

    correctives = pc.ls(["*:*_correctiveBS","*_correctiveBS"], type="blendShape")
    for correc in correctives:
        meshName = correc.name()[:-13]
        arrayAttrs = pc.listAttr("{0}.weight".format(correc.name()), multi=True)
        correctivesDic[meshName]=[]
        for weightAttr in arrayAttrs:
            if len(pc.listConnections("{0}.{1}".format(correc.name(), weightAttr), destination=False)) == 0:
                correctivesDic[meshName].append(weightAttr)

    #print ""
    #print " *** POSES :"
    for attr, poseName, attributeName, priority, params, ignorePrio  in posesData:
        #poseName is of form :   [NAMESPACE]:TKPose_[Left/Right]_[PoseName]_Params
        print "Filtering : '" + poseName + "'"
        if palt.exists(ns+attributeName):
            #We can search for attributes to connect (bs targets with name ending with $POSENAME[_Left/_Right])
            for correctedMesh, correctives in correctivesDic.iteritems():
                bsTargetName = bsTargetNameFromPose(poseName)
                #print "poseName",poseName,"bsTargetName",bsTargetName
                if correctedMesh.split(":")[-1] + "_" + bsTargetName in correctives:
                    correctAttr = correctedMesh+"_correctiveBS."+correctedMesh.split(":")[-1] + "_" + bsTargetName
                    if palt.exists(correctAttr):
                        #print "! connect =>",ns+attributeName, correctedMesh+"_correctiveBS."+correctedMesh.split(":")[-1] + "_" + bsTargetName
                        pc.connectAttr(ns+attributeName, correctedMesh+"_correctiveBS."+correctedMesh.split(":")[-1] + "_" + bsTargetName, force=True)

        for param in params:
            object_param = param.split("__")

            if not object_param[1] in allowedChannels:
                print "Stored pose won't work on scaling or non-tranformation attribute for now, dropping (%s) !" % param
                continue
            
            #If we use the neutral pose we have to create a neutral_neutral_pose
            if not palt.exists(ns + object_param[0] + "_NeutralPose_NeutralPose"):
                tkc.setNeutralPose(pc.PyNode(ns + object_param[0] + "_NeutralPose"))

            neutralParam = ns + object_param[0] + "_NeutralPose." + object_param[1]

            if not neutralParam in paramsDic:
                paramsDic[neutralParam] = []

            #manage priorities
            if not neutralParam in prioritaryAttributes:
                prioritaryAttributes[neutralParam] = {}
                ignoredPriority[neutralParam] = {}

            if palt.exists(ns+attributeName):
                paramsDic[neutralParam].append([attr.name() + "." + param, ns+attributeName])
                prioritaryAttributes[neutralParam][ns+attributeName]=priority
                ignoredPriority[neutralParam][ns+attributeName]=ignorePrio
            else:
                if failedPosesContainer == None:
                    failedPosesContainer = pc.group(name=ns + "failedPosesContainer", empty=True)
                    pc.parent(failedPosesContainer, inPosesHolder.getParent())

                paramHolder, poseAttr = (ns+attributeName).split(".")

                failedPosesHolder = None
                if not paramHolder in failedPosesHolders:
                    failedPosesHolder = pc.group(name=paramHolder + "_failed", empty=True)
                    pc.parent(failedPosesHolder, failedPosesContainer)
                    failedPosesHolders[paramHolder] = failedPosesHolder
                else:
                    failedPosesHolder = failedPosesHolders[paramHolder]

                failedParamName = failedPosesHolder + "." + poseAttr
                if not palt.exists(failedParamName):
                    failedParamName = tkc.addParameter(inobject=failedPosesHolder, name=poseAttr, inType="double", default=0)
                    pc.warning(ns+attributeName + " could not be found, attribute created here : " + failedParamName)

                paramsDic[neutralParam].append([attr.name() + "." + param, failedParamName])
                prioritaryAttributes[neutralParam][failedParamName]=priority
                ignoredPriority[neutralParam][failedParamName]=ignorePrio

    #Create expressions / nodes
    code = ""

    for key in paramsDic:
        if not pc.getAttr(key, settable=True):
            pc.warning(key + " not settable, skipping...")

        val = pc.getAttr(key)
        valuemultiplierPairs = paramsDic[key]

        realValues = []
        for valuemultiplierPair in valuemultiplierPairs:
            subVal = pc.getAttr(valuemultiplierPair[0])
            testVal = subVal
            if valuemultiplierPair[0].split("__")[-1] in scalings:
                #print "subVal before", subVal
                if not "Left_" in key and not "Right_" in key:
                    subVal = ((subVal * 2.0) - 1.0) / 2.0
                    testVal = testVal * 2.0
                    #print "subVal after", subVal
                else:
                    subVal = subVal - 1.0
                testVal = testVal - 1.0
                #print "testVal", testVal
            if math.fabs(testVal) >= tkc.CONST_EPSILON:
                realValues.append([subVal, valuemultiplierPair[1]])
            else:
                pass
                #print "Value for %s (%f) was too small and dropped !" % (valuemultiplierPair[0], val)

        if len(realValues) > 0:
            #print "key",key
            if nodal:
                isScaling = key.split(".")[-1] in scalings
                valueOffset = 1.0 if isScaling else 0.0
                #print "isScaling",isScaling
                #print "valueOffset",valueOffset

                addNode = pc.shadingNode('addDoubleLinear', asUtility=True, n=key.replace(".", "_") + "_Output_Add")
                pc.setAttr(addNode.name() + ".input1", val)
                pc.setAttr(addNode.name() + ".input2", valueOffset)
                pc.connectAttr(addNode.name() + ".output", key)
                #indicate free adding port
                addPorts = [addNode.name() + ".input2"]
                for realValue in realValues:
                    #print "realValue", realValue
                    #create a addNode if needed
                    if len(addPorts) == 1:
                        addNode = pc.shadingNode('addDoubleLinear', asUtility=True, n=key.replace(".", "_") + "_Add")
                        pc.connectAttr(addNode.name() + ".output", addPorts[0])
                        addPorts = [addNode.name() + ".input1", addNode.name() + ".input2"]
                    mulNode = pc.shadingNode('multDoubleLinear', asUtility=True, n=key.replace(".", "_") + "_Mul")
                    pc.setAttr(mulNode.name() + ".input1", realValue[0])

                    multiplierOutput = realValue[1]
                    #Manage priorities
                    #If priorities are not ignored and priority is weaker than other "realValue[1]" (multiplier), multiply by the reverse of this one as well...
                    if not ignoredPriority[key][realValue[1]]:
                        #Search 'bigger prios'
                        biggerPrios = []
                        prio = prioritaryAttributes[key][realValue[1]]
                        for otherPoseChannel in prioritaryAttributes[key]:
                            if otherPoseChannel != realValue[1] and prioritaryAttributes[key][otherPoseChannel] > prio:
                                biggerPrios.append(otherPoseChannel)

                        #Create 'bigger prios' reverse multipliers
                        if len(biggerPrios) > 0:
                            plusMinusAvg = pc.shadingNode("plusMinusAverage", asUtility=True, name=realValue[1].replace(".", "__") + "_PriosAdd")
                            plusMinusIndex = 0
                            for biggerPrio in biggerPrios:
                                pc.connectAttr(biggerPrio, plusMinusAvg.name()+".input1D["+str(plusMinusIndex)+"]")
                                plusMinusIndex += 1

                            curClamp = pc.shadingNode("clamp", asUtility=True, name=realValue[1].replace(".", "__") + "_PriosClamp")
                            curClamp.maxR.set(1.0)
                            plusMinusAvg.output1D >> curClamp.inputR

                            curReverse = pc.shadingNode("reverse", asUtility=True, name=realValue[1].replace(".", "__") + "_PriosReverse")
                            curClamp.outputR >> curReverse.inputX

                            prioMulNode = pc.shadingNode('multDoubleLinear', asUtility=True, n=realValue[1].replace(".", "__") + "_PriosMul")
                            curReverse.outputX >> prioMulNode.input1
                            pc.connectAttr(multiplierOutput, prioMulNode.input2)
                            multiplierOutput = prioMulNode.output.name()

                    pc.connectAttr(multiplierOutput, mulNode.name() + ".input2")
                    pc.connectAttr(mulNode.name() + ".output", addPorts[0])
                    addPorts.pop(0)
            else:
                code += key + " = " + str(val)
                for realValue in realValues:
                    code += " + " + str(realValue[0]) + " * " + realValue[1]
                code += ";\n"
        else:
            pass
            #print "No pose values for %s, no entry in expression required !" % key

    if len(code) > 0:
        pc.expression(s=code, name=ns + "OscarPoses_Expr")

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
     _          _                 _   _             
    / \   _ __ (_)_ __ ___   __ _| |_(_) ___  _ __  
   / _ \ | '_ \| | '_ ` _ \ / _` | __| |/ _ \| '_ \ 
  / ___ \| | | | | | | | | | (_| | |_| | (_) | | | |
 /_/   \_\_| |_|_|_| |_| |_|\__,_|\__|_|\___/|_| |_|

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''   

def getAnimated(inControls):
    animatedControls = []

    for ctrl in inControls:
        if pc.keyframe(ctrl, query=True, keyframeCount=True) > 0:
            animatedControls.append(ctrl)

    return animatedControls

def getPosed(inControls):
    movedControls = []

    for keyable in inControls:
        nControl = pc.PyNode(keyable)
        if not tkc.listsBarelyEquals(nControl.getTranslation(), [0.0,0.0,0.0]):
            movedControls.append(nControl.name())
            continue
        if not tkc.listsBarelyEquals(ozms.getPymelRotation(nControl), [0.0,0.0,0.0]):
            movedControls.append(nControl.name())
            continue
        if not tkc.listsBarelyEquals(nControl.getScale(), [1.0,1.0,1.0]):
            movedControls.append(nControl.name())
            continue

    return movedControls

def getPosedControls(inCharName, inCategory="All"):
    keyables = tkc.getKeyables(inCategory=inCategory, inCharacters=[inCharName], ordered=False)
    return getPosed(keyables)

def savePose(inCharName, inKeySet):
    pose = {}
    ctrls = getPosedControls(inCharName, inKeySet)
    for ctrl in ctrls:
        params = tkc.getParameters(ctrl, customOnly=False, keyableOnly=True)
        for param in params:
            paramName = "{0}.{1}".format(ctrl, param)
            pose[paramName] = pc.getAttr(paramName)

    return pose

def applyPose(inPose):
    for attrFullName in inPose:
        try:
            pc.setAttr(attrFullName, inPose[attrFullName])
        except:
            pc.warning("Can't find attribute : {0}".format(attrFullName))

"""
print saveSimpleConstraint(pc.selected()[0])
print saveSimplePose(pc.selected())

loadSimplePose(leashCampPose)
loadSimpleConstraint(CentralChainCns)
"""
def saveSimplePose(inObjs=None):
    if inObjs == None:
        inObjs = pc.selected()

    poses = {}
    for ctrl in inObjs:
        attrs = tkc.getParameters(ctrl, customOnly=False, keyableOnly=True)
        pose = {}
        for attr in attrs:
            pose[attr] = ctrl.attr(attr).get()
        poses[ctrl.name()] = pose
    
    return poses

def loadSimplePose(inPose, inNamespace=None):
    for obj, attrs in inPose.iteritems():
        objName = obj
        if inNamespace != None:
            objName = inNamespace + objName.split(":")[-1]
        if pc.objExists(objName):
            node = pc.PyNode(objName)
        
            for attr, value in attrs.iteritems():
                node.attr(attr).set(value)
        else:
            pc.warning("loadSimplePose failed, object \"{0}\" not found".format(objName))
            pass

def exportSimplePose(inPath=None):
    if inPath == None:
        inPath = mc.fileDialog2(caption="Save your pose file", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=0)

        if inPath != None and len(inPath) > 0:
            inPath = inPath[0]
            
    if inPath == None:
        pc.warning("Invalid file !")
        return

    poses = saveSimplePose()

    if len(poses) > 0:
        tkc.saveString(str(poses), inPath)
        print "pose successfully saved to '{}'".format(inPath)

def importSimplePose(inPath=None, inNs=None):
    if inPath == None:
        inPath = mc.fileDialog2(caption="Load your pose file", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=1)

        if inPath != None and len(inPath) > 0:
            inPath = inPath[0]
            
    if inPath == None:
        pc.warning("Invalid file !")
        return

    strPose = tkc.loadString(inPath)

    pose = None
    try:
        pose = eval(strPose)
    except:
        pass

    if not isinstance(pose, dict):
        pc.warning("Can't read '{}'' as a pose".format(inPath))
        return

    loadSimplePose(pose, inNamespace=inNs)

def saveSimpleConstraint(inObj=None):
    cns = {}

    if inObj == None:
        objs = pc.selected()
        if len(objs) == 0:
            pc.warning("Please select a constrained object to save constraint !")
            return cns
        inObj = objs[0]
    
    cons = tkc.getConstraints(inObj)
    
    if len(cons) > 0:
        cns["destination"] = inObj.name()
        cns["source"] = tkc.getConstraintTargets(cons[0])[0].name()
        
        print "cons[0]",cons[0]
        cns["attrs"] = {}
        cns["attrs"]["targetOffsetTranslate.targetOffsetTranslateX"] = cons[0].target[0].targetOffsetTranslate.targetOffsetTranslateX.get()
        cns["attrs"]["targetOffsetTranslate.targetOffsetTranslateY"] = cons[0].target[0].targetOffsetTranslate.targetOffsetTranslateY.get()
        cns["attrs"]["targetOffsetTranslate.targetOffsetTranslateZ"] = cons[0].target[0].targetOffsetTranslate.targetOffsetTranslateZ.get()
        cns["attrs"]["targetOffsetRotate.targetOffsetRotateX"] = cons[0].target[0].targetOffsetRotate.targetOffsetRotateX.get()
        cns["attrs"]["targetOffsetRotate.targetOffsetRotateY"] = cons[0].target[0].targetOffsetRotate.targetOffsetRotateY.get()
        cns["attrs"]["targetOffsetRotate.targetOffsetRotateZ"] = cons[0].target[0].targetOffsetRotate.targetOffsetRotateZ.get()
        
    return cns

def loadSimpleConstraint(inCons, inSourceNamespace=None, inDestinationNamespace=None):
    sourceNode = None
    destinationNode = None
    source = inCons["source"]
    if inSourceNamespace != None:
        source = inSourceNamespace + source.split(":")[-1]

    destination = inCons["destination"]
    if inDestinationNamespace != None:
        destination = inDestinationNamespace + destination.split(":")[-1]
        
    if pc.objExists(source) and pc.objExists(destination):
        sourceNode = pc.PyNode(source)
        destinationNode = pc.PyNode(destination)
        
        cns = tkc.constrain(destinationNode, sourceNode, "Pose", False)
        for attr, value in inCons["attrs"].iteritems():
            attrsSplit = attr.split(".")
            cns.target[0].attr(attrsSplit[0]).attr(attrsSplit[1]).set(value)
    else:
        pc.warning("loadSimpleConstraint failed, source \"{0}\" or destination \"{1}\" not found".format(source, destination))
        pass


def getAnim(inObjects=None):
    animNodes = []
    if inObjects == None:
        inObjects = pc.selected()
        
    for obj in inObjects:
        animNodes.extend(pc.listConnections(obj, destination=False, type="animCurve"))

    return animNodes

def decorateAnimNode(inAnimNode, inIgnoreNs=False):
    outputAttr = inAnimNode.output.outputs(plugs=True)[0]

    mc.addAttr(inAnimNode.name(), ln="tkConnection", dt="string")
    attr = inAnimNode.tkConnection
    attr.set(outputAttr.name() if not inIgnoreNs else outputAttr.stripNamespace())

    outputObj = outputAttr.node()
    outputParent = outputObj.getParent()

    mc.addAttr(inAnimNode.name(), ln="tkLocalSpace", dt="matrix")
    if outputParent != None:
        attr = inAnimNode.tkLocalSpace
        attr.set(outputParent.worldMatrix[0].get())

    return [inAnimNode.tkConnection, inAnimNode.tkLocalSpace]

def exportAnim(inObjects=None, inPath=None, inAppend=False, inOverride=True, inIgnoreNs=False):
    if inObjects == None:
        inObjects = pc.selected()
    
    if inPath == None:
        inPath = mc.fileDialog2(caption="Save your animation file", fileFilter="mayaAscii file (*.ma)(*.ma)", dialogStyle=1, fileMode=0)

        if inPath != None and len(inPath) > 0:
            inPath = inPath[0]

    if inPath == None:
        pc.warning("No valid output path given !")
        return

    animNodes = getAnim(inObjects)
    
    if len(animNodes) == 0:
        pc.warning("No animation found !")
        return False
        
    existingConnections = {}

    extraAttrs = []
    for animNode in animNodes:
        extraAttrs.extend(decorateAnimNode(animNode, inIgnoreNs))
        existingConnections[animNode.tkConnection.get()] = animNode

    if inAppend and os.path.isfile(inPath):
        nodes = pc.system.importFile(inPath, returnNewNodes=True)
        for node in nodes:
            connection = node.tkConnection.get()
            if connection in existingConnections:
                if inOverride:
                    node.delete()
                else:
                    existingConnections[connection].delete()
                    existingConnections[connection] = node
            else:
                existingConnections[connection] = node

    animNodes = existingConnections.values()

    pc.select(animNodes)

    try:
        pc.system.exportSelected(inPath, constructionHistory=False, type="mayaAscii", force=True)
    except:
        pc.warning("Cannot export !")
    finally:
        #remove meta
        for extraAttr in extraAttrs:
            extraAttr.delete()
        return 

    for extraAttr in extraAttrs:
        extraAttr.delete()

"""
Walker test

import tkMayaCore as tkc
reload(tkc)

import tkRig
reload(tkRig)

import tkNodeling
reload(tkNodeling)

poseName = "walk"
tkRig.importAnim(inPath=r"C:\Users\cyril\Documents\maya\projects\default\scenes\walkerAnim.ma", poseName=poseName)
pose = pc.PyNode(poseName)
tkRig.injectPose(pose)

locomotion = tkn.createAccumulatedVelocity(pc.PyNode("driver1"))

locomotion >> pose.frame
"""

def getLayer(inNode, inSuffix=None):
    neutral = tkc.getNeutralPose(inNode, inSuffix)
    if neutral is None:
        #pc.cutKey(inNode)
        #tkc.resetAll(inNode)
        neutral = tkc.setNeutralPose(inNode)

    if tkc.getNeutralPose(neutral, inSuffix) is None:
        lockedChannels = []
        channels = ["tx","ty","tz","rx","ry","rz","sx","sy","sz"]
        for channel in channels:
            if neutral.attr(channel).isLocked():
                neutral.attr(channel).unlock()
                lockedChannels.append(channel)

        tkc.setNeutralPose(neutral, inSuffix)

        for channel in lockedChannels:
            neutral.attr(channel).lock()

    return neutral

def getLayers(inNode, inConnected=True, inSuffix=None):
    neutrals = tkc.getNeutralPoses(inNode, inSuffix)

    return [n for n in neutrals if not inConnected or tkc.isConnected(n)]

def getAllLayers(inConnected=True, inSuffix=None):
    suffix = inSuffix or tkc.CONST_NEUTRALSUFFIX

    return [l for l in pc.ls("*{0}".format(suffix)) if not inConnected or tkc.isConnected(l)]

def getBaker(inNode):
    bakerName = inNode.name() + CONST_BAKERSUFFIX
    if pc.objExists(bakerName):
        return pc.PyNode(bakerName)

    baker = pc.group(empty=True, name=bakerName)
    inNode.getParent().addChild(baker)
    tkc.resetTRS(baker)

    if not pc.attributeQuery("baked", node=inNode, exists=True):
        inNode.addAttr("baked", defaultValue=0, minValue=0, maxValue=1, at="byte")

    connecteds = tkc.getConnected(inNode)

    for connected in connecteds:
        connectedAttr = inNode.attr(connected)
        connection = connectedAttr.inputs(plugs=True)[0]
        
        locked=False
        if connectedAttr.isLocked():
            connectedAttr.unlock()
            locked=True

        tkn.condition(inNode.baked, 0, "==", connection, baker.attr(connected), inName=tkn.formatAttr(connectedAttr.name()) + "_Baked_Cond") >> connectedAttr

        if locked:
            connectedAttr.lock()
    return baker

def createPose(inCurves, inName="newPose"):
    poseGroup = pc.group(empty=True, name=inName)

    start = 100000
    end = -start

    poseGroup.addAttr("frame", dv=0.0)

    for curve in inCurves:
        #.scaleX
        #print "curve name",curve.name()
        nodeName, attrName = curve.tkConnection.get().split(".")

        #TODO Scaling is skipped right now !!
        if attrName in ["sx", "sy", "sz", "scaleX", "scaleY", "scaleZ"]:#Scaling
            continue

        poseGroup.addAttr(curve.name())
        curve.output >> poseGroup.attr(curve.name())
        poseGroup.attr("frame") >> curve.input

        nKeys = curve.numKeys()
        if start > curve.getTime(0):
            start = curve.getTime(0)
        if end < curve.getTime(nKeys-1):
            end = curve.getTime(nKeys-1)

    poseGroup.addAttr("start", at="long", dv=start)
    poseGroup.addAttr("end", at="long", dv=end)
    poseGroup.addAttr("duration", at="long", dv=end-start+1)

    return poseGroup

def mulPose(inPose, inMultiplier, inName=None):
    poseName = inName or "{0}_{1}_Posemul".format(inPose.name(), tkn.formatAttr(inMultiplier, True))

    poseGroup = pc.group(empty=True, name=poseName)

    channels = [attr for attr in inPose.listAttr(userDefined=True) if not attr.longName() in ["start", "end", "duration", "frame"]]

    for channel in channels:
        #print "channel", channel
        #print "getRealAttr", tkc.getRealAttr(channel.name(), inSkipCurves=False)
        poseGroup.addAttr(channel.longName())

        node = pc.PyNode(tkc.getRealAttr(channel.name(), inSkipCurves=False)).node()
        nodeName, attrName = node.tkConnection.get().split(".")

        if attrName in ["sx", "sy", "sz", "scaleX", "scaleY", "scaleZ"]:#Scaling
            print "Mul Scaling ! (remove 1, mul, then add one)", attrName
        else:
            #print "Classic", attrName
            tkn.mul(channel, inMultiplier) >> poseGroup.attr(channel.longName())

    return poseGroup

def addPose(inPose1, inPose2, inName=None):
    poseName = inName or "{0}_{1}_Poseadd".format(inPose1.name(), inPose2.stripNamespace())

    poseGroup = pc.group(empty=True, name=poseName)

    channelsDic = {}

    channels1 = [attr for attr in inPose1.listAttr(userDefined=True) if not attr.longName() in ["start", "end", "duration", "frame"]]
    for channel in channels1:
        node = pc.PyNode(tkc.getRealAttr(channel.name(), inSkipCurves=False)).node()
        channelName = node.tkConnection.get()

        if channelName in channelsDic:
            channelsDic[channelName].append(channel)
        else:
            channelsDic[channelName] = [channel]

    channels2 = [attr for attr in inPose2.listAttr(userDefined=True) if not attr.longName() in ["start", "end", "duration", "frame"]]
    for channel in channels2:
        node = pc.PyNode(tkc.getRealAttr(channel.name(), inSkipCurves=False)).node()
        channelName = node.tkConnection.get()

        if channelName in channelsDic:
            channelsDic[channelName].append(channel)
        else:
            channelsDic[channelName] = [channel]

    for channel, attrs in channelsDic.iteritems():
        nodeName, attrName = channel.split(".")

        poseGroup.addAttr(attrs[0].longName())

        if len(attrs) == 1:
            attrs[0] >> poseGroup.attr(attrs[0].longName())
        else:
            if attrName in ["sx", "sy", "sz", "scaleX", "scaleY", "scaleZ"]:#Scaling
                print "Add Scaling ! (mul)", attrName
            else:
                #print "Classic", attrName
                tkn.add(attrs[0], attrs[1]) >> poseGroup.attr(attrs[0].longName())

    return poseGroup

def injectPose(inPose, inSiblingSuffix=None, inInclude=None, inExclude=None, inRedirect=None, inActivationAttrName="autoWalk"):
    poseGroup = tkc.getNode(inPose)

    channels = [attr for attr in poseGroup.listAttr(userDefined=True) if not attr.longName() in ["start", "end", "duration", "frame"]]

    connections = {}

    connectedAttrs = []

    for channel in channels:
        #print "channel", channel
        #print "getRealAttr", channel.name(), "=", tkc.getRealAttr(channel.name(), inSkipCurves=False)
        node = pc.PyNode(tkc.getRealAttr(channel.name(), inSkipCurves=False)).node()

        nodeName, attrName = node.tkConnection.get().split(".")

        if nodeName in connections:
            connections[nodeName][attrName] = channel
        else:
            connections[nodeName] = {attrName:channel}

    for nodeName, attrs in connections.iteritems():
        if not pc.objExists(nodeName):
            pc.warning("{0} can't be found !".format(nodeName))
            continue

        node = pc.PyNode(nodeName)

        if( not inInclude is None and not node in inInclude or 
            not inExclude is None and node in inExclude):
            continue

        if not inRedirect is None:
            for key, value in inRedirect.iteritems():
                if node.stripNamespace() == key and pc.objExists(value):
                    nodeName = pc.PyNode(value)
                    node = pc.PyNode(nodeName)
                    break

        layer = getLayer(node)

        if not inSiblingSuffix is None:
            siblingName = nodeName+"_"+inSiblingSuffix
            if not pc.objExists(siblingName):
                layer = pc.duplicate(layer, parentOnly=True)[0]
                layer.rename(siblingName)

        for attr, channel in attrs.iteritems():
            if pc.attributeQuery(attr, node=layer, exists=True):
                if not pc.attributeQuery(inActivationAttrName, node=node, exists=True):
                    node.addAttr(inActivationAttrName, minValue=0.0, maxValue=1.0, defaultValue=1.0, keyable=True)

                channelMul = tkn.mul(channel, node.attr(inActivationAttrName))

                locked = layer.attr(attr).isLocked()
                if locked:
                    layer.attr(attr).unlock()
                channelMul >> layer.attr(attr)
                if locked:
                    layer.attr(attr).lock()
                connectedAttrs.append(layer.attr(attr))
            else:
                print "{0}.{1} can't be found !".format(layer.name(), attr)

    return connectedAttrs

def importAnim(inPath=None, swapNamespace=None, verbose=False, cleanUnconnected=True, addProxies=False, poseName=None):
    if inPath == None:
        inPath = mc.fileDialog2(caption="Load your animation file", fileFilter="mayaAscii file (*.ma)(*.ma)", dialogStyle=1, fileMode=1)

        if inPath != None and len(inPath) > 0:
            inPath = inPath[0]
            
    if inPath == None:
        pc.warning("Invalid file !")
        return False

    nodes = pc.system.importFile(inPath, returnNewNodes=True)

    poseGroup = None
    if not poseName is None:
        return createPose(nodes, poseName)

    extraAttrs = []
    
    foundNodes = {}
    notFoundNodes = []
    
    for node in nodes:
        attr = node.tkConnection
        extraAttrs.append(attr)
        connection = attr.get()
        nodeName, attrName = connection.split(".")
        if swapNamespace != None:
            if len(swapNamespace) > 0:
                if ":" in nodeName:
                    nodeName = nodeName.replace(nodeName.split(":")[0], swapNamespace)
                else:
                    nodeName = swapNamespace + ":" + nodeName
            else:
                if ":" in nodeName:
                    nodeName = nodeName.split(":")[-1]             

        if not nodeName in notFoundNodes:
            if not nodeName in foundNodes:
                if pc.objExists(nodeName):
                    foundNodes[nodeName] = pc.PyNode(nodeName)
                elif not nodeName in notFoundNodes:
                    if addProxies:
                        parentMatrix = node.tkLocalSpace.get()
                        proxy=None
                        if parentMatrix == None:
                            proxy = tkc.createRigObject(None, name=nodeName, type="Controller", mode="child", match=True)
                        else:
                            parentSpace = pc.group(empty=True, name=nodeName + "_LocalSpace")
                            parentSpace.setTransformation(parentMatrix)
                            proxy = tkc.createRigObject(parentSpace, name=nodeName, type="Controller", mode="child", match=True)
                        
                        if proxy.hasAttr(attrName):
                            node.output >> proxy.attr(attrName)
                        elif verbose:
                            pc.warning("Can't find attribute {0}.{1}".format(nodeName, attrName))
                    else:
                        notFoundNodes.append(nodeName)
                        if verbose:
                            pc.warning("Can't find object {0}".format(nodeName))
            
            if nodeName in foundNodes:
                if foundNodes[nodeName].hasAttr(attrName):
                    node.output >> foundNodes[nodeName].attr(attrName)
                elif verbose:
                    pc.warning("Can't find attribute {0}.{1}".format(nodeName, attrName))

    for extraAttr in extraAttrs:
        extraAttr.delete()

    if len(notFoundNodes) > 0:
        option = "deleted" if cleanUnconnected else "kept"
        pc.warning("Some nodes have not been reconnected, they will be {0} ({1})".format(option, [n.name() for n in notFoundNodes]))
        if cleanUnconnected:
            pc.delete(notFoundNodes)

"""
import tkRig
reload(tkRig)

import tkNodeling as tkn
reload(tkn)

#tkRig.createWalker()
tkRig.project("projected", "origin", inGrounds=["pSphere1", "pCone1", "pPlane1"])
"""

def project(inObject, inProjectorObj, inProjectAttr="project", inProjectorAxis=None, inOriginObj=None, inOffset=None, inGrounds=None, inSystemName="Projection_"):
    createdObjects = []

    inObject = tkc.getNode(inObject)

    ns = inObject.namespace()

    inProjectorObj = tkc.getNode(inProjectorObj)

    if inProjectorAxis is None:
        inProjectorAxis = [0,-1,0]

    layer = getLayer(inObject)

    if inOriginObj is None:
        inOriginObj = layer.getParent()

    if inProjectAttr is None:
        inProjectAttr = "project"

    offsetNode = None
    if not inOffset is None:
        offsetNode = pc.group(empty=True, name=ns + inSystemName + str(inObject.stripNamespace()) + "_projectOffset")
        inOriginObj.addChild(offsetNode)
        offsetNode.t.set(inOffset)
        offsetNode.r.set([0,0,0])
        offsetNode.s.set([1,1,1])

    node = pc.createNode("tkProject", name=ns + inSystemName + str(inObject.stripNamespace()) + "_Project")

    createdObjects.append(node)

    worldLayer = tkn.worldMatrix(offsetNode or inOriginObj)
    worldLayer.outputTranslate >> node.origin

    direction = tkn.pointMatrixMul(inProjectorAxis, inProjectorObj.worldMatrix[0], vectorMultiply=True)
    direction >> node.direction

    #localize the output
    localized = tkn.pointMatrixMul(node.output, layer.parentInverseMatrix[0])

    if not offsetNode is None:#Remove local offset
        localized = tkn.sub(localized, 0)
        substractNode = localized.node()
        offsetNode.t >> substractNode.input3D[1]

        createdObjects.append(offsetNode)

    if isinstance(inProjectAttr, basestring):
        try:
            inProjectAttr = pc.PyNode(inProjectAttr)
        except:
            pass

    if isinstance(inProjectAttr, basestring):
        attrName = inProjectAttr.split(".")[-1]
        inObject.addAttr(attrName, minValue=0.0, maxValue=1.0, defaultValue=1.0, keyable=True)
        inProjectAttr = inObject.attr(attrName)

    mult = tkn.mul(localized, inProjectAttr)
    mult >> layer.t

    if inGrounds is not None:
        if not isinstance(inGrounds, (list,tuple)):
            inGrounds = [inGrounds]

        for i in range(len(inGrounds)):
            ground = tkc.getNode(inGrounds[i])
            if ground.type() == "transform":
                ground = ground.getShape()

            ground.worldMesh[0] >> node.attr("targets[{0}]".format(i))

    return createdObjects

#tkRig.createFootFixer("locator1", "updown.output", inBlendFrames="locator4.fixFootBlend", inDestObj="locator4")

def connectProjections(inMeshes, inNamespace=None):
    kwargs={}
    if not inNamespace is None:
        kwargs["name"] = inNamespace + ("" if inNamespace.endswith("*") else "*")

    projectNodes = pc.ls(type="tkProject", **kwargs)

    meshes = []

    for inMesh in inMeshes:
        if inMesh.type() == "transform":
            meshes.append(inMesh.getShape())
        else:
            meshes.append(inMesh)

    for projectNode in projectNodes:
        freeIndex = tkc.get_next_free_multi_index(projectNode.targets.name())
        for mesh in meshes:
            mesh.worldMesh[0] >> projectNode.attr("targets[{0}]".format(freeIndex))
            freeIndex += 1


def createFootFixer(inRef, inOnOffAttr, inBlendFrames=4, inDestObj=None):
    inRef = tkc.getNode(inRef)
    inOnOffAttr = tkc.getNode(inOnOffAttr)

    blendIsScalar = True
    if not isinstance(inBlendFrames, (int, float)):
        blendIsScalar = False
        inBlendFrames = tkc.getNode(inBlendFrames)

    inMatrix = inRef
    if inRef.type() == "transform":
        inMatrix = inRef.worldMatrix[0]

    delayedOnOff = tkn.keep(inOnOffAttr)

    reversedOnOff = tkn.reverse(inOnOffAttr)

    #Create keep system
    keepMat1 = tkn.keep(inMatrix, immediate=True, refresh=delayedOnOff)

    keepMat2 = tkn.keep(keepMat1, immediate=True, refresh=reversedOnOff)

    #Blender
    keepIter = tkn.keep(keepMat1.node().iterations, immediate=True, refresh=reversedOnOff)

    deltaFrames = tkn.sub(keepMat1.node().iterations, keepIter)

    insideBlenCond = tkn.condition(deltaFrames, inBlendFrames, inCriterion="<")
    reversedInsideBlenCond = tkn.sub(1, insideBlenCond)

    blendDivide = tkn.div(deltaFrames, inBlendFrames)
    reversedDivide = tkn.sub(1, blendDivide)
    
    #blend1 = tkn.add(keepMat1, keepMat2)
    blend1 = tkn.add(inMatrix, keepMat2)

    blendDivide >> blend1.node().wtMatrix[0].weightIn
    reversedDivide >> blend1.node().wtMatrix[1].weightIn

    blend2 = tkn.add(blend1, keepMat1)
    #blend2 = tkn.add(blend1, inMatrix)
    reversedInsideBlenCond >> blend2.node().wtMatrix[0].weightIn
    insideBlenCond >> blend2.node().wtMatrix[1].weightIn

    """
    #Pair blends
    deckeepMat1 = tkn.decomposeMatrix(keepMat1)
    deckeepMat2 = tkn.decomposeMatrix(keepMat2)

    pairBlend1 = tkn.pairBlend(deckeepMat2.outputTranslate, deckeepMat2.outputRotate,
                                deckeepMat1.outputTranslate, deckeepMat1.outputRotate, blendDivide, inName=inRef+"_blendPose1")

    pairBlend2 = tkn.pairBlend(pairBlend1.outTranslate, pairBlend1.outRotate,
                                deckeepMat1.outputTranslate, deckeepMat1.outputRotate, insideBlenCond, inName=inRef+"_blendPose2")

    """

    if not inDestObj is None:
        inDestObj = tkc.getNode(inDestObj)

        decBlend2 = tkn.decomposeMatrix(blend2)

        #todo localize the output
        decBlend2.outputTranslate >> inDestObj.t
        pairBlend2.outputRotate >> inDestObj.r

    return blend2

def groupAttrs(inRef, inNodes, inExclude=None):
    inRef = tkc.getNode(inRef)
    inNodes = tkc.getNodes(inNodes)

    for node in inNodes:
        attrs = pc.listAttr(node, keyable=True)
        for attr in attrs:
            if not inExclude is None and attr in inExclude:
                continue

            attrNode = node.attr(attr)
            if not pc.attributeQuery(attr, node=inRef, exists=True):
                inRef.addAttr(attrNode.longName(), at=attrNode.type(), defaultValue=attrNode.get(), keyable=True)
            inRef.attr(attr) >> attrNode

def createParent(inObj):
    layer = getLayer(inObj)
    parent = pc.duplicate(inObj, parentOnly=True)[0]
    parent.rename(inObj.name() + "_Parent")
    layerParentName = layer.getParent().name()
    layer.getParent().addChild(parent)
    layer.getParent().rename(parent + tkc.CONST_NEUTRALSUFFIX)
    newBuffer = tkc.addBuffer(layer)
    newBuffer.rename(layerParentName)
    parent.addChild(newBuffer)
    
    shape = inObj.getShape()

    if not shape is None:
        parentShape = pc.duplicate(shape, addShape=True)[0]
        pc.parent(parentShape, parent, add=True, shape=True)
        mc.parent(parentShape.name(), shape=True,rm=True)

        displays = tkc.getDisplay(parent)
        #([t,r,s], size, name)
        tkc.setDisplay(parent, trs=displays[0], size=displays[1] * 1.25, displayName=displays[2])

    return parent

def walkSystem(inName="WalkSystem", inParent=None):
    root = pc.group(empty=True, name=inName)

    if not inParent is None:
        inParent = tkc.getNode(inParent)
        inParent.addChild(root)

    projectSystem = pc.group(empty=True, name="{0}_Projection".format(inName))
    root.addChild(projectSystem)

    Global_Ctrl = pc.PyNode("Global_Ctrl")
    Local_Ctrl = pc.PyNode("Local_Ctrl")

    Left_Leg_IK_Ctrl = pc.PyNode("Left_Leg_IK_Ctrl")
    Right_Leg_IK_Ctrl = pc.PyNode("Right_Leg_IK_Ctrl")

    #-------------------------------------
    #Foot projections
    #-------------------------------------

    #Create "super" controls
    super_Left_Leg_IK_Ctrl = createParent(Left_Leg_IK_Ctrl)
    super_Right_Leg_IK_Ctrl = createParent(Right_Leg_IK_Ctrl)

    #Create orienter rig
    projections = []

    #Left
    super_Left_Leg_IK_Ctrl.addAttr("project", minValue=0.0, maxValue=1.0, defaultValue=1.0, keyable=True)

    heelOrient = pc.group(empty=True, name=Left_Leg_IK_Ctrl.name() + "_HeelOrient")
    super_Left_Leg_IK_Ctrl.addChild(heelOrient)
    heelOrient.t.set([-0.5,-1,0.3])
    leftHeelProject = project(heelOrient, Global_Ctrl, inProjectAttr=super_Left_Leg_IK_Ctrl.project)
    projections.append(leftHeelProject[0])

    tipOrient = pc.group(empty=True, name=Left_Leg_IK_Ctrl.name() + "_TipOrient")
    super_Left_Leg_IK_Ctrl.addChild(tipOrient)
    tipOrient.t.set([-0.5,-1,-2])
    leftTipProject = project(tipOrient, Global_Ctrl, inProjectAttr=super_Left_Leg_IK_Ctrl.project)
    projections.append(leftTipProject[0])

    sideOrient = pc.group(empty=True, name=Left_Leg_IK_Ctrl.name() + "_SideOrient")
    super_Left_Leg_IK_Ctrl.addChild(sideOrient)
    sideOrient.t.set([.5,-1,0.3])
    leftSideProject = project(sideOrient, Global_Ctrl, inProjectAttr=super_Left_Leg_IK_Ctrl.project)
    projections.append(leftSideProject[0])
    
    tkc.constrain(heelOrient, tipOrient, "Direction", False, sideOrient)

    leftLayer = getLayer(Left_Leg_IK_Ctrl)

    #WARNING Reparenting here ! 
    #print "Left_Leg_IK_Ctrl layer",layer
    heelOrient.addChild(leftLayer.getParent())

    #Right
    super_Right_Leg_IK_Ctrl.addAttr("project", minValue=0.0, maxValue=1.0, defaultValue=1.0, keyable=True)

    heelOrient = pc.group(empty=True, name=Right_Leg_IK_Ctrl.name() + "_HeelOrient")
    super_Right_Leg_IK_Ctrl.addChild(heelOrient)
    heelOrient.t.set([-0.5,-1,0.3])
    RightHeelProject = project(heelOrient, Global_Ctrl, inProjectAttr=super_Right_Leg_IK_Ctrl.project)
    projections.append(RightHeelProject[0])
    
    tipOrient = pc.group(empty=True, name=Right_Leg_IK_Ctrl.name() + "_TipOrient")
    super_Right_Leg_IK_Ctrl.addChild(tipOrient)
    tipOrient.t.set([-0.5,-1,-2])
    RightTipProject = project(tipOrient, Global_Ctrl, inProjectAttr=super_Right_Leg_IK_Ctrl.project)
    projections.append(RightTipProject[0])
    
    sideOrient = pc.group(empty=True, name=Right_Leg_IK_Ctrl.name() + "_SideOrient")
    super_Right_Leg_IK_Ctrl.addChild(sideOrient)
    sideOrient.t.set([.5,-1,0.3])
    RightSideProject = project(sideOrient, Global_Ctrl, inProjectAttr=super_Right_Leg_IK_Ctrl.project)
    projections.append(RightSideProject[0])
    
    tkc.constrain(heelOrient, tipOrient, "Direction", False, sideOrient)

    rightLayer = getLayer(Right_Leg_IK_Ctrl)

    #WARNING Reparenting here ! 
    #print "Right_Leg_IK_Ctrl layer",layer
    heelOrient.addChild(rightLayer.getParent())

    groupAttrs(projectSystem, projections)

    projectSystem.useCollisionMode.set(True)

    #-------------------------------------
    #Animation Player
    #-------------------------------------

    animSystem = pc.group(empty=True, name="{0}_Animation".format(inName))
    root.addChild(animSystem)

    animSystem.addAttr("velocity", minValue=0.0, maxValue=100.0, defaultValue=1.9, keyable=True)
    animSystem.addAttr("walkFrame", defaultValue=0, keyable=True)

    #Create velocity listener
    vel = tkn.velocity(Local_Ctrl)

    #Create global -Z axis
    xaxis = tkn.pointMatrixMul([0,0,-1], Local_Ctrl.worldMatrix[0], vectorMultiply=True)
    #Get z-axis component
    xvel = tkn.dot(vel, xaxis)

    #Accumulate
    accuxvel = tkn.accu(xvel)

    #Import walk anim
    poseName = "walk"
    importAnim(inPath=r"C:\Users\cyril\Documents\maya\projects\default\scenes\johnny_walker_animOnly.ma", poseName=poseName)
    pose = pc.PyNode(poseName)
    animSystem.addChild(pose)

    mul = tkn.mul(accuxvel, animSystem.velocity)

    mul >> animSystem.walkFrame

    animSystem.walkFrame >> pose.frame

    #Inject
    #For feet we will inject in separate objects and blend afterwards with foot fixer
    #injectPose(pose, inExclude=[Left_Leg_IK_Ctrl, Right_Leg_IK_Ctrl])
    #attributes = injectPose(pose, inSiblingSuffix="walkPose", inInclude=[Left_Leg_IK_Ctrl, Right_Leg_IK_Ctrl])

    injectPose(pose, inRedirect={   str(Left_Leg_IK_Ctrl.stripNamespace()):str(super_Left_Leg_IK_Ctrl.stripNamespace()),
                                    str(Right_Leg_IK_Ctrl.stripNamespace()):str(super_Right_Leg_IK_Ctrl.stripNamespace())})

    #-------------------------------------
    #Foot fixer
    #-------------------------------------

    fixerSystem = pc.group(empty=True, name="{0}_FootFixer".format(inName))
    root.addChild(fixerSystem)

    fixerSystem.addAttr("blend", defaultValue=3, keyable=True, at="long")

    fixerSystem.addAttr("Left_UpDown", defaultValue=1.0, keyable=True)
    fixerSystem.addAttr("Right_UpDown", defaultValue=1.0, keyable=True)

    #Left
    ref = leftLayer.getParent()
    mat = createFootFixer(ref, fixerSystem.Left_UpDown, fixerSystem.blend)
    #mat = tkn.composeMatrix(pairBlend.outTranslate, pairBlend.outRotate)

    mat = tkn.mul(mat, leftLayer.parentInverseMatrix[0])

    dec = tkn.decomposeMatrix(mat)

    dec.outputTranslate >> leftLayer.t
    dec.outputRotate >> leftLayer.r

    #Right
    ref = rightLayer.getParent()
    mat = createFootFixer(ref, fixerSystem.Right_UpDown, fixerSystem.blend)
    #mat = tkn.composeMatrix(pairBlend.outTranslate, pairBlend.outRotate)

    mat = tkn.mul(mat, rightLayer.parentInverseMatrix[0])

    dec = tkn.decomposeMatrix(mat)

    dec.outputTranslate >> rightLayer.t
    dec.outputRotate >> rightLayer.r

    root.addAttr("startFrame", defaultValue=1, keyable=True, at="long")

    keeps = pc.ls(type="tkKeep")
    for keep in keeps:
        root.startFrame >> keep.startFrame
    #groupAttrs(fixerSystem, keeps)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
  ____                          _   _      
 / ___| _   _ _ __   ___  _ __ | |_(_) ___ 
 \___ \| | | | '_ \ / _ \| '_ \| __| |/ __|
  ___) | |_| | | | | (_) | |_) | |_| | (__ 
 |____/ \__, |_| |_|\___/| .__/ \__|_|\___|
        |___/            |_|               
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#Prevoir un attribut 'Controls' (statut de visibilite) 0, 1, 2, 3

#Mettre a jour les visibilites des controleurs
#def updateControlsState(inModelName, inGroupsNames)

#Keyer les controles "courants" 
#inScope : 0 Controls, 1 Params, 2 All 
#def keyCurrent(inModelName, inScope)

#Keyer tous les params animables
#inScope : 0 All, 1 Body only, 2 Facial only 
#def keyAll(inModelName, inScope)

#Retirer les clefs a la frame courante (selection/all sinon)
#def removeKey(inModelName)

#Retirer l'animation' (selection/all sinon)
#def removeAnim(inModelName)

#Reset Anim pose on selection (TK_Reset ?)
#def reset(inModelName)

#Reset Anim pose all (TK_ResetAll ?)
#def resetAll(inModelName)

#Select all controls
#inSetName = "Main" ou "Body_Main"  ou "Facial_Main"
#def selectSet(inModelName, inSetName)

#Mirror controls (! complex)
#inPose : Mirror the pose (L => R, R => L)
#def mirror(inModelName, inControlsNames, inPose)

def getGeometries(inModel):
    geoNames = ["Geometries", "model", "*geo_grp","*geo*"]
    
    geoNullName = None
    for geoName in geoNames:
        geoNullNames = pc.ls(tkc.stripMockNamespace(inModel + ":" + geoName), transforms=True)
        if len(geoNullNames) > 0:
            geoNullName = geoNullNames[0].name()
            break
    
    children = []

    if geoNullName == None:
        children = pc.ls(tkc.stripMockNamespace(inModel + ":*"), type="mesh")
    else:
        geoNull = pc.PyNode(geoNullName)
        children = pc.listRelatives( geoNull, allDescendents=True, type="mesh" )
    
    refMeshesT = []
    for mesh in children:
        meshTrans = mesh.getParent()
        if not meshTrans in refMeshesT:
            refMeshesT.append(meshTrans)
            
    return refMeshesT

def smooth(inModel, inSubdiv):
    pc.undoInfo(openChunk=True)
    ctrls = getGeometries(inModel)
    if len(ctrls)>0:
        pc.displaySmoothness(ctrls, polygonObject=3)
        for geo in ctrls:
            shapes = geo.getShapes()
            for shape in shapes:
                pc.setAttr(geo.getShape().name() + ".smoothLevel", inSubdiv)
    pc.undoInfo(closeChunk=True)

def selectSet(inModel, inSet="All"):
    pc.undoInfo(openChunk=True)
    ctrls = tkc.getKeyables(inSet, [inModel])
    if len(ctrls)>0:
        pc.select(ctrls, replace=True)
    else:
        pc.select(clear=True)
        #pc.error("No character selected or key set don't exists ("+ inSet  +") !")
    pc.undoInfo(closeChunk=True)

def createKeySetsGroups(inCharacters=[], prefix="", suffix="_ctrls_set"):
    inCharacters = tkc.getCharacters(inCharacters)

    createdSets = []

    for char in inCharacters:
        ns = char.split(":")[0]

        if len(ns) > 0:
            ns += ":"

        prop = tkc.getProperty(char, tkc.CONST_KEYSETSTREEPROP)
        keySets = tkc.getKeySets(char)

        keySetsHierachy = []

        for keySet in keySets:
            keySetsHierachy.append((keySet,tkc.getKeySetParents(char, keySet, prop)))
            
        keySetsHierachy = sorted(keySetsHierachy, key=lambda x: len(x[1]))

        rootSets = []

        for hKeySey in keySetsHierachy:
            selectSet(char, inSet=hKeySey[0])
            createdSets.append(pc.sets(name=ns + prefix + hKeySey[0] + suffix))
            if len(hKeySey[1]) > 0:
                for parentKeySet in hKeySey[1]:
                    pc.sets(ns + prefix + parentKeySet.replace("$", "") + suffix, rm=pc.selected())

                pc.sets(ns + prefix + hKeySey[1][-1].replace("$", "") + suffix, fe=createdSets[-1])
            else:
                rootSets.append(createdSets[-1])

        for rootSet in rootSets:
            if not rootSet.name() == ns + prefix + "All" + suffix:
                pc.sets(ns + prefix + "All" + suffix, fe=rootSet)
            else:
                elems = pc.sets(rootSet.name(), query=True)
                for elem in elems:
                    if elem.type() != "objectSet":
                        pc.sets(rootSet.name(), rm=elem)

        pc.rename(ns + prefix + "All" + suffix, ns + "ctrls_set")

def symSel(mode=0):
    pc.undoInfo(openChunk=True)
    leftregexes = []
    rightregexes = []

    #pre-compile regexes
    for prefixIndex in range(len(CONST_LEFTPREFIXES)):
        leftPrefix = CONST_LEFTPREFIXES[prefixIndex]
        rightPrefix = CONST_RIGHTPREFIXES[prefixIndex]

        leftregexes.append([re.compile(leftPrefix), rightPrefix.replace("^", "")])
        rightregexes.append([re.compile(rightPrefix), leftPrefix.replace("^", "")])
        
    sel = pc.ls(sl=True)
    symSelection = []
    for selObj in sel:
        oppositeName = selObj.name()
        regexes = []
        for regexRule in leftregexes:
            if regexRule[0].search(oppositeName):
                regexes = leftregexes
                break
        if len(regexes) == 0:
            for regexRule in rightregexes:
                if regexRule[0].search(oppositeName):
                    regexes = rightregexes
                    break

        for regexRule in regexes:
            oppositeName = regexRule[0].sub(regexRule[1], oppositeName)
        if oppositeName != selObj.name() and pc.objExists(oppositeName):
            symSelection.append(oppositeName)

    if(len(symSelection) > 0):
        if(mode > 0):
            pc.select(symSelection, add=True)
        else:
            pc.select(symSelection, replace=True)
    else:
        pc.error("Cannot find any symmetrical controls !")
    pc.undoInfo(closeChunk=True)

def keySet(inModel, inSet="All"):
    pc.undoInfo(openChunk=True)
    ctrls = tkc.getKeyables(inSet, [inModel])
    if len(ctrls)>0:
        pc.setKeyframe(ctrls, hierarchy="none", shape=False)
    else:
        pc.error("No character selected or key set don't exists ("+ inSet  +") !")
    pc.undoInfo(closeChunk=True)

def resetSel(inParams=False):
    pc.undoInfo(openChunk=True)
    tkc.executeFromSelection(tkc.resetAll, 0, 0, 0, 0, "Wrong inputs !", False, inParams)
    pc.undoInfo(closeChunk=True)

def resetAll(inModel, inkeySet="All", inParams=False):
    pc.undoInfo(openChunk=True)

    ctrls = tkc.getKeyables(inkeySet, [inModel])

    if len(ctrls)>0:
        ctrlsNodes = tkc.getNodes(ctrls)
        tkc.executeFromCollection(tkc.resetAll, ctrlsNodes, 0, 0, 0, 0, "Wrong inputs !", False, inParams)
    else:
        pc.error("No character selected or key set don't exists ("+ inkeySet  +") !")
    pc.undoInfo(closeChunk=True)

def removeKey(inModel, inkeySet="All"):
    pc.undoInfo(openChunk=True)
    curtime = pc.currentTime( query=True )
    sel = pc.ls(sl=True)
    
    if(len(sel) == 0):
        #get all from model
        ctrls = tkc.getKeyables(inkeySet, [inModel])
        sel = tkc.getNodes(ctrls)

    if len(sel)>0:
        pc.cutKey(sel, time=(curtime,curtime))
    else:
        pc.error("No controls selected or key set don't exists ("+ inkeySet  +") !")
    pc.undoInfo(closeChunk=True)

    
def removeAnim(inModel, inkeySet="All"):
    pc.undoInfo(openChunk=True)
    sel = pc.ls(sl=True)
    
    if(len(sel) == 0):
        #get all from model
        ctrls = tkc.getKeyables(inkeySet, [inModel])
        sel = tkc.getNodes(ctrls)

    if len(sel)>0:
        pc.cutKey(sel)
    else:
        pc.error("No controls selected or key set don't exists ("+ inkeySet  +") !")
    pc.undoInfo(closeChunk=True)

def findIndices(inAxis):
    for i in range(len(CONST_TRANSMARKER)):
        for j in range(len(CONST_TRANSMARKER[i])):
            if CONST_TRANSMARKER[i][j] == inAxis:
                return [i,j]

    return None

channelsIndices =   {
                        "tx":(0, 0), "ty":(0, 1), "tz":(0, 2),
                        "rx":(1, 0), "ry":(1, 1), "rz":(1, 2),
                        "sx":(2, 0), "sy":(2, 1), "sz":(2, 2)
                    }

mirrorBaseRule = ("tx", "ry", "rz")
alternativeRule = ("tz", "rx", "ry")

overrideMirrorTrue =    (
                            "Foot_Reverse_0",
                            "Foot_Reverse_1",
                            "Foot_Reverse_2",
                            "Fore_FOOT_Reverse_0_Bone_Ctrl",
                            "Fore_FOOT_Reverse_1_Bone_Ctrl",
                            "Fore_FOOT_Reverse_2_Bone_Ctrl",
                            "Rear_FOOT_Reverse_0_Bone_Ctrl",
                            "Rear_FOOT_Reverse_1_Bone_Ctrl",
                            "Rear_FOOT_Reverse_2_Bone_Ctrl",
                            "Fore_FOOT_FK_0_Bone_Ctrl",
                            "Rear_FOOT_FK_0_Bone_Ctrl"
                        )
mirrorRules =   {
                    "UpperLip_Point1_Ctrl_Control":alternativeRule,
                    "UpperLip_Point2_Ctrl_Control":alternativeRule,
                    "LowerLip_Point1_Ctrl_Control":alternativeRule,
                    "LowerLip_Point2_Ctrl_Control":alternativeRule,
                    "UpperLip_1_Ctrl":alternativeRule,
                    "UpperLip_2_Ctrl":alternativeRule,
                    "LowerLip_1_Ctrl":alternativeRule,
                    "LowerLip_2_Ctrl":alternativeRule,
                    "Levator_0_Ctrl":alternativeRule,
                    "Levator_1_Ctrl":alternativeRule,
                    "Levator_2_Ctrl":alternativeRule,
                    "Levator_3_Ctrl":alternativeRule,
                    "Zygo_0_Ctrl":alternativeRule,
                    "Zygo_1_Ctrl":alternativeRule,
                    "Zygo_2_Ctrl":alternativeRule,
                    "Zygo_3_Ctrl":alternativeRule,
                    "Riso_0_Ctrl":alternativeRule,
                    "Riso_1_Ctrl":alternativeRule,
                    "Riso_2_Ctrl":alternativeRule,
                    "Riso_3_Ctrl":alternativeRule,
                    "Depressor_0_Ctrl":alternativeRule,
                    "Depressor_1_Ctrl":alternativeRule,
                    "Depressor_2_Ctrl":alternativeRule,
                    "Depressor_3_Ctrl":alternativeRule,

                    "Eyebrow_Point0_Ctrl_Control":alternativeRule,
                    "Eyebrow_Point1_Ctrl_Control":alternativeRule,
                    "Eyebrow_Point2_Ctrl_Control":alternativeRule,

                    "UpperEye_0_Ctrl":alternativeRule,
                    "UpperEye_1_Ctrl":alternativeRule,
                    "UpperEye_2_Ctrl":alternativeRule,
                    "UpperEye_3_Ctrl":alternativeRule,
                    "LowerEye_0_Ctrl":alternativeRule,
                    "LowerEye_1_Ctrl":alternativeRule,
                    "LowerEye_2_Ctrl":alternativeRule,
                    "LowerEye_3_Ctrl":alternativeRule,

                    "Leg_Knee":alternativeRule,
                    "Leg_Round_0":alternativeRule,
                    "Leg_Round_1":alternativeRule,
                    "Leg_Round_Root_Tangent":(),
                    "Leg_Round_Root":alternativeRule,
                    "Leg_Round_Eff_Tangent":(),
                    "Leg_Round_Eff":alternativeRule,

                    "Foot_Reverse_0":alternativeRule,
                    "Foot_Reverse_1":alternativeRule,
                    "Foot_Reverse_2":alternativeRule,
                    "Fore_FOOT_Reverse_0_Bone_Ctrl":alternativeRule,
                    "Fore_FOOT_Reverse_1_Bone_Ctrl":alternativeRule,
                    "Fore_FOOT_Reverse_2_Bone_Ctrl":alternativeRule,
                    "Rear_FOOT_Reverse_0_Bone_Ctrl":alternativeRule,
                    "Rear_FOOT_Reverse_1_Bone_Ctrl":alternativeRule,
                    "Rear_FOOT_Reverse_2_Bone_Ctrl":alternativeRule,
                    
                    "Leg_Extra_0":("ty", "rz", "rx"),#check
                    "Leg_Extra_1":("ty", "rz", "rx"),#check
                    "Leg_Extra_2":("ty", "rz", "rx"),#check
                    "Leg_Extra_3":("ty", "rz", "rx"),#check
                    "Leg_Extra_6":("ty", "rz", "rx"),#check
                    "Leg_Extra_5":("ty", "rz", "rx"),#check
                    "Leg_Extra_4":("ty", "rz", "rx"),#check

                    "Arm_Elbow":alternativeRule,
                    "Arm_Round_0":alternativeRule,
                    "Arm_Round_1":alternativeRule,
                    "Arm_Round_Root":alternativeRule,
                    "Arm_Round_Root_Tangent":(),
                    "Arm_Round_Eff_Tangent":(),
                    "Arm_Round_Eff":alternativeRule,
                    
                    "Arm_Extra_0":alternativeRule,#check
                    "Arm_Extra_1":alternativeRule,#check
                    "Arm_Extra_2":alternativeRule,#check
                    "Arm_Extra_3":alternativeRule,#check
                    "Arm_Extra_6":alternativeRule,#check
                    "Arm_Extra_5":alternativeRule,#check
                    "Arm_Extra_4":alternativeRule,#check

                    "Shoulder_Bone_Ctrl":alternativeRule,
                    "Pelvis_Bone_Ctrl":alternativeRule,

                    "Wing_Spring_1_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_1_1_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_2_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_2_1_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_3_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_3_1_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_4_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_4_1_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_5_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_5_1_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_6_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_6_1_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_7_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_7_1_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_8_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_8_1_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_9_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_9_1_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_10_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_10_1_Bone_Ctrl":alternativeRule,
                    "Wing_Spring_7_2_Bone_Ctrl":alternativeRule,

                    "Tail_2_Bone_Ctrl":alternativeRule,
                    "Tail_3_Bone_Ctrl":alternativeRule,

                    "Fore_FOOT_FK_0_Bone_Ctrl":alternativeRule,
                    "Rear_FOOT_FK_0_Bone_Ctrl":alternativeRule,
                    
                    "Collar_0_1_Bone_Ctrl":alternativeRule,
                    "Collar_0_2_Bone_Ctrl":alternativeRule,
                    "Collar_1_0_Bone_Ctrl":alternativeRule,
                    "Collar_1_2_Bone_Ctrl":alternativeRule,
                    "Collar_3_1_Bone_Ctrl":alternativeRule,
                    "Collar_3_2_Bone_Ctrl":alternativeRule,

                    "Internal_Wing_1_Ctrl":alternativeRule,
                    "Internal_Wing_2_Ctrl":alternativeRule,
                    "External_Wing_1_Ctrl":alternativeRule,
                    "External_Wing_2_Ctrl":alternativeRule
                }

#2016 Overrides (twisted Arm roundings)
if pc.versions.current() > 201600:
    mirrorRules["Arm_Elbow"] = ("ty", "rz", "rx")
    mirrorRules["Arm_Round_0"] = ("ty", "rz", "rx")
    mirrorRules["Arm_Round_1"] = ("ty", "rz", "rx")
    mirrorRules["Arm_Round_Root"] = ("ty", "rz", "rx")
    mirrorRules["Arm_Round_Root_Tangent"] = ("ty", "rz", "rx")
    mirrorRules["Arm_Round_Eff_Tangent"] = ()
    mirrorRules["Arm_Round_Eff"] = ("ty", "rz", "rx")
    
    mirrorRules["Leg_Round_Root_Tangent"] = alternativeRule#check
    
    mirrorRules["Eye"] = ("ty", "rx", "rz")#check
    
    #"HandRig" fingers (is not directly Mirror True but it's still hierarchically True) (names matche wf conventions)
    mirrorRules["Thumb_03"] = ()
    mirrorRules["Thumb_02"] = ()
    mirrorRules["Thumb_01"] = ()
    mirrorRules["Index_03"] = ()
    mirrorRules["Index_02"] = ()
    mirrorRules["Index_01"] = ()
    mirrorRules["Middle_03"] = ()
    mirrorRules["Middle_02"] = ()
    mirrorRules["Middle_01"] = ()
    mirrorRules["Ring_02"] = ()
    mirrorRules["Ring_03"] = ()
    mirrorRules["Ring_01"] = ()
    mirrorRules["Pinky_01"] = ()
    mirrorRules["Pinky_02"] = ()
    mirrorRules["Pinky_03"] = ()
    mirrorRules["Index_Mtc"] = ()
    mirrorRules["Middle_Mtc"] = ()
    mirrorRules["Ring_Mtc"] = ()
    mirrorRules["Pinky_Mtc"] = ()

translatedRules = None

def getRule(inName, i_inTrans, i_inChannel):
    global translatedRules

    if translatedRules == None:
        if not "mirrorBaseRule" in mirrorRules:
            mirrorRules["mirrorBaseRule"] = mirrorBaseRule

        translatedRules = {}

        for rulesKey in mirrorRules.keys():
            translatedRules[rulesKey] = [[False, False, False], [False, False, False], [False, False, False]]

            rules = mirrorRules[rulesKey]

            for ruleKey in rules:
                i_j = channelsIndices[ruleKey]
                translatedRules[rulesKey][i_j[0]][i_j[1]] = True

    if inName in translatedRules:
        return translatedRules[inName][i_inTrans][i_inChannel]

    return translatedRules["mirrorBaseRule"][i_inTrans][i_inChannel]

def getMirrorAttr(inObjName):
    obj = pc.PyNode(inObjName)

    mirror = False

    if pc.objExists(inObjName + "_OSCAR_Attributes.Mirror"):
        mirror = pc.getAttr(inObjName + "_OSCAR_Attributes.Mirror") == 1
        parents = obj.getAllParents()

        for parent in parents:
            if pc.objExists(parent.name() + "_OSCAR_Attributes.Mirror"):
                if(pc.getAttr(parent.name() + "_OSCAR_Attributes.Mirror") == 1):
                    mirror = not mirror

    return mirror

def mirrorPose(inModel, symmetry=False, inAttrs=True):
    pc.undoInfo(openChunk=True)
    keySet = "All"
    sel = pc.ls(sl=True)
    
    if(len(sel) == 0):
        #get all from model
        ctrls = tkc.getKeyables(keySet, [inModel], True)
    else:
        ctrls = tkc.orderControls(sel)

    oppositeObjs=[]
    if len(ctrls)>0:
        leftregexes = []
        rightregexes = []

        #pre-compile regexes
        for prefixIndex in range(len(CONST_LEFTPREFIXES)):
            leftPrefix = CONST_LEFTPREFIXES[prefixIndex]
            rightPrefix = CONST_RIGHTPREFIXES[prefixIndex]

            leftregexes.append([re.compile(leftPrefix), rightPrefix.replace("^", "")])
            rightregexes.append([re.compile(rightPrefix), leftPrefix.replace("^", "")])

        controlsDic = {}

        for control in ctrls:
            oppositeName = control.name()
            regexes = []
            for regexRule in leftregexes:
                if regexRule[0].search(oppositeName):
                    regexes = leftregexes
                    break
            if len(regexes) == 0:
                for regexRule in rightregexes:
                    if regexRule[0].search(oppositeName):
                        regexes = rightregexes
                        break

            for regexRule in regexes:
                oppositeName = regexRule[0].sub(regexRule[1], oppositeName)

            t = control.getTranslation(space="object")
            r = ozms.getPymelRotation(control, space="object")
            s = control.getScale()

            transform = [t,r,s]

            if oppositeName != control.name():
                if pc.objExists(oppositeName):
                    oppositeObjs.append(pc.PyNode(oppositeName))

                    rightName = oppositeName if "Right_" in oppositeName else control.name()
                    if pc.objExists(rightName + "_OSCAR_Attributes.Mirror"):
                        lazyName = oppositeName.split(':')[-1].replace("Left_", "").replace("Right_", "")
                        if not getMirrorAttr(rightName) or lazyName in overrideMirrorTrue:
                            for transIndex in range(3):
                                trans = transform[transIndex]
                                for channelIndex in range(3):
                                    if getRule(lazyName, transIndex, channelIndex):
                                        transform[transIndex][channelIndex] = -transform[transIndex][channelIndex]
                    if symmetry:
                        t[2] = -t[2]
                        r[2] = -r[2]

                    controlsDic[oppositeName] = {"Name":oppositeName,"Pos":t,"Rot":r,"Scl":s, "Attrs":{}}
                    if inAttrs:
                        attrs = tkc.getParameters(control, keyableOnly=True)
                        for attr in attrs:
                            controlsDic[oppositeName]["Attrs"][attr] = pc.getAttr(control.name()+"."+attr)
            elif not symmetry and pc.objExists(oppositeName + "_OSCAR_Attributes.inversed_Axes"):
                oppositeObjs.append(control)
                trans = [t, r, s]
                inversedAxis = pc.getAttr(oppositeName + "_OSCAR_Attributes.inversed_Axes").split(",")

                for axis in inversedAxis:
                    indices = findIndices(axis)
                    trans[indices[0]][indices[1]] = -trans[indices[0]][indices[1]]

                controlsDic[control.name()] = {"Name":oppositeName,"Pos":trans[0],"Rot":trans[1],"Scl":trans[2], "Attrs":{}}

        for control in oppositeObjs:
            data = controlsDic[control.name()]
            tkc.setTRS(control, data["Pos"], data["Rot"], data["Scl"])
            for attrName, value in data["Attrs"].iteritems():
                if pc.attributeQuery(attrName,node=control ,exists=True ):
                    pc.setAttr(control.name()+"."+attrName, value)
                else:
                    pc.warning("Attribute {0} cannot be found".format(control.name()+"."+attrName))
    else:
        pc.error("No controls selected or key set don't exists ("+ keySet  +") !")

    pc.undoInfo(closeChunk=True)

def setCtrlVisibility(inModel, ctrlLevel, value):
    pc.undoInfo(openChunk=True)

    baseParamName = "Controls"
    if ctrlLevel > 0:
        baseParamName = baseParamName + "_" + str(ctrlLevel - 1)

    charName = tkc.getCharacterName(inModel)

    if charName == "":
        pc.error("Cannot get Character Name from namespace (%s)" % inModel)
        return

    paramName = inModel + ":" + charName + "_TK_CtrlsDic.GLOBAL_VisHolder"
    paramName = tkc.stripMockNamespace(paramName)
    if pc.objExists(paramName):
        rawName = pc.getAttr(paramName)
        visParamName = tkc.stripMockNamespace(inModel + ":" + rawName + "." + baseParamName)
        if pc.objExists(visParamName):
            pc.setAttr(visParamName, value)
    else:
        #Try with GlobalSRT
        paramName = inModel + ":" + charName + "_TK_CtrlsDic.GlobalSRT_Main_Ctrl"
        paramName = tkc.stripMockNamespace(paramName)
        if pc.objExists(paramName):
            rawName = pc.getAttr(paramName)
            visParamName = tkc.stripMockNamespace(inModel + ":" + rawName + ".Control_Level")
            visGlobalParamName = tkc.stripMockNamespace(inModel + ":" + rawName + ".Controls")
            if pc.objExists(visParamName):
                combinedValue =(ctrlLevel - 1) if value else (ctrlLevel-2)
                if combinedValue < 0:
                    pc.setAttr(visGlobalParamName, 0 if not value else 1)
                else:
                    pc.setAttr(visParamName, max(0,combinedValue))
                    pc.setAttr(visGlobalParamName, 1)
            else:
                idx = 0
                prefix = "Controls_"
                visParamName = tkc.stripMockNamespace(inModel + ":" + rawName + "." + prefix + str(idx))
                while pc.objExists(visParamName):
                    if value:
                        pc.setAttr(visParamName, 1 if idx <= ctrlLevel else 0)
                    else:
                        pc.setAttr(visParamName, 1 if idx + 1 <= ctrlLevel else 0)
                    idx += 1
                    visParamName = tkc.stripMockNamespace(inModel + ":" + rawName + "." + prefix + str(idx))
        else:
            pc.error("Cannot get 'GlobalSRT_Main_Ctrl' name from dictionary (%s)" % paramName)
            return

    pc.undoInfo(closeChunk=True)

ATTRS = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
#Use as you would use a "setAttr" ( setSpace("wf_ch_bookie_rgh_1:Left_Shoulder.Orient_Space", 4) )
#If the controller is not the one the parentSpace attribute is published on (of if there are multiple objects to manage, use "alternateControls" as a PyNode list
def setSpace(inAttr, inValue, alternateControls=None, curFrame=None, forceSetKeys=False):
    tkc.storeSelection()

    if curFrame == None:
        curFrame = pc.currentTime(query=True)
    else:
        pc.currentTime(curFrame)
    
    pmAttr = pc.PyNode(inAttr) if isinstance(inAttr, basestring) else inAttr
    oldValue = pmAttr.get()

    if oldValue == inValue:
        pc.warning("Parent/Orientspace is already at the given value ({0}) !".format(inValue))
        return

    pmNodes = [pmAttr.node()] if alternateControls == None else alternateControls
    setKeys = forceSetKeys or len(pc.listConnections(inAttr, destination=False)) > 0

    for pmNode in pmNodes:
        nodeAttrs = []
        for attr in ATTRS:
            if pmNode.attr(attr).isSettable():
                nodeAttrs.append(attr)
                if not setKeys and len(pc.listConnections(pmNode.attr(attr), destination=False)) > 0:
                    setKeys = True

        pc.setAttr(pmAttr, oldValue)

        matchGroup = pc.group(empty=True, parent=pmNode.getParent())
        matchGroup.rotateOrder.set(pmNode.rotateOrder.get())
        matchGroup.t.set(pmNode.t.get())
        matchGroup.r.set(pmNode.r.get())
        matchGroup.s.set(pmNode.s.get())
        
        try:
            pc.parent(matchGroup, world=True)
            
            if setKeys:
                pc.setKeyframe(pmAttr, t=curFrame-1)
                pc.setKeyframe(pmAttr, v=inValue, t=curFrame)

            pc.setAttr(pmAttr, inValue)

            pc.parent(matchGroup, pmNode.getParent())

            for nodeAttr in nodeAttrs:
                if setKeys:
                    pc.setKeyframe(pmNode.attr(nodeAttr), v=pmNode.attr(nodeAttr).get(t=curFrame-1), t=curFrame-1)
                    pc.setKeyframe(pmNode.attr(nodeAttr), v=matchGroup.attr(nodeAttr).get(), t=curFrame)

                pmNode.attr(nodeAttr).set(matchGroup.attr(nodeAttr).get())

        except Exception as e:
            pc.warning(str(e))

        pc.delete(matchGroup)

        tkc.loadSelection()

def toggleIKFK(inIKBone0,inIKBone1,inIKBone0Scale,inIKBone1Scale,inIKEff,inIKControl,inUpV,inFKBone0,inFKBone1,inFKEff,inBlendParam,inChilds,inAutoKey,inAlternateFKEff=None,inResetBefore=None,inResetAfter=None):
    pc.undoInfo(openChunk=True)
    iCurrentBlendValue = pc.getAttr(inBlendParam)
    iAutoKey           = inAutoKey or pc.autoKeyframe(query=True, state=True)
    if(iCurrentBlendValue == 0.5):
        pc.error("Blend parameter is exactly between IK and FK, cannot proceed !")

    if(iCurrentBlendValue > 0.5):
        switchFkToIk(inFKBone0,inFKBone1,inFKEff,inIKBone0,inIKBone1,inIKBone0Scale,inIKBone1Scale,inIKControl,inUpV,inBlendParam,0,inChilds,iAutoKey,inAlternateFKEff,inResetBefore,inResetAfter)
    if(iCurrentBlendValue < 0.5):
        switchIkToFk(inFKBone0,inFKBone1,inFKEff,inIKBone0,inIKBone1,inIKEff,inBlendParam,1,inChilds,iAutoKey,inResetBefore,inResetAfter)
    pc.undoInfo(closeChunk=True)
    return True #BAD TODO: Verfier le comportement de l'IK et de l'effector_FK

def switchFkToIk(inFKBone0,inFKBone1,inFKEff,inIKBone0,inIKBone1,inIKBone0Scale,inIKBone1Scale,inIKControl,inUpV,inBlendParam,inValue,inChilds,inAutoKey,inAlternateFKEff=None,inResetBefore=None,inResetAfter=None):
    tkc.storeSelection()

    vRootEff      = MVector(0, 0, 0)
    vUpvNewPos    = MVector(0, 0, 0)
    FKBone0Length = MVector(0, 0, 0)
    FKBone1Length = MVector(0, 0, 0)
    vUpVLength    = MVector(0, 0, 0)
    newTransform  = MVector(0, 0, 0)
    iEpsilon      = 0.00000001
    aChildsTrans  = []

    iKBone0Scale  = pc.getAttr(inIKBone0 + ".Info_Scale")
    iKBone1Scale  = pc.getAttr(inIKBone1 + ".Info_Scale")

    #Check if FKBone1 have bad rotations
    localRotY = pc.getAttr(inFKBone1 + ".ry")
    if localRotY < 0 - iEpsilon  or localRotY > 0 + iEpsilon:
        if pc.confirmDialog( title='Confirm', message="You have y rotation on " + inFKBone1 + "\nThe switch will note be clean because of these rotations\nDo you want to continue?", button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' ) == 'No':
            return False

    if inResetBefore != None:
        for resetObj in inResetBefore:
            if "." in resetObj:
                if pc.getAttr(resetObj, settable=True):
                    default = None
                    if resetObj.endswith(".tx") or resetObj.endswith(".ty") or resetObj.endswith(".tz") or resetObj.endswith(".rx") or resetObj.endswith(".ry") or resetObj.endswith(".rz"):
                        default = 0.0
                    elif resetObj.endswith(".sx") or resetObj.endswith(".sy") or resetObj.endswith(".sz"):
                        default = 1.0
                    else:
                        default = pc.addAttr(resetObj, query=True, defaultValue=True)

                    if default != None: 
                        pc.setAttr(resetObj, default)
            else:
                tkc.resetTRS(pc.PyNode(resetObj))

    #Store Childs transforms
    for i in range(len(inChilds)):
        child = inChilds[i]
        if isinstance(child, tuple):
            child = child[1]
        if child == None:
            aChildsTrans.append(None)
        else:
            aChildsTrans.append(pc.xform(child, query=True, worldSpace=True, matrix=True ))

    #Calculate upV Transform
    oFKEff = pc.PyNode(inFKEff)
    oFKBone0 = pc.PyNode(inFKBone0)
    oFKBone1 = pc.PyNode(inFKBone1)

    upvMatcher = pc.group(empty=True, world=True, name="tmpUpvMatcher")
    tkc.createResPlane(upvMatcher, oFKBone0, oFKBone1, oFKEff if inAlternateFKEff == None else pc.PyNode(inAlternateFKEff))
    vUpvNewPos = upvMatcher.getTranslation(space="world")
    pc.delete(upvMatcher)

    #Set Transforms
    pc.setAttr(inIKBone0Scale, pc.getAttr(inFKBone0 + ".sx"))
    pc.setAttr(inIKBone1Scale, pc.getAttr(inFKBone1 + ".sx"))

    oIKControl = pc.PyNode(inIKControl)
    tkc.matchTRS(oIKControl, oFKEff, True, True, False)

    oUpV = pc.PyNode(inUpV)
    oUpV.setTranslation([vUpvNewPos.x, vUpvNewPos.y, vUpvNewPos.z], space="world")
    tkc.matchTRS(oUpV, oFKBone1, False, True, False)

    pc.setAttr(inBlendParam, inValue)

    #Set Childs transform
    for i in range(len(inChilds)):
        child = inChilds[i]
        if isinstance(child, tuple):
            child = child[0]
        if child != None:
            pc.xform( child, worldSpace=True, matrix=aChildsTrans[i] )

    if inResetAfter != None:
        for resetObj in inResetAfter:
            if "." in resetObj:
                if pc.getAttr(resetObj, settable=True):
                    default = None
                    if resetObj.endswith(".tx") or resetObj.endswith(".ty") or resetObj.endswith(".tz") or resetObj.endswith(".rx") or resetObj.endswith(".ry") or resetObj.endswith(".rz"):
                        default = 0.0
                    elif resetObj.endswith(".sx") or resetObj.endswith(".sy") or resetObj.endswith(".sz"):
                        default = 1.0
                    else:
                        default = pc.addAttr(resetObj, query=True, defaultValue=True)

                    if default != None: 
                        pc.setAttr(resetObj, default)
            else:
                tkc.resetTRS(pc.PyNode(resetObj))

    tkc.loadSelection()

    if not inAutoKey:
        return True

    #SaveKey    
    '''
    var cObjsToKey = new ActiveXObject( "XSI.Collection" );
        cObjsToKey.Add(inIKControl);
        cObjsToKey.Add(inUpV);
        cObjsToKey.Add(inBlendParam);
        cObjsToKey.AddItems(inChilds);
        cObjsToKey.AddItems([inIKBone0Scale,inIKBone1Scale]);
    SaveKeyOnLocal(cObjsToKey);
    '''

    return True;

def switchIkToFk(inFKBone0,inFKBone1,inFKEff,inIKBone0,inIKBone1,inIKEff,inBlendParam,inValue,inChilds,inAutoKey,inResetBefore=None,inResetAfter=None):
    vBone0 = MVector(0, 0, 0)
    vBone1 = MVector(0, 0, 0)
    aChildsTrans       = []
    bone0NewTransform  = []
    bone1NewTransform  = []
    iKBone0_Init       = pc.getAttr(inIKBone0 + ".Info_Init")
    iKBone1_Init       = pc.getAttr(inIKBone1 + ".Info_Init")

    oIKBone0 = pc.PyNode(inIKBone0)
    oIKBone1 = pc.PyNode(inIKBone1)
    oIKEff = pc.PyNode(inIKEff)

    oFKBone0 = pc.PyNode(inFKBone0)
    oFKBone1 = pc.PyNode(inFKBone1)

    oIKBone0Trans = oIKBone0.getTranslation(space="world")
    oIKBone0MTrans = MVector(oIKBone0Trans[0], oIKBone0Trans[1], oIKBone0Trans[2])
    
    oIKBone1Trans = oIKBone1.getTranslation(space="world")
    oIKBone1MTrans = MVector(oIKBone1Trans[0], oIKBone1Trans[1], oIKBone1Trans[2])

    oIKEffTrans = oIKEff.getTranslation(space="world")
    oIKEffMTrans = MVector(oIKEffTrans[0], oIKEffTrans[1], oIKEffTrans[2])
    
    #Calculate Bone length

    vBone0 = oIKBone0MTrans - oIKBone1MTrans
    vBone1 = oIKBone1MTrans - oIKEffMTrans

    #Store Childs transforms
    for i in range(len(inChilds)):
        child = inChilds[i]
        if isinstance(child, tuple):
            child = child[-2]
        if child == None:
            aChildsTrans.append(None)
        else:
            aChildsTrans.append(pc.xform(child, query=True, worldSpace=True, matrix=True ))

    pc.setAttr(inBlendParam, inValue)
    if pc.getAttr(inFKBone0 + ".sx") < 0:
        pc.setAttr(inFKBone0 + ".sx", vBone0.length() / iKBone0_Init)
        pc.setAttr(inFKBone0 + ".sy", vBone0.length() / iKBone0_Init)
        pc.setAttr(inFKBone0 + ".sz", vBone0.length() / iKBone0_Init)

        oIKBone0Rot = ozms.getPymelRotation(oIKBone0, space="object")
        pc.setAttr(inFKBone0 + ".rx", -oIKBone0Rot[0])
        pc.setAttr(inFKBone0 + ".ry", -IKBone0Rot[1])
        pc.setAttr(inFKBone0 + ".rz", IKBone0Rot[2])

        pc.setAttr(inFKBone0 + ".tx", 0)
        pc.setAttr(inFKBone0 + ".ty", 0)
        pc.setAttr(inFKBone0 + ".tz", 0)

        pc.setAttr(inFKBone1 + ".sx", vBone1.length() / iKBone1_Init)
        pc.setAttr(inFKBone1 + ".sy", vBone1.length() / iKBone1_Init)
        pc.setAttr(inFKBone1 + ".sz", vBone1.length() / iKBone1_Init)

        oIKBone1Rot = ozms.getPymelRotation(oIKBone1, space="object")
        pc.setAttr(inFKBone1 + ".rx", -oIKBone1Rot[0])
        pc.setAttr(inFKBone1 + ".ry", 0)
        pc.setAttr(inFKBone1 + ".rz", IKBone1Rot[2])

        pc.setAttr(inFKBone1 + ".tx", 0)
        pc.setAttr(inFKBone1 + ".ty", 0)
        pc.setAttr(inFKBone1 + ".tz", 0)
    else:
        #Set Transforms
        tkc.matchTRS(oFKBone0, oIKBone0, True, True, False)
        pc.setAttr(inFKBone0 + ".sx", vBone0.length() / iKBone0_Init)
        pc.setAttr(inFKBone0 + ".sy", vBone0.length() / iKBone0_Init)
        pc.setAttr(inFKBone0 + ".sz", vBone0.length() / iKBone0_Init)

        tkc.matchTRS(oFKBone1, oIKBone1, True, True, False)

        pc.setAttr(inFKBone1 + ".sx", vBone1.length() / iKBone1_Init)
        pc.setAttr(inFKBone1 + ".sy", vBone1.length() / iKBone1_Init)
        pc.setAttr(inFKBone1 + ".sz", vBone1.length() / iKBone1_Init)
        pc.setAttr(inFKBone1 + ".ry", 0)

    #Set Childs transform
    for i in range(len(inChilds)):
        child = inChilds[i]
        if isinstance(child, tuple):
            child = child[-1]
        if child != None:
            pc.xform( child, worldSpace=True, matrix=aChildsTrans[i] )

    """ DOABLE, but we will have to differenciate FK => IK and IK => FK...
    if inReset != None:
        for resetObj in inReset:
            if "." in resetObj:
                if pc.getAttr(resetObj, settable=True):
                    default = None
                    if resetObj.endswith(".tx") or resetObj.endswith(".ty") or resetObj.endswith(".tz") or resetObj.endswith(".rx") or resetObj.endswith(".ry") or resetObj.endswith(".rz"):
                        default = 0.0
                    elif resetObj.endswith(".sx") or resetObj.endswith(".sy") or resetObj.endswith(".sz"):
                        default = 1.0
                    else:
                        default = pc.addAttr(resetObj, query=True, defaultValue=True)

                    if default != None:
                        pc.setAttr(resetObj, default)
            else:
                tkc.resetTRS(pc.PyNode(resetObj))
    """

    if not inAutoKey:
        return True

    #SaveKey
    '''
    var cObjsToKey = new ActiveXObject( "XSI.Collection" );
        cObjsToKey.Add(inFKBone0);
        cObjsToKey.Add(inFKBone1);
        cObjsToKey.Add(inBlendParam);
        cObjsToKey.AddItems(inChilds);      
    SaveKeyOnLocal(cObjsToKey);
    '''


"""
SelfModelName = "chr_straightGaze_default_rig_v003"

ns = SelfModelName if len(SelfModelName) == 0 else SelfModelName + ":"

IK_To_FK = [
    {"Right_Arm_FK_01":
        {"matchR":"Right_ARM_IK_Bone_0",
         "sx":"(TK_Right_ARM_IK_Root_SetupParameters.Right_ARM_IK_Bone0_length/TK_Right_ARM_IK_Root_SetupParameters.Right_ARM_IK_Bone0_Init)*TK_Right_ARM_IK_Root_SetupParameters.Right_ARM_IK_Scale",
         "t":[0,0,0]}
    },
    {"Right_Arm_FK_02":
        {"matchR":"Right_ARM_IK_Bone_1",
         "sx":"(TK_Right_ARM_IK_Root_SetupParameters.Right_ARM_IK_Bone1_length/TK_Right_ARM_IK_Root_SetupParameters.Right_ARM_IK_Bone1_Init)*TK_Right_ARM_IK_Root_SetupParameters.Right_ARM_IK_Scale",
         "t":[0,0,0]}
    },
    {"Right_Hand_FK":
        {"match":"Right_ARM_IK_Stretch_FKREF"}
    },
    {"Right_Elbow":
        {"match":"Right_Elbow"}
    }
]

FK_To_IK = [
    {"Right_Arm_FK_02":
        {"check":("abs(Right_Arm_FK_02.rotateX) <= 0.002", "Right_Arm_FK_02 rotateX is not 0"),
         "check":("abs(Right_Arm_FK_02.rotateY) <= 0.002", "Right_Arm_FK_02 rotateY is not 0")}
    },
    {"Right_Arm_IK":
        {"match":"Right_Hand_FK_IKREF",
        "Bone0_Scale":"Right_Arm_FK_01.sx",
        "Bone1_Scale":"Right_Arm_FK_02.sx",
        "Roll":0,
        "StickJoint":0,
        "Stretch":1,
        "Squash":0}
    },
    {"Right_Arm_IK_upV":
        {"matchPV":("Right_Arm_FK_01", "Right_Arm_FK_02", "TK_Right_ARM_FK_Effector")}
    },
    {"Right_Elbow":
        {"match":"Right_Elbow"}
    }
]

#matchInPlace("Left_Arm_ParamHolder.IkFk", 0.0, FK_To_IK, ns)


toggleInPlace("Left_Arm_ParamHolder.IkFk", 0.0, IK_To_FK, 1.0, FK_To_IK, ns)

"""

def getWorldMat(inObj, inOffset=None):
    if not inOffset is None:
        grp = pc.group(empty=True, parent=inObj)
        grp.t.set(inOffset[0])
        grp.r.set(inOffset[1])
        grp.s.set(inOffset[2])

        mat = grp.worldMatrix.get()

        pc.delete(grp)

        return mat

    #Get "ref" world matrix as a starter for computation
    worldRefMat = inObj.worldMatrix.get()

    #Put the "ref" rotate pivot offset in world space
    refRp = inObj.rp.get()
    worldRefRpVec = refRp * worldRefMat

    #Add the "ref" rotate pivot to matrix
    worldRefMat.a30 += worldRefRpVec.x
    worldRefMat.a31 += worldRefRpVec.y
    worldRefMat.a32 += worldRefRpVec.z

    return worldRefMat

def setAttr(inObj, inValue):
    inObj.set(inValue)

def match(inObj, inValue):
    #Put the "target" rotate pivot offset in world space
    worldTargetMat = inObj.worldMatrix.get()

    targetRp = inObj.rp.get()
    worldTargetRp = targetRp * worldTargetMat

    targetSp = inObj.sp.get()

    #Add the "ref" rotate pivot and remove "target" rotate pivot to matrix
    inValue.a30 -= worldTargetRp[0]
    inValue.a31 -= worldTargetRp[1]
    inValue.a32 -= worldTargetRp[2]

    #Push matrix result in "target"
    pc.xform(inObj, worldSpace=True, matrix=inValue)
    #Reapply rotate pivot and scale pivot
    pc.xform(inObj, rp=targetRp, sp=targetSp, p=True)

def matchT(inObj, inValue):
    r = inObj.r.get()
    s = inObj.s.get()

    match(inObj, inValue)

    if inObj.r.isSettable():
        inObj.r.set(r)
    if inObj.s.isSettable():
        inObj.s.set(s)

def matchR(inObj, inValue):
    t = inObj.t.get()
    s = inObj.s.get()
    match(inObj, inValue)

    if inObj.t.isSettable():
        inObj.t.set(t)
    if inObj.s.isSettable():
        inObj.s.set(s)

def matchS(inObj, inValue):
    t = inObj.t.get()
    r = inObj.r.get()
    match(inObj, inValue)

    if inObj.t.isSettable():
        inObj.t.set(t)
    if inObj.r.isSettable():
        inObj.r.set(r)

def matchPV(inObj, inValue):
    topMat, middleMat, downMat = inValue

    topObj = pc.group(empty=True, world=True)
    match(topObj, topMat)
    middleObj = pc.group(empty=True, world=True)
    match(middleObj, middleMat)
    downObj = pc.group(empty=True, world=True)
    match(downObj, downMat)

    target = pc.group(empty=True, world=True)
    tkc.createResPlane(target, topObj, middleObj, downObj)

    match(inObj, getWorldMat(target))

    pc.delete([target, topObj, middleObj, downObj])

FUNCTIONS = {
    "setAttr"   :setAttr,
    "match"     :match,
    "matchT"    :matchT,
    "matchR"    :matchR,
    "matchS"    :matchS,
    "matchPV"   :matchPV,
}

def matchInPlace(inBlendAttrName, inBlendAttrValue, inMatchData, inNs=""):
    setAttrs = []
    
    confirmMessages = []

    #First calculate all attribute values that need to be set
    for matcher in inMatchData:
        for matchObj, matchSteps in matcher.iteritems():
            matchObj = inNs + matchObj

            #print "matchObj",matchObj
            for matchRule, matchRef in matchSteps.iteritems():
                #print " -matchRule",matchRule
                #print " -matchRef",matchRef
                
                if matchRule.startswith("check"):
                    if len(matchRef) != 2:
                        raise ValueError("Check function takes two arguments : expression to check and message !")
                    expr, message = matchRef
                    exprComponents = tkExpressions.Expr.getTerms(expr)
                    for exprComponent in exprComponents:
                        if "." in exprComponent:
                            #Check if this component is really an attribute name (may be a floating point number)
                            idx = exprComponent.index(".")
                            if not ( (idx == 0 or exprComponent[idx-1].isdigit()) and
                                (idx == len(exprComponent) + 1 or exprComponent[idx+1].isdigit())):
                                #print " -exprComponent",exprComponent
                                expr = expr.replace(exprComponent, str(pc.getAttr(inNs + exprComponent)))

                    rslt = eval(expr)
                    if not rslt:
                        confirmMessages.append(message)

                elif matchRule in FUNCTIONS:
                    #Match an object on another
                    if isinstance(matchRef, (list,tuple)):
                        matrices = []
                        for matchRefItem in matchRef:
                            offset = None

                            if "+" in matchRefItem:
                                matchRefItem, strOffset = matchRefItem.split("+")
                                offset = eval(strOffset.replace(":", ","))

                            matrices.append(getWorldMat(pc.PyNode(inNs + matchRefItem), offset))
                        setAttrs.append((matchRule, matchObj, matrices))
                    else:
                        offset = None

                        if "+" in matchRef:
                            matchRef, strOffset = matchRef.split("+")
                            offset = eval(strOffset.replace(":", ","))

                        setAttrs.append((matchRule, matchObj, getWorldMat(pc.PyNode(inNs + matchRef), offset)))
                else:
                    #Simple "setAttr"
                    attrName = "{0}.{1}".format(matchObj, matchRule)
                    if not pc.attributeQuery(matchRule, node=matchObj, exists=True):
                        raise ValueError("Given attribute '{0}' does not exists !".format(attrName))
                       
                    if isinstance(matchRef, basestring):
                        exprComponents = tkExpressions.Expr.getTerms(matchRef)
                        for exprComponent in exprComponents:
                            if "." in exprComponent:
                                #print " -exprComponent",exprComponent
                                #Check if this component is really an attribute name (may be a floating point number)
                                idx = exprComponent.index(".")
                                if not ( (idx == 0 or exprComponent[idx-1].isdigit()) and
                                    (idx == len(exprComponent) + 1 or exprComponent[idx+1].isdigit())):
                                    matchRef = matchRef.replace(exprComponent, str(pc.getAttr(inNs + exprComponent)))

                        #print " -MODIFIED matchRef",matchRef
                        matchRef = eval(matchRef)

                    setAttrs.append(("setAttr", attrName, matchRef))

        #print ""

    if len(confirmMessages) > 0:
        message = "Current state may be incompatible with a seamless switch:\n{0}\nDo you want to switch anyway ?".format("\n".join([" - {0}".format(m) for m in confirmMessages]))
        if "Yes" != pc.confirmDialog( title='Confirm', message=message, button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' ):
            pc.warning("Switch cancelled !")
            return

    pc.undoInfo(openChunk=True)
    
    #Set the value of the blend attribute
    pc.PyNode(inNs + inBlendAttrName).set(inBlendAttrValue)

    #Set the attributes based on values calculated in the first pass
    for setter in setAttrs:
        func, item, value = setter
        item = tkc.getNode(item)

        if func in FUNCTIONS:
            FUNCTIONS[func](item, value)
        else:
            pc.warning("Set function '{0}' is not implemented ({1}). Possible values are : {1}.".format(func, setAttr, ",".join(FUNCTIONS.keys())))
    
    pc.undoInfo(closeChunk=True)

def toggleInPlace(inBlendAttrName, inState1Value, inState1Data, inState2Value, inState2Data, inNs=""):
    toggleValue = (inState2Value - inState1Value) / 2.0 
    currentValue = pc.getAttr(inNs + inBlendAttrName)

    if currentValue == toggleValue:
        pc.warning("Blend parameter is exactly between the two states, cannot proceed !")
        return

    if currentValue < toggleValue:
        #State1 to State2
        matchInPlace(inBlendAttrName, inState2Value, inState1Data, inNs)
    else:
        #State2 to State1
        matchInPlace(inBlendAttrName, inState1Value, inState2Data, inNs)

def toggleDeformers(*args):
    sel = pc.selected()
    ns = ""

    basePattern = "*.Deformers"
    pattern = None

    if len(sel) > 0:
        ns = sel[0].namespace()
        pattern = [ns+basePattern]
    else:
        pattern = ["*:"+basePattern,basePattern]

    rigStuffs = pc.ls(pattern)

    if len(rigStuffs) > 0:
        oldVal = rigStuffs[0].get()
        for rigStuff in rigStuffs:
            rigStuff.set(not oldVal)

def toggleMeshesOverrides(*args):
    import pymel.core as pc
    meshes = pc.ls(type="mesh")

    if len(meshes) > 0:
        oldVal = meshes[0].overrideEnabled.get()
        for mesh in meshes:
            mesh.overrideEnabled.set(not oldVal)

def toggleRigStuff(*args):
    sel = pc.selected()
    ns = ""

    basePattern = "*.RigStuff"
    pattern = None

    if len(sel) > 0:
        ns = sel[0].namespace()
        pattern = [ns+basePattern]
    else:
        pattern = ["*:"+basePattern,basePattern]

    rigStuffs = pc.ls(pattern)

    if len(rigStuffs) > 0:
        oldVal = rigStuffs[0].get()
        for rigStuff in rigStuffs:
            rigStuff.set(not oldVal)

def toggleSmooth(*args):
    ns = ""

    sel = pc.selected()

    meshes=[]
    if len(sel) > 0:
        ns = sel[0].namespace()
        meshes = pc.ls(ns + "*", type="mesh")
    else:
        meshes = pc.ls(type="mesh")
        
    if len(meshes) > 0:
        oldVal = pc.displaySmoothness(meshes[0], query=True, polygonObject=True)
        cmdName = "Smooth" if oldVal == [1L] else "Unsmooth"
        print pc.warning(cmdName)
        for mesh in meshes:
            if oldVal == [1L]:
                pc.displaySmoothness(mesh, polygonObject=3L)
            else:
                pc.displaySmoothness(mesh, polygonObject=1L)
import tkMayaCore as tkc
import tkRig
import pymel.core as pc
import tkMayaCore as tkc

DEFINITION = {
    "Head":15,
    "Hips":1,
    "LeftArm":9,
    "LeftFoot":4,
    "LeftForeArm":10,
    "LeftHand":11,
    "LeftHandIndex1":54,
    "LeftHandIndex2":55,
    "LeftHandIndex3":56,
    "LeftHandMiddle1":58,
    "LeftHandMiddle2":59,
    "LeftHandMiddle3":60,
    "LeftHandPinky1":66,
    "LeftHandPinky2":67,
    "LeftHandPinky3":68,
    "LeftHandRing1":62,
    "LeftHandRing2":63,
    "LeftHandRing3":64,
    "LeftHandThumb1":50,
    "LeftHandThumb2":51,
    "LeftHandThumb3":52,
    "LeftLeg":3,
    "LeftShoulder":18,
    "LeftToeBase":16,
    "LeftUpLeg":2,
    "Neck":20,
    "Reference":0,
    "RightArm":12,
    "RightFoot":7,
    "RightForeArm":13,
    "RightHand":14,
    "RightHandIndex1":78,
    "RightHandIndex2":79,
    "RightHandIndex3":80,
    "RightHandMiddle1":82,
    "RightHandMiddle2":83,
    "RightHandMiddle3":84,
    "RightHandPinky1":90,
    "RightHandPinky2":91,
    "RightHandPinky3":92,
    "RightHandRing1":86,
    "RightHandRing2":87,
    "RightHandRing3":88,
    "RightHandThumb1":74,
    "RightHandThumb2":75,
    "RightHandThumb3":76,
    "RightLeg":6,
    "RightShoulder":19,
    "RightToeBase":17,
    "RightUpLeg":5,
    "Spine":8,
    "Spine1":23,
    "Spine2":24,
    "Spine3":25,
}

def checkHIKExists(inCreate=True):
    exists = pc.control("hikCharacterControlsDock", query=True, exists=True) and pc.control("hikCharacterControlsDock", query=True, visible=True)
    if inCreate and not exists:
        pc.mel.eval("ToggleCharacterControls")
        pc.refresh()

def getCharacter(inJoint):
    ns = str(inJoint.namespace())
    
    chars = pc.listConnections(inJoint, source=True, destination=True, type="HIKCharacterNode")
    char = chars[0] if len(chars) > 0 else None

    if char is None:
        checkHIKExists()

        char = tkc.getNode(pc.mel.eval("hikCreateCharacter \""+ns+"SourceMocap"+"\""))
        
        for key,value in DEFINITION.items():
            if not pc.objExists(ns + key):
                pc.warning("Can't find mocap hook '{}'".format(ns + key))
            else:
                pc.mel.eval("setCharacterObject(\""+ ns + key +"\",\""+char.name()+"\","+str(value)+",0);")
        
        pc.mel.eval("hikToggleLockDefinition")
        
    return char

def getCharacters():
    checkHIKExists()
    menuItems = pc.optionMenuGrp("hikCharacterList", query=True, ils=True)
    return [pc.menuItem(item, query=True, label=True) for item in menuItems]

def getCurrentCharacter():
    checkHIKExists()
    return pc.optionMenuGrp("hikCharacterList", query=True, value=True)

def getSources():
    checkHIKExists()
    menuItems = pc.optionMenuGrp("hikSourceList", query=True, ils=True)
    return [pc.menuItem(item, query=True, label=True) for item in menuItems]

def getCurrentSource():
    checkHIKExists()
    return pc.optionMenuGrp("hikSourceList", query=True, value=True)

def setCurrentCharacter(inCharacter):
    try:
        checkHIKExists()

        pc.optionMenuGrp("hikCharacterList", edit=True, value=inCharacter)
        pc.mel.eval("hikUpdateCurrentCharacterFromUI();")
    except:
        pass
    
def setCurrentSource(inSource):
    try:
        if inSource in [None,"None"]:
            inSource = " None"

        checkHIKExists()

        pc.optionMenuGrp("hikSourceList",edit=True, value=inSource)
        pc.mel.eval("hikUpdateCurrentSourceFromUI();")
        pc.mel.eval("hikUpdateContextualUI();")
    except:
        pass

def setSource(inCharacter, inSource):
    checkHIKExists()

    pc.mel.eval('hikUpdateSourceList()')

    cmd = 'hikSetCharacterInput "{dst}" "{src}"'.format(
        dst=inCharacter,
        src=inSource
    )

    pc.mel.eval(cmd)

    pc.mel.eval('hikUpdateSkeletonUI()')
    pc.mel.eval('hikUpdateCurrentSkeleton()')
    pc.mel.eval('hikUpdateSourceList()')

PREFIX = "MayaHIK_"

def poleMatcher(*args):
    ns = args[0]

    topObjName = ns+args[2]
    middleObjName = ns+args[3]
    downObjName = ns+args[4]

    target = pc.group(empty=True, parent=topObjName, name=ns+args[1])

    tkc.createResPlane(target, pc.PyNode(topObjName), pc.PyNode(middleObjName), pc.PyNode(downObjName))

    return target.name()

def injectControlLayer(inCLRootName, inRigRootName, inTemplate, inAttrHolder=None, inAttrName="mocap", inConstrain=False):
    CHANNELS = ["tx", "ty", "tz", "rx", "ry", "rz"]
    constrainedAttrs = []

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

        if len(connectionData) < 2:#No binding required
            continue

        if len(connectionData) >= 5:#Custom relation (using a custom function and list of source markers)
            func = connectionData[4]
            if isinstance(func, str):
                func = eval(func)
            #print ("func", func)

            args = [clNS, connectionData[0]]
            args.extend(connectionData[5])
            #print ("args", args)

            #execute matcher function
            matcher = func(*args)
            #print ("matcher", matcher)

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
                    pc.addAttr(inAttrHolder, longName=inAttrName, keyable=True, defaultValue=0.0, minValue=0.0, maxValue=1.0, softMinValue=0.0, softMaxValue=1.0)
                globalAttr = "{0}.{1}".format(inAttrHolder, inAttrName)

            if inConstrain:
                templateNode = pc.PyNode(templateObj)
                rigNode = pc.PyNode(rigObj)
                
                for channel in CHANNELS:
                    channelNode = rigNode.attr(channel)
                    if channelNode.isLocked():
                        channelNode.setLocked(False)

                    constrainedAttrs.append(channelNode)

                tkc.constrain(rigNode, templateNode, "Pose", True)
            else:
                tkRig.createControlLayer(pc.PyNode(templateObj), pc.PyNode(rigObj), connectionData[1], connectionData[2], localOnly, inAttrHolder, inAttrName, globalAttr)

    return constrainedAttrs

                #ControllerName:(mocapMarkerName, considerPosition, considerRotation, localOnly matchingFunction, realMocapMarkers)
template = {    #Spine FK
                "Hips":(PREFIX + "Hips", True, True),
                "Spine_FK_2":(PREFIX + "Spine", True, True),
                "Spine_FK_3":(PREFIX + "Spine1", True, True),#RIG TO ADD
                "Spine_FK_4":(PREFIX + "Spine2", True, True),#RIG TO ADD
                "Spine_FK_5":(PREFIX + "Spine3", False, True),
                
                #Spine IK
                "Chest_IK":(PREFIX + "Spine3", True, True, False),
                "Spine_IK_StartHandle":(PREFIX + "Spine", True, True, False),
                "Spine_IK_Middle":(PREFIX + "Spine1", True, True, False),#RIG TO ADD
                "Spine_IK_EndHandle":(PREFIX + "Spine2", True, True, False),#RIG TO ADD

                #Neck FK
                "Neck_FK_1":(PREFIX + "Neck", True, True),#RIG TO ADD
                "Neck_FK_2":(PREFIX + "Neck1", True, True),#RIG TO ADD
                "Head_FK":(PREFIX + "Head", True, True),

                #Neck IK
                "Head_IK":(PREFIX + "Head", True, True, False),
                "Neck_IK_Start":(PREFIX + "Neck", True, True, False),#RIG TO ADD
                "Neck_IK_Middle":(PREFIX + "Neck1", True, True, False),#RIG TO ADD

                #Left Arm
                "Left_Shoulder":(PREFIX + "LeftShoulder", False, True),

                #Left Arm FK
                "Left_Arm_FK_1":(PREFIX + "LeftArm", False, True),
                "Left_Arm_FK_2":(PREFIX + "LeftForeArm", False, True),
                "Left_Hand":(PREFIX + "LeftHand", False, True),
                
                #Left Arm IK
                "Left_Arm_upV":(PREFIX + "LeftArmPoleVector", True, False, False, "poleMatcher", (PREFIX +"LeftArm", PREFIX +"LeftForeArm_poleHelper", PREFIX +"LeftHand")),
                "Left_Arm_IK":(PREFIX + "LeftHand", True, True, False),
                
                #Left Fingers
                "Left_Thumb_1":(PREFIX + "LeftHandThumb1", False, True),
                "Left_Thumb_2":(PREFIX + "LeftHandThumb2", False, True),
                "Left_Thumb_3":(PREFIX + "LeftHandThumb3", False, True),
                "TK_Left_HandRig_Thumb_Eff_Output":(PREFIX + "LeftHandThumb4",),

                "Left_Index_Mtc":(PREFIX + "LeftHandIndex0", False, True),
                "Left_Index_1":(PREFIX + "LeftHandIndex1", False, True),
                "Left_Index_2":(PREFIX + "LeftHandIndex2", False, True),
                "Left_Index_3":(PREFIX + "LeftHandIndex3", False, True),
                "TK_Left_HandRig_Index_Eff_Output":(PREFIX + "LeftHandIndex4",),
                
                "Left_Middle_Mtc":(PREFIX + "LeftHandMiddle0", False, True),
                "Left_Middle_1":(PREFIX + "LeftHandMiddle1", False, True),
                "Left_Middle_2":(PREFIX + "LeftHandMiddle2", False, True),
                "Left_Middle_3":(PREFIX + "LeftHandMiddle3", False, True),
                "TK_Left_HandRig_Middle_Eff_Output":(PREFIX + "LeftHandMiddle4",),
                
                "Left_Ring_Mtc":(PREFIX + "LeftHandRing0", False, True),
                "Left_Ring_1":(PREFIX + "LeftHandRing1", False, True),
                "Left_Ring_2":(PREFIX + "LeftHandRing2", False, True),
                "Left_Ring_3":(PREFIX + "LeftHandRing3", False, True),
                "TK_Left_HandRig_Ring_Eff_Output":(PREFIX + "LeftHandRing4",),
                
                "Left_Pinky_Mtc":(PREFIX + "LeftHandPinky0", False, True),
                "Left_Pinky_1":(PREFIX + "LeftHandPinky1", False, True),
                "Left_Pinky_2":(PREFIX + "LeftHandPinky2", False, True),
                "Left_Pinky_3":(PREFIX + "LeftHandPinky3", False, True),
                "TK_Left_HandRig_Pinky_Eff_Output":(PREFIX + "LeftHandPinky4",),
                
                #Left HandProp
                #"Left_HandProp":(PREFIX + "Lf_HandProp_MCP_0_JNT", True, True, False),

                #Left Leg IK
                "Left_Leg_upV":(PREFIX + "LeftLegPoleVector", True, False, False, "poleMatcher", (PREFIX +"LeftUpLeg", PREFIX +"LeftLeg_poleHelper", PREFIX +"LeftFoot")),
                "Left_Leg_IK":(PREFIX + "LeftFoot", True, True, False),
                "Left_IK_Tip":(PREFIX + "LeftToeBase", True, True),
                
                #Left Leg FK
                "Left_Leg_FK_1":(PREFIX + "LeftUpLeg", False, True),
                "Left_Leg_FK_2":(PREFIX + "LeftLeg", False, True),
                "Left_Foot_FK_1":(PREFIX + "LeftFoot", False, True),
                "Left_Foot_FK_2":(PREFIX + "LeftToeBase", False, True),
                
                #"Left_Tip":(PREFIX + "Lf_Foot_MCP_2_JNT",),

                #Right Arm
                "Right_Shoulder":(PREFIX + "RightShoulder", False, True),

                #Right Arm FK
                "Right_Arm_FK_1":(PREFIX + "RightArm", False, True),
                "Right_Arm_FK_2":(PREFIX + "RightForeArm", False, True),
                "Right_Hand":(PREFIX + "RightHand", False, True),
                
                #Right Arm IK
                "Right_Arm_upV":(PREFIX + "RightArmPoleVector", True, False, False, "poleMatcher", (PREFIX +"RightArm", PREFIX +"RightForeArm_poleHelper", PREFIX +"RightHand")),
                "Right_Arm_IK":(PREFIX + "RightHand", True, True, False),
                
                #Right Fingers
                "Right_Thumb_1":(PREFIX + "RightHandThumb1", False, True),
                "Right_Thumb_2":(PREFIX + "RightHandThumb2", False, True),
                "Right_Thumb_3":(PREFIX + "RightHandThumb3", False, True),
                "TK_Right_HandRig_Thumb_Eff_Output":(PREFIX + "RightHandThumb4",),

                "Right_Index_Mtc":(PREFIX + "RightHandIndex0", False, True),
                "Right_Index_1":(PREFIX + "RightHandIndex1", False, True),
                "Right_Index_2":(PREFIX + "RightHandIndex2", False, True),
                "Right_Index_3":(PREFIX + "RightHandIndex3", False, True),
                "TK_Right_HandRig_Index_Eff_Output":(PREFIX + "RightHandIndex4",),
                
                "Right_Middle_Mtc":(PREFIX + "RightHandMiddle0", False, True),
                "Right_Middle_1":(PREFIX + "RightHandMiddle1", False, True),
                "Right_Middle_2":(PREFIX + "RightHandMiddle2", False, True),
                "Right_Middle_3":(PREFIX + "RightHandMiddle3", False, True),
                "TK_Right_HandRig_Middle_Eff_Output":(PREFIX + "RightHandMiddle4",),
                
                "Right_Ring_Mtc":(PREFIX + "RightHandRing0", False, True),
                "Right_Ring_1":(PREFIX + "RightHandRing1", False, True),
                "Right_Ring_2":(PREFIX + "RightHandRing2", False, True),
                "Right_Ring_3":(PREFIX + "RightHandRing3", False, True),
                "TK_Right_HandRig_Ring_Eff_Output":(PREFIX + "RightHandRing4",),
                
                "Right_Pinky_Mtc":(PREFIX + "RightHandPinky0", False, True),
                "Right_Pinky_1":(PREFIX + "RightHandPinky1", False, True),
                "Right_Pinky_2":(PREFIX + "RightHandPinky2", False, True),
                "Right_Pinky_3":(PREFIX + "RightHandPinky3", False, True),
                "TK_Right_HandRig_Pinky_Eff_Output":(PREFIX + "RightHandPinky4",),
                
                #Right HandProp
                #"Right_HandProp":(PREFIX + "Lf_HandProp_MCP_0_JNT", True, True, False),

                #Right Leg IK
                "Right_Leg_upV":(PREFIX + "RightLegPoleVector", True, False, False, "poleMatcher", (PREFIX +"RightUpLeg", PREFIX +"RightLeg_poleHelper", PREFIX +"RightFoot")),
                "Right_Leg_IK":(PREFIX + "RightFoot", True, True, False),
                "Right_IK_Tip":(PREFIX + "RightToeBase", True, True),
                
                #Right Leg FK
                "Right_Leg_FK_1":(PREFIX + "RightUpLeg", False, True),
                "Right_Leg_FK_2":(PREFIX + "RightLeg", False, True),
                "Right_Foot_FK_1":(PREFIX + "RightFoot", False, True),
                "Right_Foot_FK_2":(PREFIX + "RightToeBase", False, True),
                
                #"Right_Tip":(PREFIX + "Lf_Foot_MCP_2_JNT",),
           }

def ResetMocapControls(inRigRootName, inTemplate):
    rigRoot = pc.PyNode(inRigRootName)
    rigNS = rigRoot.namespace()

    mocapControls = []

    for key in inTemplate.keys():
        rigNode = tkc.getNode(rigNS + key)
        if rigNode is None:
            pc.warning("Can't find object for template key %s" % rigNS + key)
            continue

        mocapControls.append(rigNode)

    if not rigRoot in mocapControls:
         mocapControls.append(rigRoot)

    for c in mocapControls:
        tkc.removeAllCns(c)
        pc.cutKey(c)

    for c in mocapControls:
        tkc.resetAll(c)

def ConnectToMocap(inTargetObj, inSourceObj):
    sourceChar = getCharacter(inSourceObj)

    assert sourceChar is not None,"Cannot detect skeletal model template from '{}'".format(inSourceObj.name())

    sourceNs = str(inSourceObj.namespace())
    targetNs = str(inTargetObj.namespace())

    targetNsShort = targetNs
    if ":" in targetNsShort:
        targetNsShort = targetNsShort.replace(":", "")

    controls = tkc.getKeyables(inCategory="All", inCharacters=[targetNsShort], ordered=False)

    assert len(controls) > 0 and pc.objExists(targetNs+"MayaHIK"),"Cannot detect Toonkit rig from '{}'".format(inTargetObj.name())

    rigRoot = targetNs+"Local_SRT"
    Global_SRT =    targetNs+"Global_SRT"
    MocapTemplate = targetNs+"mocapJOINT_GRP"
    MocapScale = MocapTemplate if not pc.objExists(MocapTemplate + "_Scale") else MocapTemplate + "_Scale"

    #Go to frame 0
    pc.currentTime(0)
    pc.refresh()

    MocapTemplateNode = tkc.getNode(MocapTemplate)
    joints = [c for c in MocapTemplateNode.getChildren(allDescendents=True) if c.type() == "joint"]

    #set the source to None
    char = getCharacter(joints[0])
    if getCurrentCharacter() != char.name():
        setCurrentCharacter(char.name())

    source = getCurrentSource()
    if not "None" in source:
        setCurrentSource(None)

    tkRig.loadPoseInPlace(joints)

    ResetMocapControls(rigRoot, template)

    attrs = injectControlLayer(MocapTemplate, rigRoot, template, Global_SRT, inConstrain=True)

    setSource(targetNs+"MayaHIK", sourceChar.name())

    #Go to frame 1
    pc.currentTime(1)
    pc.refresh()
    #Go to frame 0
    pc.currentTime(0)
    pc.refresh()

def bakeControls(inNS="", inStart=None, inEnd=None):
    inStart = inStart or pc.playbackOptions(query=True, animationStartTime=True)
    inEnd = inEnd or pc.playbackOptions(query=True, animationEndTime=True)
    
    charname = inNS

    charname = charname.replace(":","")

    controls = tkc.getKeyables("All", inCharacters=[charname])

    constrained_controls = [c for c in controls if len(pc.listConnections(c, source=True, destination=False, type="constraint")) > 0]

    if len(constrained_controls) > 0:
        pc.bakeResults(constrained_controls, simulation=True, t=(inStart, inEnd), sampleBy=1, oversamplingRate=1, disableImplicitControl=True, preserveOutsideKeys=False, sparseAnimCurveBake=False,
                   removeBakedAttributeFromLayer=False, removeBakedAnimFromLayer=False, bakeOnOverrideLayer=False, minimizeRotation=False, controlPoints=False, shape=False)
    else:
        pc.warning("Can't find any mocap driven controls, retargeting reinitialized")

    MocapTemplate = inNS+"mocapJOINT_GRP"

    MocapTemplateNode = tkc.getNode(MocapTemplate)

    #Reinitialization
    if MocapTemplateNode is None:
        pc.warning("Can't find a mocap template... Reinitialization failed !")
        return

    joints = [c for c in MocapTemplateNode.getChildren(allDescendents=True) if c.type() == "joint"]
    
    #set the source to None
    char = getCharacter(joints[0])
    if getCurrentCharacter() != char.name():
        setCurrentCharacter(char.name())

    source = getCurrentSource()
    if not "None" in source:
        setCurrentSource(None)

    tkRig.loadPoseInPlace(joints)
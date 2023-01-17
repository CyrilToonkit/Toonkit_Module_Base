import tkMayaCore as tkc
import tkRig
import pymel.core as pc
import tkMayaCore as tkc
import tkJointOrient as tkj
from Toonkit_Core import tkLogger
from maya import cmds, mel
from maya.api import OpenMaya

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

PREFIX = "MayaHIK_"

WORLD_PRESET =  {
    "inPrimary":0,
    "inPrimaryType":0,
    "inPrimaryData":[1.0, 0.0, 0.0],
    "inPrimaryNegate":False,
    "inPrimaryChild":"",
    "inSecondary":1,
    "inSecondaryType":0,
    "inSecondaryData":[0.0, 1.0, 0.0],
    "inSecondaryNegate":False
}

YUP_ZFRONT_PRESET = {
    "inPrimary":1,
    "inPrimaryType":2,
    "inPrimaryData":[1.0, 0.0, 0.0],
    "inPrimaryNegate":False,
    "inPrimaryChild":"",
    "inSecondary":2,
    "inSecondaryType":0,
    "inSecondaryData":[0.0, 0.0, 1.0],
    "inSecondaryNegate":True
}

L_FINGER1_PRESET = {
    "inPrimary":0,
    "inPrimaryType":2,
    "inPrimaryData":[1.0, 0.0, 0.0],
    "inPrimaryNegate":False,
    "inPrimaryChild":"",
    "inSecondary":2,
    "inSecondaryType":2,
    "inSecondaryData":[0.0, 1.0, 0.0],
    "inSecondaryNegate":True
}

L_FINGER2_PRESET = {
    "inPrimary":0,
    "inPrimaryType":2,
    "inPrimaryData":[1.0, 0.0, 0.0],
    "inPrimaryNegate":False,
    "inPrimaryChild":"",
    "inSecondary":2,
    "inSecondaryType":3,
    "inSecondaryData":[0.0, 1.0, 0.0],
    "inSecondaryNegate":True
}

L_FINGER3_PRESET = {
    "inPrimary":0,
    "inPrimaryType":2,
    "inPrimaryData":[1.0, 0.0, 0.0],
    "inPrimaryNegate":False,
    "inPrimaryChild":"",
    "inSecondary":2,
    "inSecondaryType":4,
    "inSecondaryData":[0.0, 1.0, 0.0],
    "inSecondaryNegate":True
}

R_FINGER1_PRESET = {
    "inPrimary":0,
    "inPrimaryType":2,
    "inPrimaryData":[1.0, 0.0, 0.0],
    "inPrimaryNegate":True,
    "inPrimaryChild":"",
    "inSecondary":2,
    "inSecondaryType":2,
    "inSecondaryData":[0.0, 1.0, 0.0],
    "inSecondaryNegate":False
}

R_FINGER2_PRESET = {
    "inPrimary":0,
    "inPrimaryType":2,
    "inPrimaryData":[1.0, 0.0, 0.0],
    "inPrimaryNegate":True,
    "inPrimaryChild":"",
    "inSecondary":2,
    "inSecondaryType":3,
    "inSecondaryData":[0.0, 1.0, 0.0],
    "inSecondaryNegate":False
}

R_FINGER3_PRESET = {
    "inPrimary":0,
    "inPrimaryType":2,
    "inPrimaryData":[1.0, 0.0, 0.0],
    "inPrimaryNegate":True,
    "inPrimaryChild":"",
    "inSecondary":2,
    "inSecondaryType":4,
    "inSecondaryData":[0.0, 1.0, 0.0],
    "inSecondaryNegate":False
}

PRESETS = [
    (PREFIX + "Neck", YUP_ZFRONT_PRESET),
    (PREFIX + "Neck1", YUP_ZFRONT_PRESET),
    (PREFIX + "Head", YUP_ZFRONT_PRESET),

    #Lf Arm
    (PREFIX + "LeftShoulder", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[0.0, 0.0, 1.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":0,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":False,
        }),
        
    (PREFIX + "LeftArm", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":2,
            "inSecondaryType":2,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True,
        }),
        
    (PREFIX + "LeftForeArm", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":2,
            "inSecondaryType":3,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True,
        }),
    
    #Lf Hand
    (PREFIX + "LeftHand", {
            "inPrimaryType":5,
            "inPrimaryData":[-90.0, 0.0, 0.0],
            "inPrimaryChild":"Left_Hand",
        }),

    #Lf Thumb
    (PREFIX + "LeftHandThumb1", {"inPrimaryType":5,  "inPrimaryData":[-90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Thumb_1","inSecondaryNegate":True}),
    (PREFIX + "LeftHandThumb2", {"inPrimaryType":5,  "inPrimaryData":[-90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Thumb_2","inSecondaryNegate":True}),
    (PREFIX + "LeftHandThumb3", {"inPrimaryType":5,  "inPrimaryData":[-90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Thumb_3","inSecondaryNegate":True}),
    (PREFIX + "LeftHandThumb4", {"inPrimaryType":5,  "inPrimaryData":[-90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Thumb_3","inSecondaryNegate":True}),

    #Lf Index
    (PREFIX + "LeftHandIndex0", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_Mtc","inSecondary":1}),
    (PREFIX + "LeftHandIndex1", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_1","inSecondary":1}),
    (PREFIX + "LeftHandIndex2", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_2","inSecondary":1}),
    (PREFIX + "LeftHandIndex3", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_3","inSecondary":1}),
    (PREFIX + "LeftHandIndex4", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_3","inSecondary":1}),

    #Lf Middle
    (PREFIX + "LeftHandMiddle0", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_Mtc","inSecondary":1}),
    (PREFIX + "LeftHandMiddle1", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_1","inSecondary":1}),
    (PREFIX + "LeftHandMiddle2", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_2","inSecondary":1}),
    (PREFIX + "LeftHandMiddle3", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_3","inSecondary":1}),
    (PREFIX + "LeftHandMiddle4", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_3","inSecondary":1}),

    #Lf Ring
    (PREFIX + "LeftHandRing0", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_Mtc","inSecondary":1}),
    (PREFIX + "LeftHandRing1", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_1","inSecondary":1}),
    (PREFIX + "LeftHandRing2", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_2","inSecondary":1}),
    (PREFIX + "LeftHandRing3", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_3","inSecondary":1}),
    (PREFIX + "LeftHandRing4", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_3","inSecondary":1}),

    #Lf Pinky
    (PREFIX + "LeftHandPinky0", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_Mtc","inSecondary":1}),
    (PREFIX + "LeftHandPinky1", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_1","inSecondary":1}),
    (PREFIX + "LeftHandPinky2", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_2","inSecondary":1}),
    (PREFIX + "LeftHandPinky3", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_3","inSecondary":1}),
    (PREFIX + "LeftHandPinky4", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_3","inSecondary":1}),

    #Lf Leg
    (PREFIX + "LeftUpLeg", {
            "inPrimary":1,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":2,
            "inSecondaryType":2,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),
        
    (PREFIX + "LeftLeg", {
            "inPrimary":1,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":2,
            "inSecondaryType":3,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),
        
    (PREFIX + "LeftFoot", {
            "inPrimary":2,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":0,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":False
        }),
        
    (PREFIX + "LeftToeBase", {
            "inPrimary":2,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":0,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":False
        }),


    #Rt Arm
    (PREFIX + "RightShoulder", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[0.0, 0.0, 1.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":2,
            "inSecondaryType":0,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":False,
        }),
        
    (PREFIX + "RightArm", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":2,
            "inSecondaryType":2,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True,
        }),
        
    (PREFIX + "RightForeArm", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":2,
            "inSecondaryType":3,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True,
        }),
    
    #Lf Hand
    (PREFIX + "RightHand", {
            "inPrimaryType":5,
            "inPrimaryData":[90.0, 0.0, 180.0],
            "inPrimaryChild":"Right_Hand",
        }),

    #Lf Thumb
    (PREFIX + "RightHandThumb1", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Thumb_1"}),
    (PREFIX + "RightHandThumb2", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Thumb_2"}),
    (PREFIX + "RightHandThumb3", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Thumb_3"}),
    (PREFIX + "RightHandThumb4", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Thumb_3"}),

    #Lf Index
    (PREFIX + "RightHandIndex0", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Index_Mtc","inSecondary":1}),
    (PREFIX + "RightHandIndex1", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Index_1","inSecondary":1}),
    (PREFIX + "RightHandIndex2", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Index_2","inSecondary":1}),
    (PREFIX + "RightHandIndex3", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Index_3","inSecondary":1}),
    (PREFIX + "RightHandIndex4", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Index_3","inSecondary":1}),

    #Lf Middle
    (PREFIX + "RightHandMiddle0", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Middle_Mtc","inSecondary":1}),
    (PREFIX + "RightHandMiddle1", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Middle_1","inSecondary":1}),
    (PREFIX + "RightHandMiddle2", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Middle_2","inSecondary":1}),
    (PREFIX + "RightHandMiddle3", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Middle_3","inSecondary":1}),
    (PREFIX + "RightHandMiddle4", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Middle_3","inSecondary":1}),

    #Lf Ring
    (PREFIX + "RightHandRing0", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Ring_Mtc","inSecondary":1}),
    (PREFIX + "RightHandRing1", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Ring_1","inSecondary":1}),
    (PREFIX + "RightHandRing2", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Ring_2","inSecondary":1}),
    (PREFIX + "RightHandRing3", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Ring_3","inSecondary":1}),
    (PREFIX + "RightHandRing4", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Ring_3","inSecondary":1}),

    #Lf Pinky
    (PREFIX + "RightHandPinky0", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Pinky_Mtc","inSecondary":1}),
    (PREFIX + "RightHandPinky1", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Pinky_1","inSecondary":1}),
    (PREFIX + "RightHandPinky2", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Pinky_2","inSecondary":1}),
    (PREFIX + "RightHandPinky3", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Pinky_3","inSecondary":1}),
    (PREFIX + "RightHandPinky4", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Pinky_3","inSecondary":1}),

    #Lf Leg
    (PREFIX + "RightUpLeg", {
            "inPrimary":1,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":2,
            "inSecondaryType":2,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),
        
    (PREFIX + "RightLeg", {
            "inPrimary":1,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":2,
            "inSecondaryType":3,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),
        
    (PREFIX + "RightFoot", {
            "inPrimary":2,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":0,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":False
        }),
        
    (PREFIX + "RightToeBase", {
            "inPrimary":2,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":0,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":False
        }),
]

DEFAULT_UNIT_CONVERSION = 100.0

UNITSCALE = 0.01#To meters
UNITSCALE = 1.0

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

###################### Axis Integration ###############################

# create the HumanIK in the mocap skeleton.
def hIKAddSkeletonToCharacter( hikCharacter, jointName, hikNode ):
    cmds.setAttr( jointName + '.segmentScaleCompensate', 0)
    node = hikCharacter + '.' + hikNode
    #setHikCharacterJointLabel( jointName, hikNode )  <---  it's not necessary. Keep this line, just in case. The function is not created.

    #  if node is assigned to Character Object, disconnect it
    tmpConnections = cmds.listConnections( node )
    if ( tmpConnections ):
        cmds.disconnectAttr( tmpConnections[0] + '.Character', node )

    # Check if the node already has a character attribute
    lAttr = cmds.listAttr( jointName, st='Character' )
    if not (lAttr):
        cmds.addAttr( jointName, longName='Character', shortName='ch', attributeType='message' )

    # connect Node.Character to Character Definition field Attribute
    out = jointName +'.Character'
    cmds.connectAttr (out, node, f=True)

# set values from the transformations of the joint to the HIK attributes
def hIKReadStancePoseTRSOffsetsForNode( hikCharacterNode,  jntName, hikNode ):
    tmpCharObjectName = hikCharacterNode + '.' + hikNode

    # get the matrix of the joint
    lMat = cmds.xform( jntName , q=1, ws=1, m=1 )
    # GetHIKMatrixDecomposition() will convert the TRS to UI units for use with setAttr
    lTRS = cmds.GetHIKMatrixDecomposition( lMat )

    # setting Translations
    cmds.setAttr ( tmpCharObjectName + 'Tx', lTRS[0] )
    cmds.setAttr ( tmpCharObjectName + 'Ty', lTRS[1] )
    cmds.setAttr ( tmpCharObjectName + 'Tz', lTRS[2] )

    # setting Rotations
    cmds.setAttr ( tmpCharObjectName + 'Rx', lTRS[3] )
    cmds.setAttr ( tmpCharObjectName + 'Ry', lTRS[4] )
    cmds.setAttr ( tmpCharObjectName + 'Rz', lTRS[5] )


    # setting Scales
    cmds.setAttr ( tmpCharObjectName + 'Sx', lTRS[6] )
    cmds.setAttr ( tmpCharObjectName + 'Sy', lTRS[7] )
    cmds.setAttr ( tmpCharObjectName + 'Sz', lTRS[8] )

    # setting other skeleton attributes
    jntAttrs = {
                'MinRLimitx' : '.minRotXLimit',
                'MinRLimity' : '.minRotYLimit',
                'MinRLimitz' : '.minRotZLimit',

                'MaxRLimitx' : '.maxRotXLimit',
                'MaxRLimity' : '.maxRotYLimit',
                'MaxRLimitz' : '.maxRotZLimit',

                'MinRLimitEnablex' : '.minRotXLimitEnable',
                'MinRLimitEnabley' : '.minRotYLimitEnable',
                'MinRLimitEnablez' : '.minRotZLimitEnable',

                'MaxRLimitEnablex' : '.maxRotXLimitEnable',
                'MaxRLimitEnabley' : '.maxRotYLimitEnable',
                'MaxRLimitEnablez' : '.maxRotZLimitEnable',
                }

    for jntAttr in jntAttrs:
        cmds.setAttr( tmpCharObjectName + jntAttr, cmds.getAttr ( jntName + jntAttrs[jntAttr]) )

    # setting joint orientation
    jntOrient = jntName + '.jointOrient'

    if cmds.objExists( jntOrient ):
        cmds.setAttr( tmpCharObjectName + 'JointOrientx', cmds.getAttr ( jntName + '.jointOrientX' ))
        cmds.setAttr( tmpCharObjectName + 'JointOrienty', cmds.getAttr ( jntName + '.jointOrientY' ))
        cmds.setAttr( tmpCharObjectName + 'JointOrientz', cmds.getAttr ( jntName + '.jointOrientZ' ))


    # setting the rotateAxis attributes
    cmds.setAttr( tmpCharObjectName + 'RotateAxisx', cmds.getAttr ( jntName + '.rotateAxisX' ))
    cmds.setAttr( tmpCharObjectName + 'RotateAxisy', cmds.getAttr ( jntName + '.rotateAxisY' ))
    cmds.setAttr( tmpCharObjectName + 'RotateAxisz', cmds.getAttr ( jntName + '.rotateAxisZ' ))

    cmds.setAttr( tmpCharObjectName + 'RotateOrder', cmds.getAttr ( jntName + '.rotateOrder' ))

# set the limits of the hik joints, using the hikLimits attribute in the hikDict
def hIKSetLimits( hikCharacterNode, hikLimits):
    for limit in hikLimits:
        #print "Setting limit ::::: ", limit
        cmds.setAttr( hikCharacterNode + '.' + limit, hikLimits[limit] )

# main function to call to create the HumanIK
def setupHumanIK( hikCharacterNode, hikJNTDic ):

    # Create the HIKCharacterNode with the name
    cmds.createNode ('HIKCharacterNode', n = hikCharacterNode )
    # Create HIKskeleton and assign the joints to the hik solver
    for jnt in hikJNTDic:
        #print "hikCharacterNode :::::: ", hikCharacterNode, "    MocapJoint :::::: ", jnt, "    hikNode :::::: ", hikJNTDic[jnt]['hikNode'], "    hikLimits :::::: ", hikJNTDic[jnt]['hikLimits']
        if cmds.objExists( jnt ):
            cmds.setAttr( jnt + '.tx', l=0 )
            cmds.setAttr( jnt + '.ty', l=0 )
            cmds.setAttr( jnt + '.tz', l=0 )
            try:
                hIKAddSkeletonToCharacter( hikCharacterNode, jnt, hikJNTDic[jnt]['hikNode'] )
                hIKReadStancePoseTRSOffsetsForNode( hikCharacterNode, jnt, hikJNTDic[jnt]['hikNode'] )
                if len(hikJNTDic[jnt]['hikLimits'])>0:
                    hIKSetLimits( hikCharacterNode, hikJNTDic[jnt]['hikLimits'] )
            except:
                print ("\n", jnt, " not connected to mocap definition 1")
        else:
            print ("\n", jnt, " not connected to mocap definition 2")

def initialize_hik():
    """Load plugin and build HIK widget.
    Essential for some HIK mel commands to run correctly.
    """
    # make sure plugins are loaded
    for plugin_name in "mayaHIK", "mayaCharacterization":
        if not cmds.pluginInfo(plugin_name, query=True, loaded=True):
            cmds.loadPlugin(plugin_name)

    # make sure widget is built and visible
    widget_name = "hikCharacterControlsDock"

    if not cmds.workspaceControl(widget_name, exists=True):
        # mel.eval('hikCharacterControlsWindowExists()')
        # mel.eval('buildCustomRigSchematicWidget()')
        # mel.eval('hikBuildCustomRigUI()')
        # mel.eval('hikUpdateCustomRigUI()')
        # mel.eval('hikBuildCharacterControlsDockableWindow()')

        mel.eval('hikCreateCharacterControlsDockableWindow()')

    # sometimes the widget exists but some elements do not
    # so must be restored first
    cmds.workspaceControl(widget_name, edit=True, restore=True)

    # cmds.workspaceControl(widget_name, edit=True, visible=True)

    return True

def align_arms_in_tpose(unit_conversion=DEFAULT_UNIT_CONVERSION, prefix="", posePreset=None):
    """Stuff
    """

    print ("align_arms_in_tpose prefix",prefix)
    left_arm_rotation_matrix = [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
    ]

    right_arm_rotation_matrix = [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
    ]

    for armElems, rot in    (((prefix+"LeftArm", prefix+"LeftForeArm", prefix+"LeftHand"), left_arm_rotation_matrix), 
                            ((prefix+"RightArm", prefix+"RightForeArm", prefix+"RightHand"), right_arm_rotation_matrix)):
        for armElem in armElems:
            translation = cmds.xform(armElem, query=True, translation=True, worldSpace=True)

            cmds.xform(
                armElem,
                matrix=rot + [i * unit_conversion for i in translation] + [1.0],
                worldSpace=True
            )

    return True

def align_fingers_tpose(unit_conversion=DEFAULT_UNIT_CONVERSION, prefix="", posePreset=None):
    """Stuff
    """
    left_finger_rotation_matrix = [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
    ]

    right_finger_rotation_matrix = [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
    ]

    for side, finger_rotation_matrix in ("Left", left_finger_rotation_matrix), ("Right", right_finger_rotation_matrix):
        for finger in "Index", "Middle", "Ring", "Pinky":
            # skip carpal
            for i in range(1, 4):
                node = "{}{}Hand{}{}".format(prefix, side, finger, i)

                if not cmds.objExists(node):
                    print ("Finger joint not found, skipping align: {}".format(node))
                    continue

                translation = cmds.xform(node, query=True, translation=True, worldSpace=True)

                cmds.xform(
                    node,
                    matrix=finger_rotation_matrix + [i * unit_conversion for i in translation] + [1.0],
                    worldSpace=True
                )

def align_thumbs_tpose(unit_conversion=DEFAULT_UNIT_CONVERSION, prefix="", posePreset=None):
    """Align thumbs to be perfectly straight but with a natural 30 degree angle
    """
    if posePreset == "crookedThumb":
        left_thumb_global_rotation = (-90, 0, 0)
        right_thumb_global_rotation = (-90, 0, 0)
    else:
        left_thumb_global_rotation = (0, -30, -30)
        right_thumb_global_rotation = (0, 30, 30)

    # these are values grabbed from maya and roughly rounded
    # TODO figure out more accurate values

    # matrix debug Lf
    # [0.7500001395016433, -0.4330127824335305, 0.5000000845714032, 0.0]
    # [-0.4999999355305003, -0.8660252921199902, 1.82793584965968e-17, 0.0]
    # [0.4330126382389127, -0.24999996324974622, -0.8660252910785049, 0.0]

    left_matrix = [
        0.75, -0.43, 0.50, 0.0,
        0.50, 0.86, 0.0, 0.0,
        -0.43, 0.25, 0.86, 0.0,
    ]

    # matrix debug Rt
    # [0.7499998660856068, 0.4330126245767083, -0.49999991072373784, 0.0]
    # [-0.4999999456749267, 0.8660253096906511, -1.4567478024630504e-16, 0.0]
    # [0.4330126459525142, 0.24999996770319627, 0.8660252919050285, 0.0]

    right_matrix = [
        0.75, 0.43, -0.50, 0.0,
        -0.50, 0.86, 0.0, 0.0,
        0.43, 0.25, 0.86, 0.0,
    ]

    for side, global_rotation in ("Left", left_thumb_global_rotation), ("Right", right_thumb_global_rotation):
        # redundant thumb index in case of extra thumb joints
        for i in range(1, 4):
            node = "{}{}HandThumb{}".format(prefix,side, i)

            if not cmds.objExists(node):
                print ("Thumb joint not found, skipping align: {}".format(node))
                continue

            # translation = cmds.xform(node, query=True, translation=True, worldSpace=True)

            cmds.xform(
                node,
                rotation=global_rotation,
                worldSpace=True
            )

    return True

def align_legs_tpose(unit_conversion=DEFAULT_UNIT_CONVERSION, prefix="", posePreset=None):
    left_leg_rotation_matrix = [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
    ]

    right_leg_rotation_matrix = [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
    ]

    # determine foot rotation while keeping current "tilt"
    mat = cmds.xform(prefix+"LeftFoot", query=True, matrix=True, worldSpace=True)
    print (mat[0:4])
    print (mat[4:8])
    print (mat[8:12])
    print ("")
    print (mat[8:11])

    left_foot_z_vector = cmds.xform(prefix+"LeftFoot", query=True, matrix=True, worldSpace=True)[8:11]
    right_foot_z_vector = cmds.xform(prefix+"RightFoot", query=True, matrix=True, worldSpace=True)[8:11]

    left_foot_z_vector[0] = 0.0
    right_foot_z_vector[0] = 0.0

    left_foot_z_vector = OpenMaya.MVector(left_foot_z_vector)
    right_foot_z_vector = OpenMaya.MVector(right_foot_z_vector)

    left_foot_z_vector.normalize()
    right_foot_z_vector.normalize()

    # z vectors are same for both side
    foot_x_vector = OpenMaya.MVector(1.0, 0.0, 0.0)

    # cross product to get y axis
    left_foot_y_vector =  left_foot_z_vector ^ foot_x_vector
    right_foot_y_vector =  right_foot_z_vector ^ foot_x_vector

    # construct matrices
    left_foot_rotation_matrix = list(foot_x_vector) + [0.0]
    left_foot_rotation_matrix += list(left_foot_y_vector) + [0.0]
    left_foot_rotation_matrix += list(left_foot_z_vector) + [0.0]

    right_foot_rotation_matrix =  list(foot_x_vector) + [0.0]
    right_foot_rotation_matrix += list(right_foot_y_vector) + [0.0]
    right_foot_rotation_matrix += list(right_foot_z_vector) + [0.0]

    # align leg joints
    for legElems, rot in    (((prefix+"LeftUpLeg", prefix+"LeftLeg"), left_leg_rotation_matrix), 
                            ((prefix+"RightUpLeg", prefix+"RightLeg"), right_leg_rotation_matrix)):
        for legElem in legElems:
            translation = cmds.xform(legElem, query=True, translation=True, worldSpace=True)

            cmds.xform(
                legElem,
                matrix=rot + [j * unit_conversion for j in translation] + [1.0],
                worldSpace=True
            )

    # align foot joints
    for footElems, rot in   (((prefix+"LeftFoot", prefix+"LeftToeBase"), left_foot_rotation_matrix), 
                            ((prefix+"RightFoot", prefix+"RightToeBase"), right_foot_rotation_matrix)):
        for footElem in footElems:

            translation = cmds.xform(footElem, query=True, translation=True, worldSpace=True)

            cmds.xform(
                footElem,
                matrix=rot + [i * unit_conversion for i in translation] + [1.0],
                worldSpace=True
            )

    return True

def align_tpose(unit_conversion=DEFAULT_UNIT_CONVERSION, prefix="", posePreset=None):
    """Align full skeleton ready for HIK characterization
    """
    print ("align_tpose prefix",prefix)

    align_arms_in_tpose(unit_conversion=unit_conversion, prefix=prefix, posePreset=posePreset)
    align_fingers_tpose(unit_conversion=unit_conversion, prefix=prefix, posePreset=posePreset)
    align_thumbs_tpose(unit_conversion=unit_conversion, prefix=prefix, posePreset=posePreset)
    align_legs_tpose(unit_conversion=unit_conversion, prefix=prefix, posePreset=posePreset)

    return True

def apply_zero_pose(prefix="", posePreset=None):
    """Apply zero rotations to all mocap joints
    """
    if cmds.objExists("Mocap_set"):
        for attr in cmds.character("Mocap_set", query=True):
            if "rotate" not in attr:
                continue

            cmds.setAttr(attr, 0.0)
    else:
        hips = prefix+"Hips"
        if cmds.objExists(hips):

            joints = [hips] + cmds.listRelatives(hips, allDescendents=True)
            for joint in joints:
                cmds.setAttr("{}.rotateX".format(joint), 0.0)
                cmds.setAttr("{}.rotateY".format(joint), 0.0)
                cmds.setAttr("{}.rotateZ".format(joint), 0.0)
        else:
            cmds.warning("Can't get skeletal model joints !!")

def characterize_hik_node(hik_node, unit_converstion=DEFAULT_UNIT_CONVERSION, prefix="", posePreset=None):
    # update
    print ("characterize_hik_node prefix",prefix)

    cmds.refresh(force=True)
    cmds.dgdirty(a=True)

    mel.eval('hikDefinitionUpdateCharacterLists()')
    mel.eval('hikSetCurrentCharacter("{}")'.format(hik_node))
    mel.eval('hikUpdateCharacterList()')
    mel.eval('hikUpdateContextualUI')
    mel.eval('hikUpdateDefinitionUI')
    mel.eval('hikUpdateDefinitionButtonState()')
    mel.eval('hikUpdateSkeletonUI()')
    mel.eval('hikUpdateCurrentSkeleton()')

    # make sure character definition is unlocked
    mel.eval('hikCharacterLock("{}", 0, 1)'.format(hik_node))

    # straighten arms
    align_tpose(unit_conversion=unit_converstion, prefix=prefix, posePreset=posePreset)

    # don't update at this point
    # something seems to reset the pose
    # and it doesn't seem to be neccessary to refresh again before locking

    # characterize in TPose
    mel.eval('hikCharacterLock("{}", 1, 1)'.format(hik_node))

    # update HIK
    mel.eval('hikUpdateDefinitionButtonState()')
    mel.eval('hikUpdateSkeletonUI()')
    mel.eval('hikUpdateCurrentSkeleton()')

    # reset pose
    apply_zero_pose(prefix=prefix, posePreset=posePreset)

    return True

def characterize_asset(asset_name, unit_converstion=DEFAULT_UNIT_CONVERSION, anim=False, prefix="", posePreset=None):
    """Complete HIK configuration to accept mocap.

    Notes:
        The HIK code is ugly af.
        Refreshing the UI for some reason is essential to avoid errors, go figure.
        Seems to work ok when the HIK tab is not visible.
        Also seems to work ok when HIK tab is closed.
        HOWEVER if HIK widget was never built then that does cause errors (see initialize_hik)
    """

    # load hik
    initialize_hik()

    # get hik node
    hik_node = "{}HIK".format(asset_name)

    characterize_hik_node(hik_node, unit_converstion=unit_converstion, prefix=prefix, posePreset=posePreset)

    return True

###################### End of Axis Integration ###############################

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

        valid=True
        for key,value in DEFINITION.items():
            if not pc.objExists(ns + key):
                pc.warning("Can't find mocap hook '{}'".format(ns + key))
                valid=False
                
        if(valid):
            checkHIKExists()

            char = tkc.getNode(pc.mel.eval("hikCreateCharacter \""+ns+"SourceMocap"+"\""))
            
            for key,value in DEFINITION.items():
                print ("setCharacterObject(\""+ ns + key +"\",\""+char.name()+"\","+str(value)+",0);")
                pc.mel.eval("setCharacterObject(\""+ ns + key +"\",\""+char.name()+"\","+str(value)+",0);")
            
            pc.mel.eval("hikToggleLockDefinition")
        else:
            pc.warning("Motion capture model is not valid !")
        
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

def poleMatcher(*args):
    ns = args[0]

    topObjName = ns+args[2]
    middleObjName = ns+args[3]
    downObjName = ns+args[4]

    target = pc.group(empty=True, parent=topObjName, name=ns+args[1])

    tkc.createResPlane(target, pc.PyNode(topObjName), pc.PyNode(middleObjName), pc.PyNode(downObjName))

    return target.name()

def mocapPreBind(ns="", rigRoot = "local_STR"):
    if not cmds.objExists(rigRoot):
        rigRoots = cmds.ls("*:"+rigRoot)
        if len(rigRoots) > 0:
            rigRoot = rigRoots[0]
            ns = rigRoots[0].split(":")[0] + ":"

    # Global_SRT =    ns+"Global_SRT"
    MocapTemplate = ns+"mocapJOINT_GRP"
    # MocapScale = MocapTemplate if not pc.objExists(MocapTemplate + "_Scale") else MocapTemplate + "_Scale"

    hiddenObjs = []

    #Connect visibilities and add control tag
    Visibilities = pc.PyNode(ns+"Visibilities")
    if not pc.attributeQuery( "SkeletalModel",node=Visibilities, exists=True):
        tkc.addParameter(Visibilities, "SkeletalModel", inType="enum;False:True")

    joints = [j for j in tkc.getChildren(MocapTemplate, True) if j.type() == "joint"]

    for joint in joints:
        Visibilities.SkeletalModel >> joint.visibility

    tkLogger.info("joints : " + str(joints))

    #Store the bind pose
    tkRig.storePoseInPlace(joints)

    pc.select(joints)
    pc.mel.eval("TagAsController")
    pc.select(clear=True)

    #Add objects used as helpers
    refObj = PREFIX + "LeftLeg"
    transform = [0, 0, 1.5*UNITSCALE]
    obj = tkc.createRigObject(tkc.getNode(ns + refObj), name="$refObject_poleHelper", type="Group", mode="child", match=True)
    obj.t.set(transform)
    #lock
    for channel in tkc.CHANNELS:
        obj.attr(channel).setLocked(True)

    refObj = PREFIX + "RightLeg"
    transform = [0, 0, 1.5*UNITSCALE]
    obj = tkc.createRigObject(tkc.getNode(ns + refObj), name="$refObject_poleHelper", type="Group", mode="child", match=True)
    obj.t.set(transform)
    #lock
    for channel in tkc.CHANNELS:
        obj.attr(channel).setLocked(True)

    refObj = PREFIX + "LeftForeArm"
    transform = [0, 0, -1.5*UNITSCALE]
    obj = tkc.createRigObject(tkc.getNode(ns + refObj), name="$refObject_poleHelper", type="Group", mode="child", match=True)
    obj.t.set(transform)
    #lock
    for channel in tkc.CHANNELS:
        obj.attr(channel).setLocked(True)

    refObj = PREFIX + "RightForeArm"
    transform = [0, 0, -1.5*UNITSCALE]
    obj = tkc.createRigObject(tkc.getNode(ns + refObj), name="$refObject_poleHelper", type="Group", mode="child", match=True)
    obj.t.set(transform)
    #lock
    for channel in tkc.CHANNELS:
        obj.attr(channel).setLocked(True)

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

# Can't find were it used
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

def orientSkeletal(inMocapSet = "Mocap_set", prefix = PREFIX, world_Preset = WORLD_PRESET):

    mocap_set = tkc.getNode(inMocapSet)
    cons = None

    if not mocap_set is None:
        cons = tkc.getNodeConnections(tkc.getNode("Mocap_set"), "linearValues", "angularValues",inSource=False, inDestination=True, inDisconnect=True)

    for preset in PRESETS:
        tkj.writePreset(pc.PyNode(preset[0]), **preset[1])

    tkj.orientJointPreset(pc.PyNode(prefix + "Hips"), world_Preset, inIdentity=True)

    if not cons is None:
        tkc.setNodeConnections(cons, inSetBefore=True)

def snapSkeletal(MocapTemplate=template, inRigNs="", inMocapNs="", inAdditionalMatchers=None, inIterations=12):

    inAdditionalMatchers = inAdditionalMatchers or {}

    matches = []

    tempObjs = []

    for rigHook, mocapData in MocapTemplate.items():
        mocapHook = mocapData[0]

        rigHookNode = tkc.getNode(inRigNs + rigHook)
        mocapHookNode = tkc.getNode(inMocapNs + mocapHook)

        if rigHookNode is None or mocapHookNode is None:
            if rigHookNode is None:
                pc.warning("Can't find rig hook " + inRigNs + rigHook)
            if mocapHookNode is None:
                pc.warning("Can't find mocap hook " + inMocapNs + mocapHook)
        else:
            exists=False
            for match in matches:
                if match[1] == mocapHookNode:
                    exists = True
                    break

            if not exists:
                matchers = inAdditionalMatchers.get(mocapHook)
                if not matchers is None:
                    if not isinstance(matchers, (list, tuple)):
                        matchers = ((matchers, 1.0),)

                    trans = [0.0, 0.0, 0.0]
                    for matcherObj, matcherValue in matchers:
                        tempHookNode = tkc.getNode(inRigNs + matcherObj)
                        if tempHookNode is None:
                            tkc.getNode(inMocapNs + matcherObj)

                        if not tempHookNode is None:
                            trans += (tempHookNode.getTranslation(space="world") * matcherValue)
                        else:
                            pc.warning("Additional matcher '{0}' can't be found !".format(matcherObj))


                    rigHookNode = pc.group(empty=True, name="tmp")
                    rigHookNode.setTranslation(trans, space="world")
                    tempObjs.append(rigHookNode)

                matches.append((rigHookNode, mocapHookNode))
            else:
                print (mocapHookNode, "SKIPPED")

    #Match n times
    for i in range(inIterations):
        for rigHookNode, mocapHookNode in matches:
            pc.matchTransform(mocapHookNode, rigHookNode, piv=False, pos=True, rot=False, scl=False)
            
    if len(tempObjs) > 0:
        pc.delete(tempObjs)

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

def updateCharacterization(inPrefix=PREFIX, inPosePreset= "posePreset"):
    charName=None
    characters = pc.ls(type="HIKCharacterNode")
    for character in characters:
        if character.name().endswith("HIK"):
            charName = character.name()[:-3]

    if not charName is None:
        characterize_asset(charName, unit_converstion=1.0, prefix=inPrefix, posePreset=inPosePreset)
    else:
        pc.warning("Can't find a 'HIKCharacterNode' ending with 'HIK' !")

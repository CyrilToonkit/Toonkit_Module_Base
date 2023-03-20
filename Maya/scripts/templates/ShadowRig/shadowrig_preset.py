{
    "default_preset": {
        "inPrimary":1,#Y
        "inPrimaryType":2,#towards child
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":False,

        "inSecondary":2,#Z
        "inSecondaryType":0,#World vector
        "inSecondaryData":[0.0, 0.0, -1.0],
        "inSecondaryNegate":False,
        },
    "spine_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":2,#towards child
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":False,

        "inSecondary":2,#Z
        "inSecondaryType":0,#World vector
        "inSecondaryData":[0.0, 0.0, 1.0],
        "inSecondaryNegate":True,
        },
    "head_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":3,#towards parent
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":True,

        "inSecondary":2,#Z
        "inSecondaryType":0,#World vector
        "inSecondaryData":[0.0, 0.0, 1.0],
        "inSecondaryNegate":True,
    },
    "shoulder_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":2,#towards child
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":False,

        "inSecondary":2,#Z
        "inSecondaryType":0,#World vector
        "inSecondaryData":[0.0, 0.0, 1.0],
        "inSecondaryNegate":True,
    },

    "left_arm_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":2,#towards child
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":False,

        "inSecondary":2,#Z
        "inSecondaryType":1,#World point
        "inSecondaryData":("getUpVPos", "TK_Left_Arm_Twist_Up_Start_Deform", "TK_Left_Arm_Twist_Dwn_Start_Deform", "TK_Left_Arm_Twist_Dwn_End_Deform"),
        "inSecondaryNegate":False,
    },
    "right_arm_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":2,#towards child
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":False,

        "inSecondary":2,#Z
        "inSecondaryType":1,#World point
        "inSecondaryData":("getUpVPos", "TK_Right_Arm_Twist_Up_Start_Deform", "TK_Right_Arm_Twist_Dwn_Start_Deform", "TK_Right_Arm_Twist_Dwn_End_Deform"),
        "inSecondaryNegate":False,
    },
    "left_wrist_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":3,#towards parent
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":True,

        "inSecondary":0,#Z
        "inSecondaryType":1,#World point
        "inSecondaryData":("getUpVPos", "TK_Left_Arm_Twist_Up_Start_Deform", "TK_Left_Arm_Twist_Dwn_Start_Deform", "TK_Left_Arm_Twist_Dwn_End_Deform"),
        "inSecondaryNegate":True,
    },
    "right_wrist_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":3,#towards parent
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":True,

        "inSecondary":0,#Z
        "inSecondaryType":1,#World point
        "inSecondaryData":("getUpVPos", "TK_Right_Arm_Twist_Up_Start_Deform", "TK_Right_Arm_Twist_Dwn_Start_Deform", "TK_Right_Arm_Twist_Dwn_End_Deform"),
        "inSecondaryNegate":True,
    },
    "finger_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":2,#towards child
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":False,

        "inSecondary":2,#Z
        "inSecondaryType":2,#UpVChildren
        "inSecondaryData":[0.0, 0.0, 1.0],
        "inSecondaryNegate":True,
    },
    "finger2_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":2,#towards child
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":False,

        "inSecondary":2,#Z
        "inSecondaryType":3,#UpVParent
        "inSecondaryData":[0.0, 0.0, 1.0],
        "inSecondaryNegate":True,
    },
    "fingereff_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":3,#towards parent
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":True,

        "inSecondary":2,#Z
        "inSecondaryType":4,#UpVParentParent
        "inSecondaryData":[0.0, 0.0, 1.0],
        "inSecondaryNegate":True,
    },    "left_leg_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":2,#towards child
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":True,

        "inSecondary":2,#Z
        "inSecondaryType":1,#World point
        "inSecondaryData":("getUpVPos", "TK_Left_Leg_Twist_Up_Start_Deform", "TK_Left_Leg_Twist_Dwn_Start_Deform", "TK_Left_Leg_Twist_Dwn_End_Deform"),
        "inSecondaryNegate":True,
    },
    "left_legeff_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":3,#towards parent
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":False,

        "inSecondary":2,#Z
        "inSecondaryType":1,#World point
        "inSecondaryData":("getUpVPos", "TK_Left_Leg_Twist_Up_Start_Deform", "TK_Left_Leg_Twist_Dwn_Start_Deform", "TK_Left_Leg_Twist_Dwn_End_Deform"),
        "inSecondaryNegate":True,
    },
    "right_leg_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":2,#towards child
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":True,

        "inSecondary":2,#Z
        "inSecondaryType":1,#World point
        "inSecondaryData":("getUpVPos", "TK_Right_Leg_Twist_Up_Start_Deform", "TK_Right_Leg_Twist_Dwn_Start_Deform", "TK_Right_Leg_Twist_Dwn_End_Deform"),
        "inSecondaryNegate":True,
    },
    "right_legeff_preset":{
        "inPrimary":1,#Y
        "inPrimaryType":3,#towards parent
        "inPrimaryData":[0.0, 1.0, 0.0],
        "inPrimaryNegate":False,

        "inSecondary":2,#Z
        "inSecondaryType":1,#World point
        "inSecondaryData":("getUpVPos", "TK_Right_Leg_Twist_Up_Start_Deform", "TK_Right_Leg_Twist_Dwn_Start_Deform", "TK_Right_Leg_Twist_Dwn_End_Deform"),
        "inSecondaryNegate":True,
    },
}

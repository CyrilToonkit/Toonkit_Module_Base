[
    ("Ct_Neck_MCP_0_JNT", self.yup_zfront_preset),
    ("Ct_Head_MCP_0_JNT", self.yup_zfront_preset),
    ("Ct_Head_MCP_1_JNT", self.yup_zfront_preset),
    
    #Lf Arm
    ("Lf_Clavicle_MCP_0_JNT", {
            "inPrimary":1,
            "inPrimaryType":0,
            "inPrimaryData":[0.0, 0.0, 1.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":0,
            "inSecondaryType":0,
            "inSecondaryData":[1.0, 0.0, 0.0],
            "inSecondaryNegate":False
        }),
        
    ("Lf_Arm_MCP_0_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":2,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),
        
    ("Lf_Arm_MCP_1_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":3,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),
    
    #Lf Hand
    ("Lf_Arm_MCP_2_JNT", {
            "inPrimaryType":5,
            "inPrimaryData":[0.0, 0.0, 0.0],
            "inPrimaryChild":"Left_Hand",
        }),

    ("Lf_HandProp_MCP_0_JNT", {
            "inPrimary":0,
            "inPrimaryType":5,
            "inPrimaryData":[0.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"Lf_Arm_MCP_2_JNT",
            "inSecondary":1,
            "inSecondaryType":4,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),


    #Lf Thumb
    ("Lf_Thumb_MCP_0_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Thumb_1"}),
    ("Lf_Thumb_MCP_1_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Thumb_2"}),
    ("Lf_Thumb_MCP_2_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Thumb_3"}),
    ("Lf_Thumb_MCP_3_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Thumb_3"}),

    #Lf Index
    ("Lf_Index_MCP_0_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_Mtc"}),
    ("Lf_Index_MCP_1_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_1"}),
    ("Lf_Index_MCP_2_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_2"}),
    ("Lf_Index_MCP_3_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_3"}),
    ("Lf_Index_MCP_4_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_3"}),

    #Lf Middle
    ("Lf_Middle_MCP_0_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_Mtc"}),
    ("Lf_Middle_MCP_1_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_1"}),
    ("Lf_Middle_MCP_2_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_2"}),
    ("Lf_Middle_MCP_3_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_3"}),
    ("Lf_Middle_MCP_4_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_3"}),

    #Lf Ring
    ("Lf_Ring_MCP_0_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_Mtc"}),
    ("Lf_Ring_MCP_1_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_1"}),
    ("Lf_Ring_MCP_2_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_2"}),
    ("Lf_Ring_MCP_3_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_3"}),
    ("Lf_Ring_MCP_4_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_3"}),

    #Lf Pinky
    ("Lf_Pinky_MCP_0_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_Mtc"}),
    ("Lf_Pinky_MCP_1_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_1"}),
    ("Lf_Pinky_MCP_2_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_2"}),
    ("Lf_Pinky_MCP_3_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_3"}),
    ("Lf_Pinky_MCP_4_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_3"}),

    #Lf Leg
    ("Lf_Leg_MCP_0_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":2,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":False
        }),
        
    ("Lf_Leg_MCP_1_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":3,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":False
        }),
        
    ("Lf_Leg_MCP_2_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":0,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":False
        }),
        
    ("Lf_Foot_MCP_1_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":0,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":False
        }),
        
    ("Lf_Foot_MCP_2_JNT", {
            "inPrimary":0,
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
    ("Rt_Clavicle_MCP_0_JNT", {
            "inPrimary":1,
            "inPrimaryType":0,
            "inPrimaryData":[0.0, 0.0, 1.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":0,
            "inSecondaryType":0,
            "inSecondaryData":[1.0, 0.0, 0.0],
            "inSecondaryNegate":False
        }),
        
    ("Rt_Arm_MCP_0_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":2,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":False
        }),
        
    ("Rt_Arm_MCP_1_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":3,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":False
        }),

    #Rt Hand
    ("Rt_Arm_MCP_2_JNT", {
            "inPrimaryType":5,
            "inPrimaryData":[0.0, 0.0, 180.0],
            "inPrimaryChild":"Right_Hand",
        }),

    ("Rt_HandProp_MCP_0_JNT", {
            "inPrimary":0,
            "inPrimaryType":5,
            "inPrimaryData":[0.0, 0.0, 0.0],
            "inPrimaryNegate":False,
            "inPrimaryChild":"Rt_Arm_MCP_2_JNT",
            "inSecondary":1,
            "inSecondaryType":4,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),

    #Rt Thumb
    ("Rt_Thumb_MCP_0_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Thumb_1"}),
    ("Rt_Thumb_MCP_1_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Thumb_2"}),
    ("Rt_Thumb_MCP_2_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Thumb_3"}),
    ("Rt_Thumb_MCP_3_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Thumb_3"}),

    #Rt Index
    ("Rt_Index_MCP_0_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Index_Mtc"}),
    ("Rt_Index_MCP_1_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Index_1"}),
    ("Rt_Index_MCP_2_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Index_2"}),
    ("Rt_Index_MCP_3_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Index_3"}),
    ("Rt_Index_MCP_4_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Index_3"}),

    #Rt Middle
    ("Rt_Middle_MCP_0_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Middle_Mtc"}),
    ("Rt_Middle_MCP_1_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Middle_1"}),
    ("Rt_Middle_MCP_2_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Middle_2"}),
    ("Rt_Middle_MCP_3_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Middle_3"}),
    ("Rt_Middle_MCP_4_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Middle_3"}),

    #Rt Ring
    ("Rt_Ring_MCP_0_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Ring_Mtc"}),
    ("Rt_Ring_MCP_1_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Ring_1"}),
    ("Rt_Ring_MCP_2_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Ring_2"}),
    ("Rt_Ring_MCP_3_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Ring_3"}),
    ("Rt_Ring_MCP_4_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Ring_3"}),

    #Rt Pinky
    ("Rt_Pinky_MCP_0_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Pinky_Mtc"}),
    ("Rt_Pinky_MCP_1_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Pinky_1"}),
    ("Rt_Pinky_MCP_2_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Pinky_2"}),
    ("Rt_Pinky_MCP_3_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Pinky_3"}),
    ("Rt_Pinky_MCP_4_JNT", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Pinky_3"}),


    #Rt Leg
    ("Rt_Leg_MCP_0_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":2,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),
        
    ("Rt_Leg_MCP_1_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":3,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),
        
    ("Rt_Leg_MCP_2_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":0,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),
        
    ("Rt_Foot_MCP_1_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":0,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),
        
    ("Rt_Foot_MCP_2_JNT", {
            "inPrimary":0,
            "inPrimaryType":2,
            "inPrimaryData":[1.0, 0.0, 0.0],
            "inPrimaryNegate":True,
            "inPrimaryChild":"",
            "inSecondary":1,
            "inSecondaryType":0,
            "inSecondaryData":[0.0, 1.0, 0.0],
            "inSecondaryNegate":True
        }),
]
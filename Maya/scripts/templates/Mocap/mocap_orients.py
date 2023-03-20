[
    (self.mocapPrefix + "Neck", self.yup_zfront_preset),
    (self.mocapPrefix + "Neck1", self.yup_zfront_preset),
    (self.mocapPrefix + "Head", self.yup_zfront_preset),

    #Lf Arm
    (self.mocapPrefix + "LeftShoulder", {
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
        
    (self.mocapPrefix + "LeftArm", {
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
        
    (self.mocapPrefix + "LeftForeArm", {
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
    (self.mocapPrefix + "LeftHand", {
            "inPrimaryType":5,
            "inPrimaryData":[-90.0, 0.0, 0.0],
            "inPrimaryChild":"Left_Hand",
        }),

    #Lf Thumb
    (self.mocapPrefix + "LeftHandThumb1", {"inPrimaryType":5,  "inPrimaryData":[-90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Thumb_1","inSecondaryNegate":True}),
    (self.mocapPrefix + "LeftHandThumb2", {"inPrimaryType":5,  "inPrimaryData":[-90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Thumb_2","inSecondaryNegate":True}),
    (self.mocapPrefix + "LeftHandThumb3", {"inPrimaryType":5,  "inPrimaryData":[-90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Thumb_3","inSecondaryNegate":True}),
    (self.mocapPrefix + "LeftHandThumb4", {"inPrimaryType":5,  "inPrimaryData":[-90.0, 0.0, 0.0],    "inPrimaryChild":"Left_Thumb_3","inSecondaryNegate":True}),

    #Lf Index
    (self.mocapPrefix + "LeftHandIndex0", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_Mtc","inSecondary":1}),
    (self.mocapPrefix + "LeftHandIndex1", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_1","inSecondary":1}),
    (self.mocapPrefix + "LeftHandIndex2", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_2","inSecondary":1}),
    (self.mocapPrefix + "LeftHandIndex3", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_3","inSecondary":1}),
    (self.mocapPrefix + "LeftHandIndex4", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Index_3","inSecondary":1}),

    #Lf Middle
    (self.mocapPrefix + "LeftHandMiddle0", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_Mtc","inSecondary":1}),
    (self.mocapPrefix + "LeftHandMiddle1", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_1","inSecondary":1}),
    (self.mocapPrefix + "LeftHandMiddle2", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_2","inSecondary":1}),
    (self.mocapPrefix + "LeftHandMiddle3", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_3","inSecondary":1}),
    (self.mocapPrefix + "LeftHandMiddle4", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Middle_3","inSecondary":1}),

    #Lf Ring
    (self.mocapPrefix + "LeftHandRing0", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_Mtc","inSecondary":1}),
    (self.mocapPrefix + "LeftHandRing1", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_1","inSecondary":1}),
    (self.mocapPrefix + "LeftHandRing2", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_2","inSecondary":1}),
    (self.mocapPrefix + "LeftHandRing3", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_3","inSecondary":1}),
    (self.mocapPrefix + "LeftHandRing4", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Ring_3","inSecondary":1}),

    #Lf Pinky
    (self.mocapPrefix + "LeftHandPinky0", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_Mtc","inSecondary":1}),
    (self.mocapPrefix + "LeftHandPinky1", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_1","inSecondary":1}),
    (self.mocapPrefix + "LeftHandPinky2", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_2","inSecondary":1}),
    (self.mocapPrefix + "LeftHandPinky3", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_3","inSecondary":1}),
    (self.mocapPrefix + "LeftHandPinky4", {"inPrimaryType":5,  "inPrimaryData":[0.0, 0.0, 0.0],    "inPrimaryChild":"Left_Pinky_3","inSecondary":1}),

    #Lf Leg
    (self.mocapPrefix + "LeftUpLeg", {
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
        
    (self.mocapPrefix + "LeftLeg", {
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
        
    (self.mocapPrefix + "LeftFoot", {
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
        
    (self.mocapPrefix + "LeftToeBase", {
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
    (self.mocapPrefix + "RightShoulder", {
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
        
    (self.mocapPrefix + "RightArm", {
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
        
    (self.mocapPrefix + "RightForeArm", {
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
    (self.mocapPrefix + "RightHand", {
            "inPrimaryType":5,
            "inPrimaryData":[90.0, 0.0, 180.0],
            "inPrimaryChild":"Right_Hand",
        }),

    #Lf Thumb
    (self.mocapPrefix + "RightHandThumb1", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Thumb_1"}),
    (self.mocapPrefix + "RightHandThumb2", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Thumb_2"}),
    (self.mocapPrefix + "RightHandThumb3", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Thumb_3"}),
    (self.mocapPrefix + "RightHandThumb4", {"inPrimaryType":5,  "inPrimaryData":[90.0, 0.0, 180.0],    "inPrimaryChild":"Right_Thumb_3"}),

    #Lf Index
    (self.mocapPrefix + "RightHandIndex0", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Index_Mtc","inSecondary":1}),
    (self.mocapPrefix + "RightHandIndex1", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Index_1","inSecondary":1}),
    (self.mocapPrefix + "RightHandIndex2", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Index_2","inSecondary":1}),
    (self.mocapPrefix + "RightHandIndex3", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Index_3","inSecondary":1}),
    (self.mocapPrefix + "RightHandIndex4", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Index_3","inSecondary":1}),

    #Lf Middle
    (self.mocapPrefix + "RightHandMiddle0", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Middle_Mtc","inSecondary":1}),
    (self.mocapPrefix + "RightHandMiddle1", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Middle_1","inSecondary":1}),
    (self.mocapPrefix + "RightHandMiddle2", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Middle_2","inSecondary":1}),
    (self.mocapPrefix + "RightHandMiddle3", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Middle_3","inSecondary":1}),
    (self.mocapPrefix + "RightHandMiddle4", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Middle_3","inSecondary":1}),

    #Lf Ring
    (self.mocapPrefix + "RightHandRing0", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Ring_Mtc","inSecondary":1}),
    (self.mocapPrefix + "RightHandRing1", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Ring_1","inSecondary":1}),
    (self.mocapPrefix + "RightHandRing2", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Ring_2","inSecondary":1}),
    (self.mocapPrefix + "RightHandRing3", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Ring_3","inSecondary":1}),
    (self.mocapPrefix + "RightHandRing4", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Ring_3","inSecondary":1}),

    #Lf Pinky
    (self.mocapPrefix + "RightHandPinky0", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Pinky_Mtc","inSecondary":1}),
    (self.mocapPrefix + "RightHandPinky1", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Pinky_1","inSecondary":1}),
    (self.mocapPrefix + "RightHandPinky2", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Pinky_2","inSecondary":1}),
    (self.mocapPrefix + "RightHandPinky3", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Pinky_3","inSecondary":1}),
    (self.mocapPrefix + "RightHandPinky4", {"inPrimaryType":5,  "inPrimaryData":[0.0, -180.0, 0.0],    "inPrimaryChild":"Right_Pinky_3","inSecondary":1}),

    #Lf Leg
    (self.mocapPrefix + "RightUpLeg", {
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
        
    (self.mocapPrefix + "RightLeg", {
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
        
    (self.mocapPrefix + "RightFoot", {
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
        
    (self.mocapPrefix + "RightToeBase", {
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
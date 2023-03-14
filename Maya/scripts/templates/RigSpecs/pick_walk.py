[
    # Global
    {"Name": "Local_SRT","Parent": "Global_SRT","isParentGroup": None},
    {"Name": "Fly","Parent": "Local_SRT","isParentGroup": None},
    {"Name": "Hips","Parent": "Fly","isParentGroup": None},
    {"Name": "Hips_IK","Parent": "Hips","isParentGroup": None},   
    
    # Legs IK
    {"Name": "Left_Leg_upV","Parent":"Hips_IK","isParentGroup": "Legs_IK"},
    {"Name": "Left_Leg_IK","Parent": "Left_Leg_upV","isParentGroup": None},
    {"Name": "Right_Leg_upV","Parent":"Hips_IK","isParentGroup": "Legs_IK"},
    {"Name": "Right_Leg_IK","Parent": "Right_Leg_upV","isParentGroup": None},
    
    # Legs FK
    {"Name": "Left_Leg_FK_1","Parent": "Hips_IK","isParentGroup": "Legs"},
    {"Name": "Left_Leg_FK_2","Parent": "Left_Leg_FK_1","isParentGroup": None},
    {"Name": "Left_Foot_FK_1","Parent": "Left_Leg_FK_2","isParentGroup": None},
    {"Name": "Left_Foot_FK_2","Parent": "Left_Foot_FK_1","isParentGroup": None},
    {"Name": "Right_Leg_FK_1","Parent": "Hips_IK","isParentGroup": "Legs"},
    {"Name": "Right_Leg_FK_2","Parent": "Right_Leg_FK_1","isParentGroup": None},
    {"Name": "Right_Foot_FK_1","Parent": "Right_Leg_FK_2","isParentGroup": None},
    {"Name": "Right_Foot_FK_2","Parent": "Right_Foot_FK_1","isParentGroup": None},
    
    # Spine FK
    {"Name": "Spine_FK_2","Parent": "Hips","isParentGroup": "Spine"},
    {"Name": "Spine_FK_3","Parent": "Spine_FK_2","isParentGroup": None},
    {"Name": "Spine_FK_4","Parent": "Spine_FK_3","isParentGroup": None},
    {"Name": "Spine_FK_5","Parent": "Spine_FK_4","isParentGroup": None},
    
    # Spin IK
    {"Name": "Spine_IK_Middle","Parent": "Hips","isParentGroup": "Spine_IK"},
    {"Name": "Chest_IK","Parent": "Spine_IK_Middle","isParentGroup": None},
    
    # Left Arm FK
    {"Name": "Left_Shoulder","Parent": ["Spine_FK_5", "Chest_IK"],"isParentGroup": "Shoulders"},
    {"Name": "Left_Arm_FK_1","Parent": "Left_Shoulder","isParentGroup": "Arm"},
    {"Name": "Left_Arm_FK_2","Parent": "Left_Arm_FK_1","isParentGroup": None},
    {"Name": "Left_Hand","Parent": "Left_Arm_FK_2","isParentGroup": None},
    
    # Left Arm IK
    {"Name": "Left_Arm_upV","Parent": "Left_Shoulder","isParentGroup": "Arms_IK"},
    {"Name": "Left_Arm_IK","Parent": "Left_Arm_upV","isParentGroup": None},
    
    # Right Arm FK
    {"Name": "Right_Shoulder","Parent": ["Spine_FK_5", "Chest_IK"],"isParentGroup": "Shoulders"},
    {"Name": "Right_Arm_FK_1","Parent": "Right_Shoulder","isParentGroup": "Arm"},
    {"Name": "Right_Arm_FK_2","Parent": "Right_Arm_FK_1","isParentGroup": None},
    {"Name": "Right_Hand","Parent": "Right_Arm_FK_2","isParentGroup": None},
    
    # Right Arm IK
    {"Name": "Right_Arm_upV","Parent": "Right_Shoulder","isParentGroup": "Arms_IK"},
    {"Name": "Right_Arm_IK","Parent": "Right_Arm_upV","isParentGroup": None},
    
    # Left Hand
    {"Name": "Left_Thumb_1","Parent": ["Left_Hand", "Left_Arm_IK"],"isParentGroup": "Left_Fingers"},
    {"Name": "Left_Thumb_2","Parent": "Left_Thumb_1","isParentGroup": None},
    {"Name": "Left_Index_Mtc","Parent": "Left_Hand","isParentGroup": "Left_Fingers"},
    {"Name": "Left_Index_1","Parent": "Left_Index_Mtc","isParentGroup": None},
    {"Name": "Left_Index_2","Parent": "Left_Index_1","isParentGroup": None},
    {"Name": "Left_Index_3","Parent": "Left_Index_2","isParentGroup": None},
    {"Name": "Left_Middle_Mtc","Parent": "Left_Hand","isParentGroup": "Left_Fingers"},
    {"Name": "Left_Middle_1","Parent": "Left_Middle_Mtc","isParentGroup": None},
    {"Name": "Left_Middle_2","Parent": "Left_Middle_1","isParentGroup": None},
    {"Name": "Left_Middle_3","Parent": "Left_Middle_2","isParentGroup": None},
    {"Name": "Left_Ring_Mtc","Parent": "Left_Hand","isParentGroup": "Left_Fingers"},
    {"Name": "Left_Ring_1","Parent": "Left_Ring_Mtc","isParentGroup": None},
    {"Name": "Left_Ring_2","Parent": "Left_Ring_1","isParentGroup": None},
    {"Name": "Left_Ring_3","Parent": "Left_Ring_2","isParentGroup": None},
    {"Name": "Left_Pinky_Mtc","Parent": "Left_Hand","isParentGroup": "Left_Fingers"},
    {"Name": "Left_Pinky_1","Parent": "Left_Pinky_Mtc","isParentGroup": None},
    {"Name": "Left_Pinky_2","Parent": "Left_Pinky_1","isParentGroup": None},
    {"Name": "Left_Pinky_3","Parent": "Left_Pinky_2","isParentGroup": None},
    
    # Right Hand
    {"Name": "Right_Thumb_1","Parent": ["Right_Hand", "Right_Arm_IK"],"isParentGroup": "Right_Fingers"},
    {"Name": "Right_Thumb_2","Parent": "Right_Thumb_1","isParentGroup": None},
    {"Name": "Right_Index_Mtc","Parent": "Right_Hand","isParentGroup": "Right_Fingers"},
    {"Name": "Right_Index_1","Parent": "Right_Index_Mtc","isParentGroup": None},
    {"Name": "Right_Index_2","Parent": "Right_Index_1","isParentGroup": None},
    {"Name": "Right_Index_3","Parent": "Right_Index_2","isParentGroup": None},
    {"Name": "Right_Middle_Mtc","Parent": "Right_Hand","isParentGroup": "Right_Fingers"},
    {"Name": "Right_Middle_1","Parent": "Right_Middle_Mtc","isParentGroup": None},
    {"Name": "Right_Middle_2","Parent": "Right_Middle_1","isParentGroup": None},
    {"Name": "Right_Middle_3","Parent": "Right_Middle_2","isParentGroup": None},
    {"Name": "Right_Ring_Mtc","Parent": "Right_Hand","isParentGroup": "Right_Fingers"},
    {"Name": "Right_Ring_1","Parent": "Right_Ring_Mtc","isParentGroup": None},
    {"Name": "Right_Ring_2","Parent": "Right_Ring_1","isParentGroup": None},
    {"Name": "Right_Ring_3","Parent": "Right_Ring_2","isParentGroup": None},
    {"Name": "Right_Pinky_Mtc","Parent": "Right_Hand","isParentGroup": "Right_Fingers"},
    {"Name": "Right_Pinky_1","Parent": "Right_Pinky_Mtc","isParentGroup": None},
    {"Name": "Right_Pinky_2","Parent": "Right_Pinky_1","isParentGroup": None},
    {"Name": "Right_Pinky_3","Parent": "Right_Pinky_2","isParentGroup": None},

    # Neck FK
    {"Name": "Neck_FK_1","Parent": ["Spine_FK_5", "Chest_IK"],"isParentGroup": "Neck"},
    {"Name": "Neck_FK_2","Parent": "Neck_FK_1","isParentGroup": None},
    {"Name": "Head_FK","Parent": "Neck_FK_2","isParentGroup": None},

    # Neck IK
    {"Name": "Neck_IK_Start","Parent":["Spine_FK_5", "Chest_IK"],"isParentGroup": "Neck_IK"},
    {"Name": "Neck_IK_Middle","Parent": "Neck_IK_Start","isParentGroup": None},
    {"Name": "Head_IK","Parent": "Neck_IK_Middle","isParentGroup": None},
    
    # Extra Head
    {"Name": "Jaw","Parent": ["Head_FK", "Head_IK"],"isParentGroup": None},
    {"Name": "Right_Eye","Parent": ["Head_FK", "Head_IK"],"isParentGroup": None},
    {"Name": "Left_Eye","Parent":["Head_FK", "Head_IK"],"isParentGroup": None},
]
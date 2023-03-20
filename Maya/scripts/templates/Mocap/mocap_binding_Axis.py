{    #Spine FK
     "Hips":("Ct_Root_MCP_0_JNT", True, True),
     "Spine_FK_2":("SpineResolve1", True, True),
     "Spine_FK_3":("SpineResolve2", True, True),
     "Spine_FK_4":("SpineResolve3", True, True),
     "Spine_FK_5":("SpineResolve4", False, True),
     
     #Spine IK
     "Chest_IK":("SpineResolve4", True, True, False),
     "Spine_IK_StartHandle":("SpineResolve1", True, True, False),
     "Spine_IK_Middle":("SpineResolve2", True, True, False),
     "Spine_IK_EndHandle":("SpineResolve3", True, True, False),

     #Neck FK
     "Neck_FK_1":("NeckResolve1", True, True),#RIG TO ADD
     "Neck_FK_2":("NeckResolve2", True, True),#RIG TO ADD
     "Head_FK":("NeckResolve3", True, True),

     #Neck IK
     "Head_IK":("NeckResolve3", True, True, False),
     "Neck_IK_Start":("NeckResolve1", True, True, False),
     "Neck_IK_Middle":("NeckResolve2", True, True, False),

     #Left Arm
     "Left_Shoulder":("Lf_Clavicle_MCP_0_JNT", False, True),

     #Left Arm FK
     "Left_Arm_FK_1":("Lf_Arm_MCP_0_JNT", False, True),
     "Left_Arm_FK_2":("Lf_Arm_MCP_1_JNT", False, True),
     "Left_Hand":("Lf_Arm_MCP_2_JNT", False, True),
     
     #Left Arm IK
     "Left_Arm_upV":("LeftArmPoleVector", True, False, False, "poleMatcher", ("Lf_Arm_MCP_0_JNT", "Lf_Arm_MCP_1_JNT_poleHelper", "Lf_Arm_MCP_2_JNT")),
     "Left_Arm_IK":("Lf_Arm_MCP_2_JNT", True, True, False),
     
     #Left Fingers
     "Left_Thumb_1":("Lf_Thumb_MCP_0_JNT", False, True),
     "Left_Thumb_2":("Lf_Thumb_MCP_1_JNT", False, True),
     "Left_Thumb_3":("Lf_Thumb_MCP_2_JNT", False, True),
     "TK_Left_HandRig_Thumb_Eff_Output":("Lf_Thumb_MCP_3_JNT",),

     "Left_Index_Mtc":("Lf_Index_MCP_0_JNT", False, True),
     "Left_Index_1":("Lf_Index_MCP_1_JNT", False, True),
     "Left_Index_2":("Lf_Index_MCP_2_JNT", False, True),
     "Left_Index_3":("Lf_Index_MCP_3_JNT", False, True),
     "TK_Left_HandRig_Index_Eff_Output":("Lf_Index_MCP_4_JNT",),
     
     "Left_Middle_Mtc":("Lf_Middle_MCP_0_JNT", False, True),
     "Left_Middle_1":("Lf_Middle_MCP_1_JNT", False, True),
     "Left_Middle_2":("Lf_Middle_MCP_2_JNT", False, True),
     "Left_Middle_3":("Lf_Middle_MCP_3_JNT", False, True),
     "TK_Left_HandRig_Middle_Eff_Output":("Lf_Middle_MCP_4_JNT",),
     
     "Left_Ring_Mtc":("Lf_Ring_MCP_0_JNT", False, True),
     "Left_Ring_1":("Lf_Ring_MCP_1_JNT", False, True),
     "Left_Ring_2":("Lf_Ring_MCP_2_JNT", False, True),
     "Left_Ring_3":("Lf_Ring_MCP_3_JNT", False, True),
     "TK_Left_HandRig_Ring_Eff_Output":("Lf_Ring_MCP_4_JNT",),
     
     "Left_Pinky_Mtc":("Lf_Pinky_MCP_0_JNT", False, True),
     "Left_Pinky_1":("Lf_Pinky_MCP_1_JNT", False, True),
     "Left_Pinky_2":("Lf_Pinky_MCP_2_JNT", False, True),
     "Left_Pinky_3":("Lf_Pinky_MCP_3_JNT", False, True),
     "TK_Left_HandRig_Pinky_Eff_Output":("Lf_Pinky_MCP_4_JNT",),
     
     #Left HandProp
     "Left_HandProp":("Lf_HandProp_MCP_0_JNT", True, True, False),

     #Left Leg IK
     "Left_Leg_upV":("LeftLegPoleVector", True, False, False, "poleMatcher", ("Lf_Leg_MCP_0_JNT", "Lf_Leg_MCP_1_JNT_poleHelper", "Lf_Leg_MCP_2_JNT")),
     "Left_Leg_IK":("Lf_Leg_MCP_2_JNT", True, True, False),
     "Left_IK_Tip":("Lf_Foot_MCP_1_JNT", True, True),
     
     #Left Leg FK
     "Left_Leg_FK_1":("Lf_Leg_MCP_0_JNT", False, True),
     "Left_Leg_FK_2":("Lf_Leg_MCP_1_JNT", False, True),
     "Left_Foot_FK_1":("Lf_Leg_MCP_2_JNT", False, True),
     "Left_Foot_FK_2":("Lf_Foot_MCP_1_JNT", False, True),
     
     "Left_Tip":("Lf_Foot_MCP_2_JNT",),

     #Right Arm
     "Right_Shoulder":("Rt_Clavicle_MCP_0_JNT", False, True),

     #Right Arm FK
     "Right_Arm_FK_1":("Rt_Arm_MCP_0_JNT", False, True),
     "Right_Arm_FK_2":("Rt_Arm_MCP_1_JNT", False, True),
     "Right_Hand":("Rt_Arm_MCP_2_JNT", False, True),
     
     #Right Arm IK
     "Right_Arm_upV":("LeftArmPoleVector", True, False, False, "poleMatcher", ("Rt_Arm_MCP_0_JNT", "Rt_Arm_MCP_1_JNT_poleHelper", "Rt_Arm_MCP_2_JNT")),
     "Right_Arm_IK":("Rt_Arm_MCP_2_JNT", True, True, False),
     
     #Right Fingers
     "Right_Thumb_1":("Rt_Thumb_MCP_0_JNT", False, True),
     "Right_Thumb_2":("Rt_Thumb_MCP_1_JNT", False, True),
     "Right_Thumb_3":("Rt_Thumb_MCP_2_JNT", False, True),
     "TK_Right_HandRig_Thumb_Eff_Output":("Rt_Thumb_MCP_4_JNT",),

     "Right_Index_Mtc":("Rt_Index_MCP_0_JNT", False, True),
     "Right_Index_1":("Rt_Index_MCP_1_JNT", False, True),
     "Right_Index_2":("Rt_Index_MCP_2_JNT", False, True),
     "Right_Index_3":("Rt_Index_MCP_3_JNT", False, True),
     "TK_Right_HandRig_Index_Eff_Output":("Rt_Index_MCP_4_JNT",),

     "Right_Middle_Mtc":("Rt_Middle_MCP_0_JNT", False, True),
     "Right_Middle_1":("Rt_Middle_MCP_1_JNT", False, True),
     "Right_Middle_2":("Rt_Middle_MCP_2_JNT", False, True),
     "Right_Middle_3":("Rt_Middle_MCP_3_JNT", False, True),
     "TK_Right_HandRig_Middle_Eff_Output":("Rt_Middle_MCP_4_JNT",),

     "Right_Ring_Mtc":("Rt_Ring_MCP_0_JNT", False, True),
     "Right_Ring_1":("Rt_Ring_MCP_1_JNT", False, True),
     "Right_Ring_2":("Rt_Ring_MCP_2_JNT", False, True),
     "Right_Ring_3":("Rt_Ring_MCP_3_JNT", False, True),
     "TK_Right_HandRig_Ring_Eff_Output":("Rt_Ring_MCP_4_JNT",),

     "Right_Pinky_Mtc":("Rt_Pinky_MCP_0_JNT", False, True),
     "Right_Pinky_1":("Rt_Pinky_MCP_1_JNT", False, True),
     "Right_Pinky_2":("Rt_Pinky_MCP_2_JNT", False, True),
     "Right_Pinky_3":("Rt_Pinky_MCP_3_JNT", False, True),
     "TK_Right_HandRig_Pinky_Eff_Output":("Rt_Pinky_MCP_4_JNT",),

     #Right HandProp
     "Right_HandProp":("Rt_HandProp_MCP_0_JNT", True, True, False),

     #Right Leg IK
     "Right_Leg_upV":("LeftLegPoleVector", True, False, False, "poleMatcher", ("Rt_Leg_MCP_0_JNT", "Rt_Leg_MCP_1_JNT_poleHelper", "Rt_Leg_MCP_2_JNT")),
     "Right_Leg_IK":("Rt_Leg_MCP_2_JNT", True, True, False),
     "Right_IK_Tip":("Rt_Foot_MCP_1_JNT", True, True),
     
     #Right Leg FK
     "Right_Leg_FK_1":("Rt_Leg_MCP_0_JNT", False, True),
     "Right_Leg_FK_2":("Rt_Leg_MCP_1_JNT", False, True),
     "Right_Foot_FK_1":("Rt_Leg_MCP_2_JNT", False, True),
     "Right_Foot_FK_2":("Rt_Foot_MCP_1_JNT", False, True),
     
     "Right_Tip":("Rt_Foot_MCP_2_JNT",),

     #Facial
     #"Jaw_FK":("Jaw", False, True),
}
{
    "Biped":{ 
        "Left_Hand": # Poignet Gauche
            ["TK_Left_Arm_Twist_Dwn_5_Deform", "TK_Left_HandRig_Hand_Deform"],

        "Left_Arm_FK_2": # Coude Gauche
            ["TK_Left_Arm_Twist_Up_5_Deform", "TK_Left_Arm_Twist_Dwn_1_Deform"],

        "Left_Arm_FK_1": # Avent bras Gauche
            ["TK_Left_Shoulder_0_Deform", "TK_Left_Arm_Twist_Up_1_Deform"],

        "Left_Shoulder": # Epaule Gauche
            ["TK_Spine_End_Deform", "TK_Left_Shoulder_0_Deform"],

        "Left_Leg_FK_1": # Cuisse Gauche
            ["TK_Spine_Start_Deform", "TK_Left_Leg_Twist_Up_1_Deform"],

        "Left_Leg_FK_2": # Genoux Gauche
            ["TK_Left_Leg_Twist_Up_5_Deform", "TK_Left_Leg_Twist_Dwn_1_Deform"],

        "Left_Foot_FK_1": # Cheville Gauche
            ["TK_Left_Leg_Twist_Dwn_5_Deform", "TK_Left_Leg_Eff_Deform"],

        "Right_Hand": # Poignet Gauche
            ["TK_Right_Arm_Twist_Dwn_5_Deform", "TK_Right_HandRig_Hand_Deform"],

        "Right_Arm_FK_2": # Coude Gauche
            ["TK_Right_Arm_Twist_Up_5_Deform", "TK_Right_Arm_Twist_Dwn_1_Deform"],

        "Right_Arm_FK_1": # Avent bras Gauche
            ["TK_Right_Shoulder_0_Deform", "TK_Right_Arm_Twist_Up_1_Deform"],

        "Right_Shoulder": # Epaule Gauche
            ["TK_Spine_End_Deform", "TK_Right_Shoulder_0_Deform"],

        "Right_Leg_FK_1": # Cuisse Gauche
            ["TK_Spine_Start_Deform", "TK_Right_Leg_Twist_Up_1_Deform"],

        "Right_Leg_FK_2": # Genoux Gauche
            ["TK_Right_Leg_Twist_Up_5_Deform", "TK_Right_Leg_Twist_Dwn_1_Deform"],

        "Right_Foot_FK_1": # Cheville Gauche
            ["TK_Right_Leg_Twist_Dwn_5_Deform", "TK_Right_Leg_Eff_Deform"],


        "Neck_FK_1": # Cou
            ["TK_Spine_End_Deform", "TK_Neck_Start_Deform"],

        "Head_FK": # Tete
            ["TK_Neck_Start_Deform", "TK_Neck_Head_Deform"],

    },
    "Bird":{
        "Left_Leg_FK_01":
            ["TK_Left_Leg_Shoulder_Main_Deform", "TK_Left_LEG_Rounding_Deformer_Deformer_1"],

        "Left_Leg_FK_02":
            ["TK_Left_LEG_Rounding_Deformer_Deformer_4_0", "TK_Left_LEG_Rounding_Deformer_Deformer_4_1"],

        "Left_Foot_01":
            ["TK_Left_LEG_Rounding_Deformer_Deformer_7", "TK_Left_Ball_0_Deform"],

        "Left_Shoulder":
            ["TK_Spine_IK_7_Deform", "TK_Left_Shoulder_0_Deform"],

        "Left_Arm_FK_01":
            ["TK_Left_Shoulder_0_Deform", "TK_Left_WingDn_Start_Main_Deform"],

        "Left_Arm_FK_02":
            ["TK_Left_Rounding_Deformer_Deformer_4_0", "TK_Left_Rounding_Deformer_Deformer_4_1"],

        "Left_Hand_FK":
            ["TK_Left_Rounding_Deformer_Deformer_4_1", "TK_Left_Hand_Ctrl_Main_Deform"],

        "Right_Leg_FK_01":
            ["TK_Right_Leg_Shoulder_Main_Deform", "TK_Right_LEG_Rounding_Deformer_Deformer_1"],

        "Right_Leg_FK_02":
            ["TK_Right_LEG_Rounding_Deformer_Deformer_4_0", "TK_Right_LEG_Rounding_Deformer_Deformer_4_1"],

        "Right_Foot_01":
            ["TK_Right_LEG_Rounding_Deformer_Deformer_7", "TK_Right_Ball_0_Deform"],

        "Right_Shoulder":
            ["TK_Spine_IK_7_Deform", "TK_Right_Shoulder_0_Deform"],

        "Right_Arm_FK_01":
            ["TK_Right_Shoulder_0_Deform", "TK_Right_WingDn_Start_Main_Deform"],

        "Right_Arm_FK_02":
            ["TK_Right_Rounding_Deformer_Deformer_4_0", "TK_Right_Rounding_Deformer_Deformer_4_1"],

        "Right_Hand_FK":
            ["TK_Right_Rounding_Deformer_Deformer_4_1", "TK_Right_Hand_Ctrl_Main_Deform"],

        "Neck_01":
            ["TK_Spine_IK_7_Deform", "TK_Neck_IK_1_Deform"],

        "Head_FK":
            ["TK_Neck_IK_1_Deform", "TK_Head_Ctrl_0_Deform"]
    },
    "Digitigrade" : {
        "Left_ForeLeg_Leg_FK_01":
            ["TK_Left_ForeLeg_IK_Shoulder_Main_Deform", "TK_Left_ForeLeg_Rounding_Deformer_Deformer_1"],

        "Left_ForeLeg_Leg_FK_02":
            ["TK_Left_ForeLeg_Rounding_Deformer_Deformer_4_0", "TK_Left_ForeLeg_Rounding_Deformer_Deformer_4_1"],

        "Left_ForeLeg_Meta_FK":
            ["TK_Left_ForeLeg_Rounding_Deformer_Deformer_7", "TK_Left_ForeLeg_Meta_FK_def_0_Deform"],

        "Left_ForeLeg_FK_Ball_Bone_Ctrl":
            ["TK_Left_ForeLeg_Meta_FK_def_0_Deform", "TK_Left_ForeLeg_FK_Ball_def_0_Deform"],

        "Left_RearLeg_FK_Bone_0":
            ["TK_Left_RearLeg_Pelvis_Main_Deform", "TK_Left_RearLeg_Rounding_Deformer_Deformer_1"],

        "Left_RearLeg_FK_Bone_1":
            ["TK_Left_RearLeg_Rounding_Deformer_Deformer_4_0", "TK_Left_RearLeg_Rounding_Deformer_Deformer_4_1"],

        "Left_RearLeg_Meta_FK":
            ["TK_Left_RearLeg_Rounding_Deformer_Deformer_7", "TK_Left_RearLeg_Meta_FK_def_0_Deform"],

        "Left_RearLeg_FK_Ball":
            ["TK_Left_RearLeg_Meta_FK_def_0_Deform", "TK_Left_RearLeg_FK_Ball_def_0_Deform"],

        "Right_ForeLeg_Leg_FK_01":
            ["TK_Right_ForeLeg_IK_Shoulder_Main_Deform", "TK_Right_ForeLeg_Rounding_Deformer_Deformer_1"],

        "Right_ForeLeg_Leg_FK_02":
            ["TK_Right_ForeLeg_Rounding_Deformer_Deformer_4_0", "TK_Right_ForeLeg_Rounding_Deformer_Deformer_4_1"],

        "Right_ForeLeg_Meta_FK":
            ["TK_Right_ForeLeg_Rounding_Deformer_Deformer_7", "TK_Right_ForeLeg_Meta_FK_def_0_Deform"],

        "Right_ForeLeg_FK_Ball_Bone_Ctrl":
            ["TK_Right_ForeLeg_Meta_FK_def_0_Deform", "TK_Right_ForeLeg_FK_Ball_def_0_Deform"],

        "Right_RearLeg_FK_Bone_0":
            ["TK_Right_RearLeg_Pelvis_Main_Deform", "TK_Right_RearLeg_Rounding_Deformer_Deformer_1"],

        "Right_RearLeg_FK_Bone_1":
            ["TK_Right_RearLeg_Rounding_Deformer_Deformer_4_0", "TK_Right_RearLeg_Rounding_Deformer_Deformer_4_1"],

        "Right_RearLeg_Meta_FK":
            ["TK_Right_RearLeg_Rounding_Deformer_Deformer_7", "TK_Right_RearLeg_Meta_FK_def_0_Deform"],

        "Right_RearLeg_FK_Ball":
            ["TK_Right_RearLeg_Meta_FK_def_0_Deform", "TK_Right_RearLeg_FK_Ball_def_0_Deform"],

        "Neck_01":
            ["TK_Spine_IK_7_Deform", "TK_Neck_IK_1_Deform"],

        "Head_FK":
            ["TK_Neck_IK_1_Deform", "TK_Head_Ctrl_0_Deform"]
    },
    "Onguligrade" : {
        "Left_ForeLeg_Foot_01":
            ["TK_Left_ForeLeg_Rounding_Deformer_Deformer_7", "TK_Left_ForeLeg_Ball_0_Deform"],

        "Left_ForeLeg_Foot_02":
            ["TK_Left_ForeLeg_Ball_0_Deform", "TK_Left_ForeLeg_Toe_0_Deform"],
            
        "Left_ForeLeg_FK1":
            ["TK_Left_ForeLeg_Rounding_Deformer_Deformer_4_0", "TK_Left_ForeLeg_Rounding_Deformer_Deformer_4_1"],

        "Left_ForeLeg_FK0":
            ["TK_Left_ForeLeg_IK_Top_Bone_1_Main_Deform", "TK_Left_ForeLeg_Rounding_Deformer_Deformer_1"],

        "Left_ForeLeg_FK_Shoulder_Bone_1":
            ["TK_Left_ForeLeg_IK_Top_Bone_0_Main_Deform", "TK_Left_ForeLeg_IK_Top_Bone_1_Main_Deform"],

        "Left_ForeLeg_FK_Shoulder_Bone_0":
            ["TK_Spine_IK_7_Deform", "TK_Left_ForeLeg_IK_Top_Bone_0_Main_Deform"],
            
        "Left_RearLeg_FK_Toe":
            ["TK_Left_RearLeg_FK_Ball_def_0_Deform", "TK_Left_RearLeg_FK_Toe_def_0_Deform"],
            
        "Right_RearLeg_FK_Toe":
            ["TK_Right_RearLeg_FK_Ball_def_0_Deform", "TK_Right_RearLeg_FK_Toe_def_0_Deform"],

        "Left_RearLeg_FK_Ball":
            ["TK_Left_RearLeg_Meta_FK_def_0_Deform", "TK_Left_RearLeg_FK_Ball_def_0_Deform"],

        "Left_RearLeg_Meta_FK":
            ["TK_Left_RearLeg_Rounding_Deformer_Deformer_7", "TK_Left_RearLeg_Meta_FK_def_0_Deform"],

        "Left_RearLeg_FK_Bone_1":
            ["TK_Left_RearLeg_Rounding_Deformer_Deformer_4_0", "TK_Left_RearLeg_Rounding_Deformer_Deformer_4_1"],

        "Left_RearLeg_FK_Bone_0":
            ["TK_Spine_IK_1_Deform", "TK_Left_RearLeg_Rounding_Deformer_Deformer_1"],

        "Right_ForeLeg_Foot_01":
            ["TK_Right_ForeLeg_Rounding_Deformer_Deformer_7", "TK_Right_ForeLeg_Ball_0_Deform"],

        "Right_ForeLeg_Foot_02":
            ["TK_Right_ForeLeg_Ball_0_Deform", "TK_Right_ForeLeg_Toe_0_Deform"],
            
        "Right_ForeLeg_FK1":
            ["TK_Right_ForeLeg_Rounding_Deformer_Deformer_4_0", "TK_Right_ForeLeg_Rounding_Deformer_Deformer_4_1"],

        "Right_ForeLeg_FK0":
            ["TK_Right_ForeLeg_IK_Top_Bone_1_Main_Deform", "TK_Right_ForeLeg_Rounding_Deformer_Deformer_1"],

        "Right_ForeLeg_FK_Shoulder_Bone_1":
            ["TK_Right_ForeLeg_IK_Top_Bone_0_Main_Deform", "TK_Right_ForeLeg_IK_Top_Bone_1_Main_Deform"],

        "Right_ForeLeg_FK_Shoulder_Bone_0":
            ["TK_Spine_IK_7_Deform", "TK_Right_ForeLeg_IK_Top_Bone_0_Main_Deform"],

        "Right_RearLeg_FK_Ball":
            ["TK_Right_RearLeg_Meta_FK_def_0_Deform", "TK_Right_RearLeg_FK_Ball_def_0_Deform"],

        "Right_RearLeg_Meta_FK":
            ["TK_Right_RearLeg_Rounding_Deformer_Deformer_7", "TK_Right_RearLeg_Meta_FK_def_0_Deform"],

        "Right_RearLeg_FK_Bone_1":
            ["TK_Right_RearLeg_Rounding_Deformer_Deformer_4_0", "TK_Right_RearLeg_Rounding_Deformer_Deformer_4_1"],

        "Right_RearLeg_FK_Bone_0":
            ["TK_Spine_IK_1_Deform", "TK_Right_RearLeg_Rounding_Deformer_Deformer_1"],
            
        "Spine_03":
            ["TK_Spine_IK_4_Deform", "TK_Spine_IK_5_Deform"],

        "Neck_01":
            ["TK_Spine_IK_7_Deform", "TK_Neck_IK_1_Deform"],

        "Head_FK":
            ["TK_Neck_IK_5_Deform", "TK_Head_Ctrl_0_Deform"]
    },
    "PlantiDigitigrade" : {
        "Left_Shoulder":
            ["TK_Spine_IK_7_Deform", "TK_Left_Shoulder_0_Deform"],

        "Left_Arm_FK_01":
            ["TK_Left_Shoulder_0_Deform", "TK_Left_Rounding_Deformer_Deformer_1"],

        "Left_Arm_FK_02":
            ["TK_Left_Rounding_Deformer_Deformer_4_0", "TK_Left_Rounding_Deformer_Deformer_4_1"],

        "Left_Hand_FK":
            ["TK_Left_Rounding_Deformer_Deformer_7", "TK_Left_HandRig_Hand_Deform"],

        "Left_Rear_Leg_FK_01":
            ["TK_Left_Leg_Shoulder_Main_Deform", "TK_Left_Rear_Leg_Rounding_Deformer_Deformer_1"],

        "Left_Rear_Leg_FK_02":
            ["TK_Left_Rear_Leg_Rounding_Deformer_Deformer_4_0", "TK_Left_Rear_Leg_Rounding_Deformer_Deformer_4_1"],

        "Left_Rear_Leg_01":
            ["TK_Left_Rear_Leg_Rounding_Deformer_Deformer_6", "TK_Left_Rear_Leg_FK_0_0_Deform"],
            
        "Left_Rear_Leg_02":
            ["TK_Left_Rear_Leg_FK_0_0_Deform", "TK_Left_Rear_Leg_FK_1_0_Deform"],
            
        "Right_Shoulder":
            ["TK_Spine_IK_7_Deform", "TK_Right_Shoulder_0_Deform"],

        "Right_Arm_FK_01":
            ["TK_Right_Shoulder_0_Deform", "TK_Right_Rounding_Deformer_Deformer_1"],

        "Right_Arm_FK_02":
            ["TK_Right_Rounding_Deformer_Deformer_4_0", "TK_Right_Rounding_Deformer_Deformer_4_1"],

        "Right_Hand_FK":
            ["TK_Right_Rounding_Deformer_Deformer_7", "TK_Right_HandRig_Hand_Deform"],

        "Right_Rear_Leg_FK_01":
            ["TK_Right_Leg_Shoulder_Main_Deform", "TK_Right_Rear_Leg_Rounding_Deformer_Deformer_1"],

        "Right_Rear_Leg_FK_02":
            ["TK_Right_Rear_Leg_Rounding_Deformer_Deformer_4_0", "TK_Right_Rear_Leg_Rounding_Deformer_Deformer_4_1"],

        "Right_Rear_Leg_01":
            ["TK_Right_Rear_Leg_Rounding_Deformer_Deformer_6", "TK_Right_Rear_Leg_FK_0_0_Deform"],
            
        "Right_Rear_Leg_02":
            ["TK_Right_Rear_Leg_FK_0_0_Deform", "TK_Right_Rear_Leg_FK_1_0_Deform"],

        "Neck_01":
            ["TK_Spine_IK_7_Deform", "TK_Neck_IK_1_Deform"],
        
        "Head_FK":
            ["TK_Neck_IK_1_Deform", "TK_Head_Ctrl_0_Deform"]
    },
    "Plantigrade" : {
        "Left_Shoulder":
            ["TK_Spine_IK_7_Deform", "TK_Left_Shoulder_0_Deform"],

        "Left_Arm_FK_01":
            ["TK_Left_Shoulder_0_Deform", "TK_Left_Rounding_Deformer_Deformer_1"],

        "Left_Arm_FK_02":
            ["TK_Left_Rounding_Deformer_Deformer_4_0", "TK_Left_Rounding_Deformer_Deformer_4_1"],

        "Left_Hand_FK":
            ["TK_Left_Rounding_Deformer_Deformer_7", "TK_Left_HandRig_Hand_Deform"],

        "Left_Leg_FK_01":
            ["TK_Spine_IK_1_Deform", "TK_Left_LEG_Rounding_Deformer_Deformer_1"],

        "Left_Leg_FK_02":
            ["TK_Left_LEG_Rounding_Deformer_Deformer_4_0", "TK_Left_LEG_Rounding_Deformer_Deformer_4_1"],

        "Left_Foot_01":
            ["TK_Left_LEG_Rounding_Deformer_Deformer_7", "TK_Left_Ball_0_Deform"],

        "Right_Shoulder":
            ["TK_Spine_IK_7_Deform", "TK_Right_Shoulder_0_Deform"],

        "Right_Arm_FK_01":
            ["TK_Right_Shoulder_0_Deform", "TK_Right_Rounding_Deformer_Deformer_1"],

        "Right_Arm_FK_02":
            ["TK_Right_Rounding_Deformer_Deformer_4_0", "TK_Right_Rounding_Deformer_Deformer_4_1"],

        "Right_Hand_FK":
            ["TK_Right_Rounding_Deformer_Deformer_7", "TK_Right_HandRig_Hand_Deform"],

        "Right_Leg_FK_01":
            ["TK_Spine_IK_1_Deform", "TK_Right_LEG_Rounding_Deformer_Deformer_1"],

        "Right_Leg_FK_02":
            ["TK_Right_LEG_Rounding_Deformer_Deformer_4_0", "TK_Right_LEG_Rounding_Deformer_Deformer_4_1"],

        "Right_Foot_01":
            ["TK_Right_LEG_Rounding_Deformer_Deformer_7", "TK_Right_Ball_0_Deform"],

        "Neck_01":
            ["TK_Spine_IK_7_Deform", "TK_Neck_IK_1_Deform"],

        "Head_FK":
            ["TK_Neck_IK_1_Deform", "TK_Head_Ctrl_0_Deform"]
    }
}
import os
import re

import OscarZmqMayaString as ozms

import pymel.core as pc
import tkMayaCore as tkc
import tkRig
import tkDevHelpers as tkdev
import tkBlendShapes as tkb
import tkNodeling as tkn
import tkTagTool as tkt

"""
#IN ORDER

import tkMayaCore as tkc
import tkDevHelpers as tkdev
import tkNodeling as tkn
import tkExpressions as tke
import tkOptimize as tko

reload(tkc)
reload(tkdev)
reload(tkn)
reload(tke)
reload(tko)

schema_low = [  
    "RootUnder",

    "Left_ARM_Root_Ctrl",
    "Left_ARM_Root_Ctrl_OLD",
    "Right_ARM_Root_Ctrl",
    "Right_ARM_Root_Ctrl_OLD",
    "Left_LEG_Root_Ctrl",
    "Left_LEG_Root_Ctrl_OLD",
    "Right_LEG_Root_Ctrl",
    "Right_LEG_Root_Ctrl_OLD",

    "Visibility_Holder",
    "Visibility_Params",
    
    "Left_Arm",
    "Left_Leg",
    "Right_Arm",
    "Right_Leg",
    "Aim",
    "AttenuationCheekBone_ParentSwitcher",
    "Bottom_Teeth",
    "Breath_Expression_Params",
    "Breath_Params",
    "Center_Levator",
    "Cheek_Scale_Params",
    "Chest",
    "Chin",
    "Curl_Lowerlip",
    "Curl_Upperlip",
    "Depressor_Center",
    "Dynamics_Param",
    "Eye_Tweak",
    "Eyebrow_Frown",
    "Eyebrow_Tweak",
    "Eyes_Aim_ParentSpace",
    "Eyes",
    "Eyes_Root",
    "Left_Eye_Ref",
    "Left_Eyes_Params",
    "Left_eye",
    "Left_eye_Listen",
    "Left_eye_aim",
    "Left_eyelids",
    "Left_Eye_Dir",
    "Left_eye_aimDeform",
    "Left_eye_iris",
    "Left_eye_spec",
    "Left_Spec_Dir",
    "Left_Spec_Jnt",
    "Left_Eyelids_Corner_In_Local",
    "Left_Eyelids_Corner_In_Listen",
    "Left_Eyelids_Corner_Out_Local",
    "Left_UpLid",
    "Left_DownLid",
    "Left_Eyelids_Corner_In_Dir",
    "Left_Eyelids_Corner_Out_Listen",
    "Left_UpLid_Listen",
    "Left_DownLid_Listen",
    "Left_Eyelids_Corner_Out_Dir",
    "Left_Eyelids_Up_1_5_Cons",
    "Left_Eyelids_Up_1_5_Dir1",
    "Left_Eyelids_Up_1_5_Dir2",
    "Left_Eyelids_Up_1_5_Tangent",
    "Left_Eyelids_Up_1_5_Ctrl",
    "Left_Eyelids_Down_1_5_Cons",
    "Left_Eyelids_Down_1_5_Dir1",
    "Left_Eyelids_Down_1_5_Dir2",
    "Left_Eyelids_Down_1_5_Tangent",
    "Left_Eyelids_Down_1_5_Ctrl",
    "Left_eyeshaper_0_4_4_ctrl",
    "Left_eyeshaper_4_4_4_ctrl",
    "Left_eyeshaper_4_4_3_ctrl",
    "Left_eyeshaper_4_4_2_ctrl",
    "Left_eyeshaper_4_4_1_ctrl",
    "Left_eyeshaper_2_4_4_ctrl",
    "Left_eyeshaper_2_4_3_ctrl",
    "Left_eyeshaper_2_4_2_ctrl",
    "Left_eyeshaper_2_4_1_ctrl",
    "Left_eyeshaper_1_4_3_ctrl",
    "Left_eyeshaper_1_4_2_ctrl",
    "Left_eyeshaper_1_4_1_ctrl",
    "Left_eyeshaper_1_4_4_ctrl",
    "Left_eyeshaper_0_4_2_ctrl",
    "Left_eyeshaper_0_4_1_ctrl",
    "Left_eyeshaper_0_4_0_ctrl",
    "Left_eyeshaper_0_4_3_ctrl",
    "Left_eyeshaper_3_4_4_ctrl",
    "Left_eyeshaper_3_4_3_ctrl",
    "Left_eyeshaper_3_4_2_ctrl",
    "Left_eyeshaper_3_4_1_ctrl",
    "Left_eyeshaper_0_3_4_ctrl",
    "Left_eyeshaper_0_3_3_ctrl",
    "Left_eyeshaper_0_3_2_ctrl",
    "Left_eyeshaper_0_3_1_ctrl",
    "Left_eyeshaper_0_1_1_ctrl",
    "Left_eyeshaper_0_0_5_ctrl",
    "Left_eyeshaper_0_0_3_ctrl",
    "Left_eyeshaper_0_0_2_ctrl",
    "Left_eyeshaper_0_0_1_ctrl",
    "Left_eyeshaper_0_2_4_ctrl",
    "Left_eyeshaper_0_2_3_ctrl",
    "Left_eyeshaper_0_2_2_ctrl",
    "Left_eyeshaper_0_2_1_ctrl",
    "Left_eyeshaper_0_1_4_ctrl",
    "Left_eyeshaper_0_1_3_ctrl",
    "Left_eyeshaper_0_1_2_ctrl",
    "Left_eyeshaper_4_3_4_ctrl",
    "Left_eyeshaper_4_3_3_ctrl",
    "Left_eyeshaper_4_3_2_ctrl",
    "Left_eyeshaper_4_3_1_ctrl",
    "Left_eyeshaper_4_2_4_ctrl",
    "Left_eyeshaper_4_2_3_ctrl",
    "Left_eyeshaper_4_2_2_ctrl",
    "Left_eyeshaper_4_2_1_ctrl",
    "Left_eyeshaper_4_1_4_ctrl",
    "Left_eyeshaper_4_1_3_ctrl",
    "Left_eyeshaper_4_1_2_ctrl",
    "Left_eyeshaper_4_1_1_ctrl",
    "Left_eyeshaper_4_0_4_ctrl",
    "Left_eyeshaper_4_0_3_ctrl",
    "Left_eyeshaper_4_0_2_ctrl",
    "Left_eyeshaper_4_0_1_ctrl",
    "Left_eyeshaper_2_0_4_ctrl",
    "Left_eyeshaper_2_0_3_ctrl",
    "Left_eyeshaper_2_0_2_ctrl",
    "Left_eyeshaper_2_0_1_ctrl",
    "Left_eyeshaper_1_0_4_ctrl",
    "Left_eyeshaper_1_0_3_ctrl",
    "Left_eyeshaper_1_0_2_ctrl",
    "Left_eyeshaper_1_0_1_ctrl",
    "Left_eyeshaper_3_0_4_ctrl",
    "Left_eyeshaper_3_0_3_ctrl",
    "Left_eyeshaper_3_0_2_ctrl",
    "Left_eyeshaper_3_0_1_ctrl",
    "Left_eyeshaper_4_4_0_ctrl",
    "Left_eyeshaper_3_0_0_ctrl",
    "Left_eyeshaper_2_4_0_ctrl",
    "Left_eyeshaper_2_3_0_ctrl",
    "Left_eyeshaper_2_2_0_ctrl",
    "Left_eyeshaper_1_4_0_ctrl",
    "Left_eyeshaper_1_3_0_ctrl",
    "Left_eyeshaper_1_2_0_ctrl",
    "Left_eyeshaper_2_1_0_ctrl",
    "Left_eyeshaper_2_0_0_ctrl",
    "Left_eyeshaper_0_3_0_ctrl",
    "Left_eyeshaper_1_1_0_ctrl",
    "Left_eyeshaper_1_0_0_ctrl",
    "Left_eyeshaper_0_1_0_ctrl",
    "Left_eyeshaper_0_0_0_ctrl",
    "Left_eyeshaper_0_2_0_ctrl",
    "Left_eyeshaper_4_3_0_ctrl",
    "Left_eyeshaper_4_2_0_ctrl",
    "Left_eyeshaper_4_0_0_ctrl",
    "Left_eyeshaper_3_4_0_ctrl",
    "Left_eyeshaper_3_3_0_ctrl",
    "Left_eyeshaper_4_1_0_ctrl",
    "Left_eyeshaper_3_2_0_ctrl",
    "Left_eyeshaper_3_1_0_ctrl",
    "Left_eyeshaper_1_1_4_ctrl",
    "Left_eyeshaper_2_1_4_ctrl",
    "Left_eyeshaper_3_1_4_ctrl",
    "Left_eyeshaper_3_2_4_ctrl",
    "Left_eyeshaper_3_3_4_ctrl",
    "Left_eyeshaper_2_3_4_ctrl",
    "Left_eyeshaper_1_3_4_ctrl",
    "Left_eyeshaper_1_2_4_ctrl",
    "Left_eyeshaper_2_2_4_ctrl",
    "Right_Eye_Ref",
    "Right_Eyes_Params",
    "Right_eye",
    "Right_eye_Listen",
    "Right_eye_aim",
    "Right_eyelids",
    "Right_Eye_Dir",
    "Right_eye_aimDeform",
    "Right_eye_iris",
    "Right_eye_spec",
    "Right_Spec_Dir",
    "Right_Spec_Jnt",
    "Right_Eyelids_Corner_In_Local",
    "Right_Eyelids_Corner_In_Listen",
    "Right_Eyelids_Corner_Out_Local",
    "Right_UpLid",
    "Right_DownLid",
    "Right_Eyelids_Corner_In_Dir",
    "Right_Eyelids_Corner_Out_Listen",
    "Right_UpLid_Listen",
    "Right_DownLid_Listen",
    "Right_Eyelids_Corner_Out_Dir",
    "Right_Eyelids_Up_1_5_Cons",
    "Right_Eyelids_Up_1_5_Dir1",
    "Right_Eyelids_Up_1_5_Dir2",
    "Right_Eyelids_Up_1_5_Tangent",
    "Right_Eyelids_Up_1_5_Ctrl",
    "Right_Eyelids_Down_1_5_Cons",
    "Right_Eyelids_Down_1_5_Dir1",
    "Right_Eyelids_Down_1_5_Dir2",
    "Right_Eyelids_Down_1_5_Tangent",
    "Right_Eyelids_Down_1_5_Ctrl",
    "Right_eyeshaper_0_4_4_ctrl",
    "Right_eyeshaper_4_4_4_ctrl",
    "Right_eyeshaper_4_4_3_ctrl",
    "Right_eyeshaper_4_4_2_ctrl",
    "Right_eyeshaper_4_4_1_ctrl",
    "Right_eyeshaper_2_4_4_ctrl",
    "Right_eyeshaper_2_4_3_ctrl",
    "Right_eyeshaper_2_4_2_ctrl",
    "Right_eyeshaper_2_4_1_ctrl",
    "Right_eyeshaper_1_4_3_ctrl",
    "Right_eyeshaper_1_4_2_ctrl",
    "Right_eyeshaper_1_4_1_ctrl",
    "Right_eyeshaper_1_4_4_ctrl",
    "Right_eyeshaper_0_4_2_ctrl",
    "Right_eyeshaper_0_4_1_ctrl",
    "Right_eyeshaper_0_4_0_ctrl",
    "Right_eyeshaper_0_4_3_ctrl",
    "Right_eyeshaper_3_4_4_ctrl",
    "Right_eyeshaper_3_4_3_ctrl",
    "Right_eyeshaper_3_4_2_ctrl",
    "Right_eyeshaper_3_4_1_ctrl",
    "Right_eyeshaper_0_3_4_ctrl",
    "Right_eyeshaper_0_3_3_ctrl",
    "Right_eyeshaper_0_3_2_ctrl",
    "Right_eyeshaper_0_3_1_ctrl",
    "Right_eyeshaper_0_1_1_ctrl",
    "Right_eyeshaper_0_0_5_ctrl",
    "Right_eyeshaper_0_0_3_ctrl",
    "Right_eyeshaper_0_0_2_ctrl",
    "Right_eyeshaper_0_0_1_ctrl",
    "Right_eyeshaper_0_2_4_ctrl",
    "Right_eyeshaper_0_2_3_ctrl",
    "Right_eyeshaper_0_2_2_ctrl",
    "Right_eyeshaper_0_2_1_ctrl",
    "Right_eyeshaper_0_1_4_ctrl",
    "Right_eyeshaper_0_1_3_ctrl",
    "Right_eyeshaper_0_1_2_ctrl",
    "Right_eyeshaper_4_3_4_ctrl",
    "Right_eyeshaper_4_3_3_ctrl",
    "Right_eyeshaper_4_3_2_ctrl",
    "Right_eyeshaper_4_3_1_ctrl",
    "Right_eyeshaper_4_2_4_ctrl",
    "Right_eyeshaper_4_2_3_ctrl",
    "Right_eyeshaper_4_2_2_ctrl",
    "Right_eyeshaper_4_2_1_ctrl",
    "Right_eyeshaper_4_1_4_ctrl",
    "Right_eyeshaper_4_1_3_ctrl",
    "Right_eyeshaper_4_1_2_ctrl",
    "Right_eyeshaper_4_1_1_ctrl",
    "Right_eyeshaper_4_0_4_ctrl",
    "Right_eyeshaper_4_0_3_ctrl",
    "Right_eyeshaper_4_0_2_ctrl",
    "Right_eyeshaper_4_0_1_ctrl",
    "Right_eyeshaper_2_0_4_ctrl",
    "Right_eyeshaper_2_0_3_ctrl",
    "Right_eyeshaper_2_0_2_ctrl",
    "Right_eyeshaper_2_0_1_ctrl",
    "Right_eyeshaper_1_0_4_ctrl",
    "Right_eyeshaper_1_0_3_ctrl",
    "Right_eyeshaper_1_0_2_ctrl",
    "Right_eyeshaper_1_0_1_ctrl",
    "Right_eyeshaper_3_0_4_ctrl",
    "Right_eyeshaper_3_0_3_ctrl",
    "Right_eyeshaper_3_0_2_ctrl",
    "Right_eyeshaper_3_0_1_ctrl",
    "Right_eyeshaper_4_4_0_ctrl",
    "Right_eyeshaper_3_0_0_ctrl",
    "Right_eyeshaper_2_4_0_ctrl",
    "Right_eyeshaper_2_3_0_ctrl",
    "Right_eyeshaper_2_2_0_ctrl",
    "Right_eyeshaper_1_4_0_ctrl",
    "Right_eyeshaper_1_3_0_ctrl",
    "Right_eyeshaper_1_2_0_ctrl",
    "Right_eyeshaper_2_1_0_ctrl",
    "Right_eyeshaper_2_0_0_ctrl",
    "Right_eyeshaper_0_3_0_ctrl",
    "Right_eyeshaper_1_1_0_ctrl",
    "Right_eyeshaper_1_0_0_ctrl",
    "Right_eyeshaper_0_1_0_ctrl",
    "Right_eyeshaper_0_0_0_ctrl",
    "Right_eyeshaper_0_2_0_ctrl",
    "Right_eyeshaper_4_3_0_ctrl",
    "Right_eyeshaper_4_2_0_ctrl",
    "Right_eyeshaper_4_0_0_ctrl",
    "Right_eyeshaper_3_4_0_ctrl",
    "Right_eyeshaper_3_3_0_ctrl",
    "Right_eyeshaper_4_1_0_ctrl",
    "Right_eyeshaper_3_2_0_ctrl",
    "Right_eyeshaper_3_1_0_ctrl",
    "Right_eyeshaper_1_1_4_ctrl",
    "Right_eyeshaper_2_1_4_ctrl",
    "Right_eyeshaper_3_1_4_ctrl",
    "Right_eyeshaper_3_2_4_ctrl",
    "Right_eyeshaper_3_3_4_ctrl",
    "Right_eyeshaper_2_3_4_ctrl",
    "Right_eyeshaper_1_3_4_ctrl",
    "Right_eyeshaper_1_2_4_ctrl",
    "Right_eyeshaper_2_2_4_ctrl",
    "Facial_GUI1",
    "Facial_GUI_ParentSpace",
    "Facial_GUI",
    "Facial_Under_Eye_Visibility_Params",
    "Facial_Under_Eyebrow_Visibility_Params",
    "Facial_Under_Mouth_Visibility_Params",
    "GlobalSRT",
    "Global_Dyn_Params",
    "Global_Params",
    "Head_Bulge_End",
    "Head_Bulge_Global",
    "Head_Bulge_Start",
    "Head_Bulge_Upper",
    "Head_Bulge_lower",
    "Head_Ctrl_Facial",
    "Head_Ctrl",
    "Head_OrientSpace",
    "Head_Scale_Param",
    "Head_lower",
    "Hips",
    "Hips_Top",
    "IK_End_Handle",
    "IK_Start_Handle",
    "Iris_Spec_Offset_Param",
    "Jaw_Locals",
    "Jaw_Move",
    "Jaw_Open_Params",
    "Jaw_Open",
    "Jaw",
    "Jaw_Slide",
    "Left_ARM_Control",
    "Left_ARM_End_Switch",
    "Left_ARM_FK_OrientSpace",
    "Left_ARM_FK",
    "Left_ARM_IK_ParentSpace",
    "Left_ARM_IK",
    "Left_ARM_IK_Stretch_FKREF",
    "Left_ARM_IK_Stretch",
    "Left_ARM_Middle_Switch",
    "Left_ARM_Ctrl_OLD",
    "Left_ARM_Ctrl",
    "Left_ARM_Start_Switch",
    "Left_Arm_DrivenKey",
    "Left_Arm_ParamHolder",
    "Left_Arm_PoseListener",
    "Left_Arm_StickJoint_Pos",
    "Left_Arm_StickJoint",
    "Left_Back_Follow_Leg_Params",
    "Left_Ball_IK_offset",
    "Left_Ball",
    "Left_Ball_Switcher_IP",
    "Left_Biped_Leg_Offsets",
    "Left_CheekCtrl",
    "Left_Cheek_Inflate",
    "Left_Cheek_Switcher",
    "Left_Cheekbone",
    "Left_Curl_Corner",
    "Left_Depressor",
    "Left_Ear",
    "Left_Expressions_Params",
    "Left_Eye_Bulge",
    "Left_Eye_Direction",
    "Left_Eye_Global",
    "Left_Eye_Mid_Wave",
    "Left_Eye_Pinch",
    "Left_Eye",
    "Left_Eye_Target",
    "Left_Eye_Up_Cheek",
    "Left_Eye_Wave",
    "Left_Eyebrow_1",
    "Left_Eyebrow_2",
    "Left_Eyebrow_3",
    "Left_Eyebrow_4",
    "Left_Eyebrow_Ext_Rot",
    "Left_Eyebrow_In_UpDown",
    "Left_Eyebrow_Int_Rot",
    "Left_Eyebrow_Mid_UpDown",
    "Left_Eyebrow_Out_UpDown",
    "Left_Eyebrow",
    "Left_FK_Effector",
    "Left_FOOTRoll",
    "Left_FOOT_Direction",
    "Left_FOOT_Ext_Bank",
    "Left_FOOT_FK_0",
    "Left_FOOT_FK_1",
    "Left_FOOT_FK_IKREF",
    "Left_FOOT_Heel",
    "Left_FOOT_Int_Bank",
    "Left_FOOT_Reverse_0",
    "Left_FOOT_Reverse_1",
    "Left_FootRoll_Factor_Param",
    "Left_Front_Follow_Leg_Params",
    "Left_HandRig",
    "Left_Hand_FK_IKREF",
    "Left_Hand_FK_OrientSpace",
    "Left_Hand_FK",
    "Left_Hand_ParamHolder",
    "Left_Hand_Param",
    "Left_IK_arm_Position",
    "Left_Iris",
    "Left_LEG_Control",
    "Left_LEG_FK",
    "Left_LEG_IK",
    "Left_LEG_IK_Stretch_FKREF",
    "Left_LEG_IK_Stretch",
    "Left_LEG_Ctrl_OLD",
    "Left_LEG_Ctrl",
    "Left_LEG_Rounding_Deformer",
    "Left_LEG_Tangent",
    "Left_LEG_Unroll",
    "Left_LEG_middle_switch",
    "Left_LEG_start_switch",
    "Left_LEG_upV_ParentSpace",
    "Left_Leg_Angle_Listener",
    "Left_Leg_FK_OrientSpace",
    "Left_Leg_IK_ParentSpace",
    "Left_Leg_ParamHolder",
    "Left_Leg_StickJoint_Pos",
    "Left_Leg_StickJoint",
    "Left_Levator",
    "Left_Lip_Zip",
    "Left_Lips_Cheek_Switcher",
    "Left_LowerBlink",
    "Left_LowerLid",
    "Left_Lower_Pant_Backward",
    "Left_Lower_Pant_Foreward",
    "Left_Lower_Pant_Global",
    "Left_Lower_Pant_Inside",
    "Left_Lower_Pant_Outside",
    "Left_Mouth_Lowerlip_1",
    "Left_Mouth",
    "Left_Mouth_Upperlip_1",
    "Left_Nostril",
    "Left_Nostril_Up",
    "Left_Orbit_Params",
    "Left_Pinch_Corner",
    "Left_Position",
    "Left_Puff",
    "Left_Pupil",
    "Left_Riso",
    "Left_Rounding_Deformer",
    "Left_Shoulder_OrientSpace",
    "Left_Shoulder",
    "Left_SoftEye_Switcher",
    "Left_Spec_Direction",
    "Left_Spec_Target",
    "Left_Specular",
    "Left_Specular_SwitcherIP_Patch_1",
    "Left_Tangent",
    "Left_Test_Leg_Extra1",
    "Left_Tip_RotZ",
    "Left_Toe_IK_offset",
    "Left_Toe",
    "Left_Toe_Switcher_IP",
    "Left_Tongue_1",
    "Left_Tongue_2",
    "Left_Tongue_3",
    "Left_Under_Cheek_GeoCns",
    "Left_Under_Cheek",
    "Left_Under_Cheekbone_1_GeoCns",
    "Left_Under_Cheekbone_1",
    "Left_Under_Cheekbone_2_GeoCns",
    "Left_Under_Cheekbone_2",
    "Left_Under_Cheekbone_3_GeoCns",
    "Left_Under_Cheekbone_3",
    "Left_Under_Chin_GeoCns",
    "Left_Under_Chin",
    "Left_Under_Eye_Bot_1_GeoCns",
    "Left_Under_Eye_Bot_1",
    "Left_Under_Eye_Bot_2_GeoCns",
    "Left_Under_Eye_Bot_2",
    "Left_Under_Eye_Bot_3_GeoCns",
    "Left_Under_Eye_Bot_3",
    "Left_Under_Eye_Ext_GeoCns",
    "Left_Under_Eye_Ext",
    "Left_Under_Eye_Int_GeoCns",
    "Left_Under_Eye_Int",
    "Left_Under_Eye_Top_1_GeoCns",
    "Left_Under_Eye_Top_1",
    "Left_Under_Eye_Top_2_GeoCns",
    "Left_Under_Eye_Top_2",
    "Left_Under_Eye_Top_3_GeoCns",
    "Left_Under_Eye_Top_3",
    "Left_Under_Eyebrow_Bot_GeoCns",
    "Left_Under_Eyebrow_Bot",
    "Left_Under_Eyelid_Top_1_GeoCns",
    "Left_Under_Eyelid_Top_1",
    "Left_Under_Eyelid_Top_2_GeoCns",
    "Left_Under_Eyelid_Top_2",
    "Left_Under_Eyelid_Top_3_GeoCns",
    "Left_Under_Eyelid_Top_3",
    "Left_Under_Eyelid_Top_4_Bot",
    "Left_Under_Eyelid_Top_4_GeoCns",
    "Left_Under_Lip_Bot_1_GeoCns",
    "Left_Under_Lip_Bot_1",
    "Left_Under_Lip_Bot_2_GeoCns",
    "Left_Under_Lip_Bot_2",
    "Left_Under_Lip_Bot_Center_GeoCns",
    "Left_Under_Lip_Bot_Center",
    "Left_Under_Lip_Corner_1_GeoCns",
    "Left_Under_Lip_Corner",
    "Left_Under_Lip_Top_1_GeoCns",
    "Left_Under_Lip_Top_1",
    "Left_Under_Lip_Top_2_GeoCns",
    "Left_Under_Lip_Top_2",
    "Left_Under_Lip_Top_Center_GeoCns",
    "Left_Under_Lip_Top_Center",
    "Left_Under_Nostril_GeoCns",
    "Left_Under_Nostril",
    "Left_Unroll",
    "Left_UpperBlink",
    "Left_UpperLid",
    "Left_Zygo",
    "Left_upV_ParentSpace",
    "LocalSRT",
    "Local_COG",
    "LowerBody",
    "Mouth_Lowerlip_Center",
    "Mouth_Move",
    "Mouth",
    "Mouth_Tweak",
    "Mouth_Upperlip_Center",
    "Neck_End",
    "Neck_FK_0",
    "Neck_FK_2",
    "Neck_IK_End_Handle",
    "Neck_IK",
    "Neck_IK_Start_Handle",
    "Neck_OrientSpace",
    "Neck_Start",
    "NoseTip",
    "PointDown",
    "Puff_Lowerlip",
    "Puff_Upperlip",
    "Right_ARM_Control",
    "Right_ARM_End_Switch",
    "Right_ARM_FK_OrientSpace",
    "Right_ARM_FK",
    "Right_ARM_IK_ParentSpace",
    "Right_ARM_IK",
    "Right_ARM_IK_Stretch_FKREF",
    "Right_ARM_IK_Stretch",
    "Right_ARM_Middle_Switch",
    "Right_ARM_Ctrl_OLD",
    "Right_ARM_Ctrl",
    "Right_ARM_Start_Switch",
    "Right_Arm_DrivenKey",
    "Right_Arm_ParamHolder",
    "Right_Arm_PoseListener",
    "Right_Arm_StickJoint_Pos",
    "Right_Arm_StickJoint",
    "Right_AttenuationCheekBone_ParentSwitcher1",
    "Right_Back_Follow_Leg_Params",
    "Right_Ball_IK_offset",
    "Right_Ball",
    "Right_Ball_Switcher_IP",
    "Right_Biped_Leg_Offsets",
    "Right_CheekCtrl",
    "Right_Cheek_Inflate",
    "Right_Cheek_Switcher",
    "Right_Cheekbone",
    "Right_Curl_Corner",
    "Right_Depressor",
    "Right_Ear",
    "Right_Expressions_Params",
    "Right_Eye_Bulge",
    "Right_Eye_Direction",
    "Right_Eye_Global",
    "Right_Eye_Mid_Wave",
    "Right_Eye_Pinch",
    "Right_Eye",
    "Right_Eye_Target",
    "Right_Eye_Up_Cheek",
    "Right_Eye_Wave",
    "Right_Eyebrow_1",
    "Right_Eyebrow_2",
    "Right_Eyebrow_3",
    "Right_Eyebrow_4",
    "Right_Eyebrow_Ext_Rot",
    "Right_Eyebrow_In_UpDown",
    "Right_Eyebrow_Int_Rot",
    "Right_Eyebrow_Mid_UpDown",
    "Right_Eyebrow_Out_UpDown",
    "Right_Eyebrow",
    "Right_FK_Effector",
    "Right_FOOTRoll",
    "Right_FOOT_Direction",
    "Right_FOOT_Ext_Bank",
    "Right_FOOT_FK_0",
    "Right_FOOT_FK_1",
    "Right_FOOT_FK_IKREF",
    "Right_FOOT_Heel",
    "Right_FOOT_Int_Bank",
    "Right_FOOT_Reverse_0",
    "Right_FOOT_Reverse_1",
    "Right_FootRoll_Factor_Param",
    "Right_Front_Follow_Leg_Params",
    "Right_HandRig",
    "Right_Hand_FK_IKREF",
    "Right_Hand_FK_OrientSpace",
    "Right_Hand_FK",
    "Right_Hand_ParamHolder",
    "Right_Hand_Param",
    "Right_IK_arm_Position",
    "Right_Iris",
    "Right_LEG_Control",
    "Right_LEG_FK",
    "Right_LEG_IK",
    "Right_LEG_IK_Stretch_FKREF",
    "Right_LEG_IK_Stretch",
    "Right_LEG_Ctrl_OLD",
    "Right_LEG_Ctrl",
    "Right_LEG_Rounding_Deformer",
    "Right_LEG_Tangent",
    "Right_LEG_Unroll",
    "Right_LEG_middle_switch",
    "Right_LEG_start_switch",
    "Right_LEG_upV_ParentSpace",
    "Right_Leg_Angle_Listener",
    "Right_Leg_FK_OrientSpace",
    "Right_Leg_IK_ParentSpace",
    "Right_Leg_ParamHolder",
    "Right_Leg_StickJoint_Pos",
    "Right_Leg_StickJoint",
    "Right_Levator",
    "Right_Lip_Zip",
    "Right_Lips_Cheek_Switcher",
    "Right_LowerBlink",
    "Right_LowerLid",
    "Right_Lower_Pant_Backward",
    "Right_Lower_Pant_Foreward",
    "Right_Lower_Pant_Global",
    "Right_Lower_Pant_Inside",
    "Right_Lower_Pant_Outside",
    "Right_Mouth_Lowerlip_1",
    "Right_Mouth",
    "Right_Mouth_Upperlip_1",
    "Right_Nostril",
    "Right_Nostril_Up",
    "Right_Orbit_Params",
    "Right_Pinch_Corner",
    "Right_Position",
    "Right_Puff",
    "Right_Pupil",
    "Right_Riso",
    "Right_Rounding_Deformer",
    "Right_Shoulder_OrientSpace",
    "Right_Shoulder",
    "Right_SoftEye_Switcher",
    "Right_Spec_Direction",
    "Right_Spec_Target",
    "Right_Specular",
    "Right_Specular_SwitcherIP_Patch_1",
    "Right_Tangent",
    "Right_Test_Leg_Extra1",
    "Right_Tip_RotZ",
    "Right_Toe_IK_offset",
    "Right_Toe",
    "Right_Toe_Switcher_IP",
    "Right_Tongue_1",
    "Right_Tongue_2",
    "Right_Tongue_3",
    "Right_Under_Cheek_GeoCns",
    "Right_Under_Cheek",
    "Right_Under_Cheekbone_1_GeoCns",
    "Right_Under_Cheekbone_1",
    "Right_Under_Cheekbone_2_GeoCns",
    "Right_Under_Cheekbone_2",
    "Right_Under_Cheekbone_3_GeoCns",
    "Right_Under_Cheekbone_3",
    "Right_Under_Eye_Bot_1_GeoCns",
    "Right_Under_Eye_Bot_1",
    "Right_Under_Eye_Bot_2_GeoCns",
    "Right_Under_Eye_Bot_2",
    "Right_Under_Eye_Bot_3_GeoCns",
    "Right_Under_Eye_Bot_3",
    "Right_Under_Eye_Ext_GeoCns",
    "Right_Under_Eye_Ext",
    "Right_Under_Eye_Int_GeoCns",
    "Right_Under_Eye_Int",
    "Right_Under_Eye_Top_1_GeoCns",
    "Right_Under_Eye_Top_1",
    "Right_Under_Eye_Top_2_GeoCns",
    "Right_Under_Eye_Top_2",
    "Right_Under_Eye_Top_3_GeoCns",
    "Right_Under_Eye_Top_3",
    "Right_Under_Eyebrow_Bot_GeoCns",
    "Right_Under_Eyebrow_Bot",
    "Right_Under_Eyelid_Top_1_GeoCns",
    "Right_Under_Eyelid_Top_1",
    "Right_Under_Eyelid_Top_2_GeoCns",
    "Right_Under_Eyelid_Top_2",
    "Right_Under_Eyelid_Top_3_GeoCns",
    "Right_Under_Eyelid_Top_3",
    "Right_Under_Eyelid_Top_4_Bot",
    "Right_Under_Eyelid_Top_4_GeoCns",
    "Right_Under_Lip_Bot_1_GeoCns",
    "Right_Under_Lip_Bot_1",
    "Right_Under_Lip_Bot_2_GeoCns",
    "Right_Under_Lip_Bot_2",
    "Right_Under_Lip_Corner_1_GeoCns",
    "Right_Under_Lip_Corner",
    "Right_Under_Lip_Top_1_GeoCns",
    "Right_Under_Lip_Top_1",
    "Right_Under_Lip_Top_2_GeoCns",
    "Right_Under_Lip_Top_2",
    "Right_Under_Nostril_GeoCns",
    "Right_Under_Nostril",
    "Right_Unroll",
    "Right_UpperBlink",
    "Right_UpperLid",
    "Right_Zygo",
    "Right_upV_ParentSpace",
    "TKUnder",
    "Spec_Aim_ParentSpace",
    "Spec_Aim",
    "Spine_Extra5_6_Switcher",
    "Spine_FK_0",
    "Spine_FK_1",
    "Spine_FK_2",
    "Spine_IK",
    "Sticky_Lip",
    "Test_Spine_Extra1",
    "Test_Spine_Extra2",
    "Time",
    "Tongue_1",
    "Tongue_2",
    "Tongue_3",
    "Tongue_FUI",
    "Tongue_Params",
    "Tongue",
    "Top_Teeth",
    "Wind_Global_Params"
]

schema_facial_unders = [
    "Cheek_Scale_Params",
    "Left_Under_Lip_Top_Center_GeoCns",
    "Left_Under_Chin_GeoCns",
    "Left_Under_Lip_Bot_Center_GeoCns",
    "Mouth_Tweak",
    "Facial_Under_Mouth_Visibility_Params",
    "Eye_Tweak",
    "Left_Under_Lip_Top_Center",
    "Left_Under_Chin",
    "Left_Under_Lip_Bot_Center",
    "Facial_Under_Eye_Visibility_Params",
    "Left_Under_Eye_Top_2_GeoCns",
    "Left_Under_Eye_Top_3_GeoCns",
    "Left_Under_Eye_Ext_GeoCns",
    "Left_Under_Eye_Bot_3_GeoCns",
    "Left_Under_Eye_Bot_2_GeoCns",
    "Left_Under_Eye_Bot_1_GeoCns",
    "Left_Under_Cheekbone_1_GeoCns",
    "Left_Under_Lip_Bot_2_GeoCns",
    "Left_Under_Lip_Bot_1_GeoCns",
    "Left_Under_Cheekbone_3_GeoCns",
    "Left_Under_Lip_Corner_1_GeoCns",
    "Left_Under_Cheekbone_2_GeoCns",
    "Left_Under_Lip_Top_2_GeoCns",
    "Left_Under_Cheek_GeoCns",
    "Left_Under_Lip_Top_1_GeoCns",
    "Left_Under_Nostril_GeoCns",
    "Left_Under_Eye_Top_1_GeoCns",
    "Left_Under_Eye_Int_GeoCns",
    "Left_Under_Eyelid_Top_2_GeoCns",
    "Left_Under_Eyelid_Top_3_GeoCns",
    "Left_Under_Eyelid_Top_4_GeoCns",
    "Left_Under_Eyelid_Top_1_GeoCns",
    "Left_Under_Lip_Bot_1",
    "Left_Under_Lip_Bot_2",
    "Left_Under_Lip_Corner",
    "Left_Under_Nostril",
    "Left_Under_Lip_Top_2",
    "Left_Under_Cheek",
    "Left_Under_Lip_Top_1",
    "Left_Under_Eye_Int",
    "Left_Under_Eye_Ext",
    "Left_Under_Eye_Top_3",
    "Left_Under_Eye_Top_2",
    "Left_Under_Eye_Bot_1",
    "Left_Under_Eye_Bot_2",
    "Left_Under_Eye_Bot_3",
    "Left_Under_Cheekbone_2",
    "Left_Under_Cheekbone_1",
    "Left_Under_Cheekbone_3",
    "Left_Under_Eye_Top_1",
    "Left_Under_Eyelid_Top_2",
    "Left_Under_Eyelid_Top_3",
    "Left_Under_Eyelid_Top_4_Bot",
    "Left_Under_Eyelid_Top_1",
    "Right_Under_Eye_Top_1_GeoCns",
    "Right_Under_Eye_Top_2_GeoCns",
    "Right_Under_Eye_Top_3_GeoCns",
    "Right_Under_Eye_Ext_GeoCns",
    "Right_Under_Eye_Bot_3_GeoCns",
    "Right_Under_Eye_Bot_2_GeoCns",
    "Right_Under_Eye_Bot_1_GeoCns",
    "Right_Under_Eye_Int_GeoCns",
    "Right_Under_Cheekbone_1_GeoCns",
    "Right_Under_Lip_Bot_2_GeoCns",
    "Right_Under_Lip_Bot_1_GeoCns",
    "Right_Under_Cheekbone_3_GeoCns",
    "Right_Under_Nostril_GeoCns",
    "Right_Under_Lip_Corner_1_GeoCns",
    "Right_Under_Cheekbone_2_GeoCns",
    "Right_Under_Lip_Top_2_GeoCns",
    "Right_Under_Cheek_GeoCns",
    "Right_Under_Lip_Top_1_GeoCns",
    "Right_Under_Eyelid_Top_1_GeoCns",
    "Right_Under_Eyelid_Top_2_GeoCns",
    "Right_Under_Eyelid_Top_3_GeoCns",
    "Right_Under_Eyelid_Top_4_GeoCns",
    "Right_Under_Lip_Bot_1",
    "Right_Under_Lip_Bot_2",
    "Right_Under_Lip_Corner",
    "Right_Under_Nostril",
    "Right_Under_Lip_Top_2",
    "Right_Under_Cheek",
    "Right_Under_Lip_Top_1",
    "Right_Under_Eye_Top_1",
    "Right_Under_Eye_Top_2",
    "Right_Under_Eye_Top_3",
    "Right_Under_Eye_Ext",
    "Right_Under_Eye_Bot_3",
    "Right_Under_Eye_Bot_2",
    "Right_Under_Eye_Bot_1",
    "Right_Under_Eye_Int",
    "Right_Under_Cheekbone_2",
    "Right_Under_Cheekbone_1",
    "Right_Under_Cheekbone_3",
    "Right_Under_Eyelid_Top_1",
    "Right_Under_Eyelid_Top_2",
    "Right_Under_Eyelid_Top_3",
    "Right_Under_Eyelid_Top_4_Bot"
]

schema_facial = [  
    "RootUnder",

    "Bottom_Teeth",
    "Center_Levator",
    "Cheek_Scale_Params",
    "Chin",
    "Curl_Lowerlip",
    "Curl_Upperlip",
    "Depressor_Center",
    "Eye_Tweak",
    "Eyebrow_Frown",
    "Eyebrow_Tweak",
    #"Eyes_Aim_ParentSpace",

    #"Eyes",#?
    #"Eyes_Root",#?

    #"Left_Eye_Ref",#?
    #"Left_Eyes_Params",#?
    #"Left_eye",#?
    "Left_eye_Listen",#?
    #"Left_eye_aim",#?
    "Left_eyelids",#?
    #"Left_Eye_Dir",#?
    #"Left_eye_aimDeform",#?
    "Left_eye_iris",#?

    # "Left_Orbit_Params",
    # "Left_Eye_Global",
    # "Left_Eye_Target",
    # "Left_Eye_Direction",

    "Left_eye_spec",
    "Left_Spec_Dir",
    "Left_Spec_Jnt",
    "Left_Eyelids_Corner_In_Local",
    "Left_Eyelids_Corner_In_Listen",
    "Left_Eyelids_Corner_Out_Local",
    "Left_UpLid",
    "Left_DownLid",
    "Left_Eyelids_Corner_In_Dir",
    "Left_Eyelids_Corner_Out_Listen",
    "Left_UpLid_Listen",
    "Left_DownLid_Listen",
    "Left_Eyelids_Corner_Out_Dir",
    "Left_Eyelids_Up_1_5_Cons",
    "Left_Eyelids_Up_1_5_Dir1",
    "Left_Eyelids_Up_1_5_Dir2",
    "Left_Eyelids_Up_1_5_Tangent",
    "Left_Eyelids_Up_1_5_Ctrl",
    "Left_Eyelids_Down_1_5_Cons",
    "Left_Eyelids_Down_1_5_Dir1",
    "Left_Eyelids_Down_1_5_Dir2",
    "Left_Eyelids_Down_1_5_Tangent",
    "Left_Eyelids_Down_1_5_Ctrl",
    "Left_eyeshaper_0_4_4_ctrl",
    "Left_eyeshaper_4_4_4_ctrl",
    "Left_eyeshaper_4_4_3_ctrl",
    "Left_eyeshaper_4_4_2_ctrl",
    "Left_eyeshaper_4_4_1_ctrl",
    "Left_eyeshaper_2_4_4_ctrl",
    "Left_eyeshaper_2_4_3_ctrl",
    "Left_eyeshaper_2_4_2_ctrl",
    "Left_eyeshaper_2_4_1_ctrl",
    "Left_eyeshaper_1_4_3_ctrl",
    "Left_eyeshaper_1_4_2_ctrl",
    "Left_eyeshaper_1_4_1_ctrl",
    "Left_eyeshaper_1_4_4_ctrl",
    "Left_eyeshaper_0_4_2_ctrl",
    "Left_eyeshaper_0_4_1_ctrl",
    "Left_eyeshaper_0_4_0_ctrl",
    "Left_eyeshaper_0_4_3_ctrl",
    "Left_eyeshaper_3_4_4_ctrl",
    "Left_eyeshaper_3_4_3_ctrl",
    "Left_eyeshaper_3_4_2_ctrl",
    "Left_eyeshaper_3_4_1_ctrl",
    "Left_eyeshaper_0_3_4_ctrl",
    "Left_eyeshaper_0_3_3_ctrl",
    "Left_eyeshaper_0_3_2_ctrl",
    "Left_eyeshaper_0_3_1_ctrl",
    "Left_eyeshaper_0_1_1_ctrl",
    "Left_eyeshaper_0_0_5_ctrl",
    "Left_eyeshaper_0_0_3_ctrl",
    "Left_eyeshaper_0_0_2_ctrl",
    "Left_eyeshaper_0_0_1_ctrl",
    "Left_eyeshaper_0_2_4_ctrl",
    "Left_eyeshaper_0_2_3_ctrl",
    "Left_eyeshaper_0_2_2_ctrl",
    "Left_eyeshaper_0_2_1_ctrl",
    "Left_eyeshaper_0_1_4_ctrl",
    "Left_eyeshaper_0_1_3_ctrl",
    "Left_eyeshaper_0_1_2_ctrl",
    "Left_eyeshaper_4_3_4_ctrl",
    "Left_eyeshaper_4_3_3_ctrl",
    "Left_eyeshaper_4_3_2_ctrl",
    "Left_eyeshaper_4_3_1_ctrl",
    "Left_eyeshaper_4_2_4_ctrl",
    "Left_eyeshaper_4_2_3_ctrl",
    "Left_eyeshaper_4_2_2_ctrl",
    "Left_eyeshaper_4_2_1_ctrl",
    "Left_eyeshaper_4_1_4_ctrl",
    "Left_eyeshaper_4_1_3_ctrl",
    "Left_eyeshaper_4_1_2_ctrl",
    "Left_eyeshaper_4_1_1_ctrl",
    "Left_eyeshaper_4_0_4_ctrl",
    "Left_eyeshaper_4_0_3_ctrl",
    "Left_eyeshaper_4_0_2_ctrl",
    "Left_eyeshaper_4_0_1_ctrl",
    "Left_eyeshaper_2_0_4_ctrl",
    "Left_eyeshaper_2_0_3_ctrl",
    "Left_eyeshaper_2_0_2_ctrl",
    "Left_eyeshaper_2_0_1_ctrl",
    "Left_eyeshaper_1_0_4_ctrl",
    "Left_eyeshaper_1_0_3_ctrl",
    "Left_eyeshaper_1_0_2_ctrl",
    "Left_eyeshaper_1_0_1_ctrl",
    "Left_eyeshaper_3_0_4_ctrl",
    "Left_eyeshaper_3_0_3_ctrl",
    "Left_eyeshaper_3_0_2_ctrl",
    "Left_eyeshaper_3_0_1_ctrl",
    "Left_eyeshaper_4_4_0_ctrl",
    "Left_eyeshaper_3_0_0_ctrl",
    "Left_eyeshaper_2_4_0_ctrl",
    "Left_eyeshaper_2_3_0_ctrl",
    "Left_eyeshaper_2_2_0_ctrl",
    "Left_eyeshaper_1_4_0_ctrl",
    "Left_eyeshaper_1_3_0_ctrl",
    "Left_eyeshaper_1_2_0_ctrl",
    "Left_eyeshaper_2_1_0_ctrl",
    "Left_eyeshaper_2_0_0_ctrl",
    "Left_eyeshaper_0_3_0_ctrl",
    "Left_eyeshaper_1_1_0_ctrl",
    "Left_eyeshaper_1_0_0_ctrl",
    "Left_eyeshaper_0_1_0_ctrl",
    "Left_eyeshaper_0_0_0_ctrl",
    "Left_eyeshaper_0_2_0_ctrl",
    "Left_eyeshaper_4_3_0_ctrl",
    "Left_eyeshaper_4_2_0_ctrl",
    "Left_eyeshaper_4_0_0_ctrl",
    "Left_eyeshaper_3_4_0_ctrl",
    "Left_eyeshaper_3_3_0_ctrl",
    "Left_eyeshaper_4_1_0_ctrl",
    "Left_eyeshaper_3_2_0_ctrl",
    "Left_eyeshaper_3_1_0_ctrl",
    "Left_eyeshaper_1_1_4_ctrl",
    "Left_eyeshaper_2_1_4_ctrl",
    "Left_eyeshaper_3_1_4_ctrl",
    "Left_eyeshaper_3_2_4_ctrl",
    "Left_eyeshaper_3_3_4_ctrl",
    "Left_eyeshaper_2_3_4_ctrl",
    "Left_eyeshaper_1_3_4_ctrl",
    "Left_eyeshaper_1_2_4_ctrl",
    "Left_eyeshaper_2_2_4_ctrl",

    #"Right_Eye_Ref",#?
    #"Right_Eyes_Params",#?
    #"Right_eye",#?
    "Right_eye_Listen",#?
    #"Right_eye_aim",#?
    "Right_eyelids",#?
    #"Right_Eye_Dir",#?
    #"Right_eye_aimDeform",#?
    "Right_eye_iris",#?

    # "Right_Orbit_Params",
    # "Right_Eye_Global",
    # "Right_Eye_Target",
    # "Right_Eye_Direction",

    "Right_eye_spec",
    "Right_Spec_Dir",
    "Right_Spec_Jnt",
    "Right_Eyelids_Corner_In_Local",
    "Right_Eyelids_Corner_In_Listen",
    "Right_Eyelids_Corner_Out_Local",
    "Right_UpLid",
    "Right_DownLid",
    "Right_Eyelids_Corner_In_Dir",
    "Right_Eyelids_Corner_Out_Listen",
    "Right_UpLid_Listen",
    "Right_DownLid_Listen",
    "Right_Eyelids_Corner_Out_Dir",
    "Right_Eyelids_Up_1_5_Cons",
    "Right_Eyelids_Up_1_5_Dir1",
    "Right_Eyelids_Up_1_5_Dir2",
    "Right_Eyelids_Up_1_5_Tangent",
    "Right_Eyelids_Up_1_5_Ctrl",
    "Right_Eyelids_Down_1_5_Cons",
    "Right_Eyelids_Down_1_5_Dir1",
    "Right_Eyelids_Down_1_5_Dir2",
    "Right_Eyelids_Down_1_5_Tangent",
    "Right_Eyelids_Down_1_5_Ctrl",
    "Right_eyeshaper_0_4_4_ctrl",
    "Right_eyeshaper_4_4_4_ctrl",
    "Right_eyeshaper_4_4_3_ctrl",
    "Right_eyeshaper_4_4_2_ctrl",
    "Right_eyeshaper_4_4_1_ctrl",
    "Right_eyeshaper_2_4_4_ctrl",
    "Right_eyeshaper_2_4_3_ctrl",
    "Right_eyeshaper_2_4_2_ctrl",
    "Right_eyeshaper_2_4_1_ctrl",
    "Right_eyeshaper_1_4_3_ctrl",
    "Right_eyeshaper_1_4_2_ctrl",
    "Right_eyeshaper_1_4_1_ctrl",
    "Right_eyeshaper_1_4_4_ctrl",
    "Right_eyeshaper_0_4_2_ctrl",
    "Right_eyeshaper_0_4_1_ctrl",
    "Right_eyeshaper_0_4_0_ctrl",
    "Right_eyeshaper_0_4_3_ctrl",
    "Right_eyeshaper_3_4_4_ctrl",
    "Right_eyeshaper_3_4_3_ctrl",
    "Right_eyeshaper_3_4_2_ctrl",
    "Right_eyeshaper_3_4_1_ctrl",
    "Right_eyeshaper_0_3_4_ctrl",
    "Right_eyeshaper_0_3_3_ctrl",
    "Right_eyeshaper_0_3_2_ctrl",
    "Right_eyeshaper_0_3_1_ctrl",
    "Right_eyeshaper_0_1_1_ctrl",
    "Right_eyeshaper_0_0_5_ctrl",
    "Right_eyeshaper_0_0_3_ctrl",
    "Right_eyeshaper_0_0_2_ctrl",
    "Right_eyeshaper_0_0_1_ctrl",
    "Right_eyeshaper_0_2_4_ctrl",
    "Right_eyeshaper_0_2_3_ctrl",
    "Right_eyeshaper_0_2_2_ctrl",
    "Right_eyeshaper_0_2_1_ctrl",
    "Right_eyeshaper_0_1_4_ctrl",
    "Right_eyeshaper_0_1_3_ctrl",
    "Right_eyeshaper_0_1_2_ctrl",
    "Right_eyeshaper_4_3_4_ctrl",
    "Right_eyeshaper_4_3_3_ctrl",
    "Right_eyeshaper_4_3_2_ctrl",
    "Right_eyeshaper_4_3_1_ctrl",
    "Right_eyeshaper_4_2_4_ctrl",
    "Right_eyeshaper_4_2_3_ctrl",
    "Right_eyeshaper_4_2_2_ctrl",
    "Right_eyeshaper_4_2_1_ctrl",
    "Right_eyeshaper_4_1_4_ctrl",
    "Right_eyeshaper_4_1_3_ctrl",
    "Right_eyeshaper_4_1_2_ctrl",
    "Right_eyeshaper_4_1_1_ctrl",
    "Right_eyeshaper_4_0_4_ctrl",
    "Right_eyeshaper_4_0_3_ctrl",
    "Right_eyeshaper_4_0_2_ctrl",
    "Right_eyeshaper_4_0_1_ctrl",
    "Right_eyeshaper_2_0_4_ctrl",
    "Right_eyeshaper_2_0_3_ctrl",
    "Right_eyeshaper_2_0_2_ctrl",
    "Right_eyeshaper_2_0_1_ctrl",
    "Right_eyeshaper_1_0_4_ctrl",
    "Right_eyeshaper_1_0_3_ctrl",
    "Right_eyeshaper_1_0_2_ctrl",
    "Right_eyeshaper_1_0_1_ctrl",
    "Right_eyeshaper_3_0_4_ctrl",
    "Right_eyeshaper_3_0_3_ctrl",
    "Right_eyeshaper_3_0_2_ctrl",
    "Right_eyeshaper_3_0_1_ctrl",
    "Right_eyeshaper_4_4_0_ctrl",
    "Right_eyeshaper_3_0_0_ctrl",
    "Right_eyeshaper_2_4_0_ctrl",
    "Right_eyeshaper_2_3_0_ctrl",
    "Right_eyeshaper_2_2_0_ctrl",
    "Right_eyeshaper_1_4_0_ctrl",
    "Right_eyeshaper_1_3_0_ctrl",
    "Right_eyeshaper_1_2_0_ctrl",
    "Right_eyeshaper_2_1_0_ctrl",
    "Right_eyeshaper_2_0_0_ctrl",
    "Right_eyeshaper_0_3_0_ctrl",
    "Right_eyeshaper_1_1_0_ctrl",
    "Right_eyeshaper_1_0_0_ctrl",
    "Right_eyeshaper_0_1_0_ctrl",
    "Right_eyeshaper_0_0_0_ctrl",
    "Right_eyeshaper_0_2_0_ctrl",
    "Right_eyeshaper_4_3_0_ctrl",
    "Right_eyeshaper_4_2_0_ctrl",
    "Right_eyeshaper_4_0_0_ctrl",
    "Right_eyeshaper_3_4_0_ctrl",
    "Right_eyeshaper_3_3_0_ctrl",
    "Right_eyeshaper_4_1_0_ctrl",
    "Right_eyeshaper_3_2_0_ctrl",
    "Right_eyeshaper_3_1_0_ctrl",
    "Right_eyeshaper_1_1_4_ctrl",
    "Right_eyeshaper_2_1_4_ctrl",
    "Right_eyeshaper_3_1_4_ctrl",
    "Right_eyeshaper_3_2_4_ctrl",
    "Right_eyeshaper_3_3_4_ctrl",
    "Right_eyeshaper_2_3_4_ctrl",
    "Right_eyeshaper_1_3_4_ctrl",
    "Right_eyeshaper_1_2_4_ctrl",
    "Right_eyeshaper_2_2_4_ctrl",
    "Facial_GUI1",
    "Facial_GUI_ParentSpace",
    "Facial_GUI",
    "Facial_Under_Eye_Visibility_Params",
    "Facial_Under_Eyebrow_Visibility_Params",
    "Facial_Under_Mouth_Visibility_Params",
    "Iris_Spec_Offset_Param",
    "Jaw_Locals",
    "Jaw_Move",
    "Jaw_Open_Params",
    "Jaw_Open",
    "Jaw",
    "Jaw_Slide",
    "Left_CheekCtrl",
    "Left_Cheek_Inflate",
    "Left_Cheek_Switcher",
    "Left_Cheekbone",
    "Left_Curl_Corner",
    "Left_Depressor",
    "Left_Ear",
    "Left_Expressions_Params",
    "Left_Eye_Bulge",
    "Left_Eye_Mid_Wave",
    "Left_Eye_Pinch",
    "Left_Eye",
    "Left_Eye_Up_Cheek",
    "Left_Eye_Wave",
    "Left_Eyebrow_1",
    "Left_Eyebrow_2",
    "Left_Eyebrow_3",
    "Left_Eyebrow_4",
    "Left_Eyebrow_Ext_Rot",
    "Left_Eyebrow_In_UpDown",
    "Left_Eyebrow_Int_Rot",
    "Left_Eyebrow_Mid_UpDown",
    "Left_Eyebrow_Out_UpDown",
    "Left_Eyebrow",
    "Left_Iris",
    "Left_Levator",
    "Left_Lip_Zip",
    "Left_Lips_Cheek_Switcher",
    "Left_LowerBlink",
    "Left_LowerLid",
    "Left_Mouth_Lowerlip_1",
    "Left_Mouth",
    "Left_Mouth_Upperlip_1",
    "Left_Nostril",
    "Left_Nostril_Up",
    "Left_Pinch_Corner",
    "Left_Puff",
    "Left_Pupil",
    "Left_Riso",
    "Left_SoftEye_Switcher",
    "Left_Spec_Direction",
    "Left_Spec_Target",
    "Left_Specular",
    "Left_Specular_SwitcherIP_Patch_1",
    "Left_Tongue_1",
    "Left_Tongue_2",
    "Left_Tongue_3",
    "Left_Under_Cheek_GeoCns",
    "Left_Under_Cheek",
    "Left_Under_Cheekbone_1_GeoCns",
    "Left_Under_Cheekbone_1",
    "Left_Under_Cheekbone_2_GeoCns",
    "Left_Under_Cheekbone_2",
    "Left_Under_Cheekbone_3_GeoCns",
    "Left_Under_Cheekbone_3",
    "Left_Under_Chin_GeoCns",
    "Left_Under_Chin",
    "Left_Under_Eye_Bot_1_GeoCns",
    "Left_Under_Eye_Bot_1",
    "Left_Under_Eye_Bot_2_GeoCns",
    "Left_Under_Eye_Bot_2",
    "Left_Under_Eye_Bot_3_GeoCns",
    "Left_Under_Eye_Bot_3",
    "Left_Under_Eye_Ext_GeoCns",
    "Left_Under_Eye_Ext",
    "Left_Under_Eye_Int_GeoCns",
    "Left_Under_Eye_Int",
    "Left_Under_Eye_Top_1_GeoCns",
    "Left_Under_Eye_Top_1",
    "Left_Under_Eye_Top_2_GeoCns",
    "Left_Under_Eye_Top_2",
    "Left_Under_Eye_Top_3_GeoCns",
    "Left_Under_Eye_Top_3",
    "Left_Under_Eyebrow_Bot_GeoCns",
    "Left_Under_Eyebrow_Bot",
    "Left_Under_Eyelid_Top_1_GeoCns",
    "Left_Under_Eyelid_Top_1",
    "Left_Under_Eyelid_Top_2_GeoCns",
    "Left_Under_Eyelid_Top_2",
    "Left_Under_Eyelid_Top_3_GeoCns",
    "Left_Under_Eyelid_Top_3",
    "Left_Under_Eyelid_Top_4_Bot",
    "Left_Under_Eyelid_Top_4_GeoCns",
    "Left_Under_Lip_Bot_1_GeoCns",
    "Left_Under_Lip_Bot_1",
    "Left_Under_Lip_Bot_2_GeoCns",
    "Left_Under_Lip_Bot_2",
    "Left_Under_Lip_Bot_Center_GeoCns",
    "Left_Under_Lip_Bot_Center",
    "Left_Under_Lip_Corner_1_GeoCns",
    "Left_Under_Lip_Corner",
    "Left_Under_Lip_Top_1_GeoCns",
    "Left_Under_Lip_Top_1",
    "Left_Under_Lip_Top_2_GeoCns",
    "Left_Under_Lip_Top_2",
    "Left_Under_Lip_Top_Center_GeoCns",
    "Left_Under_Lip_Top_Center",
    "Left_Under_Nostril_GeoCns",
    "Left_Under_Nostril",
    "Left_UpperBlink",
    "Left_UpperLid",
    "Left_Zygo",
    "Mouth_Lowerlip_Center",
    "Mouth_Move",
    "Mouth",
    "Mouth_Tweak",
    "Mouth_Upperlip_Center",
    "NoseTip",
    "Puff_Lowerlip",
    "Puff_Upperlip",
    "Right_AttenuationCheekBone_ParentSwitcher1",
    "Right_CheekCtrl",
    "Right_Cheek_Inflate",
    "Right_Cheek_Switcher",
    "Right_Cheekbone",
    "Right_Curl_Corner",
    "Right_Depressor",
    "Right_Ear",
    "Right_Expressions_Params",
    "Right_Eye_Bulge",
    "Right_Eye_Mid_Wave",
    "Right_Eye_Pinch",
    "Right_Eye",
    "Right_Eye_Up_Cheek",
    "Right_Eye_Wave",
    "Right_Eyebrow_1",
    "Right_Eyebrow_2",
    "Right_Eyebrow_3",
    "Right_Eyebrow_4",
    "Right_Eyebrow_Ext_Rot",
    "Right_Eyebrow_In_UpDown",
    "Right_Eyebrow_Int_Rot",
    "Right_Eyebrow_Mid_UpDown",
    "Right_Eyebrow_Out_UpDown",
    "Right_Eyebrow",
    "Right_Iris",
    "Right_Levator",
    "Right_Lip_Zip",
    "Right_Lips_Cheek_Switcher",
    "Right_LowerBlink",
    "Right_LowerLid",
    "Right_Mouth_Lowerlip_1",
    "Right_Mouth",
    "Right_Mouth_Upperlip_1",
    "Right_Nostril",
    "Right_Nostril_Up",
    "Right_Pinch_Corner",
    "Right_Puff",
    "Right_Pupil",
    "Right_Riso",
    "Right_SoftEye_Switcher",
    "Right_Spec_Direction",
    "Right_Spec_Target",
    "Right_Specular",
    "Right_Specular_SwitcherIP_Patch_1",
    "Right_Tongue_1",
    "Right_Tongue_2",
    "Right_Tongue_3",
    "Right_Under_Cheek_GeoCns",
    "Right_Under_Cheek",
    "Right_Under_Cheekbone_1_GeoCns",
    "Right_Under_Cheekbone_1",
    "Right_Under_Cheekbone_2_GeoCns",
    "Right_Under_Cheekbone_2",
    "Right_Under_Cheekbone_3_GeoCns",
    "Right_Under_Cheekbone_3",
    "Right_Under_Eye_Bot_1_GeoCns",
    "Right_Under_Eye_Bot_1",
    "Right_Under_Eye_Bot_2_GeoCns",
    "Right_Under_Eye_Bot_2",
    "Right_Under_Eye_Bot_3_GeoCns",
    "Right_Under_Eye_Bot_3",
    "Right_Under_Eye_Ext_GeoCns",
    "Right_Under_Eye_Ext",
    "Right_Under_Eye_Int_GeoCns",
    "Right_Under_Eye_Int",
    "Right_Under_Eye_Top_1_GeoCns",
    "Right_Under_Eye_Top_1",
    "Right_Under_Eye_Top_2_GeoCns",
    "Right_Under_Eye_Top_2",
    "Right_Under_Eye_Top_3_GeoCns",
    "Right_Under_Eye_Top_3",
    "Right_Under_Eyebrow_Bot_GeoCns",
    "Right_Under_Eyebrow_Bot",
    "Right_Under_Eyelid_Top_1_GeoCns",
    "Right_Under_Eyelid_Top_1",
    "Right_Under_Eyelid_Top_2_GeoCns",
    "Right_Under_Eyelid_Top_2",
    "Right_Under_Eyelid_Top_3_GeoCns",
    "Right_Under_Eyelid_Top_3",
    "Right_Under_Eyelid_Top_4_Bot",
    "Right_Under_Eyelid_Top_4_GeoCns",
    "Right_Under_Lip_Bot_1_GeoCns",
    "Right_Under_Lip_Bot_1",
    "Right_Under_Lip_Bot_2_GeoCns",
    "Right_Under_Lip_Bot_2",
    "Right_Under_Lip_Corner_1_GeoCns",
    "Right_Under_Lip_Corner",
    "Right_Under_Lip_Top_1_GeoCns",
    "Right_Under_Lip_Top_1",
    "Right_Under_Lip_Top_2_GeoCns",
    "Right_Under_Lip_Top_2",
    "Right_Under_Nostril_GeoCns",
    "Right_Under_Nostril",
    "Right_UpperBlink",
    "Right_UpperLid",
    "Right_Zygo",
    "TKUnder",
    "Spec_Aim_ParentSpace",
    "Spec_Aim",
    "Sticky_Lip",
    "Tongue_1",
    "Tongue_2",
    "Tongue_3",
    "Tongue_FUI",
    "Tongue_Params",
    "Tongue",
    "Top_Teeth",
]

#tko.setDeactivator("Global_SRT.Body_LOD", inRootsKeep=schema_low, inName="body_low", inDeactivateValue=1)
#tko.setDeactivator("Global_SRT.Facial_LOD", inRootsRemove=schema_facial_unders, inName="facial_mid", inDeactivateValue=1)

#facial_mid_cond = tkn.condition(pc.PyNode("Global_SRT.Facial_LOD"), 1, "==", 0.0, 1.0, inName="facial_mid_cond")
#deformers = pc.ls(type=["ffd", "shrinkWrap"])
#for deform in deformers:
#    facial_mid_cond >> deform.envelope

#tko.setDeactivator("Global_SRT.Facial_LOD", inRootsRemove=schema_facial, inName="facial_low", inDeactivateValue=2)

#Diagnose
tko.diagnose()

#Evaluate
tko.evaluate()


#ConvertExpressions
tko.convertExpressions()

#PTTransforms
tko.deletePTTransforms()

#ConvertConstraints
tko.replaceConstraints()

#PTAttributes
tko.deletePTAttributes("(.+_OSCAR_Attributes|.+_TK_CtrlsChannelsDic|.+_TK_CtrlsDic|.+_TK_KeySets|.+_TK_KeySetsTree|.+_TK_ParamsDic)$")

#UselessTransforms
tko.deleteUselessTransforms("(.+_OSCAR_Attributes|.+_TK_CtrlsChannelsDic|.+_TK_CtrlsDic|.+_TK_KeySets|.+_TK_KeySetsTree|.+_TK_ParamsDic)$")

#UnusedNodes++
tkc.deleteUnusedNodes()
"""


#BENCHMARKING
#---------------------------------------------------
def diagnose(inProps=["Objects",
        "Transforms",
        "Locators",
        "Joints",
        "Curves",
        "Meshes",
        "Meshes Points",
        "Expressions",
        "Expressions Characters",
        "Constraints",
        "parentConstraints",
        "aimConstraints",
        "orientConstraints",
        "scaleConstraints",
        "pointConstraints",
        "poleVectorConstraints",
        "motionPaths",
        "follicles",
        "Utilities",
        "Deformers",
        "skinClusters",
        "blendshapes",
        "clusters",
        "lattices",
        "wraps",
        "shrinkWraps"]):
    
    values = tkdev.Tester("SomeRig", "SomePath").getValues(*inProps)

    for i in range(len(inProps)):
        print "{0} : {1}".format(inProps[i],values[i])

def evaluate(inFrames=100):
    fps = 100.0 / tkc.benchIt(tkdev.evaluate, inFrames)[0]
    print "{0} fps, {1} ms".format(fps, 1000.0/fps)

    return fps

def createConstraintsBenchmark(inNumber=100):
    objs = []

    for i in range(inNumber):
        objs.append(pc.spaceLocator())

    xOffset = 1.0
    i = 0
    for obj in objs:
        if i > 0:
            #move
            #obj.tx.set(i*xOffset)
            
            #parent
            tkc.constrain(obj, objs[i-1], "Position")
            #matrixPointConstrain(obj, objs[i-1], [0.0,0.0,0.0])
        i += 1

#tkc
def getAllConnections(inAttr):
    cons = inAttr.listConnections(source=True, destination=True, plugs=True, connections=True)

    if len(cons) == 0 and inAttr.isCompound():
        childAttrs = inAttr.children()
        for childAttr in childAttrs:
            cons.extend(childAttr.listConnections(source=True, destination=True, plugs=True, connections=True))

    return cons

#tkc
def getConstraintConnections(inCns):
    cons = []

    if inCns.type() == "parentConstraint":
        cons.extend(getAllConnections(inCns.target[0].targetOffsetTranslate))
        cons.extend(getAllConnections(inCns.target[0].targetOffsetRotate))
        cons.extend(getAllConnections(inCns.nodeState))
    elif inCns.type() == "scaleConstraint":
        cons.extend(getAllConnections(inCns.offset))

    return cons

def matrixConstrain(inTarget, inSource, inScale=True, inOffsetT=None, inOffsetR=None, inOffsetS=None, inForceOffset=False):
    createdNodes = []

    matrixOut = None

    offsets = [inOffsetT or [0.0,0.0,0.0], inOffsetR or [0.0,0.0,0.0], inOffsetS or [1.0,1.0,1.0]]

    autodetect = inOffsetT is None or inOffsetR is None or (inScale and inOffsetS is None)
    if autodetect:
        offset = pc.group(name=inSource + "_offset_MARKER", empty=True)
        inSource.addChild(offset)
        tkc.matchTRS(offset, inTarget)
    
        offsets = [inOffsetT or list(offset.getTranslation()), inOffsetR or list(ozms.getPymelRotation(offset)), inOffsetS or list(offset.getScale())]

        pc.delete(offset)

    offseted = inForceOffset or not (tkc.listsBarelyEquals(offsets[0], [0.0,0.0,0.0]) and
                tkc.listsBarelyEquals(offsets[1], [0.0,0.0,0.0]) and
                tkc.listsBarelyEquals(offsets[2], [1.0,1.0,1.0]))

    if offseted:
        composeOut = tkn.composeMatrix(offsets[0], offsets[1], offsets[2])
        createdNodes.append(composeOut.node())
        matrixOut = tkn.mul(composeOut, inSource.worldMatrix[0])#offset_Mul.matrixSum
        createdNodes.append(matrixOut.node())
    else:
        matrixOut = inSource.worldMatrix[0]

    invertMul = tkn.mul(matrixOut, inTarget.parentInverseMatrix[0])
    createdNodes.append(invertMul.node())

    decompMatrix = tkn.decomposeMatrix(invertMul)
    createdNodes.append(decompMatrix)

    decompMatrix.outputTranslate >> inTarget.translate
    decompMatrix.outputRotate >> inTarget.rotate
    if inScale:
        decompMatrix.outputScale >> inTarget.scale

    return createdNodes

#Does not work with offsets !!
def matrixPointConstrain(inTarget, inSource, inOffsetT=None, inForceOffset=False):
    createdNodes = []

    matrixOut = None

    offset = inOffsetT or [0.0,0.0,0.0]

    autodetect = inOffsetT is None
    if autodetect:
        offset = pc.group(name=inSource + "_offset_MARKER", empty=True)
        offsetChild = pc.group(name=inSource + "_offset_MARKER_CHILD", empty=True)

        offset.addChild(offsetChild)
        tkc.matchT(offset, inSource)
        tkc.matchT(offsetChild, inTarget)

        offset = list(offsetChild.getTranslation())

        pc.delete(offset)

    offseted = inForceOffset or not tkc.listsBarelyEquals(offset, [0.0,0.0,0.0])

    if offseted:
        composeOut = tkn.composeMatrix(offset, [0.0,0.0,0.0], [1.0,1.0,1.0])
        createdNodes.append(composeOut.node())
        matrixOut = tkn.mul(composeOut, inSource.worldMatrix[0])#offset_Mul.matrixSum
        createdNodes.append(matrixOut.node())
    else:
        matrixOut = inSource.worldMatrix[0]

    invertMul = tkn.mul(matrixOut, inTarget.parentInverseMatrix[0])
    createdNodes.append(invertMul.node())

    decompMatrix = tkn.decomposeMatrix(invertMul)
    createdNodes.append(decompMatrix)

    decompMatrix.outputTranslate >> inTarget.translate

    return createdNodes

CONS_LINKS = {
    "targetOffsetTranslate":"inputTranslate",

    "targetOffsetTranslateX":"inputTranslateX",
    "targetOffsetTranslateY":"inputTranslateY",
    "targetOffsetTranslateZ":"inputTranslateZ",

    "targetOffsetRotate":"inputRotate",
    "targetOffsetRotateX":"inputRotateX",
    "targetOffsetRotateY":"inputRotateY",
    "targetOffsetRotateZ":"inputRotateZ",

    "offset":"inputScale",
    "offsetX":"inputScaleX",
    "offsetY":"inputScaleY",
    "offsetZ":"inputScaleZ",

    "nodeState":"nodeState"
}

def replaceConstraint(inConstraint, inTarget=None, inSource=None):

    inSource = inSource or tkc.getConstraintTargets(inConstraint)[0]
    inTarget = inTarget or tkc.getConstraintOwner(inConstraint)[0]

    offsets = [list(inConstraint.target[0].targetOffsetTranslate.get()), list(inConstraint.target[0].targetOffsetRotate.get()), [1.0,1.0,1.0]]

    cons = getConstraintConnections(inConstraint)
    sclCons = []

    pc.delete(inConstraint)

    haveScale = False
    constraints = tkc.getConstraints(inTarget)
    for constraint in constraints:
        if constraint.type() == "scaleConstraint" and inSource in tkc.getConstraintTargets(constraint):
            haveScale = True
            #Search if weight is not 1.0 and/or connected
            udParams = tkc.getParameters(constraint)
            for udParam in udParams:
                if re.match("^w[0-9]+$", udParam):#It's a weight !
                    if not tkc.doubleBarelyEquals(constraint.attr(udParam).get(), 1.0) or len(constraint.attr(udParam).listConnections()) > 1: 
                        #print "!! haveScale = False",constraint.attr(udParam).get(), tkc.doubleBarelyEquals(constraint.attr(udParam).get(), 1.0), constraint.attr(udParam).listConnections()
                        haveScale = False

            if haveScale:
                #offsets[2] = list(constraint.offset.get())
                sclCons = getConstraintConnections(constraint)
                pc.delete(constraint)

            break

    haveConnections = (len(cons) + len(sclCons)) > 0

    #createdNodes = matrixConstrain(inTarget, inSource, haveScale, offsets[0], offsets[1], offsets[2], inForceOffset=haveConnections)
    createdNodes = matrixConstrain(inTarget, inSource, haveScale, inForceOffset=haveConnections)

    #Re-link offset connections
    if haveConnections:
        for linkInput, linkOutput in cons:
            inputName = linkInput.split(".")[-1]
            newInput = CONS_LINKS.get(inputName)
            if not newInput is None:
                linkOutput >> createdNodes[0].attr(newInput) if not "nodeState" in inputName else createdNodes[-1].attr(newInput)
            else:
                pc.warning("Can't reconnect {0} >> {1}".format(linkOutput, linkInput))

        for linkInput, linkOutput in sclCons:
            newInput = CONS_LINKS.get(linkInput.split(".")[-1])
            if not newInput is None:
                if not "nodeState" in linkOutput.name():
                    linkOutput >> createdNodes[0].attr(newInput)
            else:
                pc.warning("Can't reconnect {0} >> {1}".format(linkOutput, linkInput))

def replaceConstraints(inDebugFolder=None):
    debugCounter = 0

    if not inDebugFolder is None:
        if not os.path.isdir(inDebugFolder):
            os.makedirs(inDebugFolder)
        else:
            tkc.emptyDirectory(inDebugFolder)
        print "DEBUG MODE ACTIVATED ({})".format(inDebugFolder)
        tkc.capture(os.path.join(inDebugFolder, "{0:04d}_ORIGINAL.jpg".format(debugCounter)), start=1, end=1, width=1280, height=720)
        debugCounter = debugCounter + 1

    parentCons = pc.ls(type=["parentConstraint","pointConstraint"])
    print "Constraints", len(parentCons)
    
    replaced = []

    for parentCon in parentCons:
        conName = parentCon.name().replace("|", "(")

        owner = tkc.getConstraintOwner(parentCon)[0]
        targets = tkc.getConstraintTargets(parentCon)

        if len(targets) == 0:
            print "Cannot replace (NO TARGETS): ",parentCon,"on",owner
            continue

        if parentCon.type() == "pointConstraint":
            #TODO : replace anyway
            if len(targets) > 1:
                #print "Cannot replace (multiple targets): ",parentCon,"on",owner
                continue

            #TODO : replace anyway
            if len(parentCon.offset.listConnections()) > 0:
                #print "Cannot replace (position offset with connections): ",parentCon,"on",owner
                continue

            #TODO : replace anyway
            if not tkc.listsBarelyEquals(parentCon.offset.get(), [0.0,0.0,0.0]):
                #print "Cannot replace (position with offset): ",parentCon,"on",owner
                continue

            replaced.append(owner.name())
            pc.delete(parentCon)
            matrixPointConstrain(owner, targets[0], [0.0,0.0,0.0])
        elif parentCon.type() == "parentConstraint":
            #TODO : replace anyway
            if len(targets) > 1:
                #print "Cannot replace (multiple targets): ",parentCon,"on",owner
                continue

            #TODO : replace if joint have no scale ?
            if owner.type() == "joint":
                #print "Cannot replace (owner is joint): ",parentCon,"on",owner
                continue

            if not tkc.listsBarelyEquals(list(owner.rp.get()), [0.0,0.0,0.0]):
                print "Cannot replace (owner have scale pivots): ",parentCon,"on",owner
                continue

            targetPivots=False
            for target in targets:
                if not tkc.listsBarelyEquals(list(target.rp.get()), [0.0,0.0,0.0]):
                    print "Cannot replace (target {0} have scale pivots): ".format(target),parentCon,"on",owner,
                    targetPivots=True

            if targetPivots:
                continue

            replaced.append(owner.name())
            replaceConstraint(parentCon, owner, targets[0])

        #Reparent
        #------------------
        """
        constraints = tkc.getConstraints(owner)
        for constraint in constraints:
            if constraint.type() == "scaleConstraint" and targets[0] in tkc.getConstraintTargets(constraint):
                pc.delete(constraint)
                break

        pc.delete(parentCon)

        #Unlock the Transforms
        attrs = ["tx","ty", "tz", "rx","ry","rz","sx","sy","sz"]
        for attr in attrs:
           owner.attr(attr).setLocked(False) 

        if owner.getParent() != targets[0]:
            targets[0].addChild(owner)
        """
        #------------------

        if not inDebugFolder is None:
            tkc.capture(os.path.join(inDebugFolder, "{0:04d}_replaceCns_{1}.jpg".format(debugCounter, conName)), start=1, end=1, width=1280, height=720)
            debugCounter = debugCounter + 1

    print "replaced",len(replaced),replaced

#EXPRESSION REPLACEMENT
#---------------------------------------------------
#tkn.convertExpression(inExpr)
def convertExpressions():
    invalidItems = ["sin(",
                    "cos(",
                    "noise(",
                    "if("]

    replaced = []

    exprs = pc.ls(type="expression")
    print "exprs", len(exprs)
    for expr in exprs:
        #print "Expr",expr
        #print "-cons",len(expr.listConnections()),expr.listConnections()

        valid = True
        exprString = expr.getString()
        #print "-exprString",exprString

        for invalidItem in invalidItems:
            if invalidItem in exprString:
                valid = False
                break

        if valid:
            replaced.append(expr.name())
            tkn.convertExpression(expr)
        else:
            print "Cannot replace (invalid item): ",expr,exprString

    print "replaced",len(replaced),replaced


def getUselessTransforms(inExceptPattern=None):
    uselessTransforms = []
    
    ts = pc.ls( exactType=["transform", "joint"])
    
    print len(ts)
    
    for t in ts:
        #Pattern
        if not inExceptPattern is None and re.match(inExceptPattern, t.name()):
            continue

        #Children
        if len(t.getChildren()) > 0:
            continue

        #Connections
        if len(t.listConnections(source=False, destination=True)) > 0:
            print t,t.listConnections(source=False, destination=True)
            continue
    
        uselessTransforms.append(t)
        
    return uselessTransforms

def deleteUselessTransforms(inExceptPattern=None):
    MAXITER = 7

    deleted = []

    uts = getUselessTransforms(inExceptPattern)
    
    if len(uts) == 0:
        return 0

    curIter = 0

    while curIter < MAXITER:
        nUts = len(uts)
        deleted.extend([n.name() for n in uts])
        pc.delete(uts)
        uts = getUselessTransforms(inExceptPattern)

        if nUts == 0:
            print "deleteUselessTransforms",len(uts),uts
            return deleted

    print "deleteUselessTransforms",len(deleted),deleted
    pc.warning("delete useless trasforms : Max iterations reached ({0})".format(MAXITER))
    return deleted

def deletePTTransforms(inExceptPattern=None):
    uselessTransforms = []
    
    ts = pc.ls(exactType=["transform"])
    
    print len(ts)
    
    for t in ts:
        #Pattern
        if not inExceptPattern is None and re.match(inExceptPattern, t.name()):
            continue

        #Children
        if len([c for c in t.getChildren() if not c.type().endswith("Constraint")]) > 0:
            continue

        #Constraints
        cons = [c for c in tkc.getConstraints(t) if c.type() in ["parentConstraint", "scaleConstraint"]]
        otherCons = [c for c in tkc.getConstraintsUsing(t) if c.type() in ["parentConstraint", "scaleConstraint"]]
        
        if len(cons) > 0 and len(otherCons) > 0:
            if len(list(set(t.listConnections()))) != len(list(set(cons + otherCons))):
                print "PTTransforms : Other connections :",t,list(set(t.listConnections())),list(set(cons + otherCons))
                continue

            if len(getConstraintConnections(inCns)) > 0:
                print "PTTransforms : Input connections :",getConstraintConnections(inCns)
                continue

            outputCons = False
            for otherCon in otherCons:
                if len(getConstraintConnections(otherCon)) > 0:
                    print "PTTransforms : Output connections :",getConstraintConnections(otherCon)
                    outputCons=True
                    break

            if outputCons:
                continue

            uselessTransforms.append(t.name())

    print "deletePTTransforms",len(uselessTransforms),uselessTransforms
    return uselessTransforms

def deletePTAttributes(inExceptPattern=None, inDropStaticValues=True):
    uselessAttributes = []
    
    ts = pc.ls(exactType=["transform"])
    
    for t in ts:
        #Pattern
        if not inExceptPattern is None and re.match(inExceptPattern, t.name()):
            continue

        uds = tkc.getParameters(t)
        for ud in uds:

            attr = t.attr(ud)

            #Connections
            cons = attr.listConnections(source=True, destination=False, plugs=True)
            otherCons = attr.listConnections(source=False, destination=True, plugs=True)

            haveExpr = False
            for con in cons + otherCons:
                if con.node().type() == "expression":
                    print "Attribute '{0}' still have expression ('{1}') !".format(attr, con.node())
                    haveExpr = True
                    break

            if haveExpr:
                continue

            if len(cons) > 0 and len(otherCons) > 0:
                uselessAttributes.append(attr.name())

                for otherCon in otherCons:
                    lock = otherCon.isLocked()
                    if lock:
                        otherCon.setLocked(False)

                    cons[0] >> otherCon

                    if lock:
                        otherCon.setLocked(True)

                try:
                    pc.deleteAttr(attr)
                    uselessAttributes.append(attr.name())
                except:
                    pass

            elif inDropStaticValues and not tkRig.isControl(t):
                if len(otherCons) > 0:
                    allSettable = True
                    #Should be useless to filter expressions because filtered before
                    """
                    for otherCon in otherCons:
                        if otherCon.node().type() == "expression":
                            allSettable = False
                            break
                    """

                    if allSettable:
                        value = attr.get()
                        for otherCon in otherCons:
                            attr.disconnect(otherCon)
                            otherCon.set(value)

                        try:
                            pc.deleteAttr(attr)
                            uselessAttributes.append(attr.name())
                        except:
                            pass
                else:
                    try:
                        pc.deleteAttr(attr)
                        uselessAttributes.append(attr.name())
                    except:
                        pass

    print "deletePTAttributes",len(uselessAttributes),uselessAttributes

    return uselessAttributes

"""
def setDeactivator(inAttr, inNodesToKeep, inName=None, inDeactivateValue=1, inIgnoreTags=["hd"], inHide=True):
    nodesRootToRemove, nodesRootToKeep, allGivenNodes = tkRig.OscarSplitNodes(inNodesToKeep)

    setDeactivatorOnRemoved(inAttr, nodesRootToRemove, inName, inDeactivateValue=inDeactivateValue, inIgnoreTags=inIgnoreTags, inHide=inHide)
"""
def deactivate(inObj, inCond=None, inCondVis=None, inExceptTypes=None, inKeepVisible=False, inRecur=0):
    #print " " * inRecur + "DEACTIVATE",inObj,inCond,inCondVis,inExceptTypes

    if isinstance(inObj, pc.nodetypes.Transform):
        if not inKeepVisible:
            if inCondVis is None:
                inObj.v.set(0)
            else:
                tkn.conditionAnd(inObj.v, inCondVis)
        
        for shape in inObj.getShapes():
            deactivate(shape, inCond=inCond, inCondVis=inCondVis, inExceptTypes=inExceptTypes, inKeepVisible=inKeepVisible, inRecur=inRecur+1)

    elif isinstance(inObj, pc.nodetypes.Mesh):
        if not inKeepVisible:
            if inCondVis is None:
                inObj.v.set(0)
            else:
                tkn.conditionAnd(inObj.v, inCondVis)

        defs = pc.listHistory(inObj, gl=True, pdo=True, lf=True, f=False, il=2)
        if defs != None:
            for deform in defs:
                if pc.attributeQuery("envelope" , node=deform, exists=True):
                    if inExceptTypes is None or not deform.type() in inExceptTypes:
                        deactivate(deform, inCond=inCond, inCondVis=inCondVis, inExceptTypes=inExceptTypes, inKeepVisible=inKeepVisible, inRecur=inRecur+1)
                        deactivate(deform, inCond=inCond, inCondVis=inCondVis, inExceptTypes=inExceptTypes, inKeepVisible=inKeepVisible, inRecur=inRecur+1)
    # else:# else:
    #    pc.warning("Don't know how to deactivate {0} of type {1}".format(inObj, type(inObj)))

    if inCond is None:
        inObj.nodeState.set(2)
    else:
        tkn.conditionAnd(inObj.nodeState, inCond)

def setDeactivator(inAttr, inRootsKeep=None, inRootsRemove=None, inDeactivateValue=1, inName=None, inReplaceDeformers=None, inIgnoreTags=["hd"], inPolyReduceMin=0, inPolyReduceMax=0, inHide=True):
    if inRootsKeep is None and inRootsRemove is None:
        raise ValueError("inRootsKeep and inRootsRemove can't both be None !")

    inRoots = inRootsKeep or inRootsRemove
    nodesRootToRemove, nodesRootToKeep, allGivenNodes = [None,None,None]

    if not inRootsKeep is None:
        nodesRootToRemove, nodesRootToKeep, allGivenNodes = tkRig.OscarSplitNodes(inRootsKeep)
    else:
        nodesRootToKeep, nodesRootToRemove, allGivenNodes = tkRig.OscarSplitNodes(inRootsRemove)
        """
        if len(inRoots) > 0 and isinstance(inRoots[0], basestring):
            rootsStrs = inRoots[:]
            inRoots = []

            notFound = []

            for rootsStr in rootsStrs:
                nodeName = tkRig.getRootName(rootsStr)
                if pc.objExists(nodeName):
                    inRoots.append(pc.PyNode(nodeName))
                else:
                    notFound.append(rootsStr)

            if len(notFound) > 0:
                print "Some given nodes cannot be found :",notFound
        """

    print "nodesRootToRemove",len(nodesRootToRemove),nodesRootToRemove
    print "nodesRootToKeep",len(nodesRootToKeep),nodesRootToKeep
    print "nodesNotFound",len(allGivenNodes),allGivenNodes

    inAttr = tkc.getNode(inAttr)

    cond = tkn.condition(inAttr, inDeactivateValue, "==", 2.0, 0.0)
    condVis = tkn.condition(inAttr, inDeactivateValue, "!=", 1.0, 0.0)

    inverse = tkn.reverse(cond)
    inverseVis = tkn.reverse(condVis)

    #if inHide:
    for root in nodesRootToRemove:
        tkn.conditionAnd(root.v, condVis)

    cns, cnsAll = tkc.getExternalConstraints(nodesRootToRemove, inSource=True, inDestination=True, inReturnAll=True, inProgress=True)

    externalOwners = []
    print " Constraints :",len(cns),cns

    for cn in cnsAll:
        """
        if cn in cns:
            owner = tkc.getConstraintOwner(cn)
            ownerRoot = tkc.getParent(owner[0], root=True)

            #print "  -cn",cn
            #print "  -owner",owner
            #print "  -ownerRoot",ownerRoot

            if not ownerRoot in nodesRootToRemove:
                externalOwners.append(ownerRoot)
                if len(tkc.getConstraintTargets(cn)) > 1:
                    pc.warning("BLENDED " + cn.name())
                    continue
        """
        #DEACTTIVATE CONSTRAINT
        deactivate(cn, cond, condVis)

    if len(externalOwners) > 0:
        pc.warning("External Owners : {0} {1}".format(len(externalOwners), externalOwners))

    origGeos = [m.getParent() for m in pc.ls(type="mesh") if len(m.getParent().v.listConnections()) > 0 or m.getParent().v.get()]

    deformersToReplace = {}
    #Find deformers to replace

    removedDeformers = []
    skinClusters = []
    for nodeRoot in nodesRootToRemove:
        deformers = nodeRoot.getChildren(allDescendents=True, type='joint')
        removedDeformers.extend(deformers)

        for deformer in deformers:
            #deformersToReplace[deformer.name()] = deformer.getTranslation(space="world")
            skinClusters.extend(deformer.listConnections(type="skinCluster"))

    skinClusters = list(set(skinClusters))
    geos = [skin.getGeometry()[0] for skin in skinClusters]

    deformersRemaining = []

    #Find remaining deformers 
    for nodeRoot in nodesRootToKeep:
        deformers = nodeRoot.getChildren(allDescendents=True, type='joint')
        deformersRemaining.extend([n.name() for n in deformers])

    replacingDeformers = []

    if not inReplaceDeformers is None:
        for replaceDeformer in inReplaceDeformers:
            print " deformersRemaining","replaceDeformer",replaceDeformer, replaceDeformer,"deformersRemaining",len(deformersRemaining),deformersRemaining
            if replaceDeformer in deformersRemaining:
                replacingDeformers.append(pc.PyNode(replaceDeformer))

    print " deformersRemaining",len(deformersRemaining),deformersRemaining

    print " replacingDeformers",len(replacingDeformers),replacingDeformers

    #Find and add "siblings" geo (geo deformed by an existing one)
    siblingsGeos = []
    for geo in geos:
        histos = geo.listHistory(future=True, type="mesh")
        for histo in histos:
            """
            if len([d for d in histo.listHistory() if d.type() in ["blendShape", "skinCluster"]]) > 0:
                print " siblingsGeo have other deformers :",histo,[d for d in histo.listHistory() if d.type() in ["blendShape", "skinCluster"]]
                continue
            """
            if not histo in siblingsGeos and not histo in geos:
                siblingsGeos.append(histo)
                print " siblingsGeo OK :",geo,"=>",histo

    geos.extend(siblingsGeos)

    proxies = []

    for geo in geos:
        print "-",geo,geo.type()
        """
        if not geo.type() == "mesh":
            continue
        """
        transform = geo.getParent()
        underGeo = None
        isOrphanGeo = True
        keptTopInfs = []

        geoSkin = tkc.getSkinCluster(geo)
        if not geoSkin is None:
            keptTopInfs = geoSkin.influenceObjects()

            remainingTopInfs = [inf for inf in keptTopInfs if inf.name() in deformersRemaining]

            otherDeformers = [d for d in geo.listHistory() if d.type() in ["blendShape", "wrap"]]


            #'Live' blendshape targets
            #------------------------------------
            blendShapes = geo.listHistory(type="blendShape")
            for blendShape in blendShapes:
                if pc.objExists(blendShape):
                    cons = pc.listConnections(blendShape, source=True, destination=False, type="mesh")
                    for con in cons:
                        skin = tkc.getSkinCluster(con)
                        if not skin is None:
                            BSinfs = skin.influenceObjects()
                            #Determine if most of the influences are kept or dropped
                            keptInfs = [inf for inf in BSinfs if inf.name() in deformersRemaining]

                            if len(keptInfs) > len(remainingTopInfs):
                                underGeo = con
                                break

            isOrphanGeo = len(remainingTopInfs) == 0 and len(replacingDeformers) == 0 and underGeo is None

        print " isOrphanGeo",isOrphanGeo
        print " underGeo",underGeo
        print " inIgnoreTags",len(inIgnoreTags),inIgnoreTags
        print " len(tkt.getTags([geo], inIgnoreTags))",len(tkt.getTags([transform], inIgnoreTags))
        print " visible",tkc.isVisibleAfterAll(geo)
        isSafe = False

        if inIgnoreTags is None or len(inIgnoreTags) == 0 or len(tkt.getTags([transform], inIgnoreTags)) == 0:
            if not isOrphanGeo and tkc.isVisibleAfterAll(geo):
                infsToRemove = []

                for inf in keptTopInfs:
                    if inf in removedDeformers:
                        infsToRemove.append(inf)

                #print " infs",len(keptTopInfs),keptTopInfs
                #print " infsToRemove",len(infsToRemove),infsToRemove

                if geo.type() == "mesh":
                    #Create geometry proxy
                    #------------------------
                    dupe = tkc.getNode(tkc.duplicateAndClean(geo.name(), inTargetName=("$REF_dupe" if inName is None else "$REF_" + inName), inMuteDeformers=False))
                    
                    if inPolyReduceMin < inPolyReduceMax:
                        tkc.polyReduceComplexity(dupe, inPolyReduceMin, inPolyReduceMax)

                    proxies.append(dupe)

                    infsLeft = len(keptTopInfs) - len(infsToRemove)

                    newSkin = None
                    if not underGeo is None:
                        print " Proxy",dupe,"created with gator under",underGeo,"approach" 
                        tkc.gator([dupe], underGeo)
                        newSkin = tkc.getSkinCluster(dupe)
                        dupeInfs = newSkin.influenceObjects()

                        infsToRemove = []

                        for inf in dupeInfs:
                            if inf in removedDeformers:
                                infsToRemove.append(inf)

                        pc.skinCluster(newSkin,e=True,ri=infsToRemove)
                    elif infsLeft == 0:
                        if len(replacingDeformers) > 0:
                            print " Proxy",dupe,"created with replacingDeformers approach",dupe,replacingDeformers
                            newSkin = pc.skinCluster(dupe,replacingDeformers, name=dupe.name() + "_skinCluster", toSelectedBones=True)
                        elif len(deformersRemaining) > 0:
                            print " Proxy",dupe,"created with deformersRemaining approach" ,dupe,deformersRemaining
                            newSkin = pc.skinCluster(dupe,deformersRemaining, name=dupe.name() + "_skinCluster", toSelectedBones=True)
                    else:
                        print " Proxy",dupe,"created with gator",geo,"approach" 
                        tkc.gator([dupe], geo)
                        newSkin = tkc.getSkinCluster(dupe)
                        pc.skinCluster(newSkin,e=True,ri=infsToRemove)

                    tkRig.hammerCenter(dupe)
                    pc.skinPercent(newSkin, dupe, pruneWeights=0.005 )
                    removedInfs = tkc.removeUnusedInfs(newSkin)

                    deactivate(dupe, inverse, inverseVis, inKeepVisible=not inHide)
                    #------------------------

        #Connect "old" geometry
        #------------------------
        deactivate(geo, cond, condVis, inKeepVisible=not inHide or not tkc.isVisibleAfterAll(geo))

        if underGeo is not None:
            #DEACTTIVATE GEOMETRY
            deactivate(underGeo, cond, condVis, inKeepVisible=not inHide or not tkc.isVisibleAfterAll(underGeo))

    print "cns",len(cns),cns
    print "cnsAll",len(cnsAll),cnsAll
    print "geos",len(geos),geos
    print "proxies",len(proxies),proxies

def createLazySwitch(inConstrained, inConstrainers, inAttrName="switch"):
    parent = inConstrained.getParent()
    
    if pc.attributeQuery(inAttrName , node=parent, exists=True):
        pc.deleteAttr(parent.attr(inAttrName))

    param = tkc.addParameter(parent, inAttrName, "enum;"+":".join([n.name() for n in inConstrainers]))
    
    switchAttr = parent.attr(inAttrName)
    
    i = 0
    oldTransform = None
    for inConstrainer in inConstrainers:
        name = "{0}_LazyTo_{1}".format(inConstrainer,inConstrained)
        if pc.objExists(name):
            pc.delete(name)

        constrainedNode = pc.group(name=name, empty=True)
        parent.addChild(constrainedNode)    
        tkc.matchTRS(constrainedNode, inConstrained)
        
        cns = tkc.constrain(constrainedNode, inConstrainer, "parent")
        
        if not oldTransform is None:
            t, r, s = oldTransform
            
            #Translation
            oldCond = None
            oldConds = inConstrained.t.listConnections(type=["condition", "unitConversion"], source=True, destination=False)
            print "oldConds",inConstrained.t,oldConds
            for possibleOldCond in oldConds:
                if possibleOldCond.type() == "condition":
                    oldCond = possibleOldCond
                    break
                else:
                    possibleOldConds = possibleOldCond.input.listConnections(type=["condition"], source=True, destination=False)
                    print "possibleOldConds",possibleOldCond.input,possibleOldConds
                    if len(possibleOldConds) > 0:
                        oldCond = possibleOldConds[0]
                        break

            if oldCond is None:
                tkn.condition(switchAttr, i, "==", constrainedNode.t, t) >> inConstrained.t
            else:
                print "Old cond for",inConstrained.t,oldCond 
                tkn.condition(switchAttr, i, "==", constrainedNode.t, oldCond.outColor) >> inConstrained.t

            #Rotation
            oldCond = None
            oldConds = inConstrained.r.listConnections(type=["condition", "unitConversion"], source=True, destination=False)
            print "oldConds",inConstrained.r,oldConds
            for possibleOldCond in oldConds:
                if possibleOldCond.type() == "condition":
                    oldCond = possibleOldCond
                    break
                else:
                    possibleOldConds = possibleOldCond.input.listConnections(type=["condition"], source=True, destination=False)
                    print "possibleOldConds",possibleOldCond.input,possibleOldConds
                    if len(possibleOldConds) > 0:
                        oldCond = possibleOldConds[0]
                        break

            if oldCond is None:
                tkn.condition(switchAttr, i, "==", constrainedNode.r, r) >> inConstrained.r
            else:
                print "Old cond for",inConstrained.r,oldCond 
                tkn.condition(switchAttr, i, "==", constrainedNode.r, oldCond.outColor) >> inConstrained.r

        tkn.conditionAnd(cns.nodeState, tkn.condition(switchAttr, i, "!=", 2, 0))

        oldTransform = (constrainedNode.t, constrainedNode.r, constrainedNode.s)
        i += 1

    return switchAttr
"""
def getExternalLinks(inRoot):
    CONSTRAINT_TYPES = ["parentConstraint", "pointConstraint", "scaleConstraint", "orientConstraint"]

    extInputs = []
    extOutputs = []

    if not isinstance(inRoot,(list,tuple)):
        inRoot = [inRoot]

    allChildren = []
    for root in inRoot:
        allChildren.extend(root.getChildren(allDescendents=True, type="transform"))
    allChildren.extend(inRoot)

    for child in allChildren:
        if child.type() in CONSTRAINT_TYPES:
            continue

        cons = child.listConnections(source=True, destination=False, plugs=True, connections=True)
        for con in cons:
            if con[0].type() in CONSTRAINT_TYPES or con[1].type() in CONSTRAINT_TYPES:
                continue

            if con[1].type() == "transform" and con[1].node() in allChildren:
                continue

            extInputs.append(con)

        cons = child.listConnections(source=False, destination=True, plugs=True, connections=True)
        for con in cons:
            if con[0].type() in CONSTRAINT_TYPES or con[1].type() in CONSTRAINT_TYPES:
                continue

            if con[0].type() == "transform" and con[0].node() in allChildren:
                continue

            extOutputs.append(con)

    return (extInputs, extOutputs)

def getExternalLinks3(inRoot):
    CONSTRAINT_TYPES = ["parentConstraint", "pointConstraint", "scaleConstraint", "orientConstraint"]

    extInputs = []
    extOutputs = []

    if not isinstance(inRoot,(list,tuple)):
        inRoot = [inRoot]

    allChildren = []
    for root in inRoot:
        allChildren.extend(root.getChildren(allDescendents=True, type="transform"))
    allChildren.extend(inRoot)

    for child in allChildren:
        if child.type() in CONSTRAINT_TYPES:
            continue

        cons = child.listHistory(future=True)
        for con in cons:
            if con.type() in CONSTRAINT_TYPES:
                continue

            if con.type() == "transform" and con in allChildren:
                continue

            extInputs.append(con)

        cons = child.listHistory()
        for con in cons:
            if con[0].type() in CONSTRAINT_TYPES or con[1].type() in CONSTRAINT_TYPES:
                continue

            if con[0].type() == "transform" and con[0].node() in allChildren:
                continue

            extOutputs.append(con)

    return (extInputs, extOutputs)



setActivator("Left_Hand_ParamHolder_Main_Ctrl.IkFk")



cns = tkc.getExternalConstraints(pc.selected()[0])



uts = getUselessTransforms("(.+_OSCAR_Attributes|.+_TK_CtrlsChannelsDic|.+_TK_CtrlsDic|.+_TK_KeySets|.+_TK_KeySetsTree|.+_TK_ParamsDic)$")
print len(uts),uts

print deleteUselessTransforms("(.+_OSCAR_Attributes|.+_TK_CtrlsChannelsDic|.+_TK_CtrlsDic|.+_TK_KeySets|.+_TK_KeySetsTree|.+_TK_ParamsDic)$")
"""
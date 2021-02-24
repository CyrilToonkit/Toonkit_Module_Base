import pymel.core as pc

import tkRig

def do(inNs):
    IK_To_FK = [
        {"Left_Arm_FK_1":
            {"matchR":"Left_Arm_Bone_0",
             "sx":"(TK_Left_Arm_Root_SetupParameters.Left_Arm_Bone0_length/TK_Left_Arm_Root_SetupParameters.Left_Arm_Bone0_Init)*TK_Left_Arm_Root_SetupParameters.Left_Arm_Scale",
             "t":[0,0,0]}
        },
        {"Left_Arm_FK_2":
            {"matchR":"Left_Arm_Bone_1",
             "sx":"(TK_Left_Arm_Root_SetupParameters.Left_Arm_Bone1_length/TK_Left_Arm_Root_SetupParameters.Left_Arm_Bone1_Init)*TK_Left_Arm_Root_SetupParameters.Left_Arm_Scale",
             "t":[0,0,0]}
        },
        {"Left_Hand":
            {"match":"Left_Arm_FK_Eff_IKREF"}
        },
        {"Left_Arm_Middle":
            {"match":"Left_Arm_Middle"}
        }
    ]

    FK_To_IK = [
        {"Left_Arm_IK":
            {"match":"Left_Arm_IK_FKREF",
            "Bone0_Scale":"Left_Arm_FK_1.sx",
            "Bone1_Scale":"Left_Arm_FK_2.sx",
            "Roll":0,
            "Slide":0,
            "StickJoint":0,
            "Stretch":1,
            "Squash":0}
        },
        {"Left_Arm_upV":
            {"matchPV":("Left_Arm_FK_1", "Left_Arm_FK_2", "TK_Left_Arm_FK_Bone_1_Eff")}
        },
        {"Left_Arm_Middle":
            {"match":"Left_Arm_Middle"}
        }
    ]

    tkRig.toggleInPlace("Left_Arm_ParamHolder.IKFK", 0.0, IK_To_FK, 1.0, FK_To_IK, inNs)
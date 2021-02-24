import pymel.core as pc

import tkRig

def do(inNs):
    IK_To_FK = [
        {"Right_Arm_FK_1":
            {"matchR":"Right_Arm_Bone_0",
             "sx":"(TK_Right_Arm_Root_SetupParameters.Right_Arm_Bone0_length/TK_Right_Arm_Root_SetupParameters.Right_Arm_Bone0_Init)*TK_Right_Arm_Root_SetupParameters.Right_Arm_Scale",
             "t":[0,0,0]}
        },
        {"Right_Arm_FK_2":
            {"matchR":"Right_Arm_Bone_1",
             "sx":"(TK_Right_Arm_Root_SetupParameters.Right_Arm_Bone1_length/TK_Right_Arm_Root_SetupParameters.Right_Arm_Bone1_Init)*TK_Right_Arm_Root_SetupParameters.Right_Arm_Scale",
             "t":[0,0,0]}
        },
        {"Right_Hand":
            {"match":"Right_Arm_FK_Eff_IKREF"}
        },
        {"Right_Arm_Middle":
            {"match":"Right_Arm_Middle"}
        }
    ]

    FK_To_IK = [
        {"Right_Arm_IK":
            {"match":"Right_Arm_IK_FKREF",
            "Bone0_Scale":"Right_Arm_FK_1.sx",
            "Bone1_Scale":"Right_Arm_FK_2.sx",
            "Roll":0,
            "Slide":0,
            "StickJoint":0,
            "Stretch":1,
            "Squash":0}
        },
        {"Right_Arm_upV":
            {"matchPV":("Right_Arm_FK_1", "Right_Arm_FK_2", "TK_Right_Arm_FK_Bone_1_Eff")}
        },
        {"Right_Arm_Middle":
            {"match":"Right_Arm_Middle"}
        }
    ]

    tkRig.toggleInPlace("Right_Arm_ParamHolder.IKFK", 0.0, IK_To_FK, 1.0, FK_To_IK, inNs)
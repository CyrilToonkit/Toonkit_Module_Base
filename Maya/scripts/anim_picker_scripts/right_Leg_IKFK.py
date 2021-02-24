import pymel.core as pc

import tkRig

def do(inNs):
    IK_To_FK = [
        {"Right_Leg_FK_1":
            {"matchR":"Right_Leg_Bone_0",
             "sx":"(TK_Right_Leg_Root_SetupParameters.Right_Leg_Bone0_length/TK_Right_Leg_Root_SetupParameters.Right_Leg_Bone0_Init)*TK_Right_Leg_Root_SetupParameters.Right_Leg_Scale",
             "t":[0,0,0]}
        },
        {"Right_Leg_FK_2":
            {"matchR":"Right_Leg_Bone_1",
             "sx":"(TK_Right_Leg_Root_SetupParameters.Right_Leg_Bone1_length/TK_Right_Leg_Root_SetupParameters.Right_Leg_Bone1_Init)*TK_Right_Leg_Root_SetupParameters.Right_Leg_Scale",
             "t":[0,0,0]}
        },
        {"Right_Foot_FK_1":
            {"match":"Right_Leg_FK_Eff_IKREF"}
        },
        {"Right_Foot_FK_2":
            {"match":"Right_IK_Tip"}
        },
        {"Right_Leg_Middle":
            {"match":"Right_Leg_Middle"}
        }
    ]

    FK_To_IK = [
        {"Right_Leg_FK_1":
            {"check":("abs(Right_Leg_FK_1.translateX) <= 0.002", "Right_Leg_FK_1 translateX is not 0"),
             "check":("abs(Right_Leg_FK_1.translateY) <= 0.002", "Right_Leg_FK_1 translateY is not 0"),
             "check":("abs(Right_Leg_FK_1.translateZ) <= 0.002", "Right_Leg_FK_1 translateZ is not 0"),}
        },
        {"Right_Leg_IK":
            {"match":"Right_Leg_IK_FKREF",
            "Bone0_Scale":"Right_Leg_FK_1.sx",
            "Bone1_Scale":"Right_Leg_FK_2.sx",
            "Roll":0,
            "StickJoint":0,
            "Stretch":1,
            "Squash":0,
            "Bank":0,
            "SoftDistance":0,
            "FootRoll":0,
            "ToeRaise":0
            }
        },
        {"Right_Tip":
            {"match":"Right_Foot_Tip_FKREF"}
        },
        {"Right_Foot_Reverse":
            {"match":"Right_Foot_Reverse_0_FKREF"}
        },
        {"Right_IK_Tip":
            {"match":"Right_Foot_FK_2"}
        },
        {"Right_Leg_upV":
            {"matchPV":("Right_Leg_FK_1", "Right_Leg_FK_2", "TK_Right_Leg_FK_Bone_1_Eff")}
        },
        {"Right_Leg_Middle":
           {"match":"Right_Leg_Middle"}
        }
    ]

    tkRig.toggleInPlace("Right_Leg_ParamHolder.IKFK", 0.0, IK_To_FK, 1.0, FK_To_IK, inNs)
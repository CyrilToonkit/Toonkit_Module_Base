import pymel.core as pc
import tkRig

def do(inNs):
    IK_To_FK = [
        {"Left_Leg_FK_1":
            {"matchR":"Left_Leg_Bone_0",
             "sx":"(TK_Left_Leg_Root_SetupParameters.Left_Leg_Bone0_length/TK_Left_Leg_Root_SetupParameters.Left_Leg_Bone0_Init)*TK_Left_Leg_Root_SetupParameters.Left_Leg_Scale",
             "t":[0,0,0]}
        },
        {"Left_Leg_FK_2":
            {"matchR":"Left_Leg_Bone_1",
             "sx":"(TK_Left_Leg_Root_SetupParameters.Left_Leg_Bone1_length/TK_Left_Leg_Root_SetupParameters.Left_Leg_Bone1_Init)*TK_Left_Leg_Root_SetupParameters.Left_Leg_Scale",
             "t":[0,0,0]}
        },
        {"Left_Foot_FK_1":
            {"match":"Left_Leg_FK_Eff_IKREF"}
        },
        {"Left_Foot_FK_2":
            {"match":"Left_IK_Tip"}
        },
        {"Left_Leg_Middle":
            {"match":"Left_Leg_Middle"}
        }
    ]

    FK_To_IK = [
        {"Left_Leg_FK_1":
            {"check":("abs(Left_Leg_FK_1.translateX) <= 0.002", "Left_Leg_FK_1 translateX is not 0"),
             "check":("abs(Left_Leg_FK_1.translateY) <= 0.002", "Left_Leg_FK_1 translateY is not 0"),
             "check":("abs(Left_Leg_FK_1.translateZ) <= 0.002", "Left_Leg_FK_1 translateZ is not 0"),}
        },
        {"Left_Leg_IK":
            {"match":"Left_Leg_IK_FKREF",
            "Bone0_Scale":"Left_Leg_FK_1.sx",
            "Bone1_Scale":"Left_Leg_FK_2.sx",
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
        {"Left_Tip":
            {"match":"Left_Foot_Tip_FKREF"}
        },
        {"Left_Foot_Reverse":
            {"match":"Left_Foot_Reverse_0_FKREF"}
        },
        {"Left_IK_Tip":
            {"match":"Left_Foot_FK_2"}
        },
        {"Left_Leg_upV":
            {"matchPV":("Left_Leg_FK_1", "Left_Leg_FK_2", "TK_Left_Leg_FK_Bone_1_Eff")}
        },
        {"Left_Leg_Middle":
           {"match":"Left_Leg_Middle"}
        }
    ]

    tkRig.toggleInPlace("Left_Leg_ParamHolder.IKFK", 0.0, IK_To_FK, 1.0, FK_To_IK, inNs)
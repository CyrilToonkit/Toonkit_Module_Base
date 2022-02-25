import pymel.core as pc
import tkRig

def do(inNs):
    IK_To_FK = [
        {"Neck_FK_0":
            {"match":"Neck_Start"}
        },
       {"Neck_FK_1":
        {"match":"Neck_IK_StartHandle"}
        },
       {"Neck_FK_2":
        {"match":"Neck_IK_Middle"}
        },
       {"Neck_FK_3":
        {"match":"Neck_IK_EndHandle"}
        },
       {"Neck_FK_4":
        {"match":"Neck_End"}
        },
    ]

    FK_To_IK = [
       {"Neck_End":
        {"match":"Neck_FK_4"}
        },
       {"Neck_IK_Middle":
        {"match":"Neck_FK_2"}
        },
       {"Neck_IK_StartHandle":
        {"match":"Neck_FK_1"}
        },
       {"Neck_IK_EndHandle":
        {"match":"Neck_FK_3"}
        },
        {"Neck_Start":
            {"match":"Neck_FK_0"}
        },
    ]

  tkRig.toggleInPlace("Neck_ParamHolder.IKFK", 0.0, IK_To_FK, 1.0, FK_To_IK, inNs)
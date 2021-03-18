import pymel.core as pc
import tkRig

def do(inNs):
    IK_To_FK = [
        {"Spine_FK_1":
            {"match":"Hips_IK"}
        },
       {"Spine_FK_2":
        {"match":"Spine_IK_StartHandle"}
        },
       {"Spine_FK_3":
        {"match":"Spine_IK_Middle"}
        },
       {"Spine_FK_4":
        {"match":"Spine_IK_EndHandle"}
        },
       {"Spine_FK_5":
        {"match":"Chest_IK"}
        },
    ]

    FK_To_IK = [
       {"Chest_IK":
        {"match":"Spine_FK_5"}
        },
       {"Spine_IK_Middle":
        {"match":"Spine_FK_3"}
        },
       {"Spine_IK_StartHandle":
        {"match":"Spine_FK_2"}
        },
       {"Spine_IK_EndHandle":
        {"match":"Spine_FK_4"}
        },
    ]

    tkRig.toggleInPlace("Spine_ParamHolder.IKFK", 0.0, IK_To_FK, 1.0, FK_To_IK, inNs)
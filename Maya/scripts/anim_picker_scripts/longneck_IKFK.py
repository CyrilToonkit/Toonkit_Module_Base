import pymel.core as pc
import tkRig

def do(inNs):
    IK_To_FK = [
        {"Neck_FK_0_Offset":
            {"t":[0,0,0],
            "r":[0,0,0],
            "s":[1,1,1]}
        },
        {"Neck_FK_0":
            {"match":"Neck_Start_Offset"}
        },
        {"Neck_FK_0":
            {"match":"Neck_Start"}
        },

        {"Neck_FK_1_Offset":
            {"t":[0,0,0],
            "r":[0,0,0],
            "s":[1,1,1]}
        },
       {"Neck_FK_1":
        {"match":"Neck_IK_StartHandle_Offset"}
        },
       {"Neck_FK_1":
        {"match":"Neck_IK_StartHandle"}
        },
        
        {"Neck_FK_2_Offset":
            {"t":[0,0,0],
            "r":[0,0,0],
            "s":[1,1,1]}
        },
       {"Neck_FK_2":
        {"match":"Neck_IK_Middle_Offset"}
        },
       {"Neck_FK_2":
        {"match":"Neck_IK_Middle"}
        },
        
        {"Neck_FK_3_Offset":
            {"t":[0,0,0],
            "r":[0,0,0],
            "s":[1,1,1]}
        },
       {"Neck_FK_3":
        {"match":"Neck_IK_EndHandle_Offset"}
        },
       {"Neck_FK_3":
        {"match":"Neck_IK_EndHandle"}
        },
        
        {"Neck_FK_4_Offset":
            {"t":[0,0,0],
            "r":[0,0,0],
            "s":[1,1,1]}
        },
       {"Neck_FK_4":
        {"match":"Neck_End_Offset"}
        },
       {"Neck_FK_4":
        {"match":"Neck_End"}
        },
    ]

    FK_To_IK = [
        {"Neck_End_Offset":
            {"t":[0,0,0],
            "r":[0,0,0],
            "s":[1,1,1]}
        },
       {"Neck_End":
        {"match":"Neck_FK_4_Offset"}
        },
       {"Neck_End":
        {"match":"Neck_FK_4"}
        },
        
        {"Neck_IK_Middle_Offset":
            {"t":[0,0,0],
            "r":[0,0,0],
            "s":[1,1,1]}
        },
       {"Neck_IK_Middle":
        {"match":"Neck_FK_2_Offset"}
        },
       {"Neck_IK_Middle":
        {"match":"Neck_FK_2"}
        },
        
        {"Neck_IK_StartHandle_Offset":
            {"t":[0,0,0],
            "r":[0,0,0],
            "s":[1,1,1]}
        },
       {"Neck_IK_StartHandle":
        {"match":"Neck_FK_1_Offset"}
        },
       {"Neck_IK_StartHandle":
        {"match":"Neck_FK_1"}
        },
        
        {"Neck_IK_EndHandle_Offset":
            {"t":[0,0,0],
            "r":[0,0,0],
            "s":[1,1,1]}
        },
       {"Neck_IK_EndHandle":
        {"match":"Neck_FK_3_Offset"}
        },
       {"Neck_IK_EndHandle":
        {"match":"Neck_FK_3"}
        },
        
        {"Neck_Start_Offset":
            {"t":[0,0,0],
            "r":[0,0,0],
            "s":[1,1,1]}
        },
        {"Neck_Start":
            {"match":"Neck_FK_0_Offset"}
        },
        {"Neck_Start":
            {"match":"Neck_FK_0"}
        },
    ]

    tkRig.toggleInPlace("Neck_ParamHolder.IKFK", 0.0, IK_To_FK, 1.0, FK_To_IK, inNs)
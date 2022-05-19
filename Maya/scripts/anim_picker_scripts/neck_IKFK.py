import pymel.core as pc
import tkRig

def do(inNs):
  IK_To_FK = [
      {"Neck_FK_1_Offset":
            {"t":[0,0,0],
            "r":[0,0,0],
            "s":[1,1,1]}
        },
      {"Neck_FK_1":
          {"match":"Neck_IK_Start_Offset"}
      },
      {"Neck_FK_1":
          {"match":"Neck_IK_Start"}
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

      {"Head_FK_Offset":
            {"t":[0,0,0],
            "r":[0,0,0],
            "s":[1,1,1]}
        },
     {"Head_FK":
      {"match":"Head_IK"}
      },
     {"Head_FK":
      {"match":"Head_IK_Offset"}
      },
  ]

  FK_To_IK = [
     {"Head_IK":
      {"match":"Head_FK"}
      },
     {"Neck_IK_Middle":
      {"match":"Neck_FK_2"}
      },
      {"Neck_IK_Start":
          {"match":"Neck_FK_1"}
      },
  ]

  tkRig.toggleInPlace("Neck_ParamHolder.IKFK", 0.0, IK_To_FK, 1.0, FK_To_IK, inNs)
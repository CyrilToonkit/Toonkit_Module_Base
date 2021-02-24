import pymel.core as pc

import tkRig

def do(inNs):
  IK_To_FK = [
      {"Neck_FK_1":
          {"match":"Neck_IK_Start"}
      },
     {"Neck_FK_2":
      {"match":"Neck_IK_Middle"}
      },
     {"Head_FK":
      {"match":"Head_IK"}
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
import tkRig
import pymel.core as pc
tkRig.createSuperIK(pc.selected()[0], pc.selected()[1], pc.selected()[2], pc.selected()[3])
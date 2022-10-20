import tkBlendShapes as tkb
import pymel.core as pc

for obj in pc.selected():
    tkb.rebuildAllTargets(obj, inProgress=True)
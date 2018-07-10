"""
Parent a shape (instanciate) under a transform node
Select two objects, the shape to parent first, then the transform and run
"""
import pymel.core as pc

sel = pc.selected()

if len(sel) == 2 and sel[0].type() != "transform" and sel[1].type() == "transform":
	pc.parent(sel[0], sel[1], shape=True, add=True)
else:
	pc.warning("Please select two objects, the shape to parent first, then the transform")
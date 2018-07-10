"""
Reorder a shape by forcing it to the bottom
Select a shape to reorder and run
"""
import pymel.core as pc
import maya.cmds as mc

def sendShapeToBack(inShape):
    shapeParent = inShape.getParent()
    sillyGrp = pc.group(empty=True, world=True)
    
    newShape = pc.parent(inShape, sillyGrp, shape=True, add=True)
    mc.parent(inShape.name(), shape=True, removeObject=True)
    pc.parent(newShape, shapeParent, shape=True, add=True)
    
    pc.delete(sillyGrp)

sel = pc.selected()

if len(sel) == 1 and sel[0].type() != "transform":
	sendShapeToBack(sel[0])
else:
	pc.warning("Please select a shape to reorder")
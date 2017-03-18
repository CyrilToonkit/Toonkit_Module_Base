import tkMayaCore as tkc
import pymel.core as pc

sel = pc.ls(sl=True)
if len(sel) > 1:
    newDef = sel[-1]
    oldDefs = sel[:-1]

    tkc.replaceDeformers(oldDefs, newDef)
else:
    pc.error("Please select at least two objects, old deformer(s) first, then new deformer !")
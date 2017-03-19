import pymel.core as pc

import tkMayaCore as tkc

sel = pc.ls(sl=True)
result = None
if len(sel) >= 3:
    curves = sel[:len(sel) - 2]
    refCurve = sel[-2]
    refParent = sel[-1]

    #Verify inputs
    for crv in curves:
        shp = crv.getShape()
        if shp == None or shp.type() != "nurbsCurve":
            pc.error("Spread Deform : WRONG INPUTS !\nDeformed objects must be nurbsCurves.")

    shp = refCurve.getShape()
    if shp == None or shp.type() != "nurbsCurve":
        pc.error("Spread Deform : WRONG INPUTS !\nReference object must be a nurbsCurve.")

    if tkc.getSkinCluster(refCurve) == None:
        pc.error("Spread Deform : WRONG INPUTS !\nReference curve must be skinned (before last selected object).")

    if refParent.type() != "transform":
        pc.error("Spread Deform : WRONG INPUTS !\nReference parent must be a transform node.")

    tkc.applySpreadDeforms(curves, refCurve, refParent)
else:
    pc.error("Spread Deform : WRONG INPUTS !\nPlease select any number of curves to be deformed, then the reference curve with skinCluster and reference parent for skinned curve.")

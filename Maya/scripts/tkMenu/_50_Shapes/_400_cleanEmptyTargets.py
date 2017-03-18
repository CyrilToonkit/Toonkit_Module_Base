import tkBlendShapes
import pymel.core as pc

selObjs = pc.ls(sl=True)

for selObj in selObjs:
    if selObj.type() != "blendShape":
        bsOps = pc.ls(pc.listHistory(selObj, gl=True, pdo=True, lf=True, f=False, il=2), type="blendShape")
        for bsOp in bsOps:
            tkBlendShapes.cleanUpBlendShapeWeights(bsOp.name())
    else:
        tkBlendShapes.cleanUpBlendShapeWeights(selObj.name())
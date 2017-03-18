import tkBlendShapes
import pymel.core as pc

def duplicateClean(*args):#I'll take muteDeformers:bool
    muteDeformers = False

    if len(args) > 1:
        muteDeformers = args[1]

    selObjs = pc.ls(sl=True)

    for selObj in selObjs:
        tkBlendShapes.duplicateAndClean(selObj.name(), "$REF_dupe", muteDeformers)

duplicateClean()
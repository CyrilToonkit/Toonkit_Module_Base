import tkBlendShapes
import pymel.core as pc

def matchPointPositions(*args):#I'll take scope:string(All, LeftOnly, RightOnly), treshold:float
    sel = pc.ls(sl=True)
    if len(sel) > 1:
        sided = False
        rightToLeft=False
        treshold=2.0

        if len(args) > 1:
            if args[1] == "Right only":
                sided = True
                rightToLeft = True
            elif args[1] == "Left only":
                sided = True

        if len(args) > 2:
            treshold = args[2]

        for selObj in sel[:-1]:
            tkBlendShapes.matchPointPositions(sel[-1], selObj, sided, rightToLeft, treshold)

    else:
        pc.error("Please select at least two objects (any number of meshes to receive point positions, then a \"Reference\" mesh) !")

matchPointPositions()
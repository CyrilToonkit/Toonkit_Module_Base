import maya.cmds as cmds
import pymel.core as pc

import tkMayaCore as tkc
import tkBlendShapes

def wmIndexedToFlat(inWm, inNbPoints=None, inGeo=None, inNeutralValue=0.0):
    assert inNbPoints is not None or inGeo is not None, "inNbPoints and inGeo can't both be None !"

    if inNbPoints is None:
        inNbPoints = tkc.getPointsCount(tkc.getNode(inGeo))

    return [inWm.get(i, inNeutralValue) for i in range(inNbPoints)]

def wmFlatToIndexed(inWm, inNeutralValue=0.0):
    return {i:v for i, v in enumerate(inWm) if v != inNeutralValue}

def matchPointPositions(*args):#I'll take scope:string(All, LeftOnly, RightOnly), treshold:float

    richSel = tkc.getSoftSelections()

    if len(richSel) > 1:
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

        for richSelObj, richSelComps in richSel[:-1]:
            if sided or richSelComps is None:
                tkBlendShapes.matchPointPositions(tkc.getNode(richSel[-1][0]), tkc.getNode(richSelObj), sided, rightToLeft, treshold)
            else:
                tkBlendShapes._matchPointPositions(tkc.getNode(richSel[-1][0]), tkc.getNode(richSelObj), inMap=wmIndexedToFlat(richSelComps, inGeo=richSelObj))
    else:
        pc.error("Please select at least two objects (any number of meshes to receive point positions, then a \"Reference\" mesh) !")

matchPointPositions()
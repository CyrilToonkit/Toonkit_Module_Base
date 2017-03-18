import tkMayaCore as tkc
import pymel.core as pc

def gator(*args):#I'll take strictCopy:bool, matchMatrices:bool
    sel = pc.ls(sl=True)
    if len(sel) > 1:
        strictCopy = False
        if len(args) > 1:
            strictCopy = args[1]
        copyMatrices = False
        if len(args) > 2:
            copyMatrices = args[2]

        tkc.gator(sel[:-1], sel[-1], copyMatrices, strictCopy)
    else:
        pc.warning("Please select at least two objects (any number of meshes to receive weights, then a \"Reference\" mesh) !")

gator()
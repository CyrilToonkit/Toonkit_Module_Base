"""
Exports constraints on selected objects to a *.cns file
"""
import tkMayaCore as tkc
import maya.cmds as mc
import pymel.core as pc

sel = pc.selected()

if len(sel) == 0:
    pc.warning("Please select objects with constraints !")
else:
    path = mc.fileDialog2(caption="Save your constraints file", fileFilter="cns file (*.cns)(*.cns)", dialogStyle=2, fileMode=0)

    if path != None and len(path) > 0:
        path = path[0]

    if path == None:
        pc.warning("No valid output path given !")
    else:
        tkc.storeConstraints(sel, inRemove=False, inPath=path)
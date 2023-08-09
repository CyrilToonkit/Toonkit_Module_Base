"""
Exports constraints on selected object to a *.cns file
"""
import maya.cmds as mc

import tkMayaCore as tkc
import pymel.core as pc

sel = pc.selected()

if len(sel) == 0:
    pc.warning("Please select an object !")
else:
    path = mc.fileDialog2(caption="Save your connections file", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=0)

    if path != None and len(path) > 0:
        path = path[0]

    if path == None:
        pc.warning("No valid output path given !")
    else:
        tkc.storeConnections(sel[0], inPath=path)
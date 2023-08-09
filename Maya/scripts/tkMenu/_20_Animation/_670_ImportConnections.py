"""
Import animation from ".ma" file saved with "Export Anim" feature
"""
import maya.cmds as mc

import tkRig
import pymel.core as pc

sel = pc.selected()

if len(sel) == 0:
    pc.warning("Please select an object !")
else:
    path = pc.fileDialog2(caption="Load your connections file", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=1)

    if path != None and len(path) > 0:
        path = path[0]

    if path == None:
        pc.warning("No valid output path given !")
    else:
        tkc.loadConnections(path, sel[0])
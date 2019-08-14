"""
Exports constraints on selected objects to a *.cns file
"""
import tkMayaCore as tkc
import maya.cmds as mc
import pymel.core as pc

sel = pc.selected()

if len(sel) == 0:
    pc.warning("Please select root objects !")
else:
    path = mc.fileDialog2(caption="Save your constraints file", fileFilter="cns file (*.cns)(*.cns)", dialogStyle=2, fileMode=0)

    if path != None and len(path) > 0:
        path = path[0]

    if path == None:
        pc.warning("No valid output path given !")
    else:
    	cns = tkc.getExternalConstraints(sel, inSource=True, inDestination=False, returnObjects=False, inReturnAll=False, inProgress=False)
        tkc.storeConstraintsList(cns, inRemove=False, inPath=path)
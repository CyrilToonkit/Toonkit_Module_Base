import tkMayaCore as tkc
import maya.cmds as mc
import pymel.core as pc

path = mc.fileDialog2(caption="Load your constraints file", fileFilter="cns file (*.cns)(*.cns)", dialogStyle=2, fileMode=1)

if path != None and len(path) > 0:
    path = path[0]

if path is None:
    pc.warning("Invalid file !")
else:
    sel = pc.selected() if len(pc.selected()) > 0 else None
    tkc.loadConstraints(path, sel, inRemoveOld=True, inMaintainOffset=True)
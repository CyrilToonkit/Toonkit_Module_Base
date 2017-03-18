import tkMayaCore as tkc
import pymel.core as pc

sel = pc.selected()

if len(sel) == 0:
    pc.warning("Please select deformer(s) (influence(s)), geometries or skinCluster(s) to reset bind poses !")
    return

if sel[0].type() == "joint":
    tkc.setRefPoses(sel, inSkins=None)
elif sel[0].type() == "skinCluster":
    setRefPoses(None, sel)
else:
    skins = []
    for selNode in sel:
        skin = tkc.getSkinCluster(selNode)
        if skin != None:
            skins.append(skin)

    if len(skins) == 0:
        pc.warning("No skinCLusters found on selected objects !")
        return

    tkc.setRefPoses(None, skins)
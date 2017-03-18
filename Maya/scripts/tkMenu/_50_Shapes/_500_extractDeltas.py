import tkMayaCore as tkc
import pymel.core as pc

sel = pc.ls(sl=True)
result = None
if len(sel) == 2:
    if tkc.getSkinCluster(sel[0]) != None:
        result = pc.extractDeltas(s=sel[0].name(), c=sel[1].name())
    else:
        pc.error("Extract deltas : WRONG INPUTS !\nFirst selected mesh must have a skinCluster.")
else:
    pc.error("Extract deltas : WRONG INPUTS !\nPlease select skinned mesh first, then undeformed ('freezed') corrective mesh.")

if result != None:
    print "Corrective blendshape created : " + result
else:
    pc.error("Extract deltas : UNKNOWN ERROR !\nSomething unexpected went wrong...")

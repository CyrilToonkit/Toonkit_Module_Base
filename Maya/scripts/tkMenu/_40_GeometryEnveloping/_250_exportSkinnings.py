import tkMayaCore as tkc
import pymel.core as pc

inPath = None
inPath = pc.fileDialog2(caption="Save your envelopes", fileFilter="Text file (*.txt)(*.txt)", dialogStyle=1, fileMode=0)

if inPath != None and len(inPath) > 0:
    inPath = inPath[0]

    tkc.storeSkins(pc.selected(), inPath)
import tkMayaCore as tkc
import pymel.core as pc

inPath = None
inPath = pc.fileDialog2(caption="Load your envelopes", fileFilter="Text file (*.txt)(*.txt)", dialogStyle=2, fileMode=1)

if inPath != None and len(inPath) > 0:
    inPath = inPath[0]

    tkc.loadSkins(inPath, pc.selected())
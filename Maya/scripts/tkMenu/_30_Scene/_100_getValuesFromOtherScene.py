import pymel.core as pc
import tkParseMA

sel = pc.ls(sl=True)

if len(sel) == 0:
    pc.error("Please select some objects")

maFile = pc.fileDialog2(caption="Select the .ma reference file", fileFilter="Maya ascii (*.ma)(*.ma)", dialogStyle=2, fileMode=1)
if maFile == None:
    print "getValuesFromOtherScene aborted"
    return

tkParseMA.setValuesFromOtherScene( pc.ls(sl=True), maFile)

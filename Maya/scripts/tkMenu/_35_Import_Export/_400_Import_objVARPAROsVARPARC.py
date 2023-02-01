import maya.cmds as cmds
from Toonkit_Core import tkLogger

fileDialogArgs = {
    "dialogStyle":1,
    "fileFilter":"Obj Files (*.obj)",
    "fileMode":4,
    "caption":"Import objs",
}

results = cmds.fileDialog2(**fileDialogArgs)

if results is None or len(results) == 0:
    tkLogger.debug("ImportObjs cancelled by user")
else:
	importArgs = {
		"import":True,
	 	"type":"OBJ",
	 	"ignoreVersion":True,
	 	"ra":True,
	 	"mergeNamespacesOnClash":True,
	 	"namespace":":",
	 	"options":"mo=1;lo=0",
	 	"pr":True,
	 	"importTimeRange":"combine",
	}

	tkLogger.debug("Import arguments : " + str(importArgs))
	for result in results:
		cmds.file(result, **importArgs)
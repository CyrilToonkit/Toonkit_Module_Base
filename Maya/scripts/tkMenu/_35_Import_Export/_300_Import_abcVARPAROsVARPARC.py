import maya.cmds as cmds
from Toonkit_Core import tkLogger

fileDialogArgs = {
    "dialogStyle":1,
    "fileFilter":"Abc Files (*.abc)",
    "fileMode":4,
    "caption":"Import abcs",
}

results = cmds.fileDialog2(**fileDialogArgs)

if results is None or len(results) == 0:
    tkLogger.debug("ImportAbcs cancelled by user")
else:
	importArgs = {
		"mode":"import",
	}

	tkLogger.debug("Import arguments : " + str(importArgs))
	for result in results:
		cmds.AbcImport(result, **importArgs)
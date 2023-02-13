"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Author : Cyril GIBAUD - Toonkit
    Copyright (C) 2014-2017 Toonkit
    http://toonkit-studio.com/

    Toonkit Module Lite is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Toonkit Module Lite is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with Toonkit Module Lite.  If not, see <http://www.gnu.org/licenses/>
-------------------------------------------------------------------------------
"""
import os

import maya.cmds as cmds

import pymel.core as pc

from Toonkit_Core import tkLogger
from Toonkit_Core.tkToolOptions.tkOptions import Options
from Toonkit_Core.tkProjects import tkContext
from tkMayaTools.tkMayaTool import MayaTool as Tool

import tkMayaCore as tkc
import abcExporter

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.0.0.0"

def inclusiveRange(start, stop, step):
    lst = [start]
    
    it = 1
    while start + it * step < stop:
        lst.append(start + it * step)
        it += 1
    
    lst.append(stop)
    
    return lst

class ExportAbcs(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(ExportAbcs, self).__init__(inName="Export abc(s)", inDescription="Export abc(s)",
            inUsage="Select some objects (if Selected option is used) then execute script", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("Selected", False, "Export only selected objects","Selected")
        self.options.addOption("Speed", 1.0, "Speed","Speed", inMin=0.001, inMax=100)
        self.options.addOption("Scope", 0, "Frames to be exported","Scope", False, None, inValues=["Current frame only", "One file per frame", "All frames in one file"])
        self.options.addOption("FilePattern", "{sceneName}_{frame:[0-9]{3}}.abc", "Name of the files when we export multiple ones","File Pattern")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(ExportAbcs, self).execute(*args, **kwargs)

        fileDialogArgs = {
            "dialogStyle":1,
            "fileFilter":"Abc Files (*.abc)",
            "fileMode":0 if self.options["Scope"] in [0,2] else 3,
            "caption":"Export abc" if self.options["Scope"] == 0 else "Pick a folder to export your files to",
        }

        filepath = cmds.file(q=True, sn=True)
        filename = os.path.basename(filepath)
        raw_name, extension = os.path.splitext(filename)

        currentTime = cmds.currentTime(query=True)

        if self.options["Scope"] == 0:
            fileDialogArgs["startingDirectory"]=tkContext.expandVariables(self.options["FilePattern"], {"sceneName":raw_name, "frame":currentTime})

        results = cmds.fileDialog2(**fileDialogArgs)

        if results is None or len(results) == 0:
            tkLogger.debug("ExportAbcs cancelled by user")
            return

        path = results[0]
        outFolder, outFilename = os.path.split(path)
        raw_path, path_extension = os.path.splitext(outFilename)

        exported = []

        objsDef = pc.selected if self.options["Selected"] else abcExporter.getAllMeshesT

        ABC_PRESETS = {}

        if self.options["Scope"] == 0:
            ABC_PRESETS = {raw_path:{"def":objsDef, "args":[], "overrides":{"frameRange":(currentTime,currentTime)}}}

        elif self.options["Scope"] == 1:
            startFrame = int(cmds.playbackOptions(animationStartTime=True, query=True))
            endFrame = int(cmds.playbackOptions(animationEndTime=True, query=True))

            for frame in inclusiveRange(startFrame, endFrame, self.options["Speed"]):
                filePattern = tkContext.expandVariables(self.options["FilePattern"], {"sceneName":raw_name, "frame":startFrame+(frame - startFrame)/self.options["Speed"]})
                raw_filePattern, filePattern_extension = os.path.splitext(filePattern)

                ABC_PRESETS[raw_filePattern]={"def":objsDef, "args":[], "overrides":{"frameRange":(frame,frame)}}
        else:
            startFrame = int(cmds.playbackOptions(animationStartTime=True, query=True))
            endFrame = int(cmds.playbackOptions(animationEndTime=True, query=True))

            overrides = {"frameRange":(startFrame,endFrame)}
            if not tkc.doubleBarelyEquals(self.options["Speed"], 1.0):
                overrides["step"]=self.options["Speed"]

            ABC_PRESETS[raw_path]={"def":objsDef, "args":[], "overrides":overrides}

        abcExporter.abcPrepare(outFolder if self.options["Scope"] != 1 else path, ABC_PRESETS)
        abcExporter.abcExport(inClean=True)
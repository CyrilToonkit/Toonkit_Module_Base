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
from tkOptions import Options
from tkMayaTool import MayaTool as Tool

import pymel.core as pc
import tkMayaCore as tkc

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.0.0.0"

class ImportSkinnings(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(ImportSkinnings, self).__init__(inName="Import skinnings", inDescription="Import skinnings from a '.txt' file exported from 'Export skinnings', eventually using fusion modes",
            inUsage="Select some meshes and run, and eventually joints to skip when using overwrite mode", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("Overwrite", False, "When checked, will import skinning only on unnormalized areas and/or through influences that are not selected", "Overwrite")
        self.options.addOption("Opacity", 1.0, "Blending with current envelope", "Opacity")
        self.options.addOption("Normalize", True, "Normalize envelope", "Normalize")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(ImportSkinnings, self).execute(*args, **kwargs)

        sel = pc.selected()
        joints =  pc.ls(sel, type="joint")

        zeroInfs = None
        if len(joints) > 0:
            sel = [s for s in sel if s not in joints]
            zeroInfs = [n.stripNamespace() for n in joints]

        mode = 0
        if self.options["Opacity"] < 1.0:
            mode = 3
        elif self.options["Overwrite"]:
            mode = 1

        print "mode",mode
        print "opacity",self.options["Opacity"]

        inPath = None
        inPath = pc.fileDialog2(caption="Load your envelopes", fileFilter="Text file (*.txt)(*.txt)", dialogStyle=2, fileMode=1)

        if inPath != None and len(inPath) > 0:
            inPath = inPath[0]

            tkc.loadSkins(inPath, sel, inZeroInfs=zeroInfs, inMode=mode, inOpacity=self.options["Opacity"], inNormalize=self.options["Normalize"])
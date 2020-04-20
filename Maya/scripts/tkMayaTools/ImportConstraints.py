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

import tkMayaCore as tkc
import maya.cmds as mc
import pymel.core as pc

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.0.0.0"

class ImportConstraints(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(ImportConstraints, self).__init__(inName="Import constraints", inDescription="Import constraints from a *.cns file",
            inUsage="Just set and execute, you'll be asked to browse for a '*.cns' file afterwards", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("RemoveExisting", True, "Remove any existing constraints", "Remove existing")
        self.options.addOption("MaintainOffset", False, "MaintainOffset", "Maintain offset")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(ImportConstraints, self).execute(*args, **kwargs)

        path = mc.fileDialog2(caption="Load your constraints file", fileFilter="cns file (*.cns)(*.cns)", dialogStyle=2, fileMode=1)

        if path != None and len(path) > 0:
            path = path[0]

        if path is None:
            pc.warning("Invalid file !")
        else:
            sel = pc.selected() if len(pc.selected()) > 0 else None
            tkc.loadConstraints(path, sel, *self.arguments)
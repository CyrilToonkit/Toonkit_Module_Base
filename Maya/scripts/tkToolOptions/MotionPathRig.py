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
import tkRig

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.0.0.0"

class MotionPathRig(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(MotionPathRig, self).__init__(inName="MotionPath rig", inDescription="Create a rig based on motionPaths, suitable for snakes",
            inUsage="Select a nurbsCurve to use as path", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("Number", 10, "Number of sections", "Number of sections")
        self.options.addOption("Length", 10, "Length of the rig", "Length of the rig")
        self.options.addOption("Name", "motionPathRig", "Name of the rig", "Name of the rig")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(MotionPathRig, self).execute(*args, **kwargs)

        sel = pc.selected()

        if len(sel) > 0:
            tkRig.motionPathRig(sel[0], *self.arguments)
        else:
            self.warning("Please select a nurbsCurve to use as path !")
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


class polyReduceComplexity(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(polyReduceComplexity, self).__init__(inName="polyReduceComplexity", inDescription="Use polyReduce from Maya or not depending on a threshold",
            inUsage="Select a mesh to reduce", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("MinComplx", 0.015, "Threshold min for complexity", "Threshold min for complexity", inMin=0.0, inMax=10.0)
        self.options.addOption("MaxComplx", 0.50, "Threshold max for complexity", "Threshold max for complexity", inMin=0.0, inMax=10.0)
        self.options.addOption("MinPercent", 0, "Percentage min", "Percentage min", inMin=0, inMax=100)
        self.options.addOption("MaxPercent", 100, "Percentage max", "Percentage max", inMin=0, inMax=100)

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(polyReduceComplexity, self).execute(*args, **kwargs)

        sel = pc.ls(sl=True)
        if len(sel) > 0:
            tkc.polyReduceComplexity(sel[0], *self.arguments)
        else:
            self.warning("Please select one object to reduce !")
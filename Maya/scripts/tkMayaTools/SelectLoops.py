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
from Toonkit_Core.tkToolOptions.tkOptions import Options
from tkMayaTools.tkMayaTool import MayaTool as Tool

import pymel.core as pc
import tkMayaCore as tkc

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.0.0.0"

class SelectLoops(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(SelectLoops, self).__init__(inName="Select loops", inDescription="Select components by growing proximity, excluding any number of iterations",
            inUsage="Select some loops of components and launch", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("Number", 1, "Skipped loops", "Skipped loops")
        self.options.addOption("ShowWaves", False, "Show each iteration", "Show each iteration")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(SelectLoops, self).execute(*args, **kwargs)

        sel = pc.selected()

        if len(sel) > 0:
            tkc.selectLoops(*self.arguments)
        else:
            self.warning("Please select some loops of components !")
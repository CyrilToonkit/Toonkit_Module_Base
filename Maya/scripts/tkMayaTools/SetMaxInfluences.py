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

class SetMaxInfluences(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(SetMaxInfluences, self).__init__(inName="Set max influences", inDescription="Reduce influences per vertex to specified max on selected meshes",
            inUsage="Select some meshes and run", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("MaxInfs", 8, "Max influences", "Max influences")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(SetMaxInfluences, self).execute(*args, **kwargs)

        sel = [s for s in pc.selected() if s.getShape() != None and s.getShape().type() in ["mesh", "nurbsCurve"]]

        if len(sel) > 0:
            for selItem in sel:
                tkc.limitDeformers(selItem, *self.arguments)
        else:
            self.warning("Please select some meshes !")
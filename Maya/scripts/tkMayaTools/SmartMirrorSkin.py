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

__author__ = "Mickael GARCIA - Toonkit"

VERSIONINFO = "1.0.0.0"

SIDES = ["Left_", "Right_"]

class SmartMirrorSkin(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(SmartMirrorSkin, self).__init__(inName="Smart Mirror Skin", inDescription="Maya mirror skin but add useful deformers by label side, usable on unique object or side object to oposite side (left/right) if inSource used",
            inUsage="Select one or two object that you need to smart mirror skin", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("SidesPrefix", "Left_,Right_", "Mirror Sides Prefix", "Sides")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(SmartMirrorSkin, self).execute(*args, **kwargs)
        sel = pc.selected()

        sides = self.arguments[0].split(",")
        
        if len(sel) == 0:
            pc.warning(self.usage)
        elif len(sel) == 1:
            tkc.smartMirrorSkin(sel[0], inSides=sides)
        else:
            tkc.smartMirrorSkin(sel[0], sel[1], inSides=sides)

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

class OffsetAnim(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(OffsetAnim, self).__init__(inName="Offset anim", inDescription="Offset animation of a certain number of frames, eventually incremented for each object.",
            inUsage="Select some transforms or animCurves and run", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("NbFrames", 5, "Number of frames to offset", "Number of frames")
        self.options.addOption("Increment", False, "Increment", "Increment")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(OffsetAnim, self).execute(*args, **kwargs)

        sel = pc.ls(sl=True)

        if len(sel) == 0:
            sel = pc.ls(["*", "*:*"], type=tkc.ANIMTYPES)

        if len(sel) > 0 and (sel[0].type() == "transform" or sel[0].type() in tkc.ANIMTYPES):
            if self.arguments[1]:
                offset = self.arguments[0]
                for selItem in sel:
                    pc.keyframe(selItem, edit=True, relative=True, timeChange=offset)
                    offset += self.arguments[0]
            else:
                pc.keyframe(sel, edit=True, relative=True, timeChange=self.arguments[0])

        else:
            self.warning("Please select some transforms or animCurves !")
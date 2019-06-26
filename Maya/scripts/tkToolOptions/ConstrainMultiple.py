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

CONSTYPES = ["parent", "scale", "point", "surface"]

class ConstrainMultiple(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(ConstrainMultiple, self).__init__(inName="Constrain multiple", inDescription="Constrain several objects to other object(s)",
            inUsage="Select multiple transforms to be constrained, then the constrainer", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("Type", "surface", "Constraint type ("+",".join(CONSTYPES)+")", "Type")
        self.options.addOption("MaintainOffset", True, "Maintain Offset", "Maintain Offset")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(ConstrainMultiple, self).execute(*args, **kwargs)

        cnsType = self.arguments[0]

        if not cnsType in CONSTYPES:
            pc.warning("Given type ('{0}') is unknown, valid values are : {1}".format(cnsType, ",".join(CONSTYPES)))
            return

        sel = pc.selected()

        if len(sel) < 2:
            pc.warning(self.usage)
            return

        objs = sel[0:-1]
        ref = sel[-1]

        for obj in objs:
            tkc.constrain(obj, ref, *self.arguments)
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
import tkRig

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.0.0.0"

class CreateOnSurface(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(CreateOnSurface, self).__init__(inName="Create on surface", inDescription="Create multiple locators on surface",
            inUsage="Select a mesh or nurbsSurface then execute script", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("UNumber", 1, "U number", "U number",inMin=1, inMax=1000)
        self.options.addOption("VNumber", 1, "V number", "V number",inMin=1, inMax=1000)
        self.options.addOption("UStart", 0.0, "U start", "U start")
        self.options.addOption("UEnd", 1.0, "U end", "U end")
        self.options.addOption("VStart", 0.0, "V start", "V start")
        self.options.addOption("VEnd", 1.0, "V end", "V end")
        self.options.addOption("UClosed", False, "U Closed", "U Closed")
        self.options.addOption("VClosed", False, "V Closed", "V Closed")

        """
        if not self.options.isSaved():
            self.saveOptions()
        """

    def execute(self, *args, **kwargs):
        super(CreateOnSurface, self).execute(*args, **kwargs)

        candidate = None
        for selObj in pc.selected():
            if selObj.type() == "mesh" or selObj.type() == "nurbsSurface":
                candidate = selObj
                break
            elif selObj.type() == "transform":
                shp = selObj.getShape()
                if not shp is None and (shp.type() == "mesh" or shp.type() == "nurbsSurface"):
                    candidate = shp
                    break

        if not candidate is None:
            tkRig.createOnSurface(candidate, *self.arguments)
        else:
            self.warning("Please select a mesh or nurbsSurface !")
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
from tkTool import Tool

import pymel.core as pc
import tkMayaCore as tkc

__author__ = "Cyril GIBAUD - Toonkit"

class gatorTool(Tool):
    def __init__(self):
        self.name = "Gator"
        self.description = "Copy skinning across geometries (creating the skinCluster with appropriate influences, using Maya copy skin or direct weights table copy)"
        self.usage = "Select any number of meshes to match first, then the ref mesh"
        self.version = "1.0.0.0"
        self.context = None
        self.debug = False

        self.opts = Options(inPath=self.getOptionsPath())
        self.opts.addOption("CopyMatrices", False, "Match the influences bind poses", "Match bind poses")
        self.opts.addOption("DirectCopy", False, "Copy the weights table (or use Maya copy skin)", "Strict copy (weights array)")

    def execute(self, *args, **kwargs):
        super(gatorTool, self).execute(*args, **kwargs)

        sel = pc.ls(sl=True)
        if len(sel) > 1:
            tkc.gator(sel[:-1], sel[-1], *self.arguments)
        else:
            self.warning("Please select at least two objects (any number of meshes to receive weights, then a \"Reference\" mesh) !")
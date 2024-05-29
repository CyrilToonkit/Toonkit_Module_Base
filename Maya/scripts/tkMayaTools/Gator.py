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

VERSIONINFO = "1.1.0.0"

class Gator(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(Gator, self).__init__(inName="Gator (copy skin)", inDescription="Copy skinning across geometries (creating the skinCluster with appropriate influences, using Maya copy skin or direct weights table copy)",
            inUsage="Select any number of meshes to match first, then the ref mesh, or, when using 'Multiple sources' mode, any number of meshes to copy weights from, then the target mesh", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("CopyMatrices", False, "Match the influences bind poses", "Match bind poses")
        self.options.addOption("DirectCopy", False, "Copy the weights table (or use Maya copy skin)", "Strict copy (weights array)")
        self.options.addOption("Reversed", False, "Copy the weights from several objects to one", "Multiple sources")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(Gator, self).execute(*args, **kwargs)

        richSelNodes = []
        richSel = tkc.getSoftSelections()

        wms = []
        for richSelObj, richSelComps in richSel:
            richSelNode = tkc.getNode(richSelObj)

            if richSelNode.type() != "transform":
                richSelNode = richSelNode.getParent()

            richSelNodes.append(richSelNode)

            wms.append(richSelComps)

        if len(richSelNodes) > 1:
            args = self.arguments + [wms]
            tkc.gator(richSelNodes[:-1], richSelNodes[-1], *args)
        else:
            message = "Please select at least two objects (any number of meshes to receive weights, then a \"Reference\" mesh) !"
            if self.options["Reversed"]:
                message = "Please select at least two objects (any number of meshes to copy weights from, then the \"Target\" mesh) !"
            self.warning(message)
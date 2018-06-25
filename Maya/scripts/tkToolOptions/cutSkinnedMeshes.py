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
import tkRig as tkr

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.0.0.0"


class cutSkinnedMeshes(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(cutSkinnedMeshes, self).__init__(inName="cutSkinnedMeshes", inDescription="Cut and combine the skinned meshes selected",
            inUsage="Select any number of meshes skinned", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("DeleteMesh", False, "Delete the original meshes", "Delete original meshes")
        self.options.addOption("FillHole", False, "Close borders of created meshes", "Close borders")
        self.options.addOption("NamePolyCombine", 'low_poly', "Name of the new combine meshes", "Rename the new meshes")
        self.options.addOption("ToJointParent", False, "The new mesh is parent of the joint", "Mesh parent joint")
        self.options.addOption("DeleteJoints", False, "Delete the joints", "Delete the joints")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(cutSkinnedMeshes, self).execute(*args, **kwargs)

        sel = pc.ls(sl=True)
        if len(sel) > 0:
            tkr.cutSkinnedMeshes(sel, *self.arguments)
        else:
            self.warning("Please select at least one object skinned !")
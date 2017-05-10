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
import tkRig

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.0.0.0"

class JointsFromCurve(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(JointsFromCurve, self).__init__(inName="Joints from curve", inDescription="Create a certain number of joints on a curve and add envenutally add splineIk, clusters, stretching...",
            inUsage="Select a curve and run", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("NbJoints", 4, "Number of joints to create", "Number of joints")
        self.options.addOption("SplineIK", False, "Generate a spline IK handle", "Spline IK")
        self.options.addOption("Scale", False, "Make the spine scale", "Scale")
        self.options.addOption("Squash", False, "Make the spine squash and stretch", "Squash")
        self.options.addOption("Clusters", False, "Create clusters on the spline points", "Clusters")
        self.options.addOption("Prefix", "", "Add a prefix on objects", "Prefix")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(JointsFromCurve, self).execute(*args, **kwargs)

        sel = pc.ls(sl=True)
        if len(sel) > 0 and sel[0].type() == "transform" and sel[0].getShape().type() == "nurbsCurve":
            #tkRig.jointsFromCurve(pc.selected()[0], inNbJoints=14, inSplineIK=True, inScl=True, inSquash=True, inClusters=False, inPrefix="Test")
            tkRig.jointsFromCurve(sel[0], *self.arguments)
        else:
            self.warning("Please select a Curve !")
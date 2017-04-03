"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Author : Cyril GIBAUD - Toonkit, Stephane Bonnot - Parallel Dev
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
import os
import sys

import maya.cmds as cmds
import pymel.core as pc
import pymel.core.system as pmsys
import maya.mel as mel

import locationModule

__author__ = "Cyril GIBAUD - Toonkit, Stephane Bonnot - Parallel Dev"

modulepath = locationModule.OscarModuleLocation()
moduleRootPath = os.path.abspath(os.path.join(modulepath, os.pardir, os.pardir))
mayaRootPath = os.path.abspath(os.path.join(modulepath, os.pardir))

pythonPackagesPath = os.path.join( mayaRootPath , "Python", "lib", "site-packages")
commonPythonPath = os.path.join(moduleRootPath, "Python", "Oscar")

if os.path.isdir(pythonPackagesPath):
    sys.path.append(pythonPackagesPath)

if os.path.isdir(commonPythonPath):
    sys.path.append(commonPythonPath)

#Core python libraries
import tkMayaCore as tkc
import tkMayaSIBar as tksi
import tkSIGroups
import TKuserSetup

#Import specific scripts/menus
pc.mel.eval("source abSymMesh")
pc.mel.eval("source qa_skinPasterUI")

coreOptions = tkc.getOptions()

#if mayabatch and supplied arguments contains a script, execute, else show menu
app = sys.executable
if "mayabatch" in app:
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        fileName, fileExtension = os.path.splitext(args[0])
        if coreOptions["hookmayabatch"] and ".py" in fileExtension and os.path.isfile(args[0]):
            result = None
            print "Toonkit mayabatcher : environment loaded from Maya batch, execute script from arguments (%s)" % str(args)
            result = tkc.executeFile(args[0], strlng=1, functionName="do", args=[] if len(args) == 0 else args[1:])
            print "Toonkit mayabatcher : result {0}".format(result)
else:
    if not coreOptions["hidemenu"]:
        cmds.evalDeferred(TKuserSetup.menu)
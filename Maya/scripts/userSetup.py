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

#if mayabatch and supplied arguments contains a script, execute items
app = sys.executable
if ("mayabatch.exe" in app and len(sys.argv) > 1):
    fileName, fileExtension = os.path.splitext(sys.argv[1])
    if ".py" in fileExtension and os.path.isfile(sys.argv[1]):
        import mayaexecpythonfile
        print "Environment loaded from Maya batch, try to execute script from arguments (%s)" % str(sys.argv)
        try:
            mayaexecpythonfile.execpythonfile(sys.argv[1])
        except:
            pass
    else:
        pc.warning("Incorrect python script file argument (%s). File cannot be found or have incorrect extension (.py, .pyw) !" % sys.argv[1])

cmds.evalDeferred(TKuserSetup.menu)
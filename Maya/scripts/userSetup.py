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

# Initialize OScar toolbox
print "Executing Toonkit's root userSetup..."

__author__ = "Cyril GIBAUD - Toonkit, Stephane Bonnot - Parallel Dev"

CONST_SPECDIR = "Specific"

def mayasublimeports():
	cmds.commandPort(name=":7001", sourceType="mel")
	cmds.commandPort(name=":7002", sourceType="python")

oscarmodulepath = locationModule.OscarModuleLocation()
oscarpythonpackagespath = oscarmodulepath + "\\..\\Python\\lib\\site-packages"
oscarcommonpythonpath = oscarmodulepath + "\\..\\..\\Python\\Oscar"

if os.path.isdir(oscarcommonpythonpath):
    print "Initializing Python Oscar common libraries"
    sys.path.append(oscarcommonpythonpath)
else:
    print "Python Oscar common libraries not found ! (%s)" % oscarcommonpythonpath

if os.path.isdir(oscarpythonpackagespath):
    print "Initializing Python Oscar communication layer"
    sys.path.append(oscarpythonpackagespath)

    try:
        exec 'import zmq' in globals()
        exec 'import OscarZmqAsyncServer' in globals()
        exec 'import LaunchMayaServer' in globals()
        #installoscarshelf()
        exec 'LaunchMayaServer.initoscar()'

        print "Done Initializing Python Oscar library !"

        OSCAR = OscarZmqAsyncServer.oscarserver._callback
    except:
        pc.warning("Can't load Python Oscar communication layer (%s) !" % oscarpythonpackagespath)
else:
    print "Python Oscar communication layer not found ! (%s)" % oscarpythonpackagespath

#mayasublimeports()

#Core python library
import tkMayaCore as tkc
import tkMayaSIBar as tksi
import tkSIGroups
import tkPalette
import tkSpring
import tkRig
import tkDevHelpers
import tkParseMA
import TKuserSetup

#Import specific scripts/menus

import zvRadialBlendShape
import undoableSmuffe
pc.mel.eval("source abSymMesh")
pc.mel.eval("source qa_skinPasterUI")

# -Oscar project specific


# - Customer specific

specificPath = os.path.join(oscarmodulepath, CONST_SPECDIR)

if not os.path.isdir(specificPath):
    print "Specific scripts directory does not exists ! (%s)" % specificPath
else:
    subfiles = os.listdir(specificPath)
    if len(subfiles) == 0:
        print "No specific scripts to load..."
    else:
        sys.path.append(specificPath)
        for specfile in os.listdir(specificPath):
            fileName, fileExtension = os.path.splitext(specfile)
            if ".py" in fileExtension and fileExtension != ".pyc":
                baseName = os.path.basename(specfile).split(".")[0]
                print "Initializing Python %s library" % baseName
                try:
                    exec 'import ' + baseName in globals()
                    exec 'if hasattr('+ baseName +', "menu") : pc.evalDeferred('+ baseName +'.menu)'
                except:
                    pc.warning("Can't load specific script file (%s) !" % specfile)

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

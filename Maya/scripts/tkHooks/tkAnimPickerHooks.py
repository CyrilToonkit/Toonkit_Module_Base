"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Authors : Cyril GIBAUD - Toonkit, Stephane Bonnot - Parallel Dev
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
import pymel.core as pc

import tkMayaCore as tkc

def conformPath(inPath):
    return inPath.replace("\\", "/")

def resolvePath(inPath, inProdPath, inDebug=False,
                inRootVar="$ROOT", inProjectPathVar="$PROJECTPATH",
                inDebugPath="\\\\NHAMDS\\ToonKit\\ToonKit\\Rnd\\Picker\\Picker_Files", inAsset=None):
    #Initialize
    replacements = []

    ROOT = inDebugPath
    replacements.append((inRootVar, ROOT))

    PROJECTPATH = os.path.join(ROOT, tkc.getTool().options["project"])
    replacements.append((inProjectPathVar, PROJECTPATH))

    #Perform paths replacements
    for replacement in replacements:
        if replacement[0] in inPath:
            if inDebug:
                print "Replace", replacement[0], "by", replacement[1],"(", inPath, "=>",inPath.replace(replacement[0], replacement[1]),")"

            inPath = inPath.replace(replacement[0], replacement[1])

    if not inDebug:
        inPath = inPath.replace(inDebugPath, inProdPath)
        inPath = inPath.replace(conformPath(inDebugPath), inProdPath)

    return conformPath(inPath)
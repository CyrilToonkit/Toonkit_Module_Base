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

"""
Maya scene batch script launcher
"""

import tkBatcher
from Toonkit_Core.tkToolOptions.tkOptions import Options

def do(inDataPath):
    data = Options(None, inDataPath)
    return tkBatcher.doBatch(data['batchName'], data['node'], data['code'], inForce=data['force'], inSaveFile=data['saveFile'], inSavePath=data['savefilePath'], inVariables=data['variables'], inLogDirPath=data["logpath"], inLoadRefs=data['loadRefs'], inScriptNodes=data['scriptNodes'])
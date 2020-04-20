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
import tkTool
from tkTool import Tool
import pymel.core as pc

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.0.0.0"

class MayaTool(Tool):
    def log(self, *args, **kwargs):
        if kwargs.get("inPrefix") == tkTool.WARNING_PREFIX :
            pc.warning(tkTool.WARNING_PREFIX + " {0} : {1}".format(self.name, " ".join([str(arg) for arg in args])))
            return

        super(MayaTool, self).log(*args, **kwargs)
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

import pymel.core as pc

import tkMath
import tkMayaCore as tkc 

__author__ = "Cyril GIBAUD - Toonkit"


def setWeightsMap(inObj, inAttrName, inRefObjects, inMode=0, inSetter=0, inInterp=0, inRadius=0.0, inExtrapStart=0, inExtrapEnd=0, inIntervalAxis=[1,0,0]):
    """Sets a weightmap on a geometry depending on transformation of "gizmo objects"

    Arguments :
    inMode                  -- 0 = Flood,    1 = Add,                            2 = Remove
    inSetter                -- 0 = Radius,   1 = Interval (Cylinder/Capsules)
    inInterp                -- 0 = Linear,   1 = Hermite,                        2 = Cosine
    inExtrap (Start/End)    -- 0 = None,     1 = Flood,                          2 = Capsule

    inRadius                --

    """

    if inSetter == 0:#Radius
        if len(inRefObjects) == 0:
            pc.warning("One object ")


    pass
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

import math

__author__ = "Cyril GIBAUD - Toonkit"

EPSILON = sys.float_info.epsilon * 10
OMEGA = 1.0/EPSILON

def linearInterp(x0, y0, x1, y1, x):
    """Linearly interpolates from (x0,y0) to (x1, y1) for value x"""
    return ( y0 * (x1 - x) + y1 * (x - x0) ) / (x1 - x0)

def cosineInterp(x0, y0, x1, y1, x):
    """Interpolates with cosine from (x0,y0) to (x1, y1) for value x"""
    return (math.cos(math.pi*(linearInterp(x0, y0, x1, y1, x)+1)) + 1.0) / 2.0
    
def hermiteInterp(x0, y0, x1, y1, x):
    """Interpolates with hermite-type polynomial from (x0,y0) to (x1, y1) for value x"""
    lin = linearInterp(x0, y0, x1, y1, x)
    return -2 * pow(lin,3) + 3 * pow(lin,2)

def normalize(*inLists, inUnits=1.0):
    """Normalize a single vector with itself, or multiple lists versus one another"""
    #Flat case (vectortype)
    if len(inLists) == 1:
        total = 0
        for item in inLists[0]:
            total += item

        mul = inUnits / total

        if abs(mul - 1.0) > EPSILON:
            inLists[0] = [i * mul for i in inLists[0]]

        return

    #Dimensionnal case



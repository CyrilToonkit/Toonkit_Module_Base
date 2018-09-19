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

import pymel.core as pc

#import tkMath
import tkMayaCore as tkc 
import tkSkinner as tks

__author__ = "Cyril GIBAUD - Toonkit"

def getLoc(inLoc, inIntervalAxis=[1,0,0]):
    return inLoc[0] * inIntervalAxis[0] + inLoc[1] * inIntervalAxis[1] + inLoc[2] * inIntervalAxis[2]

def setWeightsMap(inObj, inAttrName, inRefObjects=None, inMode=0, inSetter=0, inInterp=0, inRadius=1.0, inExtrapStart=0, inExtrapEnd=0, inIntervalAxis=[1,0,0], inSecondaryAxis=[0,1,0], inReverse=False):
    """Sets a weightmap on a geometry depending on transformation of "gizmo objects"

    Arguments :
    inMode                  -- 0 = Flood,    1 = Add,                            2 = Remove
    inSetter                -- 0 = Radius,   1 = Interval (Cylinder/Capsules)    2 = Selection      3 = Angular     4 = Existing map(s)
    inInterp                -- 0 = Linear,   1 = Hermite,                        2 = Cosine
    inExtrap (Start/End)    -- 0 = None,     1 = Flood,                          2 = Capsule

    inRadius                --

    """
    
    obj = pc.PyNode(inObj)
    attr = pc.PyNode(inAttrName)
    refObjects = tkc.getNodes(inRefObjects or [])

    if inSetter == 0:#Radius
        if not refObjects is None and len(refObjects) != 1:
            pc.warning("One object needed")
            return
            
        loc = refObjects[0]
        refPoint = loc.getTranslation(space="world")
        
        i = 0
        for point in obj.getPoints(space="world"):
            dist = (refPoint - point).length()
            value = max(0, 1 - dist / inRadius)
            attr[i].set(value)
        
            i += 1
        
        return

    if inSetter == 1:#Interval
        if not refObjects is None and len(refObjects) != 2:
            pc.warning("Two objects needed")
            return
            
        start, end = refObjects

        startLoc = getLoc(start.getTranslation(space="world"), inIntervalAxis)
        endLoc = getLoc(end.getTranslation(space="world"), inIntervalAxis)
        length = endLoc - startLoc
        
        #print "startLoc",startLoc,"endLoc",endLoc,"length",length

        i = 0
        for point in obj.getPoints(space="world"):
            loc = getLoc(point, inIntervalAxis)
            
            value = (loc - startLoc) / length
            #print i, "loc", loc, "value", value
            attr[i].set(value)
        
            i += 1

    if inSetter == 2:#Selection
        sel = pc.selected()
        if len(sel) == 0:
            pc.warning("Vertices selection needed !")
            return

        components = []
        opacities = []

        allDags, allComps, allOpacities = tks.getSoftSelection()
        if len(allOpacities) > 0:
            for dagIndex in range(len(allOpacities)):
                node = pc.PyNode(allDags[dagIndex].partialPathName())

                if not node.getParent() == obj:
                    continue

                for index, value in allOpacities[dagIndex].iteritems():
                    components.append(index)
                    opacities.append(value)
        else:
            componentNodes = tkc.expandCompIndices(sel)
            for component in componentNodes:
                components.append(component.indices()[0])
                opacities.append(1.0)

        """
        print "allDags",allDags
        print "allComps",allComps   
        print "allOpacities",allOpacities

        print "components",components
        print "opacities",opacities
        """

        for i in range(pc.polyEvaluate(obj, vertex=True)):
            if i in components:
                v = opacities[components.index(i)]
                if inReverse:
                    v = 1 + (v * -1)
                attr[i].set(v)
            else:
                attr[i].set(1.0 if inReverse else 0.0)

    if inSetter == 3:#Angular
        if not refObjects is None and len(refObjects) != 1:
            pc.warning("One object needed")
            return

        loc = refObjects[0]
        refPoint = loc.getTranslation(space="world")

        refVec = pc.datatypes.Vector(inIntervalAxis)
        refVec.normalize()

        i = 0
        for point in obj.getPoints(space="world"):
            localVec = point - refPoint
            
            #Fake projection considering only strict X, Y or Z
            if inSecondaryAxis[0] > 0:
                localVec.x = 0
            elif inSecondaryAxis[1] > 0:
                localVec.y = 0
            else:
                localVec.z = 0
                
            localVec.normalize()
            
            #value = ((math.asin(localVec.dot(refVec)) * 2 / math.pi) + 1) / 2.0   #180degrees
            value = max(0, ((math.asin(localVec.dot(refVec)) * 2 / math.pi) + 0) / 1.0)   #90degrees
            attr[i].set(value)
        
            i += 1
        
        return

#pc.cluster("mod:eye_L_eyelid_geo", weightedNode=["locator1", "locator1"], relative=True)

#setWeightsMap("pSphere1", "cluster1.weightList[0].weights", ["locator1", "locator2"], inSetter=1)
#setWeightsMap("pSphere1", "cluster4.weightList[0].weights", inSetter=2)
#setWeightsMap("mod:eye_L_eyelid_geo", "cluster2.weightList[0].weights", ["locator2"], inSetter=3, inIntervalAxis=[0,-1,0], inSecondaryAxis=[1,0,0])*

#blendShape1.inputTarget[0].inputTargetGroup[0].targetWeights
setWeightsMap("mod:eye_L_eyelid_geo", "blendShape8.inputTarget[0].inputTargetGroup[0].targetWeights", inSetter=2)

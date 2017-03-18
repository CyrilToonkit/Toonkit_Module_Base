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

import maya.cmds as cmds

import zvRadialBlendShape

__author__ = "Cyril GIBAUD - Toonkit"

def create(inGeo, name="$_rBS"):
    if "$" in name:
        name = name.replace("$", inGeo)
    return cmds.deformer(inGeo, typ=zvRadialBlendShape._rbsNodeName, foc=True, name=name)

def addTarget(inGeo, inTarget, inPrefix="L", inIndex=0L):
    opposite = False
    
    rbsNode = zvRadialBlendShape._getRbs(inGeo)
    if rbsNode == None:
        cmds.warning("Cannot find a radial blendShape node on " + inGeo)
        return False
    
    """Adds new eyelid inputs (if needed)"""
    if not cmds.attributeQuery('%s_upper' % inPrefix, node=rbsNode, exists=True):
        # find first available lower lid index
        miList = zvRadialBlendShape._getEyeIdxList(rbsNode)
        print miList
        idx = 0
        while idx in miList or (idx+1) in miList:
            idx += 2
        
        lowerAttr = '%s.it[%d]' % (rbsNode, idx)
        upperAttr = '%s.it[%d]' % (rbsNode, idx+1)
        lowerName = '%s_lower' % inPrefix
        upperName = '%s_upper' % inPrefix
        
        # add lower and upper indices
        cmds.getAttr('%s.im' % lowerAttr)
        cmds.getAttr('%s.im' % upperAttr)

        # set the aliases for the inputTarget attributes (lower and upper)
        if cmds.aliasAttr(lowerAttr, q=True) != lowerName:
            zvRadialBlendShape._setAlias(lowerAttr, lowerName)
        if cmds.aliasAttr(upperAttr, q=True) != upperName:
            zvRadialBlendShape._setAlias(upperAttr, upperName)
        
        # create and connect locators
        zvRadialBlendShape._createEyeLocators(rbsNode, idx)

    targetName = zvRadialBlendShape._getTargetNameFromIdx(rbsNode, inIndex)
    
    if inIndex == -1:
        raise Exception, 'Input target %s does not exist, please refresh GUI' % targetName
    
    # make the connection if not yet done
    srcAttr = '%s.outMesh' % inTarget
    destAttr = '%s.it[%d].%s' % (rbsNode, inIndex, zvRadialBlendShape._targetAttrs[int(opposite)])
    connections = cmds.listConnections(destAttr, d=False) or []
    if inTarget in connections:
        cmds.warning('The geometry you selected is already connected to %s' % destAttr)
        return
    
    # connect geometry
    cmds.connectAttr(srcAttr, destAttr, f=True)
    
    if not opposite:
        # set default values
        for i, attr in enumerate(zvRadialBlendShape._attrs):
            cmds.setAttr('%s.%s[%d]' % (rbsNode, attr, inIndex), zvRadialBlendShape._defAttrValues[i])
        
        for i, attr in enumerate(zvRadialBlendShape._offsetAttrs):
            cmds.getAttr('%s.%s[%d]' % (rbsNode, attr, inIndex))

        for i, attr in enumerate(zvRadialBlendShape._offsetInfluenceAttrs):
            upIdx = inIndex + 1 - inIndex%2
            # don't set it if it has already been set by the other lid (since it's a common value)
            if not upIdx in zvRadialBlendShape._getAttrIdxList(rbsNode, attr):
                cmds.setAttr('%s.%s[%d]' % (rbsNode, attr, upIdx), zvRadialBlendShape._defOffsetInfluenceValues[i])

        # just for odd indices (upper lid) set the blink attribute
        if inIndex % 2 == 1:
            for attr in zvRadialBlendShape._blinkAttrs:
                cmds.setAttr('%s.%s[%d]' % (rbsNode, attr, inIndex), 0.0)

        # set aliases
        zvRadialBlendShape._setAttrAliases(rbsNode, inIndex)
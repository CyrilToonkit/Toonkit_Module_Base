"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Author : Stephane Bonnot - Parallel Dev
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
	Maya Python alternatives to commands	
	alternative methods to do stuff in python/api rather than through cmds
"""
import maya.cmds as mc
import pymel.core as pmc
import pymel.core.general as pmg
import maya.OpenMaya as om        
from maya.OpenMaya import MGlobal as omg	
import pymel.all as pma

__author__ = "Stephane Bonnot - Parallel Dev"

def pathtoshapepath(path):
	selectionList = om.MSelectionList()
	selectionList.add( path )
	dagPath = om.MDagPath()
	selectionList.getDagPath( 0, dagPath )
	try:
		dagPath.extendToShape()
		return dagPath.partialPathName()
	except:
		return path

def clearselection():
	emptylist = om.MSelectionList()
	omg.setActiveSelectionList(emptylist)

def exists(name):
	return mc.objExists(name)
	"""
	try:
		pmg.PyNode( name )
		return True
	#except pmg.MayaObjectError:
	except Exception:
		return False
	"""
def parent(childnode, parentnode):
	parentnode.addChild(childnode)

def setTRSPreserveChildPosition(boolVal):
	#optionVar -iv trsManipsPreserveChildPosition $turnOn;
	pma.optionVar['trsManipsPreserveChildPosition'] = 1 if boolVal else 0	
	pmc.context.manipMoveContext(pcp=boolVal)
	pmc.context.manipRotateContext(pcp=boolVal)
	pmc.context.manipScaleContext(pcp=boolVal)

def getparent(node):	
	try:	
		if hasattr(node,'firstParent'):
			return node.firstParent()
		else:
			return None
	except pmg.MayaObjectError:
		return None
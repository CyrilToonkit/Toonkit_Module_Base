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
	Way to reproduce Softimage attributes overrides when using groups (= Maya "Sets")  
"""

import pymel.core as pc

import tkMayaCore as tkc

__author__ = "Cyril GIBAUD - Toonkit"

PARAM_SETPRIORITY = "tkSetPriority"
PARAM_VisOldValue = "tkSetVisibilityOldValue"
PARAM_SelOldValue = "tkSetSelectabilityOldValue"
PARAM_Vis = "visibility"
PARAM_Sel = "selectability"

VIS_VALUES = ['Hide', 'Show', 'No effect']
SEL_VALUES = ['Do not allow', 'Allow', 'No effect']

def getGroupPriority(inGroup):
	if pc.attributeQuery(PARAM_Vis, node=inGroup, exists=True):
		return pc.getAttr(inGroup.name() + "." + PARAM_SETPRIORITY)
	else:
		return 1000000

def collect(namespace="", sort=True, includeSimpleSets=False):
	sets =[]
	if namespace != "":
		sets = pc.ls(namespace + ":*", type='objectSet')
	else:
		sets = pc.ls(type='objectSet')
	groups = []

	#filter sets
	for i in range(len(sets)-1, -1, -1):
		mSet = sets[i]
		if mSet.name() == "defaultLightSet" or mSet.name() == "defaultObjectSet":
			sets.remove(mSet)
			continue
		if not mSet.type() == "objectSet" or not isinstance(mSet, pc.nodetypes.ObjectSet):
			sets.remove(mSet)
			continue
		if pc.mel.eval("setFilterScript " + mSet.name()) != 1:
			sets.remove(mSet)
			continue

	for mSet in sets:
		if includeSimpleSets or pc.attributeQuery( PARAM_SETPRIORITY,node=mSet ,exists=True):
			groups.append(mSet)
	if sort:
		groups.sort(key=lambda name: -getGroupPriority(name))
	return groups

def clean(inSet):
	if pc.attributeQuery(PARAM_SETPRIORITY, node=inSet, exists=True):
		pc.deleteAttr(inSet, at=PARAM_SETPRIORITY )

	if pc.attributeQuery(PARAM_VisOldValue, node=inSet, exists=True):
		pc.deleteAttr(inSet, at=PARAM_VisOldValue )

	if pc.attributeQuery(PARAM_SelOldValue, node=inSet, exists=True):
		pc.deleteAttr(inSet, at=PARAM_SelOldValue )

	if pc.attributeQuery(PARAM_Vis, node=inSet, exists=True):
		pc.deleteAttr(inSet, at=PARAM_Vis )

	if pc.attributeQuery(PARAM_Sel, node=inSet, exists=True):
		pc.deleteAttr(inSet, at=PARAM_Sel )

def cleanSelection():
	for obj in pc.selected():
		if obj.type() == "objectSet":
			clean(obj)

def getBiggerPrio(groups=None):
	if groups == None:
		groups = collect()

	biggerPrio = -1000000
	for group in groups:
		prio = pc.getAttr(group + "." + PARAM_SETPRIORITY)
		if prio > biggerPrio:
			biggerPrio = prio
	
	if biggerPrio == -1000000:
		biggerPrio = -1

	return biggerPrio

def decorate(inSet):
	biggerPrio = getBiggerPrio()

	if not pc.attributeQuery(PARAM_SETPRIORITY, node=inSet, exists=True):
		tkc.addParameter(inSet, PARAM_SETPRIORITY, "int", biggerPrio + 1, expose=False)

	if not pc.attributeQuery(PARAM_VisOldValue, node=inSet, exists=True):
		tkc.addParameter(inSet, PARAM_VisOldValue, "int", 2, expose=False)

	if not pc.attributeQuery(PARAM_SelOldValue, node=inSet, exists=True):
		tkc.addParameter(inSet, PARAM_SelOldValue, "int", 2, expose=False)

	if not pc.attributeQuery(PARAM_Vis, node=inSet, exists=True):
		visItems = "enum;" + ":".join(VIS_VALUES)
		tkc.addParameter(inSet, PARAM_Vis, visItems, "No effect")
	if not pc.attributeQuery(PARAM_Sel, node=inSet, exists=True):
		selItems = "enum;" + ":".join(SEL_VALUES)
		tkc.addParameter(inSet, PARAM_Sel, selItems, "No effect")

def decorateSelection():
	for obj in pc.selected():
		if obj.type() == "objectSet":
			decorate(obj)

def create(name="Group", useSelection=True, modifySelection=True):
	#Find appropriate priority (Biggest)
	groups = collect()
	biggerPrio = getBiggerPrio(groups)

	#Remove Sets from selection cause it creates nasty group hierarchies
	sel = []
	tkc.storeSelection()

	if useSelection:
		sel = pc.ls(sl=True)
		setsInSel = []
		counter = 0
		for selObj in sel:
			if selObj.type() == "objectSet":
				setsInSel.append(counter)
			counter += 1

		setsInSel.sort(reverse=True)

		for mSet in setsInSel:
			del sel[mSet]

		pc.select(sel,replace=True)

	mSet = pc.sets(name=name, empty=not useSelection)
	decorate(mSet)

	tkc.loadSelection()

	if modifySelection and len(sel) == 0:
		pc.select(mSet, noExpand=True, replace=True)

	return mSet

def refreshOverrides(namespace="", useJointsDrawStyle=True):
	groups = collect()
	groupsValues = []
	objects = []
	objectsGroups = []
	visOkObjects = []
	selOkObjects = []

	grpCounter = 0
	for group in groups:

		oldVis = pc.getAttr(group + "." + PARAM_VisOldValue)
		vis = pc.getAttr(group + "." + PARAM_Vis)
		oldSel = pc.getAttr(group + "." + PARAM_SelOldValue)
		sel = pc.getAttr(group + "." + PARAM_Sel)

		groupsValues.append([vis, sel, oldVis, oldSel])

		objs = pc.sets(group,query=True)

		#Collect info for each object
		for obj in objs:
			objShapes = tkc.getShapes(obj)
			if len(objShapes) == 0:
				objShapes = [obj]

			for objShape in objShapes:
				objName = objShape.name()
				objectGroups = []
				index = len(objects)

				if not objName in objects:
					objects.append(objName)
					objectsGroups.append([])
				else:
					index = objects.index(objName)
					objectGroups = objectsGroups[index]

				objectGroups.append(grpCounter)

				objectsGroups[index] = objectGroups

		''' Original version (1 shape by object only), kept for debugging if needed
		#Collect info for each object
		for obj in objs:
			objShape = obj
			objShapes = tkc.getShapes(obj)
			if len(objShapes) > 0:
				objShape = objShapes[0]
			objName = objShape.name()
			objectGroups = []
			index = len(objects)

			if not objName in objects:
				objects.append(objName)
				objectsGroups.append([])
			else:
				index = objects.index(objName)
				objectGroups = objectsGroups[index]

			objectGroups.append(grpCounter)

			objectsGroups[index] = objectGroups
		'''

		grpCounter += 1

	objCounter = 0
	for obj in objects:
		override = False
		visibility = None
		selectability = None
		visOk=False
		selOk=False
		for groupsId in objectsGroups[objCounter]:
			values = groupsValues[groupsId]
			if values[0] == 2 and values[1] == 2:
				continue

			override = True

			if not visOk and values[0] != 2:
				visibility = values[0] == 1
				visOk = True

			if  not selOk and values[1] != 2:
				selectability = values[1] == 1
				selOk = True

		#Preserve custom color in override if != 0
		override |= pc.getAttr(obj + ".overrideColor") > 0
		if pc.versions.current() > 201600:
			override |= pc.getAttr(obj + ".overrideRGBColors")

		#Verify if attributes are free
		if pc.getAttr(obj + ".overrideEnabled", settable=True):
			pc.setAttr(obj + ".overrideEnabled", override)

			if useJointsDrawStyle and pc.nodeType(obj) == "joint":
				if pc.getAttr(obj + ".drawStyle", settable=True):
					if visibility != None:
						pc.setAttr(obj + ".drawStyle", 0 if visibility else 2)
					else:
						pc.setAttr(obj + ".drawStyle", 0 if pc.getAttr(obj + ".visibility") else 2)
			else:
				if pc.getAttr(obj + ".overrideVisibility", settable=True):
					if visibility != None:
						pc.setAttr(obj + ".overrideVisibility", visibility)
					"""elif override:
						pc.setAttr(obj + ".overrideVisibility", pc.getAttr(obj + ".visibility"))
					"""
			if pc.getAttr(obj + ".overrideDisplayType", settable=True):
				if selectability != None:
					pc.setAttr(obj + ".overrideDisplayType", 0 if selectability else 2)
				elif override:
					pc.setAttr(obj + ".overrideDisplayType", 0 if not pc.getAttr(obj + ".template") else 1)

		objCounter += 1

	grpCounter = 0
	for group in groups:
		if "TK_NEUTRALGROUP" in group.name():
			pc.delete(group)

def removeGroups():
	sel = pc.ls(sl=True, type="objectSet")
	groups = collect()
	print groups
	for selObj in sel:
		if selObj in groups:
			pc.setAttr(selObj + "." + PARAM_Vis, 2)
			pc.setAttr(selObj + "." + PARAM_Sel, 2)
	refreshOverrides()
	pc.delete(sel)

def add(group="", objects=[], refresh=True):
	pc.sets(group, include=objects)
	if refresh:
		refreshOverrides()

def getNeutralGrp():
	try:
		grp = pc.PyNode("TK_NEUTRALGROUP")
	except:
		grp = create(name="TK_NEUTRALGROUP", useSelection=False,  modifySelection=False)
	return grp

def remove(group="", objects=[], refresh=True):
	pc.sets(group, remove=objects)
	neutralGrp = getNeutralGrp()
	pc.sets(neutralGrp, include=objects)
	if refresh:
		refreshOverrides()
		#pc.delete(neutralGrp)
	'''
	Old version, one "neutralization" per group
	groups = collect()
	if group in groups:
		neutralGrp = create(name="TK_NEUTRALGROUP", useSelection=False,  modifySelection=False)
		pc.sets(neutralGrp, include=objects)
		if refresh:
			refreshOverrides()
			pc.delete(neutralGrp)
	'''

def collectSelection():
	sel = pc.ls(sl=True)
	selGrps = pc.ls(sl=True, type="objectSet")
	
	for grp in selGrps:
		sel.remove(grp)

	if len(selGrps) == 0:
		pc.error("No set found in selection !")

	if len(sel) == 0:
		pc.error("No objects found in selection !")

	return (selGrps, sel)

def addFromSelection():
	selGrps_sel = collectSelection()
	for grp in selGrps_sel[0]:
		add(grp, selGrps_sel[1])
	refreshOverrides()

def removeFromSelection():
	selGrps_sel = collectSelection()
	for grp in selGrps_sel[0]:
		remove(grp, selGrps_sel[1])

def selectMembers():
	sel = pc.ls(sl=True, type="objectSet")
	pc.select(sel)

def mergeGroups(group, refGroup, remove=True):
	members = pc.sets(group, query=True)
	pc.sets(refGroup, include=members)
	if remove:
		pc.delete(group)

def splitGroup(group, root):
	pass

def merge(rigName, refRigName, remove=True):
	oldGroups = pc.ls(refRigName + "_*" + tkc.CONST_GROUPSUFFIX, type="objectSet")
	rigGroups = pc.ls(rigName + "_*" + tkc.CONST_GROUPSUFFIX, type="objectSet")

	for group in rigGroups:
		groupName = group.name()[len(rigName)+1:]
		merged = False
		for oldGroup in oldGroups:
			oldGroupName = oldGroup.name()[len(refRigName)+1:]
			if groupName == oldGroupName:
				mergeGroups(group, oldGroup, remove)
				merged = True
				break
		if not merged:
			#print group.name()
			group.rename(group.name().replace(rigName, refRigName))

'''''''''''''''''''''''''''''''''''''''''''''''''''''

Attribute Editor functions

'''''''''''''''''''''''''''''''''''''''''''''''''''''

def AEaddIntSliderCB( plug, slider ):
	val = pc.intSliderGrp( slider, q=1, v=1 )
	pc.setAttr( plug, val )
	refreshOverrides()

def AEaddIntSlider(	plug, sliderLabel, annot ):
	obj_Attr = plug.split(".")
	if pc.attributeQuery( obj_Attr[1], node=obj_Attr[0] ,exists=True ):
		pc.columnLayout()
		val = pc.getAttr( plug )
		slider = pc.intSliderGrp( annotation=annot, label=sliderLabel, minValue=-10, maxValue=10, fieldMinValue=-100, fieldMaxValue=100, v=val )
		pc.intSliderGrp( slider, e=1, cc="tkSIGroups.AEaddIntSliderCB('" + plug + "', '" + slider + "')" )
		pc.setParent( u=1 )
	pc.button(label="Select members", c="tkSIGroups.selectMembers()")
	pc.rowLayout(nc=2)
	pc.button(label="Add objects", c="tkSIGroups.addFromSelection()")
	pc.button(label="Remove objects", c="tkSIGroups.removeFromSelection()")
	pc.setParent( u=1 )
	pc.rowLayout(nc=2)
	pc.button(label="Delete groups", c="tkSIGroups.removeGroups()")
	pc.button(label="Refresh overrides", c="tkSIGroups.refreshOverrides()")
	pc.setParent( u=1 )

def AEaddEnumCB( plug, slider ):
	val = pc.optionMenu( slider, q=1, v=1 )
	pc.setAttr( plug, val )
	refreshOverrides()

def AEaddEnumMenu(	plug, sliderLabel, annot, values ):
	obj_Attr = plug.split(".")
	if pc.attributeQuery( obj_Attr[1], node=obj_Attr[0] ,exists=True ):
		pc.rowLayout(nc=2)
		pc.text(label=sliderLabel)
		val = pc.getAttr( plug )
		slider = pc.optionMenu()
		for value in values:
			pc.menuItem( label=value )
		pc.optionMenu( slider, e=1, v=values[val])
		pc.optionMenu( slider, e=1, cc="tkSIGroups.AEaddEnumCB('" + plug + "', '" + slider + "')") 
		pc.setParent( u=1 )

def AEaddVisEnumMenu(	plug, sliderLabel, annot ):
	AEaddEnumMenu(	plug, sliderLabel, annot, VIS_VALUES )

def AEaddSelEnumMenu(	plug, sliderLabel, annot ):
	AEaddEnumMenu(	plug, sliderLabel, annot, SEL_VALUES )


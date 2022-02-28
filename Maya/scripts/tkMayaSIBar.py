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
	Maya "Softimage style" Toolbar
"""

import os
import math

import pymel.core as pc

import OscarZmqMayaString as ozms
import tkMayaCore as tkc
import tkSIGroups

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "v2.8"

G_TRANSCMD = None
G_TRANSMIN = 0
G_TRANSMAX = 0
G_TRANSFIRST = 0
G_TRANSLAST = 0

G_CONSCMD = None
G_CONSMIN = 0
G_CONSMAX = 0
G_CONSFIRST = 0
G_CONSLAST = 0
G_CONSARGS = []

G_PRIMCMD = None
G_PRIMMIN = 0
G_PRIMMAX = 0
G_PRIMFIRST = 0
G_PRIMLAST = 0
G_PRIMARGS = []

G_QTNAME = "tkSIBar"

G_OPT_SELCHANGEDID = "tkSIBarSelChangedID"
G_OPT_SELCHANGEDMUTED = "tkSIBarSelChangedMuted"

G_OPT_UIVISIBLE = "tkMayaSIBarVisible"
G_OPT_PANE = "tkSIBarPane"
G_OPT_DOCK = "tkSIBarDock"

DECIMALS = 3

def showHelp():
	pc.showHelp("https://docs.google.com/document/d/1q_aRS0SVRLwTaLVA8Zm6DHvS6vEcjPFptFu--1kXoe0/pub#h.esf50jvk1bzi", absolute=True)

def deActivate():
	if pc.control(G_QTNAME, query=True, exists=True) and pc.control("tksiSelectionGRP", query=True, visible=True):
		showHide("Selection", False)

def activate():
	if pc.control(G_QTNAME, query=True, exists=True) and not pc.control("tksiSelectionGRP", query=True, visible=True):
		showHide("Selection", True)

def showHide(tabName, inVisible):
	pc.control("tksi"+ tabName +"GRP", edit=True, visible = inVisible)
	pc.control("tksiShow"+ tabName +"BT", edit=True, visible = not inVisible)
	pc.control("tksiShowColorsBT", edit=True, visible = inVisible)

	if tabName == "Selection":
		if inVisible :
			jobId = pc.scriptJob(event=["SelectionChanged", selectionChanged])
			pc.optionVar(intValue=(G_OPT_SELCHANGEDID, jobId))
			pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 0))
			selectionChanged()
		else:
			pc.mel.evalDeferred("scriptJob -kill " + str(pc.optionVar(query=G_OPT_SELCHANGEDID)))
			pc.optionVar(remove = G_OPT_SELCHANGEDID )
			pc.optionVar(remove = G_OPT_SELCHANGEDMUTED )

def lockSelClick():
	updateSelExplorer()

def selExplorerChanged():
	if pc.optionVar(query=G_OPT_SELCHANGEDMUTED) == 1:
		return

	#locked = pc.checkBox("lockSelCB", query=True, value=True)
	pc.select(pc.textScrollList("tksiSelExplorerLB", query=True, selectItem=True), noExpand=True)
	'''
	if locked:
		
		print sel
	else:
		pc.textScrollList("tksiSelExplorerLB", edit=True, selectItem=pc.textScrollList("tksiSelExplorerLB", query=True, allItems=True))
	'''

def updateSelExplorer(sel=None):
	if sel == None:
		sel = pc.ls(sl=True, transforms=True)

	locked = pc.checkBox("lockSelCB", query=True, value=True)
	if not locked:
		pc.textScrollList("tksiSelExplorerLB", edit=True, removeAll=True)
		if len(sel) > 0:
			pc.textScrollList("tksiSelExplorerLB", edit=True, append=sel, selectItem=sel)

def selectionChanged():
	#In rare cases this is called when the window is already closed, just check that a control exists and skip if it does not
	if not pc.control("tksiLocalRB", query=True, exists=True):
		return

	pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 1))
	sel = pc.ls(sl=True, transforms=True)

	isLocal = pc.radioButton("tksiLocalRB", query=True, sl=True)
	space = "transform" if isLocal else "world"
	if len(sel) == 1:
		pc.textField("tksiSelectionNamesLE", edit=True, text=sel[0].name())
		t = sel[0].getTranslation(space=space)
		pc.textField("tksiSelectionPosXLE", edit=True, text=str(round(t[0], DECIMALS)).rstrip("0").rstrip("."))
		pc.textField("tksiSelectionPosYLE", edit=True, text=str(round(t[1], DECIMALS)).rstrip("0").rstrip("."))
		pc.textField("tksiSelectionPosZLE", edit=True, text=str(round(t[2], DECIMALS)).rstrip("0").rstrip("."))

		r = sel[0].getRotation(space=space)
		pc.textField("tksiSelectionRotXLE", edit=True, text=str(round(r[0], DECIMALS)).rstrip("0").rstrip("."))
		pc.textField("tksiSelectionRotYLE", edit=True, text=str(round(r[1], DECIMALS)).rstrip("0").rstrip("."))
		pc.textField("tksiSelectionRotZLE", edit=True, text=str(round(r[2], DECIMALS)).rstrip("0").rstrip("."))

		s = sel[0].getScale()
		pc.textField("tksiSelectionSclXLE", edit=True, text=str(round(s[0], DECIMALS)).rstrip("0").rstrip("."))
		pc.textField("tksiSelectionSclYLE", edit=True, text=str(round(s[1], DECIMALS)).rstrip("0").rstrip("."))
		pc.textField("tksiSelectionSclZLE", edit=True, text=str(round(s[2], DECIMALS)).rstrip("0").rstrip("."))
	
		attrName = pc.textField("tksiSelectionAttrNameLE", query=True, text=True)
		attrType = pc.optionMenu("tksiSelectionAttrTypeCombo", query=True, value=True)

		if attrName != "":
			pc.textField("tksiSelectionAttrValueLE", edit=True, text=evaluate(attrName, "$V", attrType))
	else:
		#Display "maxObjs" names
		maxObjs = 3
		selLen = len(sel)
		if(selLen > 0):
			selNames = sel[0].name()
			for i in range(1,maxObjs):
				if i < selLen:
					selNames = selNames + "," + sel[i].name()

			if selLen > maxObjs:
				selNames = selNames + "...(" + str(selLen) + " total)"
		else:
			selNames = ""

		pc.textField("tksiSelectionNamesLE", edit=True, text=selNames)			

		refValues = ["" for i in range(9)]
		valuesToTest = list(range(9))
		textFieldKeys = ["PosX","PosY","PosZ","RotX","RotY","RotZ","SclX","SclY","SclZ"]

		epsilon = 1 / math.pow(10, DECIMALS)

		for obj in sel:
			trans = []
			trans.extend(obj.getTranslation(space=space))
			trans.extend(obj.getRotation(space=space))
			trans.extend(obj.getScale())

			toRemove = []
			for i in valuesToTest:
				if refValues[i] != "" and math.fabs(refValues[i] - trans[i]) > epsilon:
					refValues[i] = ""
					toRemove.append(i)
				else:
					refValues[i] = trans[i]

			for i in toRemove:
				valuesToTest.remove(i)

		for i in range(9):
			formattedVal = refValues[i]
			if refValues[i] != "":
				formattedVal = str(round(refValues[i], DECIMALS))
				if formattedVal != "0":
					formattedVal = formattedVal.rstrip("0").rstrip(".")

			pc.textField("tksiSelection"+textFieldKeys[i]+"LE", edit=True, text=formattedVal)

	#Selection explorer
	updateSelExplorer(sel)

	pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 0))

def prefix():
	pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 1))
	pc.textField("tksiSelectionNamesLE", edit=True, text="PREFIX-")
	pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 0))

def suffix():
	pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 1))
	pc.textField("tksiSelectionNamesLE", edit=True, text="SUFFIX+")
	pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 0))

def replace():
	pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 1))
	pc.textField("tksiSelectionNamesLE", edit=True, text="SEARCH|REPLACE*")
	pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 0))

def remove():
	pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 1))
	pc.textField("tksiSelectionNamesLE", edit=True, text="5/ #(debut) ou -5/ (fin)")
	pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 0))

def precisionChanged():
	global DECIMALS
	DECIMALS = int(pc.optionMenu("tksiPrecisionCombo", query=True, value=True).split(" ")[0])
	selectionChanged()

def updateSelectionSets():
	pc.textScrollList("tksiSetsLB", edit=True, removeAll=True)
	if pc.optionVar(exists = tkc.OPT_SELSETS):
		sets = pc.optionVar(query = tkc.OPT_SELSETS )
		if len(sets) > 0:
			pc.textScrollList("tksiSetsLB", edit=True, append=sets)

def createSelSet():
	name = pc.textField("tksiSetsNameLE", query=True, text=True)
	tkc.storeSelection(name)
	updateSelectionSets()

def deleteSelSet():
	selItems = pc.textScrollList("tksiSetsLB", query=True, selectItem=True)
	if len(selItems) > 0 and pc.confirmDialog( title='Confirm', message='Are you sure you want to delete items "%s" ?' %",".join(selItems), button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' ) == "Yes":
		for item in selItems:
			tkc.cleanPreset(item)

		updateSelectionSets()

def getSelectedItemsObjects():
	sel=[]
	selItems = pc.textScrollList("tksiSetsLB", query=True, selectItem=True)
	for item in selItems:
		coll = tkc.loadCollection(item, False)
		for obj in coll:
			if not obj in sel:
				sel.append(obj)

	return sel

def selSelSet():
	sel=getSelectedItemsObjects()

	if len(sel) > 0:
		pc.select(sel, replace=True)
		print ("#select "+ " ".join([o.name() for o in sel]))
		print ("pc.select("+ ",".join(['"{0}"'.format(o.name()) for o in sel]) +")")

def addToSelSet():
	sel=getSelectedItemsObjects()
	if len(sel) > 0:
		pc.select(sel, add=True)

def removeFromSelSet():
	sel=getSelectedItemsObjects()
	if len(sel) > 0:
		pc.select(sel, deselect=True)

def createUI():
	dirname, filename = os.path.split(os.path.abspath(__file__))
	ui = pc.loadUI(uiFile=dirname + "/UI/TkMayaSIBar.ui")

	return ui

def cleanUI():
	if pc.control(G_QTNAME, query=True, exists=True):
		pc.deleteUI(G_QTNAME, control=True)
		pc.deleteUI(pc.optionVar(query=G_OPT_DOCK), control=True)
		pc.optionVar(remove = G_OPT_DOCK )

		jobId = pc.optionVar(query=G_OPT_SELCHANGEDID)
		if jobId != 0 :
			pc.mel.evalDeferred("scriptJob -kill " + str(jobId))
			pc.optionVar(remove = G_OPT_SELCHANGEDID )

		tkc.clearHelpLine()

		print ("tkMayaSIBar killed, options and events cleaned")

def UIVisChanged(args):
	#Defer the execution in case hidiung is temporary (docking/undocking)
	pc.evalDeferred("tksi.cleanIfHidden()")

def cleanIfHidden():
	if not pc.control(pc.optionVar(query=G_OPT_DOCK), query=True, visible=True):
		pc.evalDeferred("tksi.cleanUI()")

def toggleUI():
	if pc.control(G_QTNAME, query=True, exists=True):
		cleanUI()
	else:
		showUI()

def showUI():
	global G_QTNAME 
	cleanUI()

	mainWindow = pc.mel.eval("$tmp = $gMainPane")
	dockLayout = pc.paneLayout(configuration='single', parent=mainWindow)
	dockName = pc.dockControl(allowedArea='all', area='right', floating=False, content=dockLayout, label='TK SI ToolBar', vcc=UIVisChanged)

	G_QTNAME = createUI()
	pc.showWindow(G_QTNAME)

	#Initialization
	showHide("Selection", True)
	updateSelectionSets()

	pc.control(G_QTNAME, e=True, parent=dockLayout)

	pc.optionVar(stringValue=(G_OPT_DOCK, dockName)) 

	tkc.helpLog("SIBar " + VERSIONINFO + " loaded")

#/!\ Nampespaces !!
# maybe create new namespaces on the fly
def setName():
	if pc.optionVar(query=G_OPT_SELCHANGEDMUTED) == 1:
		return

	ignoreNamespace = pc.checkBox("siIgnoreNamespace", query=True, value=True)
	pattern = pc.textField("tksiSelectionNamesLE", query=True, text=True)

	sel = pc.ls(sl=True)
	counter = 0
	for obj in sel:
		newName = tkc.parseValue(pattern, "string", obj.name(), counter, inAllowComments=True, inExcludeNS=ignoreNamespace)
		if newName != None:
			print (obj, newName)
			tkc.rename(obj, newName, renameAttrs=True)
		counter = counter + 1

	pc.evalDeferred(selectionChanged)

def selectHierarchyClick():
	allObjs = []

	for sel in pc.selected():
		allObjs.append(sel)
		allObjs.extend(tkc.getChildren(sel, True))

	pc.select(list(set(allObjs)))

def setSelection():
	print (pc.textScrollList("tksiSelectionNamesLV", query=True, selectItem=True))

def setSpace(inGlobal):
	if inGlobal:
		pc.manipMoveContext("Move", edit=True, mode=2)
		pc.manipRotateContext("Rotate", edit=True, mode=1)
		pc.manipScaleContext("Scale", edit=True, mode=2)
	else:
		pc.manipMoveContext("Move", edit=True, mode=0)
		pc.manipRotateContext("Rotate", edit=True, mode=0)
		pc.manipScaleContext("Scale", edit=True, mode=0)
	selectionChanged()

def setSRT(transform, xyz):
	if pc.optionVar(query=G_OPT_SELCHANGEDMUTED) == 1:
		return

	sel = pc.ls(sl=True, transforms=True)

	if len(sel) == 0:
		return

	isLocal = pc.radioButton("tksiLocalRB", query=True, sl=True)
	space = "transform" if isLocal else "world"

	axis = ["", "X", "Y", "Z"]
	textFieldKey = ["", "Pos", "Rot", "Scl"]

	value = pc.textField("tksiSelection" + textFieldKey[transform] + axis[xyz] + "LE", query=True, text=True)


	values = []

	selLen = len(sel)
	for i in range(selLen):
		obj = sel[i]
		if transform == 1:
			oldValues = obj.getTranslation(space=space)
			oldValue = oldValues[xyz -1]
			oldValues[xyz -1] = tkc.parseValue(value, "double", str(oldValue), i, selLen)
			values.append(oldValues)
		elif transform == 2:
			oldValues = ozms.getPymelRotation(obj, space=space)
			oldValue = oldValues[xyz -1]
			oldValues[xyz -1] = tkc.parseValue(value, "double", str(oldValue), i, selLen)
			values.append(oldValues)
		else:
			oldValues = obj.getScale()
			oldValue = oldValues[xyz -1]
			oldValues[xyz -1] = tkc.parseValue(value, "double", str(oldValue), i, selLen)
			values.append(oldValues)

	for i in range(selLen):
		obj = sel[i]
		if transform == 1:
			#obj.setTranslation(values[i], space=space)
			tkc.setTRS(obj, inTValues = values[i], inTrans=True, inRot=False, inScl=False, inWorldSpace=not isLocal)
		elif transform == 2:
			#obj.setRotation(values[i], space=space)
			tkc.setTRS(obj, inRValues = values[i], inTrans=False, inRot=True, inScl=False, inWorldSpace=not isLocal)
		else:
			#obj.setScale(values[i], space=space)
			tkc.setTRS(obj, inSValues = values[i], inTrans=False, inRot=False, inScl=True, inWorldSpace=not isLocal)

	pc.evalDeferred(selectionChanged)

def setAttr():
	attrName = pc.textField("tksiSelectionAttrNameLE", query=True, text=True)
	attrValue = pc.textField("tksiSelectionAttrValueLE", query=True, text=True)
	attrType = pc.optionMenu("tksiSelectionAttrTypeCombo", query=True, value=True)

	tkc.storeSelection()
	#if attrName starts with CONST_CNSVARIABLE ("$CNS") + ".", we want to act on contraints of this object
	lenConst = len(tkc.CONST_CNSVARIABLE) + 1
	if attrName[:lenConst] == "%s." % tkc.CONST_CNSVARIABLE:
		attrName = attrName[lenConst:]
		sel = pc.ls(sl=True)
		cons = []
		for selObj in sel:
			objCons = tkc.getConstraints(selObj)
			if len(objCons) > 0:
				cons.extend(objCons)

		if len(cons) > 0:
			pc.select(cons, replace=True)

	#if attrName starts with CONST_SHAPEVARIABLE ("$SHP") + ".", we want to act on shapes of this object
	lenConst = len(tkc.CONST_SHAPEVARIABLE) + 1
	if attrName[:lenConst] == "%s." % tkc.CONST_SHAPEVARIABLE:
		attrName = attrName[lenConst:]
		sel = pc.ls(sl=True)
		shps = []
		for selObj in sel:
			objShps = selObj.getShapes()
			if len(objShps) > 0:
				shps.extend(objShps)

		if len(shps) > 0:
			pc.select(shps, replace=True)

	tkc.setAttrParseOnSel(attrName, attrValue, strType=attrType)
	tkc.loadSelection()

def evaluate(attrName, attrValue, attrType):
	strCurValue = ""

	tkc.storeSelection()
	#if attrName starts with CONST_CNSVARIABLE ("$CNS") + ".", we want to act on contraints of this object
	lenConst = len(tkc.CONST_CNSVARIABLE) + 1
	if attrName[:lenConst] == "%s." % tkc.CONST_CNSVARIABLE:
		attrName = attrName[lenConst:]
		sel = pc.ls(sl=True)
		cons = []
		for selObj in sel:
			objCons = tkc.getConstraints(selObj)
			if len(objCons) > 0:
				cons.extend(objCons)

		if len(cons) > 0:
			pc.select(cons, replace=True)

	lenConst = len(tkc.CONST_SHAPEVARIABLE) + 1
	if attrName[:lenConst] == "%s." % tkc.CONST_SHAPEVARIABLE:
		attrName = attrName[lenConst:]
		sel = pc.ls(sl=True)
		shps = []
		for selObj in sel:
			objShps = selObj.getShapes()
			if len(objShps) > 0:
				shps.extend(objShps)

		if len(shps) > 0:
			pc.select(shps, replace=True)

	sel = pc.ls(sl=True)
	if len(sel) > 0:
		if pc.attributeQuery(attrName , node=sel[0].name(), exists=True ):
			strCurValue = str(pc.getAttr(sel[0].name() + "." + attrName))
		else:
			pc.warning(sel[0].name() + "." + attrName + " don't exists")

	tkc.loadSelection()

	return 	str(tkc.parseValue(attrValue, attrType, strCurValue))

def evaluateClick():
	attrName = pc.textField("tksiSelectionAttrNameLE", query=True, text=True)
	attrValue = pc.textField("tksiSelectionAttrValueLE", query=True, text=True)
	attrType = pc.optionMenu("tksiSelectionAttrTypeCombo", query=True, value=True)

	pc.textField("tksiSelectionAttrValueLE", edit=True, text=evaluate(attrName, attrValue, attrType))
	tkc.loadSelection()

def attrName():
	attribName = pc.optionMenu("tksiSelectionAttrNameCB", query=True, value=True)
	if " (" in attribName:
		attribName_attribType = attribName.split(" (")
		attribName_attribType[1] = attribName_attribType[1][:-1]
		pc.textField("tksiSelectionAttrNameLE", edit=True, text=attribName_attribType[0])
		pc.optionMenu("tksiSelectionAttrTypeCombo", edit=True, value=attribName_attribType[1])
		pc.optionMenu("tksiSelectionAttrNameCB", edit=True, value="Attr name :")

def freeze():
	tkc.pickSession("freeze", 1, 1, 0, 0, "Select an object to freeze !")

def freezeModeling():
	tkc.pickSession("freezeModeling", 1, 1, 0, 0, "Select an object to freezeModeling !")

def transformCommand():
	cmd = pc.optionMenu("TransformCombo", query=True, value=True)
	global G_TRANSCMD
	global G_TRANSMIN
	global G_TRANSMAX
	global G_TRANSFIRST
	global G_TRANSLAST

	if cmd == "Transform" or "----" in cmd:
		if cmd != "Transform":
			pc.optionMenu("TransformCombo", edit=True, value="Transform")
		return

	G_TRANSCMD = "No command"

	if cmd == "Reset All Transforms":
		G_TRANSCMD = "resetTRS";G_TRANSMIN=1;G_TRANSMAX=1;G_TRANSFIRST=0;G_TRANSLAST=0
		tkc.pickSession("resetTRS", 1, 1)
	elif cmd == "Reset Scale":
		G_TRANSCMD = "resetS";G_TRANSMIN=1;G_TRANSMAX=1;G_TRANSFIRST=0;G_TRANSLAST=0
		tkc.pickSession("resetS", 1, 1)
	elif cmd == "Reset Rotation":
		G_TRANSCMD = "resetR";G_TRANSMIN=1;G_TRANSMAX=1;G_TRANSFIRST=0;G_TRANSLAST=0
		tkc.pickSession("resetR", 1, 1)
	elif cmd == "Reset Translation":
		G_TRANSCMD = "resetT";G_TRANSMIN=1;G_TRANSMAX=1;G_TRANSFIRST=0;G_TRANSLAST=0
		tkc.pickSession("resetT", 1, 1)
	elif cmd == "Set Neutral Pose":
		G_TRANSCMD = "setNeutralPose";G_TRANSMIN=1;G_TRANSMAX=99;G_TRANSFIRST=0;G_TRANSLAST=0
		tkc.pickSession("setNeutralPose", 1, 1)
	elif cmd == "Remove Neutral Pose":
		G_TRANSCMD = "removeNeutralPose";G_TRANSMIN=1;G_TRANSMAX=99;G_TRANSFIRST=0;G_TRANSLAST=0
		tkc.pickSession("removeNeutralPose", 1, 1)
	elif cmd == "Match All Transforms":
		G_TRANSCMD = "matchTRS";G_TRANSMIN=2;G_TRANSMAX=2;G_TRANSFIRST=0;G_TRANSLAST=1
		tkc.pickSession("matchTRS", 2, 2, 0, 1)
	elif cmd == "Match Scale":
		G_TRANSCMD = "matchS";G_TRANSMIN=2;G_TRANSMAX=2;G_TRANSFIRST=0;G_TRANSLAST=1
		tkc.pickSession("matchS", 2, 2, 0, 1)
	elif cmd == "Match Rotation":
		G_TRANSCMD = "matchR";G_TRANSMIN=2;G_TRANSMAX=2;G_TRANSFIRST=0;G_TRANSLAST=1
		tkc.pickSession("matchR", 2, 2, 0, 1)
	elif cmd == "Match Translation":
		G_TRANSCMD = "matchT";G_TRANSMIN=2;G_TRANSMAX=2;G_TRANSFIRST=0;G_TRANSLAST=1
		tkc.pickSession("matchT", 2, 2, 0, 1)
	else :
		pc.error("Unrecognized command " + cmd)

	pc.textField("repeatTransLE", edit=True, text=G_TRANSCMD)
	pc.optionMenu("TransformCombo", edit=True, value="Transform")

def repeatTransformClick():
	global G_TRANSCMD
	global G_TRANSMIN
	global G_TRANSMAX
	global G_TRANSFIRST
	global G_TRANSLAST

	if G_TRANSCMD != None:
		print ("repeating " + G_TRANSCMD + " with " + str((G_TRANSMIN, G_TRANSMAX, G_TRANSFIRST, G_TRANSLAST)))
		tkc.pickSession(G_TRANSCMD, G_TRANSMIN, G_TRANSMAX, G_TRANSFIRST, G_TRANSLAST)

def constrainCommand():
	cmd = pc.optionMenu("ConstrainCombo", query=True, value=True)
	global G_CONSCMD
	global G_CONSMIN
	global G_CONSMAX
	global G_CONSFIRST
	global G_CONSLAST
	global G_CONSARGS

	if cmd == "Constrain" or "----" in cmd:
		if cmd != "Constrain":
			pc.optionMenu("ConstrainCombo", edit=True, value="Constrain")
		return

	G_CONSCMD = "No command"

	if cmd == "Unpin all":
		tkc.unpinAll()
	elif cmd == "Pin Object into Position":
		sel = pc.selected()
		for selObj in sel:
			tkc.constrain(selObj, None, "Pin")
	elif cmd == "Position" or cmd == "Orientation" or cmd == "Scaling" or cmd == "Direction" or cmd == "Pose (parent)" or cmd == "Path (percent)" or cmd == "Curve (param)" or cmd == "Surface (point on poly)" or cmd == "Follicle":
		realCnsName = cmd
		if " " in realCnsName:
			realCnsName = realCnsName.split(" ")[0]

		cnsNArgs = 2
		cnsArgs = [realCnsName, True]
		cnsLastInArgs = 1

		if realCnsName == "Path" or realCnsName == "Curve":
			cnsArgs = [realCnsName, True]
			cnsLastInArgs = 1
		if realCnsName == "Curve":
			realCnsName = "Path"
			cnsNArgs = 2
			cnsArgs = [realCnsName, True, True]
			cnsLastInArgs = 1
		if realCnsName == "Surface":
			cnsArgs = [realCnsName, True, False]
		if realCnsName == "Follicle":
			print ("realCnsName", realCnsName)
			realCnsName = "Surface"
			cnsArgs = [realCnsName, True, True]

		G_CONSCMD = "constrain("+realCnsName+")";G_CONSMIN=cnsNArgs;G_CONSMAX=cnsNArgs;G_CONSFIRST=0;G_CONSLAST=cnsLastInArgs;G_CONSARGS=cnsArgs
		repeatConstrainClick()
	elif cmd == "Remove all constraints":
		G_CONSCMD = "removeAllCns()";G_TRANSMIN=1;G_TRANSMAX=1;G_TRANSFIRST=0;G_TRANSLAST=0
		tkc.pickSession("removeAllCns", 1, 1)
	elif cmd == "Select constraining":
		G_CONSCMD = "selectConstraining()";G_TRANSMIN=1;G_TRANSMAX=1;G_TRANSFIRST=0;G_TRANSLAST=0
		tkc.pickSession("selectConstraining", 1, 1)
	elif cmd == "Select constrained":
		G_CONSCMD = "selectConstrained()";G_TRANSMIN=1;G_TRANSMAX=1;G_TRANSFIRST=0;G_TRANSLAST=0
		tkc.pickSession("selectConstrained", 1, 1)
	else :
		pc.error("Unrecognized command " + cmd)

	pc.textField("repeatConsLE", edit=True, text=G_CONSCMD)
	pc.optionMenu("ConstrainCombo", edit=True, value="Constrain")

def repeatConstrainClick():
	global G_CONSCMD
	global G_CONSMIN
	global G_CONSMAX
	global G_CONSFIRST
	global G_CONSLAST
	global G_CONSARGS

	if G_CONSCMD != None:
		if "Path" in G_CONSCMD:
			G_CONSARGS[1] = pc.checkBox("cnsCompCB", query=True, value=True)
		else:
			print ("G_CONSARGS", G_CONSARGS)
			G_CONSARGS[1] = pc.checkBox("cnsCompCB", query=True, value=True)
		tkc.pickSession(G_CONSCMD.split("(")[0], G_CONSMIN, G_CONSMAX, G_CONSFIRST, G_CONSLAST, "Select constrained then constraining", True, False, *G_CONSARGS)

def rigObjCommand():
	cmd = pc.optionMenu("RigObjectsCombo", query=True, value=True)
	global G_PRIMCMD
	global G_PRIMMIN
	global G_PRIMMAX
	global G_PRIMFIRST
	global G_PRIMLAST
	global G_PRIMARGS

	if cmd == "Rig primitives" or "----" in cmd:
		if cmd != "Rig primitives":
			pc.optionMenu("RigObjectsCombo", edit=True, value="Rig primitives")
		return

	
	mode = pc.optionMenu("RigObjectsModeCB", query=True, value=True)
	suffix = mode
	if cmd == "Controller":
		suffix = "Ctrl"
	elif cmd == "Deformer":
		suffix = "Def"

	G_PRIMCMD = "createRigObject("+cmd+","+mode +")"
	G_PRIMMIN=1;G_PRIMMAX=1;G_PRIMFIRST=0;G_PRIMLAST=0;G_PRIMARGS=["$OBJNAME_" + suffix, cmd, mode, True]
	repeatRigObjClick()

	pc.textField("repeatRigObjsLE", edit=True, text=G_PRIMCMD)
	pc.optionMenu("RigObjectsCombo", edit=True, value="Rig primitives")

def repeatRigObjClick():
	global G_PRIMCMD
	global G_PRIMMIN
	global G_PRIMMAX
	global G_PRIMFIRST
	global G_PRIMLAST
	global G_PRIMARGS

	if G_PRIMCMD != None:
		tkc.pickSession(G_PRIMCMD.split("(")[0], G_PRIMMIN, G_PRIMMAX, G_PRIMFIRST, G_PRIMLAST, "Select an object as reference to create new primitive", True, True, *G_PRIMARGS)

def parentClick():
	tkc.pickSession("parent", 2, 2, 0, 1, "Select child then parent")

def cutClick():
	tkc.pickSession("parent", 1, 1, 0, 0, "Select object to cut", True, False, None, pc.checkBox("siRememberParentCB", query=True, value=True))

def unCutClick():
	tkc.reParent(pc.ls(sl=True))

def childCompClick():
	if pc.checkBox("childCompCB", query=True, value=True):
		pc.mel.eval("setTRSPreserveChildPosition true;")
	else:
		pc.mel.eval("setTRSPreserveChildPosition false;")

def cnsCompClick():
	if pc.checkBox("cnsCompCB", query=True, value=True):
		sel = pc.ls(sl=True)
		for obj in sel:
			tkc.compensateCns(obj)
		pass

def colorCommand(color):
	if color==None:
		tkc.pickSession("clearObjectColor", 1, 1, 0, 0, "Select an object to color !")
	else:
		tkc.pickSession("setObjectColor", 1, 1, 0, 0, "Select an object to color !", True, True, color)

	tkSIGroups.refreshOverrides()

def select():
	pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 1))

	names = pc.textField("tksiSelectNameLE", query=True, text=True)
	types = pc.optionMenu("tksiSelectTypeLE", query=True, value=True)
	tranforms = pc.checkBox("tksiSelectTransformsLE", query=True, value=True)
	selection = pc.checkBox("tksiSelectFilterCB", query=True, value=True)

	if names == "*" and types == "*":
		if pc.confirmDialog( title='Confirm', message="Your request could return a lot of results and take a while to execute, do it anyway ?", button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' ) != "Yes":
			return

	if names == "*":
		names = ["*", "*:*"]
	elif "," in names:
		names = names.split(",")
		oldNames = names[:]
		for name in oldNames:
			if not ":" in name and name.startsWith("*"):
				if not "*:"+name in names:
					names.append("*:"+name)

	if "," in types:
		types = types.split(",")
	else:
		types = [types]

	objects = []

	filterFunctions = []
	realTypes = []
	if len(types) > 0 and types != ["*"]:
		for filterType in types:
			if "(" in filterType:
				filterFunctions.append(filterType)
			else:
				realTypes.append(filterType)

	if len(realTypes) > 0:
		objects = pc.ls(names, type=realTypes, selection=selection)
	else:
		objects = pc.ls(names, selection=selection)

	if tranforms:
		objectsTransforms = []
		for obj in objects:
			if issubclass(obj.__class__, pc.nodetypes.DagNode):
				if obj.type() != "joint" and obj.type() != "transform":
					trans = obj.getParent()

					if not trans in objectsTransforms:
						objectsTransforms.append(trans)
				else:
					objectsTransforms.append(obj)
		objects = objectsTransforms

	if len(filterFunctions) > 0:
		for strFunc in filterFunctions:
			filteredObjects = objects[:]
			for obj in filteredObjects:
				#print "eval", strFunc.replace(";", ",").replace("$OBJ", "'{0}'".format(obj.name()))
				if not eval(strFunc.replace(";", ",").replace("$OBJ", "'{0}'".format(obj.name()))):
					objects.remove(obj)

	pc.select(objects, noExpand=True)

	pc.optionVar(intValue=(G_OPT_SELCHANGEDMUTED, 0))

def haveAttr(inObj, inAttr):
	return pc.attributeQuery(inAttr, node=inObj, exists=True)  
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
	Maya ".ma" format simple parser
	Used to retrieve static values from all attributes of specified nodes (regular expressions)  
	Credits : Vincent Guibert - Ellipsanime Angouleme : Original idea and request
"""

import os
import re

import pymel.core as pc

__author__ = "Cyril GIBAUD - Toonkit"

MASIGNATURE = ""
MALINES = []

def loadMA(inPath):
	global MALINES
	global MASIGNATURE
	
	if not os.path.isfile(inPath):
		pc.warning("File not found (%s)" % inPath)
		return []
	elif os.path.splitext(inPath)[1] != ".ma":
		pc.warning("Wrong file kind, '.ma' expected (%s)" % inPath)
		return []
		
	#Check if we already have a file stamp
	if inPath == MASIGNATURE:
		return MALINES
	
	MALINES = []
	MASIGNATURE = ""
	
	f = None
	try:
		f = open(inPath, 'r')
		MALINES =  f.readlines()
		MASIGNATURE = inPath
	except Exception as e:
		pc.warning("Cannot load .ma file from " + inPath + " : " + str(e))
	finally:
		if f != None:
			f.close()
		return MALINES
		
	return MALINES

def saveMA(inPath):
	if os.path.splitext(inPath)[1] != ".ma":
		pc.warning("Wrong file kind, '.ma' expected (%s)" % inPath)

	f = None
	try:
		f = open(inPath, 'w')
		f.writelines(MALINES)
	except Exception as e:
		pc.warning("Cannot save .ma file to " + inPath + " : " + str(e))
	finally:
		if f != None:
			f.close()

def removeLines(inLinesIndices=None):
	global MALINES

	if len(inLinesIndices) > 0:
		inLinesIndices.sort(reverse=True)

		for lineToRemove in inLinesIndices:
			del MALINES[lineToRemove]

def removeRequires(*exceptArgs):
	linesToRemove = []
	foundOne = False

	for i in range(len(MALINES)):
		if MALINES[i].startswith("requires"):
			foundOne = True

			exception = False
			for exceptArg in exceptArgs:
				print MALINES[i], exceptArg
				if MALINES[i].startswith(exceptArg):
					exception = True
					break

			if exception:
				continue

			linesToRemove.append(i)

		elif foundOne:
			break

	removeLines(linesToRemove)

def polishMA(inPath, backup=True):
	content = loadMA(inPath)
	if len(content) == 0:
		return

	if backup:
		saveMA(inPath.replace(".ma", "_BCK.ma"))

	removeRequires("requires maya")

	saveMA(inPath)

def getAttributes(inPath, inNodes, inProgress=True):
	attributes = {}
	lines = loadMA(inPath)
	
	setAttrRegex = re.compile(".*setAttr( -\S \S+ | )\"\.(\S+)\"( -type \".+\" | )(.*);")
	regexes = []
	
	for node in inNodes:
		regexes.append([re.compile("createNode .* -n \""+ node +"\""), node])
	
	counter = 0
	linesLength = len(lines)
	
	gMainProgressBar = None
	if inProgress:
		gMainProgressBar = mel.eval('$tmp = $gMainProgressBar')
		pc.progressBar( gMainProgressBar,
		edit=True,
		beginProgress=True,
		isInterruptable=True,
		status="Searching in .ma file...",
		maxValue=100 )
	
	factor = 100.0 / linesLength
	lastStep = 0
	
	while(counter < linesLength):
		line = lines[counter]
		if line != "\t":
			for regex in regexes:
				if regex[0].search(line):
					while lines[counter+1][0] == "\t":
						matchObj = setAttrRegex.match(lines[counter+1])
						if matchObj:
							isValid = False
							flag = matchObj.group(1).strip()
							attr = matchObj.group(2).strip()
							type = matchObj.group(3).strip()
							value = matchObj.group(4).strip()
							
							if "double3" in type:
								splitVal = value.split(" ")
								try:
									value = [float(val) for val in splitVal]
									isValid = True
								except:
									pass
							else:
								if value == "no" or value == "off":
									value = False
									isValid = True
								elif value == "yes" or value == "on":
									value = True
									isValid = True
								else:
									try:
										value = float(value)
										isValid = True
									except:
										pass
	
							if isValid:
								attributes[regex[1] + "." + attr] = (attr, value, type, flag, counter+1)
							else:
								pass
								#print "Attribute not managed yet %s : %s (%s)" % (attr, value, type)
						counter+=1
					break
		counter += 1
		
		counterPercent = int(factor * counter)
		if inProgress and counterPercent > lastStep:
			pc.progressBar(gMainProgressBar, edit=True, step=counterPercent - lastStep)
			lastStep = counterPercent

	if inProgress:
		pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

	return attributes

def setValuesFromOtherScene(inObjects, inPath, revertNotFound=True, addShapes=True, inIgnoreNamespace=False):
	#prepare searching list
	nodesToSearch = []
	nodes = []
	
	attributesChanges = {}
	
	for obj in inObjects:
		subObjects = [obj]
		if addShapes and obj.type() == "transform":
			subObjects.extend(obj.getShapes())
		for subObj in subObjects:
			nodes.append(subObj)
			if inIgnoreNamespace and subObj.namespace():
				ns = subObj.namespace()
				if ns != "":
					nodesToSearch.append(subObj.name().replace(ns, ".*:"))
				else:
					nodesToSearch.append("(.*:|)"+subObj.name())
			else:
				nodesToSearch.append(subObj.name())

	if len(nodesToSearch) > 0:
		attrs = getAttributes(inPath, nodesToSearch)
		if len(attrs) > 0:
			changedParams = {}
			attrsKeys = attrs.keys()
			for i in range(len(nodesToSearch)):
				changedParams[nodes[i].name()] = []
				found = False
				
				for attrKey in attrsKeys:
					if nodesToSearch[i] in attrKey:
						found = True
						attrOtherValues = attrs[attrKey]
						if pc.attributeQuery(attrOtherValues[0], node=nodes[i], exists=True):
							attrName = nodes[i].name() + "." + attrOtherValues[0]
							oldValue = pc.getAttr(attrName)
							changedParams[nodes[i].name()].append(attrOtherValues[0])
							#print "%s => %s (%s)" % (attrName, oldValue, attrOtherValues[1])
							if oldValue != attrOtherValues[1]:
								changed = False
								attributesChanges[attrName] = (oldValue, attrOtherValues[1])
								
								try:
									if "double3" in attrOtherValues[2]:
										pc.setAttr(attrName, attrOtherValues[1], type="double3")
										changed = True
									else:
										pc.setAttr(attrName, attrOtherValues[1])
										changed = True
								except Exception as e:
									pc.warning(str(e))

								if not changed:
									pc.warning("Cannot set attribute value %s => %s (%s)" % (attrName, str(attrOtherValues[1]), attrOtherValues[2]))
				if not found:
					print "Can't find attributes for node %s" % nodes[i].name()

			#Reset values to default if not overriten by other scene
			if revertNotFound:
				for i in range(len(nodesToSearch)):
					inobject = nodes[i]
					params = pc.listAttr(inobject, keyable=True, shortNames=True)
					dynParams = pc.listAttr(inobject, userDefined=True, shortNames=True)
					for param in params:
						if not param in changedParams[inobject.name()]:
							attrName = inobject.name() + "." + param
							if param == "v":
								pc.setAttr(attrName, 1)
							if param == "tx" or param == "ty" or param == "tz":
								if not "t" in changedParams[inobject.name()]:
									pc.setAttr(attrName, 0.0)
							elif param == "rx" or param == "ry" or param == "rz":
								if not "r" in changedParams[inobject.name()]:
									pc.setAttr(attrName, 0.0)
							elif param == "sx" or param == "sy" or param == "sz":
								if not "s" in changedParams[inobject.name()]:
									pc.setAttr(attrName, 1.0)
							else:
								if param in dynParams:
									default = pc.addAttr(attrName, query=True, defaultValue=True)
									if default != None:
										pc.setAttr(attrName, default)
									else:
										pc.warning("Cannot reset %s to default..." % attrName)

		else:
			pc.warning("No attributes found with given search patterns (%s) !" % str(nodesToSearch))
			
	else:
		pc.warning("No objects given !")
		
	return attributesChanges

'''
Tests

path = "Z:\\EllipseAngouleme\\testKitchen_done.ma"
nodes = ["*:AmbientLight_BTY_NGTShape"]

#setValuesFromOtherScene( pc.ls(sl=True), path, inIgnoreNamespace=False)

rslt = tkc.benchIt(setValuesFromOtherScene, pc.ls(sl=True), path)
print rslt[1]

print rslt[0]
print rslt[1]

params = pc.listAttr(inobject, keyable=True, shortNames=True)
for param in params:
	attrName = inobject.name() + "." + param
	default = pc.addAttr(attrName, query=True, defaultValue=True)
	if default != None:
		pc.setAttr(attrName, default)
'''
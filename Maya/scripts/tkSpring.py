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
	Maya "tkSpringNode" convenience methods
"""

import os
import shutil

import pymel.core as pc
import pymel.core.system as pcsys

import tkMayaCore as tkc

__author__ = "Cyril GIBAUD - Toonkit"

TK_SPRING_TYPE = "tkSpring"
MSG_NOSPRINGS = "No '"+TK_SPRING_TYPE+"'s found. Maybe your scene don't have any or you didn't select any valid targets or 'springy' objects..."

def create(target=None, collider=None, node=None, name="tkSpringNode"):
	if(target is None):
		pc.error("You must provide at least a target !")

	if(node is None):
		springObjName = tkc.getUniqueName("SpringObject")
		node = pc.spaceLocator(name=springObjName)
		pc.parent(node, target)

	springNode = pc.createNode(TK_SPRING_TYPE, name=name)
	pc.connectAttr(target.name() + ".matrix", springNode + ".targetMat")
	pc.connectAttr(springNode + ".outputTrans", node.name() + ".translate")
	pc.connectAttr(node.name() + ".parentMatrix[0]", springNode + ".parentMat")
	pc.connectAttr("time1.outTime", springNode + ".time")

	if(not collider is None):
		pc.connectAttr(collider.name() + ".matrix", springNode + ".colliderMat")
		pc.setAttr(springNode + ".collide", True)

	return springNode

def collect(objects=[]):
	springs = []
	if len(objects) == 0:
		springs = pc.ls(type=TK_SPRING_TYPE)
	else:
		for obj in objects:
			cons=[]
			if pc.nodeType(obj) == TK_SPRING_TYPE:
				cons.append(obj)
			else:
				cons = pc.listConnections(obj, type=TK_SPRING_TYPE)
			
			if len(cons) == 0:
				#No springs found at this point, consider whole hierarchy
				root = tkc.getParent(obj, root=True)
				if root != None:
					children = tkc.getChildren(root, True)
					for child in children:
						subCons = pc.listConnections(child, type=TK_SPRING_TYPE)
						if len(subCons) > 0:
							cons.extend(subCons)
							break
			if len(cons) > 0:
				for springCon in cons:
					if not springCon in springs:
						springs.append(springCon)
	return springs

def select():
	springs = collect(pc.ls(sl=True))
	springsLen = len(springs)
	if springsLen == 0:
		pc.select(clear=True)
		pc.error(MSG_NOSPRINGS)
		return

	pc.select(springs, replace=True)
	springNames = [obj.name() for obj in springs]
	pc.warning(str(springsLen) + " '" + TK_SPRING_TYPE + ("' was" if springsLen == 1 else "s' were") + " selected (" + str(springNames) + ")")

def initializeSpring(inSpring, startFrame=None, endFrame=None):
	if startFrame == None:
		startFrame = pc.playbackOptions(query=True, animationStartTime=True)
	if endFrame == None:
		endFrame = pc.playbackOptions(query=True, animationEndTime=True)

	pc.setAttr(inSpring + ".startFrame", startFrame)
	pc.setAttr(inSpring + ".endFrame", endFrame)

def activate(value=True, initialize=False):
	springs = collect(pc.ls(sl=True))
	if len(springs) == 0:
		pc.error(MSG_NOSPRINGS)
		return

	startFrame = endFrame = None
	if initialize:
		startFrame = pc.playbackOptions(query=True, animationStartTime=True)
		endFrame = pc.playbackOptions(query=True, animationEndTime=True)

	for spring in springs:
		if initialize:
			initializeSpring(spring, startFrame, endFrame)
		tkc.setRealAttr(spring + ".reset", not value)

def initialize():
	springs = collect(pc.ls(sl=True))
	if len(springs) == 0:
		pc.error(MSG_NOSPRINGS)
		return
	
	startFrame = pc.playbackOptions(query=True, animationStartTime=True)
	endFrame = pc.playbackOptions(query=True, animationEndTime=True)

	for spring in springs:
		initializeSpring(spring, startFrame, endFrame)

def on():
	activate(True, True)

def off():
	activate(False, False)

def cache(value=True, manageCacheAnim=True):
	springs = collect(pc.ls(sl=True))
	if len(springs) == 0:
		pc.error(MSG_NOSPRINGS)
		return

	if manageCacheAnim:
		if value:#Rebuild cache
			cache(False)

			minStartFrame = 1000000000
			maxEndFrame = -1000000000
			springBounds = []
			for spring in springs:
				startFrame = pc.getAttr(spring + ".startFrame")
				endFrame = pc.getAttr(spring + ".endFrame")
				springBounds.append([startFrame, endFrame])

				if startFrame < minStartFrame:
					minStartFrame = startFrame
				if endFrame > maxEndFrame:
					maxEndFrame = endFrame

			for frame in range(int(minStartFrame), int(maxEndFrame) + 1):
				pc.currentTime(frame, edit=True, update=True )
				for springId in range(len(springs)):
					spring = springs[springId]
					bounds = springBounds[springId]

					if bounds[0] <= frame and frame <= bounds[1]:
						attenuationAttr = spring + ".attenuation"#tkc.getRealAttr(spring + ".attenuation")
						#print "attenuationAttr",attenuationAttr,"orig",spring + ".attenuation"
						attenuation = pc.getAttr(attenuationAttr)
						mul = 0 if attenuation >=1.0 else 1.0/(1.0-attenuation)

						pc.setKeyframe(spring + ".cX", value=pc.getAttr(spring + ".otX") * mul)
						pc.setKeyframe(spring + ".cY", value=pc.getAttr(spring + ".otY") * mul)
						pc.setKeyframe(spring + ".cZ", value=pc.getAttr(spring + ".otZ") * mul)

		else:#Clean cache
			for spring in springs:
				cons = pc.listConnections(spring + ".cacheTransX", type=["animCurveTU", "animCurveUU"])
				cons.extend(pc.listConnections(spring + ".cacheTransY", type=["animCurveTU", "animCurveUU"]))
				cons.extend(pc.listConnections(spring + ".cacheTransZ", type=["animCurveTU", "animCurveUU"]))
				for con in cons:
				    pc.delete(con)

	for spring in springs:
		pc.cutKey(spring, attribute="cache")
		pc.setAttr(spring + ".cache", value)

def testScene():
	sourcePath = "Z:\\ToonKit\\RnD\\Src\\TK_SpringNode\\x64\\Release\\tkSpringNode.mll"
	destPath = "Z:\\ToonKit\\RnD\\MAYA\\WORKGROUP_2013x64\\plug-ins\\tkSpringNode.mll"

	pcsys.newFile(force=True)
	pc.unloadPlugin( 'tkSpringNode.mll' )
	shutil.copy(sourcePath, destPath);
	pc.loadPlugin( 'tkSpringNode.mll' )

	#Create objects for spring 1
	targetRef = pc.spaceLocator(name="SpringRef")
	targetLoc = pc.spaceLocator(name="SpringTarget")
	pc.parent(targetLoc, targetRef)
	collider = pc.group(name="SpringCollider", empty=True, parent=targetRef)

	colliderCtrl = tkc.createCubeIcon("SpringColliderCtrl")
	pc.parent(colliderCtrl, targetLoc)
	pContraint = pc.parentConstraint(colliderCtrl,collider, name=collider.name() + "_prCns")
	sConstraint = pc.scaleConstraint(colliderCtrl,collider, name=collider.name() + "_sCns")

	springNode = create(targetLoc, collider)

	#Create objects for spring 2
	targetRef1 = pc.spaceLocator(name="SpringRef1")
	targetLoc1 = pc.spaceLocator(name="SpringTarget1")
	pc.parent(targetLoc1, targetRef1)
	collider1 = pc.group(name="SpringCollider1", empty=True, parent=targetRef1)

	colliderCtrl1 = tkc.createCubeIcon("SpringColliderCtrl1")
	pc.parent(colliderCtrl1, targetLoc1)
	pContraint1 = pc.parentConstraint(colliderCtrl1,collider1, name=collider1.name() + "_prCns")
	sConstraint1 = pc.scaleConstraint(colliderCtrl1,collider1, name=collider1.name() + "_sCns")

	springNode1 = create(targetLoc1, collider1)


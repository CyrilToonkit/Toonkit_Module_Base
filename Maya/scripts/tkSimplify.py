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

#Simplify Spoky's Bipeds to Video game constraints (Unity)
# Just simple envelope deformations
# Minimum envelopes (41 ?)
# 3 per Leg/Foot * 2	= 6
# 3 for Spine			= 3
# 2 for Tail 			= 2
# 2 per Arm * 2			= 4
# 9 per Hand * 2		= 18
# 2 for Head/Neck		= 2
# 1 per Eye * 2			= 2
# 1-2 per Ear * 2 		= 2 - 4
#------------------------------
# 						= 39 - 41

import pymel.core as pc
import pymel.core.system as pmsys

import tkMayaCore as tkc

__author__ = "Cyril GIBAUD - Toonkit"

# Some constants
toOptimize = []

def append(inStr, sided=False, ancestor="", remove=True):
	if sided:
		toOptimize.append(["Left_" + inStr, ("Left_" + ancestor if not "*" in ancestor else ancestor.replace("*", "")), remove])
		toOptimize.append(["Right_" + inStr, ("Right_" + ancestor if not "*" in ancestor else ancestor.replace("*", "")), remove])
	else:
		toOptimize.append([inStr, ancestor, remove])

def cleanKeySets(charName):
	keySetsProp = pc.PyNode(charName + ":" + charName + "_TK_KeySets")
	keySets = tkc.getParameters(keySetsProp)
	
	for keySet in keySets:
		values = pc.getAttr(keySetsProp.name() + "." + keySet).replace("$", charName + ":").split(",")
		newValues = []
		for value in values:
			if pc.objExists(value):
				newValues.append(value.replace(charName + ":", "$"))
		
		if len(newValues) == 0:
			pc.deleteAttr(keySetsProp, at=keySet)
			print keySet + " is empty, keySet removed"
		else:
			pc.setAttr(keySetsProp.name() + "." + keySet, ",".join(newValues))

def mergeAsset(inNS, inTargetNS):
	#merge Geometries
	geoLoc = pc.PyNode(inNS + ":Geometries")
	targetGeoLoc = pc.PyNode(inTargetNS + ":Geometries")
	
	geos = tkc.getChildren(geoLoc, False);
	
	for geo in geos:
		tkc.parent(geo, targetGeoLoc)
	
	#merge Rigs
	rigLoc = pc.PyNode(inNS + ":TKRig")
	targetRigLoc = pc.PyNode(inTargetNS + ":TKRig")
	
	rigs = tkc.getChildren(rigLoc, False);
	
	for rig in rigs:
		tkc.parent(rig, targetRigLoc)
		
	#merge KeySets
	keySetsProp = pc.PyNode(inNS + ":" + inNS + "_TK_KeySets")
	keySets = tkc.getParameters(keySetsProp)
	
	targetKeySetsProp = pc.PyNode(inTargetNS + ":" + inTargetNS + "_TK_KeySets")
	targetKeySets = tkc.getParameters(targetKeySetsProp)
	
	for keySet in keySets:
		set = keySetsProp.name() + "." + keySet
		if keySet in targetKeySets:
			targetSet = targetKeySetsProp.name() + "." + keySet
			pc.setAttr(targetSet, pc.getAttr(targetSet) + "," + pc.getAttr(set))
		else:
			tkc.addParameter(targetKeySetsProp, keySet, "string", pc.getAttr(set))
	
	#merge VisHolder
	visHolder = pc.PyNode(inNS + ":TK_VisHolder_Root")
	visHolderCtrl = pc.PyNode(inNS + ":VisHolder_Main_Ctrl")
	targetVisHolderCtrl = pc.PyNode(inTargetNS + ":VisHolder_Main_Ctrl")
	
	holderContent = tkc.getChildren(visHolder, True)
	holderContent.append(visHolder);
	
	for holderObj in holderContent:
		tkc.rename(holderObj, holderObj.name().replace(":", ":" + inNS + "_"))
		
	tkc.parent(visHolder, targetRigLoc)
	
	pc.setAttr(visHolder.name() + ".visibility", 0)
	
	visParams = tkc.getParameters(visHolderCtrl)
	targetVisParams = tkc.getParameters(targetVisHolderCtrl)
	
	for visParam in visParams:
		if visParam in targetVisParams:
			pc.connectAttr(targetVisHolderCtrl.name() + "." + visParam, visHolderCtrl.name() + "." + visParam, force=True)
		else:
			pc.warning("Can't find" + visParam)
	
	#delete the rest
	pc.delete(inNS + ":" + inNS)

def simplifyBiped(ns):
	#HANDS
	append("Thumb_Claw_Bone_Ctrl", True)
	append("Index_Claw_Bone_Ctrl", True)
	append("Middle_Claw_Bone_Ctrl", True)
	append("Ring_Claw_Bone_Ctrl", True)
	
	append("Meta_Index", True)
	append("Meta_Middle", True)
	append("Ring_Meta_Bone_Ctrl", True)
	append("Thumb_1", True)
	append("Index_2", True)
	append("Middle_2", True)
	append("Ring_2_Bone_Ctrl", True)
	append("Ring_0_Bone_Ctrl", True, "Middle_0")
	append("Ring_1_Bone_Ctrl", True, "Middle_1")

	#SHOULDERS
	append("Shoulder", True, "*Spine_Reverse_0")

	#FEET
	append("Foot_Toe_1_Claw_Bone_Ctrl", True)
	append("Foot_Toe_1_Bone_Ctrl", True)
	append("Foot_Toe_2_Claw_Bone_Ctrl", True)
	append("Foot_Toe_2_Bone_Ctrl", True)
	append("Foot_Toe_3_Claw_Bone_Ctrl", True)
	append("Foot_Toe_3_Bone_Ctrl", True)
	
	append("Foot_FK_1", True, "Foot_FK_0")
	append("Foot_Reverse_1", True)

	#TAIL
	append("Tail_Spring2_Bone_Ctrl")
	append("Tail_Spring4_Bone_Ctrl")
	append("Tail_Spring6_Bone_Ctrl")
	append("Tail_Spring8_Bone_Ctrl")
	append("Tail_Spring10_Bone_Ctrl")

	#SPINE
	append("Spine_Reverse_2", False, "Spine_Reverse_3", False)

	#NECK
	append("Neck_FK_2")
	append("Neck_FK_3")

	#FACIAL
	append("Head_Buldge_Start", False, "Head_FK")
	append("Top_Teeth_Main_Ctrl", False, "Head_FK")
	append("Bottom_Teeth_Main_Ctrl", False, "Head_FK")
	append("Jaw_Bone_Ctrl", False, "Head_FK")
	append("TK_Jaw_Locals_Main_Ctrl", False, "Head_FK")
	append("Cheek", True, "*Head_FK")

	append("Tongue_3", True, "*Head_FK")
	append("Tongue_2", True, "*Head_FK")
	append("Tongue_1", True, "*Head_FK")
	append("Tongue_3", False, "Head_FK")
	append("Tongue_2", False, "Head_FK")
	append("Tongue_1", False, "Head_FK")
	append("Tongue_0", False, "Head_FK")

	append("UpperLid_Bone_Ctrl", True, "*Head_FK")
	append("LowerLid_Bone_Ctrl", True, "*Head_FK")
	append("UpperEye_Curve", True, "*Head_FK")
	append("LowerEye_Curve", True, "*Head_FK")
	append("Pupille_Main_Ctrl", True, "*Head_FK")
	append("Eyelid_Out", True, "*Head_FK")
	append("Eyelid_In", True, "*Head_FK")
	append("Eyelid_In", True, "*Head_FK")

	append("TK_Left_MouthCorner_Locals_Main_Ctrl", False, "*Head_FK")
	append("TK_Right_MouthCorner_Locals_Main_Ctrl", False, "*Head_FK")

	append("UpperLip_Center", False, "Head_FK")
	append("LowerLip_Center", False, "Head_FK")
	append("UpperLip_CenterDef_Main_Ctrl", False, "Head_FK")
	append("LowerLip_CenterDef_Main_Ctrl", False, "Head_FK")

	append("MouthCorner", True, "*Head_FK")
	append("Levator_Handle_1_Control", True, "*Head_FK")
	append("Zygo_Handle_1_Control", True, "*Head_FK")
	append("Riso_Handle_2_Control", True, "*Head_FK")
	append("Depressor_Handle_1_Control", True, "*Head_FK")
	append("UpperLip_Inter", True, "*Head_FK")
	append("LowerLip_Inter", True, "*Head_FK")

	append("Nose_Bone_Bone_Ctrl", False, "Head_FK")
	append("Nose_Bone_Ctrl", False, "Head_FK")

	append("Second_EyeBrow_Point0_Ctrl_Control", True, "*Head_FK")
	append("Eyebrow_Mid", True, "*Head_FK")

	append("TK_Left_EyeBrow1_Switch1_Root", False, "Head_FK")
	append("TK_Left_EyeBrow1_Switch2_Root", False, "Head_FK")
	append("TK_Left_EyeBrow2_Switch1_Root", False, "Head_FK")
	append("TK_Left_EyeBrow2_Switch2_Root", False, "Head_FK")
	append("TK_Left_EyeBrow3_Switch1_Root", False, "Head_FK")
	append("TK_Left_EyeBrow3_Switch2_Root", False, "Head_FK")

	append("TK_Right_EyeBrow1_Switch1_Root", False, "Head_FK")
	append("TK_Right_EyeBrow1_Switch2_Root", False, "Head_FK")
	append("TK_Right_EyeBrow2_Switch1_Root", False, "Head_FK")
	append("TK_Right_EyeBrow2_Switch2_Root", False, "Head_FK")
	append("TK_Right_EyeBrow3_Switch1_Root", False, "Head_FK")
	append("TK_Right_EyeBrow3_Switch2_Root", False, "Head_FK")

	#Ears/Fur
	append("Meche_Orient_Main_Ctrl", False, "Head_FK")
	append("Ear_Orient_Main_Ctrl", True, "*Head_FK")
	append("Fur_Ear_Orient_Main_Ctrl", True, "*Head_FK")
	append("Fur_Ear_Spring_Bone_Ctrl", True, "*Head_FK")

	append("Fur1_Orient_Main_Ctrl", False)
	append("Fur1_Spring_Bone_Ctrl", False)
	append("Fur2_Orient_Main_Ctrl", False)
	append("Fur2_Spring_Bone_Ctrl", False)
	
	append("Meche_0_Spring_Bone_Ctrl", False, "Head_FK")
	append("Lower_Teeth_1_Main_Ctrl", True, "*Head_FK")
	append("Lower_Teeth_Middle_Main_Ctrl", False, "*Head_FK")
	append("Upper_Teeth_1_Main_Ctrl", True, "*Head_FK")
	
	append("Mustache_Spring_Bone_Ctrl", True, "*Head_FK")
	append("Mustache_Spring1_Bone_Ctrl", True, "*Head_FK")
	append("Mustache_Spring3_Bone_Ctrl", True, "Mustache_Spring2_Bone_Ctrl")
	
	append("Noeud_Pape_Bone_Ctrl", True, "*Head_FK")
	
	#LAUNCH
	gMainProgressBar = pc.mel.eval('$tmp = $gMainProgressBar')
	pc.progressBar( gMainProgressBar,
				edit=True,
				beginProgress=True,
				isInterruptable=False,
				status="Simplify Rig ",
				maxValue=len(toOptimize))

	for objData in toOptimize:
		strObj = objData[0]
		tkRig.safeByPassNode(ns, objData[0], objData[1], objData[2])
		pc.progressBar(gMainProgressBar, edit=True, step=1)

	pc.progressBar(gMainProgressBar, edit=True, endProgress=True)

	#Post-processes
	newDeformers = []
	deleteDeformers=True

	#Neck deformers !!
	oldDefs = [pc.PyNode(ns + ":TK_NECK_Deformers_Deform_1")]
	oldDefs.append(pc.PyNode(ns + ":TK_NECK_Deformers_Deform_3"))
	oldDefs.append(pc.PyNode(ns + ":TK_NECK_Deformers_Deform_7"))
	tkc.replaceDeformers(oldDefs, pc.PyNode(ns + ":TK_NECK_Deformers_Deform_5"), doDelete=deleteDeformers)

	#LEGS (Roundings can have two names : "Rounding_Deformer" or "Skin"...)
	#Legs deformers !!
	#Left_Leg
	roundingName = "Rounding_Deformer" if pc.objExists(ns + ":TK_Left_LEG_Rounding_Deformer_Deformer_1") else "Skin"
	
	newDef0 = tkc.createRigObject(pc.PyNode(ns + ":TK_Left_LEG_start_switch_Child"), name="Left_Leg_Joint0", type="Deformer", mode="child", match=True)
	newDeformers.append(newDef0)
	pc.setAttr(newDef0.name() + ".radius", 0.3)
	oldDefs = [pc.PyNode(ns + ":TK_Left_LEG_"+ roundingName +"_Deformer_1")]
	oldDefs.append(pc.PyNode(ns + ":TK_Left_LEG_"+ roundingName +"_Deformer_2"))
	oldDefs.append(pc.PyNode(ns + ":TK_Left_LEG_"+ roundingName +"_Deformer_3"))
	oldDefs.append(pc.PyNode(ns + ":TK_Left_LEG_"+ roundingName +"_Deformer_4"))
	tkc.replaceDeformers(oldDefs, newDef0, doDelete=deleteDeformers)

	newDef1 = tkc.createRigObject(pc.PyNode(ns + ":TK_Left_LEG_middle_switch_Child"), name="Left_Leg_Joint1", type="Deformer", mode="child", match=True)
	newDeformers.append(newDef1)
	pc.setAttr(newDef1.name() + ".radius", 0.3)
	oldDefs = [pc.PyNode(ns + ":TK_Left_LEG_"+ roundingName +"_Deformer_7")]
	oldDefs.append(pc.PyNode(ns + ":TK_Left_LEG_"+ roundingName +"_Deformer_6"))
	oldDefs.append(pc.PyNode(ns + ":TK_Left_LEG_"+ roundingName +"_Deformer_5"))
	tkc.replaceDeformers(oldDefs, newDef1, doDelete=deleteDeformers)

	#Right_Leg
	newDef0 = tkc.createRigObject(pc.PyNode(ns + ":TK_Right_LEG_start_switch_Child"), name="Right_Leg_Joint0", type="Deformer", mode="child", match=True)
	newDeformers.append(newDef0)
	pc.setAttr(newDef0.name() + ".radius", 0.3)
	oldDefs = [pc.PyNode(ns + ":TK_Right_LEG_"+ roundingName +"_Deformer_1")]
	oldDefs.append(pc.PyNode(ns + ":TK_Right_LEG_"+ roundingName +"_Deformer_2"))
	oldDefs.append(pc.PyNode(ns + ":TK_Right_LEG_"+ roundingName +"_Deformer_3"))
	oldDefs.append(pc.PyNode(ns + ":TK_Right_LEG_"+ roundingName +"_Deformer_4"))
	tkc.replaceDeformers(oldDefs, newDef0, doDelete=deleteDeformers)

	newDef1 = tkc.createRigObject(pc.PyNode(ns + ":TK_Right_LEG_middle_switch_Child"), name="Right_Leg_Joint1", type="Deformer", mode="child", match=True)
	newDeformers.append(newDef1)
	pc.setAttr(newDef1.name() + ".radius", 0.3)
	oldDefs = [pc.PyNode(ns + ":TK_Right_LEG_"+ roundingName +"_Deformer_7")]
	oldDefs.append(pc.PyNode(ns + ":TK_Right_LEG_"+ roundingName +"_Deformer_6"))
	oldDefs.append(pc.PyNode(ns + ":TK_Right_LEG_"+ roundingName +"_Deformer_5"))
	tkc.replaceDeformers(oldDefs, newDef1, doDelete=deleteDeformers)

	#ARMS
	#Arms deformers !!
	#Left_Arm
	armRoundingName = "Rounding_Deformer" if pc.objExists(ns + ":TK_Left_Rounding_Deformer_Deformer_1") else "Arm_Skin"
	
	newDef0 = tkc.createRigObject(pc.PyNode(ns + ":TK_Left_ARM_Start_Switch_Child"), name="Left_ARM_Joint0", type="Deformer", mode="child", match=True)
	newDeformers.append(newDef0)
	pc.setAttr(newDef0.name() + ".radius", 0.3)
	oldDefs = [pc.PyNode(ns + ":TK_Left_"+ armRoundingName +"_Deformer_1")]
	oldDefs.append(pc.PyNode(ns + ":TK_Left_"+ armRoundingName +"_Deformer_2"))
	oldDefs.append(pc.PyNode(ns + ":TK_Left_"+ armRoundingName +"_Deformer_3"))
	oldDefs.append(pc.PyNode(ns + ":TK_Left_"+ armRoundingName +"_Deformer_4"))
	tkc.replaceDeformers(oldDefs, newDef0, doDelete=deleteDeformers)

	newDef1 = tkc.createRigObject(pc.PyNode(ns + ":TK_Left_ARM_Middle_Switch_Child"), name="Left_ARM_Joint1", type="Deformer", mode="child", match=True)
	newDeformers.append(newDef1)
	pc.setAttr(newDef1.name() + ".radius", 0.3)
	oldDefs = [pc.PyNode(ns + ":TK_Left_"+ armRoundingName +"_Deformer_7")]
	oldDefs.append(pc.PyNode(ns + ":TK_Left_"+ armRoundingName +"_Deformer_6"))
	oldDefs.append(pc.PyNode(ns + ":TK_Left_"+ armRoundingName +"_Deformer_5"))
	tkc.replaceDeformers(oldDefs, newDef1, doDelete=deleteDeformers)

	#Right_Arm
	newDef0 = tkc.createRigObject(pc.PyNode(ns + ":TK_Right_ARM_Start_Switch_Child"), name="Right_ARM_Joint0", type="Deformer", mode="child", match=True)
	newDeformers.append(newDef0)
	pc.setAttr(newDef0.name() + ".radius", 0.3)
	oldDefs = [pc.PyNode(ns + ":TK_Right_"+ armRoundingName +"_Deformer_1")]
	oldDefs.append(pc.PyNode(ns + ":TK_Right_"+ armRoundingName +"_Deformer_2"))
	oldDefs.append(pc.PyNode(ns + ":TK_Right_"+ armRoundingName +"_Deformer_3"))
	oldDefs.append(pc.PyNode(ns + ":TK_Right_"+ armRoundingName +"_Deformer_4"))
	tkc.replaceDeformers(oldDefs, newDef0, doDelete=deleteDeformers)

	newDef1 = tkc.createRigObject(pc.PyNode(ns + ":TK_Right_ARM_Middle_Switch_Child"), name="Right_ARM_Joint1", type="Deformer", mode="child", match=True)
	newDeformers.append(newDef1)
	pc.setAttr(newDef1.name() + ".radius", 0.3)
	oldDefs = [pc.PyNode(ns + ":TK_Right_"+ armRoundingName +"_Deformer_7")]
	oldDefs.append(pc.PyNode(ns + ":TK_Right_"+ armRoundingName +"_Deformer_6"))
	oldDefs.append(pc.PyNode(ns + ":TK_Right_"+ armRoundingName +"_Deformer_5"))
	tkc.replaceDeformers(oldDefs, newDef1, doDelete=deleteDeformers)

	#Connect new deformers visibilities
	for newDef in newDeformers:
		pc.setAttr(newDef.name() + ".overrideEnabled", 1)
		pc.connectAttr( ns + ":VisHolder_Main_Ctrl.Deformers",newDef.name() + ".overrideVisibility")

	#'Unnecessary' cleaning
	# Arm roundings
	pc.delete(ns + ":TK_Left_"+ armRoundingName +"_Root")
	pc.delete(ns + ":TK_Left_Tangent_Root")
	pc.delete(ns + ":TK_Right_"+ armRoundingName +"_Root")
	pc.delete(ns + ":TK_Right_Tangent_Root")
	#  need to "re-parent" Arm/Hand holders
	tkc.constrain(pc.PyNode(ns + ":TK_Left_Arm_ParamHolder_Root"), pc.PyNode(ns + ":Left_ARM_Joint1"))
	tkc.constrain(pc.PyNode(ns + ":TK_Left_Hand_ParamHolder_Root"), pc.PyNode(ns + ":TK_Left_Hand_Bone_0_0_Deform"))
	tkc.constrain(pc.PyNode(ns + ":TK_Right_Arm_ParamHolder_Root"), pc.PyNode(ns + ":Right_ARM_Joint1"))
	tkc.constrain(pc.PyNode(ns + ":TK_Right_Hand_ParamHolder_Root"), pc.PyNode(ns + ":TK_Right_Hand_Bone_0_0_Deform"))
	#Arm unrolls
	pc.delete(ns + ":TK_Left_Unroll_Root")
	pc.delete(ns + ":TK_Right_Unroll_Root")

	# Leg roundings
	pc.delete(ns + ":TK_Left_LEG_"+ roundingName +"_Root")
	pc.delete(ns + ":TK_Left_LEG_Tangent_Root")
	pc.delete(ns + ":TK_Right_LEG_"+ roundingName +"_Root")
	pc.delete(ns + ":TK_Right_LEG_Tangent_Root")
	#  need to "re-parent" Leg/Foot holders
	tkc.constrain(pc.PyNode(ns + ":TK_Left_Leg_ParamHolder_Root"), pc.PyNode(ns + ":Left_Leg_Joint1"))
	tkc.constrain(pc.PyNode(ns + ":TK_Left_Foot_ParamHolder_Root"), pc.PyNode(ns + ":TK_Left_FOOT_FK_0_0_Deform"))
	tkc.constrain(pc.PyNode(ns + ":TK_Right_Leg_ParamHolder_Root"), pc.PyNode(ns + ":Right_Leg_Joint1"))
	tkc.constrain(pc.PyNode(ns + ":TK_Right_Foot_ParamHolder_Root"), pc.PyNode(ns + ":TK_Right_FOOT_FK_0_0_Deform"))
	#Leg unrolls
	pc.delete(ns + ":TK_Left_LEG_Unroll_Root")
	pc.delete(ns + ":TK_Right_LEG_Unroll_Root")

	#Clean keySets
	cleanKeySets(ns)

#--------------------------------------------------------------------------------------------------
#Simplify Spoky
#--------------------------------------------------------------------------------------------------
'''
ns = "ref_rig_spoky"
#simplifyBiped(ns)

#Remove Ears
tkRig.safeByPassNode(ns, "Left_Ear_Spring_Bone_Ctrl", "Head_FK", True)
tkRig.safeByPassNode(ns, "Left_Ear_Spring_1_Bone_Ctrl", "Head_FK", True)
tkRig.safeByPassNode(ns, "Right_Ear_Spring_Bone_Ctrl", "Head_FK", True)
tkRig.safeByPassNode(ns, "Right_Ear_Spring_1_Bone_Ctrl", "Head_FK", True)

secondaryNs = "ref_rig_casque_spoky"
#Import "casque_spoky"
pmsys.importFile("Z:/spoky_pre_prod/RT/ref_rig_casque_spoky.ma", namespace=secondaryNs)

#Optimize "casque_spoky"
tkRig.safeByPassNode(secondaryNs, "Local_SRT", "", True)
globalSRT = pc.PyNode(secondaryNs + ":Global_SRT");
targetGlobalSRT = pc.PyNode(ns + ":Global_SRT");
tkc.constrain(globalSRT, targetGlobalSRT, "Pose")
pc.rename(globalSRT, ns + ":TK_Global_SRT")

globalSRTRoot = pc.PyNode(secondaryNs + ":TK_GlobalSRT_Root");
pc.setAttr(globalSRTRoot.name() + ".visibility", 0)
 
cleanKeySets(secondaryNs)
mergeAsset(secondaryNs, ns)

tkRig.safeByPassNode(ns, "Left_Ear_1_Bone_Ctrl", "Head_FK", True)
tkRig.safeByPassNode(ns, "Right_Ear_1_Bone_Ctrl", "Head_FK", True)

#constrain helmet to head
helmetCnser = pc.PyNode(ns + ":Head_FK_Cnsed_Main_Ctrl");
head = pc.PyNode(ns + ":Head_FK");

tkc.constrain(helmetCnser, head, "Pose")

#deform to head
tkRig.safeByPassNode(ns, "Helmet_Main_Ctrl", "Head_FK", True)

cleanKeySets(ns)
'''

#--------------------------------------------------------------------------------------------------
#Simplify Gouttierez
#--------------------------------------------------------------------------------------------------
'''
ns = "ref_rig_gouttierez"
simplifyBiped(ns)
'''

#--------------------------------------------------------------------------------------------------
#Simplify Siam
#--------------------------------------------------------------------------------------------------
ns = "ref_rig_siam"
simplifyBiped(ns)
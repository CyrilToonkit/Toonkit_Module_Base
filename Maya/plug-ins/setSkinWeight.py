"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Author : Cyril GIBAUD and Mickael GARCIA - Toonkit
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

import sys
import pymel.core as pc
import TkApi.maya_api as tkapi
import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.cmds as cmds

kPluginCmdName = 'setSkinWeight'


# -------------------------------------------------------------------------------------------------
#  Arguments Flags
# -------------------------------------------------------------------------------------------------
classic_linearFlag = "-cl"
classic_linearFlagLong = "-classicLinear"
dual_quaternionFlag = "-dq"
dual_quaternionFlagLong = "-dualQuaternion"
weight_listFlag = "-wl"
weight_listFlagLong = "-weightList"
influenceFlag = "-i"
influenceFlagLong = "-influence"
influence_weightFlag = "-iw"
influence_weightFlagLong = "-influenceWeight"

def maya_useNewAPI():
	"""
	The presence of this function tells Maya that the plugin produces, and
	expects to be passed, objects created using the Maya Python API 2.0.
	"""
	pass


class setSkinWeight( om.MPxCommand ):
    
    def __init__(self):
        om.MPxCommand.__init__(self)
        self.inSkinClusterName = None
        self.classicLinear = False
        self.dualQuaternion = False
        self.weightList = None
        self.influence = None
        self.influenceWeight = None

        self.currentSkinWeight = None

    def doIt(self, args):
        """Function that set skin cluster with diffrents methodes: classicLinear, dualQuaternion, and can replace skin of one given influance.
Usage eg: "pc.setSkinWeight("skinCluster1", wl=weight["classic_linear"], cl=True)" 
            "pc.setSkinWeight("skinCluster1", i="Left_arm_inf", iw = [0.0, 0.0, 1.0, 1.0])"
    Args:
        first no flag arg (str), skinCluster name
        -classicLinear -cl (Bool), is classic linear skin
        -dualQuaternion -dq (Bool), is dual Quaternion skin
        -weightList -wl (list(float)), list of wieghts (eg: see tkapi.get_weights_data)
        -infulence -i (str), name of a joint to replace influances on it with giver influenceWeight
        -influenceWeight -iw, (list(float)), list of wieghts for the given joint"""
        
        self.args = args
        self.dagModifier = om.MDagModifier()
        self.parseArguments( args )
        
        mesh_geo = cmds.skinCluster(self.inSkinClusterName, q=1, g=1)
        self.skin_node = oma.MFnSkinCluster(tkapi.get_api_nodes(self.inSkinClusterName, dag_path=False)[0])
        self.mesh_dag_path = tkapi.get_api_nodes(mesh_geo)[0]
        self.components =  om.MObject()

        self.currentSkinWeight = tkapi.get_weights_data(mesh_geo[0], self.inSkinClusterName)
        if self.weightList is not None:
            self.weightList = om.MDoubleArray(self.weightList)
        
        self.execute()

    def execute(self):
        if self.classicLinear:
            influence_indices = om.MIntArray([i for i in range(len(self.skin_node.influenceObjects()))])
            self.skin_node.setWeights(self.mesh_dag_path, self.components, influence_indices, self.weightList)
        if self.dualQuaternion:
            self.skin_node.setBlendWeights(self.mesh_dag_path, self.components, self.weightList)
        if self.influence is not None:
            inf_index = [i for i, inf in enumerate(self.skin_node.influenceObjects()) if inf.partialPathName() == self.influence][0]
            inf_sel = self.skin_node.getPointsAffectedByInfluence(tkapi.get_api_nodes(self.influence)[0])
            inf_components = tkapi.get_components_from_selection_list(inf_sel[0])
            self.skin_node.setWeights(self.mesh_dag_path, inf_components, inf_index, self.influenceWeight)

    def redoIt(self):
        self.execute()

    def undoIt(self):
        """Undo the last doIt or redoIt execution. No parameters
        """
        if self.classicLinear:
            influence_indices = om.MIntArray([i for i in range(len(self.skin_node.influenceObjects()))])
            self.skin_node.setWeights(self.mesh_dag_path, self.components, influence_indices, self.currentSkinWeight["classic_linear"])
        if self.dualQuaternion:
            self.skin_node.setBlendWeights(self.mesh_dag_path, self.components, self.currentSkinWeight["dual_quaternion"])

    def isUndoable(self):
        return True
        
    def parseArguments(self, args):
        argData = om.MArgParser( self.syntax(), args )
        
        # -first no kwarg argument as skinCluster str name
        self.inSkinClusterName = argData.commandArgumentString(0)

        # -classicLinear -cl argument
        if argData.isFlagSet(classic_linearFlag):
            self.classicLinear = argData.flagArgumentBool(classic_linearFlag, 0)

        # -dualQUaternion -dq argument
        if argData.isFlagSet(dual_quaternionFlag):
            self.classicLinear = argData.flagArgumentBool(dual_quaternionFlag, 0)
        
        numOfUse_weight_listFlag = argData.numberOfFlagUses(weight_listFlag)
        if argData.isFlagSet(weight_listFlag):
            self.weightList = []
            for x in range(numOfUse_weight_listFlag):
                self.weightList.append(argData.getFlagArgumentList(weight_listFlag, x).asFloat(0))

        if argData.isFlagSet(influenceFlag):
            self.influence = argData.getFlagArgumentList(influenceFlag)
        
        if argData.isFlagSet(influence_weightFlag):
            numOfUse_influence_weightFlag = argData.numberOfFlagUses(influence_weightFlag)
            self.influenceWeightList = []
            for x in range(numOfUse_influence_weightFlag):
                self.influenceWeight.append(argData.getFlagArgumentList(influence_weightFlag, x).asFloat(0))


        # ... If there are more flags, process them here ...

##########################################################
# Plug-in initialization.
##########################################################
def cmdCreator():
    return setSkinWeight() 

def syntaxCreator():
    syntax = om.MSyntax()
    syntax.addArg(om.MSyntax.kString)
    syntax.addFlag( classic_linearFlag, classic_linearFlagLong, om.MSyntax.kBoolean)
    syntax.addFlag( dual_quaternionFlag, dual_quaternionFlagLong, om.MSyntax.kBoolean)
    syntax.addFlag( weight_listFlag, weight_listFlagLong, om.MSyntax.kLong)
    syntax.makeFlagMultiUse(weight_listFlag)
    syntax.addFlag( influenceFlag, influence_weightFlagLong, om.MSyntax.kString)
    syntax.addFlag( influence_weightFlag, influence_weightFlagLong, om.MSyntax.kLong)
    syntax.makeFlagMultiUse(influence_weightFlag)
    return syntax
    
def initializePlugin( mobject ):
    ''' Initialize the plug-in when Maya loads it. '''
    mplugin = om.MFnPlugin( mobject,'Original plugin by Mickael Garcia for Toonkit Studio', '1.0', 'Any')
    try:
        mplugin.registerCommand( kPluginCmdName, cmdCreator, syntaxCreator )
    except:
        sys.stderr.write( 'Failed to register command: ' + kPluginCmdName )

def uninitializePlugin( mobject ):
    ''' Uninitialize the plug-in when Maya un-loads it. '''
    mplugin = om.MFnPlugin( mobject )
    try:
        mplugin.deregisterCommand( kPluginCmdName )
    except:
        sys.stderr.write( 'Failed to unregister command: ' + kPluginCmdName )


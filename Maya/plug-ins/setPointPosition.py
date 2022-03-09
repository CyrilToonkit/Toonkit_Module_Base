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

kPluginCmdName = 'setPointPositions'


# -------------------------------------------------------------------------------------------------
#  Arguments Flags
# -------------------------------------------------------------------------------------------------
pointsPositionsFlag = "-pp"
pointsPositionsFlagLong = "-pointsPositions"
worldSpaceFlag = "-ws"
worldSpaceFlagLong = "-worldSpace"

def maya_useNewAPI():
	"""
	The presence of this function tells Maya that the plugin produces, and
	expects to be passed, objects created using the Maya Python API 2.0.
	"""
	pass


class setPointPositions( om.MPxCommand ):
    
    def __init__(self):
        om.MPxCommand.__init__(self)
        self.inObjectName = None
        self.inPOintPositions = None
        self.worldSpace = False
          

    def doIt(self, args):
        """Function that set points position of a given mesh to a given point positions data.
        Args:
            (str) Target object. 
            -pointsPositions -pp: (List(Tuple)) List of tuple of eatch points
            -worldSpace -ws: (bool) allow to set point position in world space or in local space. False by default.
        """
        self.args = args
        self.dagModifier = om.MDagModifier()
        self.parseArguments( args )
        
        if self.worldSpace:
            self.Mspace = om.MSpace.kWorld
        else:
            self.Mspace = om.MSpace.kObject

        if self.inObjectName is None:
            self.inObjectName = pc.ls(sl=True, ap=True)
            if len(self.inObjectName) > 0:
                self.inObjectName = self.inObjectName[0].name()
            else:
                om.MGlobal.displayError("You must use select or give an object as first argument !")
        if not self.inPointPositions:
            om.MGlobal.displayError("You must use pointsPositions (pp) flag !")

        self.MPointPositions = om.MPointArray(self.inPointPositions)
        self.targetDagPath = tkapi.get_api_nodes([self.inObjectName])[0]
        targetDagPathShape = self.targetDagPath.extendToShape()
        if self.targetDagPath.apiType() == 296: # 269 is the id of kMesh object from maya api
            self.target_mPointArray = om.MFnMesh(targetDagPathShape).getFloatPoints(self.Mspace)
        elif self.targetDagPath.apiType() == 294: # 294 is the id of kNurbsSurface object from maya api
            self.target_mPointArray = om.MFnNurbsSurface(targetDagPathShape).cvPositions(self.Mspace)
        elif self.targetDagPath.apiType() == 267: # 267 is the id of kNurbsCurve object from maya api
            self.target_mPointArray = om.MFnNurbsCurve(targetDagPathShape).cvPositions(self.Mspace)
        self.execute()


    def execute(self):
        if len(self.target_mPointArray) == len(self.MPointPositions):
            if self.targetDagPath.apiType() == 296:
                om.MFnMesh(self.targetDagPath).setPoints(self.MPointPositions, self.Mspace)
            elif self.targetDagPath.apiType() == 294:
                om.MFnNurbsSurface(self.targetDagPath).updateSurface()
                om.MFnNurbsSurface(self.targetDagPath).setCVPositions(self.MPointPositions, self.Mspace)
                om.MFnNurbsSurface(self.targetDagPath).updateSurface()
            elif self.targetDagPath.apiType() == 267:
                om.MFnNurbsCurve(self.targetDagPath).setCVPositions(self.MPointPositions, self.Mspace)
                om.MFnNurbsCurve(self.targetDagPath).updateCurve()

    def redoIt(self):
        self.execute()

    def undoIt(self):
        """Undo the last doIt or redoIt execution. No parameters
        """
        if self.targetDagPath.apiType() == 296:
            om.MFnMesh(self.targetDagPath).setPoints(self.target_mPointArray, self.Mspace)
        elif self.targetDagPath.apiType() == 294:
            om.MFnNurbsSurface(self.targetDagPath).setCVPositions(self.target_mPointArray, self.Mspace)
            om.MFnNurbsSurface(self.targetDagPath).updateSurface()
        elif self.targetDagPath.apiType() == 267:
            om.MFnNurbsCurve(self.targetDagPath).setCVPositions(self.target_mPointArray, self.Mspace)
            om.MFnNurbsCurve(self.targetDagPath).updateCurve()

    def isUndoable(self):
        return True
        
    def parseArguments(self, args):
        argData = om.MArgParser( self.syntax(), args )
        
        # -first no kwarg argument
        try:
            self.inObjectName = argData.commandArgumentString(0)
        except:
            self.inObjectName = None

        # -pointsPositions -pp argument
        numOfUse = argData.numberOfFlagUses(pointsPositionsFlag)
        if argData.isFlagSet(pointsPositionsFlag):
            self.inPointPositions = []
            for x in range(numOfUse):
                argList = argData.getFlagArgumentList(pointsPositionsFlag, x)
                self.inPointPositions.append((argList.asFloat(0), argList.asFloat(1), argList.asFloat(2)))
        
        # -worldSpace -ws argument
        if argData.isFlagSet(worldSpaceFlag):
            self.worldSpace = argData.flagArgumentBool(worldSpaceFlag, 0)
            
        
        # ... If there are more flags, process them here ...

##########################################################
# Plug-in initialization.
##########################################################
def cmdCreator():
    return setPointPositions() 

def syntaxCreator():
    syntax = om.MSyntax()
    syntax.addArg(om.MSyntax.kString)
    syntax.addFlag( pointsPositionsFlag, pointsPositionsFlagLong, (om.MSyntax.kDouble, om.MSyntax.kDouble, om.MSyntax.kDouble))
    syntax.makeFlagMultiUse(pointsPositionsFlag)
    syntax.addFlag( worldSpaceFlag, worldSpaceFlagLong, om.MSyntax.kBoolean)
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


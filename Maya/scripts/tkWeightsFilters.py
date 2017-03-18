"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Author : Cyril GIBAUD - Toonkit, Guido Pollini
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

import maya.cmds     as mc
import maya.mel      as mm
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma

__author__ = "Cyril GIBAUD - Toonkit, Guido Pollini"

"""
import tkWeightsFilters
tkWeightsFilters.smooth()
#tkWeightsFilters.sharpen()
#tkWeightsFilters.harden()
"""

def initPaint():
  cmd = '''
    global string $tf_skinSmoothPatin_selection[];

    global proc tf_smoothBrush( string $context )
    {
      artUserPaintCtx -e -ic "tf_init_smoothBrush" -svc "tf_set_smoothBrushValue"
      -fc "" -gvc "" -gsc "" -gac "" -tcc "" $context;
    }

    global proc tf_init_smoothBrush( string $name )
    {
        global string $tf_skinSmoothPatin_selection[];
        
        $tf_skinSmoothPatin_selection = {};
        string $sel[] = `ls -sl -fl`;
        string $obj[] = `ls -sl -o`;
        $objName = $obj[0];
        
        int $i = 0;
        for($vtx in $sel)
        {
            string $buffer[];
            int $number = `tokenize $vtx ".[]" $buffer`;
            $tf_skinSmoothPatin_selection[$i] = $buffer[2];
            $i++;
            if ($number != 0)
                $objName = $buffer[0];
        }
        
        python("import tkWeightsFilters;paint = tkWeightsFilters.weightsFiltersClass()"); 
    }

    global proc tf_set_smoothBrushValue( int $slot, int $index, float $val )        
    {
        global string $tf_skinSmoothPatin_selection[];

            if($tf_skinSmoothPatin_selection[0] != "")
            {
                if( stringArrayContains($index, $tf_skinSmoothPatin_selection) )
                    python("paint.setWeight("+$index+","+$val+")"); 
            }
            else
                python("paint.setWeight("+$index+","+$val+")");        
    }

    global proc tf_sharpenBrush( string $context )
    {
      artUserPaintCtx -e -ic "tf_init_sharpenBrush" -svc "tf_set_sharpenBrushValue"
      -fc "" -gvc "" -gsc "" -gac "" -tcc "" $context;
    }

    global proc tf_init_sharpenBrush( string $name )
    {
        global string $tf_skinSharpenPatin_selection[];
        
        $tf_skinSharpenPatin_selection = {};
        string $sel[] = `ls -sl -fl`;
        string $obj[] = `ls -sl -o`;
        $objName = $obj[0];
        
        int $i = 0;
        for($vtx in $sel)
        {
            string $buffer[];
            int $number = `tokenize $vtx ".[]" $buffer`;
            $tf_skinSharpenPatin_selection[$i] = $buffer[2];
            $i++;
            if ($number != 0)
                $objName = $buffer[0];
        }
        
        python("import tkWeightsFilters;paint = tkWeightsFilters.weightsFiltersClass('sharpen')"); 
    }

    global proc tf_set_sharpenBrushValue( int $slot, int $index, float $val )        
    {
        global string $tf_skinSharpenPatin_selection[];

            if($tf_skinSharpenPatin_selection[0] != "")
            {
                if( stringArrayContains($index, $tf_skinSharpenPatin_selection) )
                    python("paint.setWeight("+$index+","+$val+")"); 
            }
            else
                python("paint.setWeight("+$index+","+$val+")");        
    }

    global proc tf_hardenBrush( string $context )
    {
      artUserPaintCtx -e -ic "tf_init_hardenBrush" -svc "tf_set_hardenBrushValue"
      -fc "" -gvc "" -gsc "" -gac "" -tcc "" $context;
    }

    global proc tf_init_hardenBrush( string $name )
    {
        global string $tf_skinHardenPatin_selection[];
        
        $tf_skinHardenPatin_selection = {};
        string $sel[] = `ls -sl -fl`;
        string $obj[] = `ls -sl -o`;
        $objName = $obj[0];
        
        int $i = 0;
        for($vtx in $sel)
        {
            string $buffer[];
            int $number = `tokenize $vtx ".[]" $buffer`;
            $tf_skinHardenPatin_selection[$i] = $buffer[2];
            $i++;
            if ($number != 0)
                $objName = $buffer[0];
        }
        
        python("import tkWeightsFilters;paint = tkWeightsFilters.weightsFiltersClass('harden')"); 
    }

    global proc tf_set_hardenBrushValue( int $slot, int $index, float $val )        
    {
        global string $tf_skinHardenPatin_selection[];

            if($tf_skinHardenPatin_selection[0] != "")
            {
                if( stringArrayContains($index, $tf_skinHardenPatin_selection) )
                    python("paint.setWeight("+$index+","+$val+")"); 
            }
            else
                python("paint.setWeight("+$index+","+$val+")");        
    }
  '''
  mm.eval(cmd)

def smooth():
  cmd = '''
    ScriptPaintTool;
    artUserPaintCtx -e -tsc "tf_smoothBrush" `currentCtx`;
  '''
  mm.eval(cmd)

def sharpen():
  cmd = '''
    ScriptPaintTool;
    artUserPaintCtx -e -tsc "tf_sharpenBrush" `currentCtx`;
  '''
  mm.eval(cmd)

def harden():
  cmd = '''
    ScriptPaintTool;
    artUserPaintCtx -e -tsc "tf_hardenBrush" `currentCtx`;
  '''
  mm.eval(cmd)

initPaint()

def interpolate(value1, value2, blend):
  return value1 * blend + value2 * (1 - blend) 
 
class weightsFiltersClass():
  
  def __init__(self, filter="smooth"):

    self.filterName = filter

    self.skinCluster = ''
    self.obj = ''
    self.mitVex = ''
    
    # select the skinned geo
    selection = om.MSelectionList()
    om.MGlobal.getActiveSelectionList( selection )

    # get dag path for selection
    dagPath = om.MDagPath()
    components = om.MObject()
    array = om.MIntArray()
    selection.getDagPath( 0, dagPath, components )
    self.obj = dagPath
    dagPath.extendToShape()
    
    # currentNode is MObject to your mesh
    currentNode = dagPath.node()
    self.mitVtx = om.MItMeshVertex (dagPath)
    
    # get skincluster from shape
    try:
      itDG = om.MItDependencyGraph(currentNode, om.MFn.kSkinClusterFilter, om.MItDependencyGraph.kUpstream)
      while not itDG.isDone():
        oCurrentItem = itDG.currentItem()
        fnSkin = oma.MFnSkinCluster(oCurrentItem)
        self.skinCluster = fnSkin
        break
    except:
      mc.error("No skinCluster")
    
    self.jointNames = mc.skinCluster(fnSkin.name(), query=True, inf=True)

  def getFilter(self, nVerts): 
    if self.filterName == "sharpen":
      return (nVerts+1, -1.0)

    return (0, 1.0/nVerts)#return smooth by default

  def setWeight(self, vtx, value):    
    dagPath    = self.obj
    fnSkin     = self.skinCluster
    mitVtx     = self.mitVtx
    jointNames = self.jointNames # the commandEngine "skinPercent" has an horrid syntax with joint names!

    if not fnSkin:    
      om.MGlobal.displayError("No SkinCluster to paint on")
    else:
      component = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
      om.MFnSingleIndexedComponent(component).addElement( vtx )

      oldWeights = om.MDoubleArray()
      surrWeights = om.MDoubleArray()
      infCount = om.MScriptUtil()
      int = infCount.asUintPtr()
      surrVtxArray = om.MIntArray()
      newWeights = om.MDoubleArray()
      infIndices = om.MIntArray()
      prevVtxUtil = om.MScriptUtil( )
      prevVtx = prevVtxUtil.asIntPtr()
      
      # create mesh iterator and get conneted vertices for averaging
      mitVtx = om.MItMeshVertex (dagPath, component)
      mitVtx.getConnectedVertices(surrVtxArray)
      surrVtxCount = len(surrVtxArray)
            
      surrComponents = om.MFnSingleIndexedComponent().create(om.MFn.kMeshVertComponent)
      om.MFnSingleIndexedComponent(surrComponents).addElements( surrVtxArray )
      
      # read weight from single vertex (oldWeights) and from the surrounding vertices (surrWeights)
      fnSkin.getWeights(dagPath, component, oldWeights, int)
      fnSkin.getWeights(dagPath, surrComponents, surrWeights, int)
      influenceCount = om.MScriptUtil.getUint(int)
      
      skinClusterName = fnSkin.name()
      vertexName      = dagPath.fullPathName() + ".vtx[" + str(vtx) + "]"
      transformValues = []
      
      if self.filterName == "harden":
        nonZeroes = []
        oldNonZeroesWeights = []
        lenNonZeroes = 0.0

        for i in range(influenceCount):
          oldWeight = oldWeights[i]
          if oldWeight > 0.0:
            nonZeroes.append(jointNames[i])
            oldNonZeroesWeights.append(oldWeight)

        lenNonZeroes = len(nonZeroes)
        average = 1.0/lenNonZeroes

        for i in range(lenNonZeroes):
          oldWeight = oldNonZeroesWeights[i]
          newWeight = min(1.0,max(0.0, 2 * oldNonZeroesWeights[i] - average))
          transformValues.append((nonZeroes[i], interpolate(newWeight, oldWeight, value)))
      else:
        curFilter = self.getFilter(surrVtxCount)

        for i in range(influenceCount):
          newWeight = oldWeights[i] * curFilter[0]
          oldWeight = oldWeights[i]
          for j in range(i, len(surrWeights), influenceCount):
            newWeight += surrWeights[j] * curFilter[1]
          transformValues.append((jointNames[i], interpolate(min(1.0,max(0.0,newWeight)), oldWeight, value)))

      """ the only commandObject created for each vertex (incapsulated in a bigger undoChunk for each stroke)"""
      mc.skinPercent(skinClusterName, vertexName, transformValue=transformValues)
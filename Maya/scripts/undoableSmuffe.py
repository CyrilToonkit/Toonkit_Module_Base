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

"""
import undoableSmuffe
undoableSmuffe.smuffeItHard()
"""
import maya.cmds     as mc
import maya.mel      as mm
import maya.OpenMaya as om
import maya.OpenMayaAnim as oma

__author__ = "Cyril GIBAUD - Toonkit, Guido Pollini"

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
        
        python("paint = undoableSmuffe.smoothPaintClass()"); 
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
  '''
  mm.eval(cmd)



def smuffeItHard():
  cmd = '''
    ScriptPaintTool;
    artUserPaintCtx -e -tsc "tf_smoothBrush" `currentCtx`;
  '''
  mm.eval(cmd)



initPaint()



class smoothPaintClass():
  
  def __init__(self):
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
      
      for i in range(influenceCount):
        newWeight = 0.0
        for j in range(i, len(surrWeights), influenceCount):
          newWeight += (((surrWeights[j] / surrVtxCount) * value) + ((oldWeights[i] / surrVtxCount) * (1-value)))
        transformValues.append((jointNames[i], newWeight)) 
      
      
      """ the only commandObject created for each vertex (incapsulated in a bigger undoChunk for each stroke)"""
      mc.skinPercent(skinClusterName, vertexName, transformValue=transformValues)



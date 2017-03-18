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

import maya.cmds as cmds

__author__ = "Cyril GIBAUD - Toonkit"

SLIDERS = []
UINAME = "tkPoseScaler"

KINEMATICS = ["tx", "ty", "tz", "rx", "ry", "rz", "sx", "sy", "sz"]
SCALE_VALUES = [1.0,  1.0, 1.0, 1.0,  1.0,1.0,1.0, 1.0,1.0,1.0, 1.0,1.0,1.0]
OLD_VALUES = {}

def scalePoseSelection():
    global OLD_VALUES
    
    transScaleX = SCALE_VALUES[0] * SCALE_VALUES[1] * SCALE_VALUES[4]
    transScaleY = SCALE_VALUES[0] * SCALE_VALUES[1] * SCALE_VALUES[5]
    transScaleZ = SCALE_VALUES[0] * SCALE_VALUES[1] * SCALE_VALUES[6]
    
    rotScaleX = SCALE_VALUES[0] * SCALE_VALUES[2] * SCALE_VALUES[7]
    rotScaleY = SCALE_VALUES[0] * SCALE_VALUES[2] * SCALE_VALUES[8]
    rotScaleZ = SCALE_VALUES[0] * SCALE_VALUES[2] * SCALE_VALUES[9]
    
    sclScaleX = SCALE_VALUES[3] * SCALE_VALUES[10]#Don't take Global/All into account
    sclScaleY = SCALE_VALUES[3] * SCALE_VALUES[11]#Don't take Global/All into account
    sclScaleZ = SCALE_VALUES[3] * SCALE_VALUES[12]#Don't take Global/All into account
    
    scalings = [transScaleX, transScaleY, transScaleZ, rotScaleX, rotScaleY, rotScaleZ, sclScaleX, sclScaleY, sclScaleZ]
    
    sel = cmds.ls(sl=True)
    for selObj in sel:
        for attrIndex in range(9):
            attrName = selObj + "." + KINEMATICS[attrIndex] 
            if not attrName in OLD_VALUES:
                if cmds.getAttr(attrName, settable=True):
                    OLD_VALUES[attrName] = cmds.getAttr(attrName)
                else:
                    OLD_VALUES[attrName] = None
            if OLD_VALUES[attrName] != None:
                cmds.setAttr(attrName, OLD_VALUES[attrName] * scalings[attrIndex])

def init(*args):
    global OLD_VALUES
    global SCALE_VALUES
    OLD_VALUES = {}
    SCALE_VALUES = [1.0,  1.0, 1.0, 1.0,  1.0,1.0,1.0, 1.0,1.0,1.0, 1.0,1.0,1.0]
    
    for slider in SLIDERS:
        cmds.floatSliderGrp( slider, edit=True, value=1.0)

def reset(*args):
    global SCALE_VALUES
    SCALE_VALUES = [1.0,  1.0, 1.0, 1.0,  1.0,1.0,1.0, 1.0,1.0,1.0, 1.0,1.0,1.0]
    scalePoseSelection();
    for slider in SLIDERS:
        cmds.floatSliderGrp( slider, edit=True, value=1.0)

def globalScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[0] = args[0]
    scalePoseSelection();
    
def transScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[1] = args[0]
    scalePoseSelection();

def rotScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[2] = args[0]
    scalePoseSelection();
    
def sclScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[3] = args[0]
    scalePoseSelection();
    
def transXScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[4] = args[0]
    scalePoseSelection();
def transYScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[5] = args[0]
    scalePoseSelection();
def transZScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[6] = args[0]
    scalePoseSelection();
    
def rotXScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[7] = args[0]
    scalePoseSelection();
def rotYScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[8] = args[0]
    scalePoseSelection();
def rotZScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[9] = args[0]
    scalePoseSelection();
    
def sclXScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[10] = args[0]
    scalePoseSelection();
def sclYScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[11] = args[0]
    scalePoseSelection();
def sclZScaleChanged(*args):
    global SCALE_VALUES
    SCALE_VALUES[12] = args[0]
    scalePoseSelection();

def showUI():
    global SLIDERS
    global UINAME

    if cmds.control(UINAME, query=True, exists=True):
        cmds.deleteUI(UINAME, control=True)

    UINAME = cmds.window(UINAME, title='Pose Scaler')
    colLayout = cmds.columnLayout()

    cmds.frameLayout(label="Global", collapsable=True, borderStyle="etchedIn")
    GLOBAL_SLIDER = cmds.floatSliderGrp( label='All', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=globalScaleChanged, cc=globalScaleChanged)
    TRANS_SLIDER = cmds.floatSliderGrp( label='Translation', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=transScaleChanged, cc=transScaleChanged)
    ROT_SLIDER = cmds.floatSliderGrp( label='Rotation', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=rotScaleChanged, cc=rotScaleChanged)
    SCL_SLIDER = cmds.floatSliderGrp( label='Scaling', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=sclScaleChanged, cc=sclScaleChanged)
    cmds.setParent(colLayout)

    cmds.frameLayout(label="Position", collapsable=True, borderStyle="etchedIn")
    TRANSX_SLIDER = cmds.floatSliderGrp( label='TranslationX', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=transXScaleChanged, cc=transXScaleChanged)
    TRANSY_SLIDER = cmds.floatSliderGrp( label='TranslationY', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=transYScaleChanged, cc=transYScaleChanged)
    TRANSZ_SLIDER = cmds.floatSliderGrp( label='TranslationZ', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=transZScaleChanged, cc=transZScaleChanged)
    cmds.setParent(colLayout)
    
    cmds.frameLayout(label="Rotation", collapsable=True, borderStyle="etchedIn")
    ROTX_SLIDER = cmds.floatSliderGrp( label='RotationX', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=rotXScaleChanged, cc=rotXScaleChanged)
    ROTY_SLIDER = cmds.floatSliderGrp( label='RotationY', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=rotYScaleChanged, cc=rotYScaleChanged)
    ROTZ_SLIDER = cmds.floatSliderGrp( label='RotationZ', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=rotZScaleChanged, cc=rotZScaleChanged)
    cmds.setParent(colLayout)

    cmds.frameLayout(label="Scaling", collapsable=True, borderStyle="etchedIn")
    SCLX_SLIDER = cmds.floatSliderGrp( label='ScalingX', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=sclXScaleChanged, cc=sclXScaleChanged)
    SCLY_SLIDER = cmds.floatSliderGrp( label='ScalingY', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=sclYScaleChanged, cc=sclYScaleChanged)
    SCLZ_SLIDER = cmds.floatSliderGrp( label='ScalingZ', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=-1000.0, fieldMaxValue=1000, value=1.0,dc=sclZScaleChanged, cc=sclZScaleChanged)
    cmds.setParent(colLayout)

    SLIDERS = [GLOBAL_SLIDER,TRANS_SLIDER,ROT_SLIDER,SCL_SLIDER,TRANSX_SLIDER,ROTX_SLIDER,SCLX_SLIDER,TRANSY_SLIDER,ROTY_SLIDER,SCLY_SLIDER,TRANSZ_SLIDER,ROTZ_SLIDER,SCLZ_SLIDER]
    cmds.rowLayout(numberOfColumns=2, columnWidth2=[195,195])
    cmds.button(label='Use this pose', width=195, c=init)
    cmds.button(label='Reset', width=195, c=reset)
     
    cmds.showWindow( UINAME )
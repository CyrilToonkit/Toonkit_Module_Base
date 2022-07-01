"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Author : Cyril GIBAUD & Mickael GARCIA - Toonkit
    Copyright (C) 2014-2022 Toonkit
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

import Toonkit_Core.Qt.Components as tkqt
from qtpy import QtWidgets, QtCore
import maya.OpenMaya as om
import tkMayaCore as tkc
import pymel.core as pc
from functools import partial
import tkMayaCore as tkc

DISPLAY_MAYA_WINDOW = "OscarParamEditorWindow"
DISPLAY_DOCK_LAYOUT = "OscarParamEditorLayout" 
DISPLAY_DOCK_WINDOW = "OscarParamEditorDoc"

AVAILABLE_TYPE_ATTR = ["double", "int"]

class OscarParamEditor(QtWidgets.QVBoxLayout):
    def __init__(self, parent=None):
        super(OscarParamEditor, self).__init__(parent)
        self.attrCollection = {}
        self.displayIsChanging = False
        self.centralLayout = QtWidgets.QVBoxLayout()
        grpBox = QtWidgets.QGroupBox()
        grpBox.setLayout(self.centralLayout)
        self.scroll = QtWidgets.QScrollArea()
        self.scroll.setWidget(grpBox)
        self.scroll.setWidgetResizable(True)
        self.addWidget(self.scroll)
        self.spaceItem = QtWidgets.QSpacerItem(20, 5000, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        
        self.mayaEventId = om.MEventMessage.addEventCallback("SelectionChanged", self.updateUI)
        self.updateUI()

    def updateUI(self, *args):
        self.uiElements = {}
        attrCollection = getAttributesCollection(attributes = {})
        if not attrCollection is None:
            self.cleenLayout(layout = self.centralLayout)
        
        for key, values in attrCollection.items():
            attrMax = tkc.getNode(values[-1]).getMax()
            attrMin = tkc.getNode(values[-1]).getMin()
            if attrMax is None:
                attrMax = 100000
            if attrMin is None:
                attrMin = -100000
            spinBox = tkqt.QSpinBoxGrp(self.centralLayout, key, maximum=attrMax, minimum=attrMin, uiMin = -100, uiMax = 100,  decimals = 3)
            spinBox.valueChanged.connect(partial(self.updateValues, spinBox))
            spinBox.editingFinished.connect(partial(self.updateValueLast, spinBox))
            self.uiElements[key] = spinBox
            newValues = []
            for x in values:
                newValues.append(pc.getAttr(x))
            spinBox.values = newValues
            spinBox.updateUI()
        self.attrCollection = attrCollection
        if len(self.uiElements) > 0:
            self.centralLayout.addItem(self.spaceItem)

    def updateValues(self, uiObj, *args):
        if not self.displayIsChanging:
            pc.undoInfo(openChunk=True, chunkName="Update Displays")
            self.displayIsChanging = True
        for niceName, uiElements in self.uiElements.items():
            if uiElements == uiObj:
                for index, trueAttr in enumerate(self.attrCollection[niceName]):
                    pc.setAttr(trueAttr, uiElements.values[index])
    
    def updateValueLast(self, uiObj, *args):
        for niceName, uiElements in self.uiElements.items():
            if uiElements == uiObj:
                for index, trueAttr in enumerate(self.attrCollection[niceName]):
                    pc.setAttr(trueAttr, uiElements.values[index])
        if self.displayIsChanging:
            pc.undoInfo(closeChunk=True)
        self.displayIsChanging = False

    def cleenLayout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if item != self.spaceItem:
                if not widget is None:
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    self.cleenLayout(layout = item)

    def cleenEventId(self, *args):
        pc.evalDeferred(self.removeScriptJobs)

    def removeScriptJobs(self):
        try:
            om.MMessage.removeCallback(self.mayaEventId)
            print("tkOscarParamEditor killed.")
        except:pass


def UIVisChanged(displayWindow, *args):
    #Defer the execution in case hiding is temporary (docking/undocking)
    pc.evalDeferred(partial(cleenIfIsHidden, displayWindow))

def cleenIfIsHidden(displayWindow):
    if not pc.control(DISPLAY_DOCK_WINDOW, q=True, visible=True):
        pc.evalDeferred(partial(cleenScriptJob, displayWindow))

def cleenScriptJob(displayWindow, *args):
    pc.evalDeferred(displayWindow.cleenEventId)
    pc.deleteUI(DISPLAY_MAYA_WINDOW)
    pc.deleteUI(DISPLAY_DOCK_LAYOUT)
    pc.deleteUI(DISPLAY_DOCK_WINDOW)
    
def showUI():
    if not pc.window(DISPLAY_MAYA_WINDOW, q=True, exists=True):
        mayaWindow = pc.window(DISPLAY_MAYA_WINDOW, title = "Oscar Param Editor Window")
        allwidgets = QtWidgets.QApplication.allWidgets()
        for widget in allwidgets:
            try:
                if widget.windowIconText() == "Oscar Param Editor Window":
                    QtWindow = widget
            except:pass
        displayWindow = OscarParamEditor(QtWindow)

    mainWindow = pc.mel.eval("$tmp = $gMainPane")
    if not pc.paneLayout(DISPLAY_DOCK_LAYOUT, q=True, exists=True):
        dockLayout = pc.paneLayout(DISPLAY_DOCK_LAYOUT, configuration='single', parent=mainWindow)
    if not pc.dockControl(DISPLAY_DOCK_WINDOW, q=True, exists=True):
        pc.dockControl(DISPLAY_DOCK_WINDOW, allowedArea='all', area='right', floating=False, content=dockLayout, label='Oscar Param Editor', vcc=partial(UIVisChanged,displayWindow))
        pc.control(mayaWindow, e=True, parent= dockLayout)
    if not pc.dockControl(DISPLAY_DOCK_WINDOW, q=True, visible=True):
        pc.dockControl(DISPLAY_DOCK_WINDOW,e=True, visible=True)

def toggleUI():
    if not pc.control(DISPLAY_MAYA_WINDOW, q=True, exists=True):
        showUI()
    else:
        pc.control(DISPLAY_DOCK_WINDOW,e=True, visible=False)

def getAttributesCollection(sel = None, attributes = {}):
    if not sel:
        sel = pc.selected()
    for x in sel:
        rigRoot = tkc.getParent(x, root=True) # Pymel object
        if not rigRoot is None:
            rigName = tkc.getRigName(rigRoot.stripNamespace()) # String
            properties = [x for x in tkc.getProperties(rigRoot) if "Parameters" in x.name()]
            for prop in properties:
                attributesName = tkc.getParameters(prop)
                for attr in attributesName:
                    attrNode = tkc.getNode(prop.name() +"." + attr)
                    if pc.getAttr(attrNode, k=True) and not pc.getAttr(attrNode, l=True) and len(attrNode.inputs()) == 0:
                        niceName = attr.replace(rigName + "_", "")
                        if pc.getAttr(prop.name() + "." + attr, type=True) in AVAILABLE_TYPE_ATTR:
                            if niceName in attributes.keys():
                                attributes[niceName].append(prop.name() + "." + attr)
                            elif not niceName in attributes.keys():
                                attributes[niceName] = [prop.name() + "." + attr]
    return attributes
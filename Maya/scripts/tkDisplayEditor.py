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



class Display_Editor(QtWidgets.QVBoxLayout):
    close = QtCore.Signal()
    
    def __init__(self, parent=None):
        super(Display_Editor, self).__init__(parent)
        
        self.size = tkqt.QSpinBoxGrp(self, label = "Size :")
        self.resetButton = QtWidgets.QPushButton("Reset Display")
        self.addWidget(self.resetButton)
        self.xOffset = tkqt.QSpinBoxGrp(self, label="X Offset :")
        self.yOffset = tkqt.QSpinBoxGrp(self, label="Y Offset :")
        self.zOffset = tkqt.QSpinBoxGrp(self, label="Z Offset :")
        self.xScale = tkqt.QSpinBoxGrp(self, label="X Scale :")
        self.yScale = tkqt.QSpinBoxGrp(self, label="Y Scale :")
        self.zScale = tkqt.QSpinBoxGrp(self, label="Z Scale :")
        spaceItem = QtWidgets.QSpacerItem(20, 5000, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.addItem(spaceItem)
        self.elements = {
                        "size":self.size,
                        "offsetDisplayX": self.xOffset, 
                        "offsetDisplayY": self.yOffset,
                        "offsetDisplayZ": self.zOffset,
                        "scaleDisplayX": self.xScale,
                        "scaleDisplayY": self.yScale, 
                        "scaleDisplayZ": self.zScale
                        }

        self.mayaEventId = om.MEventMessage.addEventCallback("SelectionChanged", self.updateDisplayValues)
        for value in self.elements.values():
            value.valueChanged.connect(partial(self.updateDisplays, value))
            value.editingFinished.connect(partial(self.updateDisplaysLast, value))

        self.displayIsChanging = False
        self.updateDisplayValues()
        self.resetButton.pressed.connect(self.resetDisplay)

    def updateDisplayValues(self, *args):
        selection = pc.selected(type="transform")
        
        for attr, ui in self.elements.items():
            newValues = []
            for obj in selection:
                if not tkc.getNode(obj.name()+ ".offsetDisplayX") is None:
                    newValues.append(pc.getAttr(obj + "." + attr))
            if len(newValues) == 0:
                ui.values = [0.0]
            else:
                ui.values = newValues
            ui.updateUI()

    def updateDisplays(self, inUiObj, values):
        selection = pc.selected(type="transform")
        for index, trObj in enumerate(selection):
            if not tkc.getNode(trObj.name()+".offsetDisplayX") is None:
                if not self.displayIsChanging:
                    pc.undoInfo(openChunk=True, chunkName="Update Displays")
                    self.displayIsChanging = True
                for attr, uiObj in self.elements.items():
                    if uiObj == inUiObj:
                        if ("scale" in attr or "size" in attr) and abs(values[index]) < 0.00001:
                            pc.setAttr(trObj.name() + "." + attr, 0.00001)
                        else:
                            pc.setAttr(trObj.name() + "." + attr, values[index])
            tkc.updateDisplay(trObj)

    def updateDisplaysLast(self, inUiObj, values):
        selection = pc.selected(type="transform")
        for index, trObj in enumerate(selection):
            if not tkc.getNode(trObj.name()+".offsetDisplayX") is None:
                for attr, uiObj in self.elements.items():
                    if uiObj == inUiObj:
                        if ("scale" in attr or "size" in attr) and abs(values[index]) < 0.00001:
                            pc.setAttr(trObj.name() + "." + attr, 0.00001)
                        else:
                            pc.setAttr(trObj.name() + "." + attr, values[index])

            tkc.updateDisplay(trObj)
        if self.displayIsChanging:
            pc.undoInfo(closeChunk=True)
        self.displayIsChanging = False

    def resetDisplay(self):
        pc.undoInfo(openChunk=True)
        for attr, ui in self.elements.items():
            if "scale" in attr or "size" in attr:
                ui.setValue(1)
            else:
                ui.setValue(0)
            self.displayIsChanging = True
            self.updateDisplays(ui, ui.values)
            self.displayIsChanging = False
        pc.undoInfo(closeChunk=True)

    def cleenEventId(self, *args):
        pc.evalDeferred(self.removeScriptJobs)

    def closeEvent(self, event):
        self.close.emit()

    def removeScriptJobs(self):
        try:
            om.MMessage.removeCallback(self.mayaEventId)
            print("tkDisplayEditor killed.")
        except:pass


    
def UIVisChanged(displayWindow, *args):
    #Defer the execution in case hiding is temporary (docking/undocking)
    pc.evalDeferred(partial(cleenIfIsHidden, displayWindow))

def cleenIfIsHidden(displayWindow):
    if not pc.control("DisplayEditorDoc", q=True, visible=True):
        pc.evalDeferred(partial(cleenScriptJob, displayWindow))

def cleenScriptJob(displayWindow, *args):
    pc.evalDeferred(displayWindow.cleenEventId)
    if pc.control("DisplayEditorDoc", q=True, exists=True):
        pc.deleteUI("DisplayEditorDoc")
    

def showUI():
    displayMayaWindow = "DisplayEditorWindow"
    displayDockLayout = "DisplayEditorLayout" 
    displayDockWindow = "DisplayEditorDoc"

    if not pc.window(displayMayaWindow, q=True, exists=True):
        mayaWindow = pc.window(displayMayaWindow, title = "Display Editor Window")
        allwidgets = QtWidgets.QApplication.allWidgets()
        for widget in allwidgets:
            try:
                if widget.windowIconText() == "Display Editor Window":
                    QtWindow = widget
            except:pass
        displayWindow = Display_Editor(QtWindow)

    mainWindow = pc.mel.eval("$tmp = $gMainPane")
    if not pc.paneLayout(displayDockLayout, q=True, exists=True):
        dockLayout = pc.paneLayout(displayDockLayout, configuration='single', parent=mainWindow)
    if not pc.dockControl(displayDockWindow, q=True, exists=True):
        pc.dockControl(displayDockWindow, allowedArea='all', area='right', floating=False, content=dockLayout, label='Display Editor', vcc=partial(UIVisChanged,displayWindow))
        pc.control(mayaWindow, e=True, parent= dockLayout)
    if not pc.dockControl(displayDockWindow, q=True, visible=True):
        pc.dockControl(displayDockWindow,e=True, visible=True)

def toggleUI():
    if not pc.control("DisplayEditorWindow", q=True, exists=True):
        showUI()
    else:
        pc.control("DisplayEditorDoc",e=True, visible=False)

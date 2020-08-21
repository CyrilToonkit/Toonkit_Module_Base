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
LOAD

Native

import anim_picker
#reload(anim_picker)
anim_picker.load(edit=True)

Pimped version

import tkAnimPicker
reload(tkAnimPicker)
tkAnimPicker.load(edit=True, debug=True)

Syno example:
$PROJECTPATH\Synoptic\Quadruped_Body.xml;$PROJECTPATH\Synoptic\Facial_Complete.xml
"""
import os
import pymel.core as pc

import tkMayaCore as tkc

import anim_picker
from anim_picker import node
from anim_picker import gui
from anim_picker import handlers

from tkHooks import tkAnimPickerHooks as hook

__author__ = "Cyril GIBAUD - Toonkit"

ROOTVAR = "$ROOT"
PROJECTPATHVAR = "$PROJECTPATH"

DEBUG=False

DEBUGPATH = "\\\\NHAMDS\\ToonKit\\ToonKit\\Rnd\\Picker\\Picker_Files"
PRODPATH = None

PICKERFILESCHUNK = os.path.join("scripts", "anim_picker","Picker_Files")

def mergePickers(inMainPicker, inPickerToAdd):
    for tab in inPickerToAdd["tabs"]:
        inMainPicker["tabs"].append(tab)

def resolveReferences(inPicker, inNs):
    needResolve=False
    for tab in inPicker["tabs"]:
        if not DEBUG and "background" in tab["data"]:
            if hook.conformPath(DEBUGPATH) in tab["data"]["background"]:
                tab["data"]["background"] = hook.resolvePath(tab["data"]["background"], PRODPATH, DEBUG, ROOTVAR, PROJECTPATHVAR, DEBUGPATH, inNs[:-1])
        newItems = []
        for item in tab["data"]["items"]:
            if "action_script" in item and "#REF:" in item["action_script"]:
                path = hook.resolvePath(item["action_script"][5:], PRODPATH, DEBUG, ROOTVAR, PROJECTPATHVAR, DEBUGPATH, inNs[:-1])
                if os.path.isfile(path):
                    nodeData = anim_picker.handlers.file_handlers.read_data_file(path)
                    resolveReferences(nodeData, inNs)

                    if len(nodeData["tabs"]) > 0 and len(nodeData["tabs"][0]["data"]["items"]) > 0:
                        needResolve=True
                        for subItem in nodeData["tabs"][0]["data"]["items"]:
                            subItem["position"][0] += item["position"][0]
                            subItem["position"][1] += item["position"][1]
                            newItems.append(subItem)
            else:
                if "controls" in item:
                    menus = []
                    for i in range(len(item["controls"])):
                        if "\n" in item["controls"][i]:
                            splitValues = [it for it in item["controls"][i].split("\n") if len(it) > 0]

                            if len(splitValues) > 1:
                                if splitValues[0].startswith("#"):
                                    space = splitValues[0][1:]
                                    if DEBUG:
                                        print "Space switcher detected ({0}, {1}) !".format(space, inNs)

                                    spaceNode, spaceAttr = space.split(".")
                                    if pc.objExists(inNs + spaceNode):
                                        if pc.attributeQuery(spaceAttr, node=inNs + spaceNode, exists=True):
                                            enums = pc.attributeQuery(spaceAttr, node=inNs + spaceNode, listEnum=True)[0].split(":")
                                            for j in range(len(enums)):
                                                menus.append([enums[j], "import tkRig\ntkRig.setSpace(__NAMESPACE__+\":"+space+"\", "+str(j)+")"])
                                        else:
                                            pc.warning("'" + inNs + spaceNode + "." + spaceAttr + "' does not exists !!")
                                    else:
                                        pc.warning("'" + inNs + spaceNode + "' does not exists !!")

                                    item["controls"][i] = splitValues[-1]
                                else:
                                    item["controls"][i] = splitValues[0]
                            else:
                                item["controls"][i] = splitValues[0]

                    if len(menus) > 0:
                        item['menus'] = menus

                newItems.append(item)

        if needResolve:
            tab["data"]["items"] = newItems

def load(edit=False, multi=False, path=None, debug=False, forceRebuild=False):
    '''Toonkit-friendly load method
    '''
    #Initialize
    global DEBUG
    global PRODPATH

    if debug:
        DEBUG=True

    PRODPATH=os.path.join(tkc.oscarmodulepath, PICKERFILESCHUNK)
    pickers = {}

    #Collect animPicker Maya Nodes
    pickerNodes = pc.ls('*.%s'%anim_picker.node.DataNode.__TAG__, o=True, r=True) or list()
    if forceRebuild:
        if len(pickerNodes) > 0:
            pc.delete(pickerNodes)
            pickerNodes = []
    else:
        for pickerNode in pickerNodes:
            #maya_node.picker_datas_file.set(path)
            pickers[pickerNode.namespace()] = pickerNode

    #Collect "SynopticPath" attributes
    synoAttrs = pc.ls(["*:*:*_OSCAR_Attributes.SynopticPath", "*:*_OSCAR_Attributes.SynopticPath", "*_OSCAR_Attributes.SynopticPath"]) or list()
    for synoAttr in synoAttrs:
        transformNode = synoAttr.node()
        if not transformNode.namespace() in pickers:
            pickers[transformNode.namespace()] = hook.resolvePath(synoAttr.get(), PRODPATH, DEBUG, ROOTVAR, PROJECTPATHVAR, DEBUGPATH, transformNode.namespace()[:-1]).replace(".xml", ".pkr")

    #Path brute force override
    if path != None:
        for pickerNode in pickerNodes:
            pickerNode.picker_datas_file.set(path)

    if DEBUG:
        print "Root Path", hook.resolvePath(ROOTVAR, PRODPATH, DEBUG, ROOTVAR, PROJECTPATHVAR, DEBUGPATH)
        print "Project Path", hook.resolvePath(PROJECTPATHVAR, PRODPATH, DEBUG, ROOTVAR, PROJECTPATHVAR, DEBUGPATH)

    for pickerNs, pickerPaths in pickers.iteritems():
        if isinstance(pickerPaths, basestring):
            #Need to create and build a picker from scratch
            mainPicker = None
            pickerFiles = pickerPaths.split(";")
            for pickerFile in pickerFiles:
                if os.path.isfile(pickerFile):
                    nodeData = anim_picker.handlers.file_handlers.read_data_file(pickerFile)
                    resolveReferences(nodeData, pickerNs)
                    if mainPicker != None:
                        mergePickers(mainPicker, nodeData)
                    else:
                        mainPicker = nodeData

                    #Add optional "_Lite" versions on the fly
                    litePath = pickerFile.replace(".pkr", "_Lite.pkr")
                    if os.path.isfile(litePath):
                        nodeData = anim_picker.handlers.file_handlers.read_data_file(litePath)
                        resolveReferences(nodeData, pickerNs)
                        mergePickers(mainPicker, nodeData)
                else:
                    pc.warning("Synoptic picker file " + pickerFile + " not found !")

            if mainPicker != None:
                data_node = anim_picker.node.DataNode(pickerNs + "tkAnimPicker")
                data_node.data = mainPicker
                data_node.create()
                data_node.write_data()

    ui = anim_picker.gui.load(edit=edit, multi=multi)

    return

def show(*args):
    rebuild=False

    if len(args) > 0:
        if isinstance(args[0], bool):
            rebuild = args[0]
        elif isinstance(args[0], basestring):
            #TODO Check : can't remember why a string argument matters... 
            pass

    mods = pc.getModifiers()

    #print "modifiers",mods
    #print "mods & 8",mods & 8

    load(mods & 8, forceRebuild=rebuild)

DUMPED_WINDOW = None
PICKER_WINDOW_NAME = "ctrl_picker_window"

def toggle():
    global DUMPED_WINDOW
    existsOne = True

    try:
        DUMPED_WINDOW = (
            pc.window(PICKER_WINDOW_NAME, query=True, topLeftCorner=True),
            pc.window(PICKER_WINDOW_NAME, query=True, width=True),
            pc.window(PICKER_WINDOW_NAME, query=True, height=True),
            )
    except:
        existsOne = False

    if existsOne:
        while existsOne:
            try:
                pc.deleteUI(PICKER_WINDOW_NAME, window=True)
            except:
                existsOne = False
    else:
        show(True)
        
        if not DUMPED_WINDOW is None:
            pc.window(PICKER_WINDOW_NAME, edit=True, topLeftCorner=DUMPED_WINDOW[0])
            pc.window(PICKER_WINDOW_NAME, edit=True, width=DUMPED_WINDOW[1])
            pc.window(PICKER_WINDOW_NAME, edit=True, height=DUMPED_WINDOW[2])
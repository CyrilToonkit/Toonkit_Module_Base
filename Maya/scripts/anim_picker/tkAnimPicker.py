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

import anim_picker.tkAnimPicker
reload(anim_picker.tkAnimPicker)
anim_picker.tkAnimPicker.load(edit=True, debug=True)

Syno example:
$PROJECTPATH\Synoptic\Quadruped_Body.xml;$PROJECTPATH\Synoptic\Facial_Complete.xml
"""
import os
import pymel.core as pc

import tkMayaCore as tkc

import gui
import node
from handlers import file_handlers

__author__ = "Cyril GIBAUD - Toonkit"

PROJECT = "wf"
DEBUG=False

DEBUGPATH = "\\\\NHAMDS\\ToonKit\\ToonKit\\Rnd\\Picker\\Picker_Files"
PRODPATH = None

PICKERFILESCHUNK = "scripts\\anim_picker\\Picker_Files"

def conformPath(inPath):
    return inPath.replace("\\", "/")

def resolvePath(inPath):
    #Initialize
    replacements = []

    ROOT = DEBUGPATH
    replacements.append((ROOTVAR, ROOT))

    PROJECTPATH = os.path.join(ROOT, PROJECT)
    replacements.append((PROJECTPATHVAR, PROJECTPATH))

    #Perform paths replacements
    for replacement in replacements:
        if replacement[0] in inPath:
            if DEBUG:
                print "Replace", replacement[0], "by", replacement[1],"(", inPath, "=>",inPath.replace(replacement[0], replacement[1]),")"

            inPath = inPath.replace(replacement[0], replacement[1])

    if not DEBUG:
        inPath = inPath.replace(DEBUGPATH, PRODPATH)
        inPath = inPath.replace(conformPath(DEBUGPATH), PRODPATH)

    return conformPath(inPath)

def mergePickers(inMainPicker, inPickerToAdd):
    for tab in inPickerToAdd["tabs"]:
        inMainPicker["tabs"].append(tab)

def resolveReferences(inPicker, inNs):
    needResolve=False
    for tab in inPicker["tabs"]:
        if not DEBUG and "background" in tab["data"]:
            if conformPath(DEBUGPATH) in tab["data"]["background"]:
                tab["data"]["background"] = resolvePath(tab["data"]["background"])
        newItems = []
        for item in tab["data"]["items"]:
            if "action_script" in item and "#REF:" in item["action_script"]:
                path = resolvePath(item["action_script"][5:])
                if os.path.isfile(path):
                    nodeData = file_handlers.read_data_file(path)
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
                            splitValues = item["controls"][i].split("\n")
                            space = splitValues[0][1:]
                            if DEBUG:
                                print "Space switcher detected ({0}, {1}) !".format(space, inNs)

                            spaceNode, spaceAttr = space.split(".")
                            if pc.objExists(inNs + spaceNode):
                                if pc.attributeQuery(spaceAttr, node=inNs + spaceNode, exists=True):
                                    enums = pc.attributeQuery(spaceAttr, node=inNs + spaceNode, listEnum=True)[0].split(":")
                                    for j in range(len(enums)):
                                        menus.append([enums[j], "import tkRig\ntkRig.setSpace(__NAMESPACE__+\":"+space+"\", "+str(j)+")"])

                            item["controls"][i] = splitValues[-1]

                    if len(menus) > 0:
                        item['menus'] = menus

                newItems.append(item)

        if needResolve:
            tab["data"]["items"] = newItems

def load(edit=False, multi=False, path=None, debug=False, project=None, forceRebuild=False):
    '''Toonkit-friendly load method
    '''
    #Initialize
    global DEBUG
    global PROJECT
    global PRODPATH

    if debug:
        DEBUG=True

    if project != None:
        PROJECT=project

    PRODPATH=os.path.join(tkc.oscarmodulepath, PICKERFILESCHUNK)
    pickers = {}

    #Collect animPicker Maya Nodes
    pickerNodes = pc.ls('*.%s'%node.DataNode.__TAG__, o=True, r=True) or list()
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
            pickers[transformNode.namespace()] = resolvePath(synoAttr.get()).replace(".xml", ".pkr")

    #Path brute force override
    if path != None:
        for pickerNode in pickerNodes:
            pickerNode.picker_datas_file.set(path)

    if DEBUG:
        print "Root Path", resolvePath("$ROOT")
        print "Project Path", resolvePath("$PROJECTPATH")

    for pickerNs, pickerPaths in pickers.iteritems():
        if isinstance(pickerPaths, basestring):
            #Need to create and build a picker from scratch
            mainPicker = None
            pickerFiles = pickerPaths.split(";")
            for pickerFile in pickerFiles:
                if os.path.isfile(pickerFile):
                    nodeData = file_handlers.read_data_file(pickerFile)
                    resolveReferences(nodeData, pickerNs)
                    if mainPicker != None:
                        mergePickers(mainPicker, nodeData)
                    else:
                        mainPicker = nodeData
                else:
                    pc.warning("Synoptic picker file " + pickerFile + " not found !")

            if mainPicker != None:
                data_node = node.DataNode(pickerNs + "tkAnimPicker")
                data_node.data = mainPicker
                data_node.create()
                data_node.write_data()

    ui = gui.load(edit=edit, multi=multi)

    return

def show(*args):
    rebuild=False

    proj = PROJECT
    if len(args) > 0:
        if isinstance(args[0], basestring):
            proj = args[0]
        elif isinstance(args[0], bool):
            rebuild = args[0]
        if len(args) > 1:
            if isinstance(args[1], bool):
                rebuild = args[1]

    mods = pc.getModifiers()

    load(mods & 8, project=proj, forceRebuild=rebuild)
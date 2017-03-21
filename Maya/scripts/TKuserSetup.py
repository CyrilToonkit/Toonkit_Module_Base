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
    Main loader for Toonkit's python modules and Menu
"""

import os

import pymel.core as pc

import locationModule
import tkMayaCore as tkc
import tkMenus

__author__ = "Cyril GIBAUD - Toonkit"

UINAME = "tkMenuToolsUI"

HOTKEYS =   [
                #SI Style
                {"name":"tkResetTRS_C"  , "key":"R" , "ctrl":True , "alt":False, "mel":False,
                    "desc":"Reset All Transforms",
                    "code":"import tkMayaCore as tkc;tkc.executeFromSelection('resetAll')"
                },
                {"name":"tkOutliner_C"  , "key":"_" , "ctrl":False , "alt":False, "mel":True,
                    "desc":"Show Outliner",
                    "code":"tearOffPanel \"Outliner\" \"outlinerPanel\" false"
                },
                {"name":"tkCompEd_C"  , "key":"e" , "ctrl":True , "alt":False, "mel":True,
                    "desc":"Show Component editor",
                    "code":"tearOffPanel \"Component Editor\" \"componentEditorPanel\" true"
                },
                {"name":"tkNodeEd_C"  , "key":"(" , "ctrl":False , "alt":False, "mel":True,
                    "desc":"Show Node editor",
                    "code":"nodeEditorWindow"
                },
                {"name":"tkToVerts_C"  , "key":"T" , "ctrl":True , "alt":False, "mel":True,
                    "desc":"Vertices selection",
                    "code":"changeSelectMode -object;changeSelectMode -component;setComponentPickMask \"Point\" true;setComponentPickMask \"Facet\" false;setComponentPickMask \"Line\" false;"
                },
                {"name":"tkToFaces_C"  , "key":"U" , "ctrl":True , "alt":False, "mel":True,
                    "desc":"Faces selection",
                    "code":"changeSelectMode -object;changeSelectMode -component;setComponentPickMask \"Point\" false;setComponentPickMask \"Facet\" true;setComponentPickMask \"Line\" false;"
                },
                {"name":"tkToEdges_C"  , "key":"Y" , "ctrl":True , "alt":False, "mel":True,
                    "desc":"Edges selection",
                    "code":"changeSelectMode -object;changeSelectMode -component;setComponentPickMask \"Point\" false;setComponentPickMask \"Facet\" false;setComponentPickMask \"Line\" true;"
                },

                #Tools
                {"name":"tkshowSIBAR_C"  , "key":"W" , "ctrl":True , "alt":False, "mel":False,
                    "desc":"Toggle SIBar",
                    "code":"import tkMayaSIBar as tksi;tksi.toggleUI()"
                },
                {"name":"tkshowSynopTiK_C"  , "key":"Q" , "ctrl":True , "alt":False, "mel":False,
                    "desc":"Show SynopTiK view",
                    "code":"import tkMayaCore as tkc;tkc.showSynopTiK()"
                },
                {"name":"tkshowAnimPicker_C"  , "key":"X" , "ctrl":True , "alt":False, "mel":False,
                    "desc":"Show AnimPicker",
                    "code":"import anim_picker.tkAnimPicker;anim_picker.tkAnimPicker.show()"
                },
                {"name":"tkshowSkinpaster_C"  , "key":"A" , "ctrl":True , "alt":False, "mel":True,
                    "desc":"Show qaSkinPaster",
                    "code":"qa_skinPasterUI"
                },
                {"name":"tkshowSkinner_C"  , "key":"E" , "ctrl":True , "alt":False, "mel":False,
                    "desc":"Show Principal Skinner",
                    "code":"import tkSkinner;tkSkinner.showUI()"
                }
            ]

#print "Initializing Toonkit's core library (%s)" % tkc.VERSIONINFO


VERSIONINFO = tkc.VERSIONINFO + " [Toonkit - Prod]"

NEEDEDPLUGINS = {"extractDeltas.py":False, "tkResPlaneNode.mll":False, "tkSoftIKNode.mll":False, "tkSpreadDeformNode.mll":False, "tkSpringNode.mll":False, "tkWheelNode.mll":False, "ngSkinTools.mll":False, "radialBlendShape.mll":False}

#Pre-load needed plug-ins first, as it's a pre-requisite
for k in NEEDEDPLUGINS:
    try:
        pc.loadPlugin( k, quiet=True )
        NEEDEDPLUGINS[k] = True
        #print "Toonkit plugin %s loaded" % k
    except:
        pass
        #print("Can't load Toonkit plugin %s, this could be by design..." % k)

def setHotKey(inName, inShortCut, inCtrlMod=False, inAltMod=False, code="print 'HelloWorld'", desc="", mel=False):
    #starting from maya 2016, we now have different "hotKey sets"
    if pc.versions.current() > 201600:
        if pc.hotkeySet("Toonkit_KeySet", exists=True):
            pc.hotkeySet("Toonkit_KeySet", edit=True, delete=True)
        pc.hotkeySet( "Toonkit_KeySet", current=True )

    #clear existing hotkey
    pc.hotkey(keyShortcut=inShortCut, ctrlModifier=inCtrlMod, altModifier=inAltMod, name='')
    #create named command for custom tool
    #For some reason you need to run the python tool command through a python command in mel
    pc.nameCommand(inName, ann=desc, c=code if mel else "python(\""+ code +"\");", default=False)
    #assign it a hotkey
    pc.hotkey( keyShortcut=inShortCut, ctrlModifier=inCtrlMod, altModifier=inAltMod, name=inName)

def setHotKeys():
    #Refer to HOTKEYS constant
    for hotKey in HOTKEYS:
        setHotKey(hotKey["name"], hotKey["key"], hotKey["ctrl"], hotKey["alt"], hotKey["code"], hotKey["desc"], hotKey["mel"])

    if pc.popupMenu("tkRMBAdd", query=True, exists=True):
        pc.deleteUI("tkRMBAdd")

    pc.popupMenu("tkRMBAdd", button=3 ,parent="viewPanes",mm=True)
    pc.menuItem("Select deformers", command="tkc.selectDeformers()")

def hotKeyMap(*args):
    global UINAME

    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("hotKeyMapWD", title='Toonkit Hotkeys')
        
    colLayout = pc.columnLayout()

    for hotKey in HOTKEYS:
        pc.rowLayout(numberOfColumns=2, parent=colLayout, columnWidth2=(120, 450), columnAlign=(1, 'left'), adjustableColumn=2)
        shortcut = hotKey["key"].lower()

        if hotKey["key"].isupper():
            shortcut = "Shift + " + shortcut
        if hotKey["alt"]:
            shortcut = "Alt + " + shortcut
        if hotKey["ctrl"]:
            shortcut = "Ctrl + " + shortcut

        pc.text(hotKey["name"] + "_shortcut_txt", label="' {0} '".format(shortcut))
        pc.text(hotKey["name"] + "_desc_txt", label=": {0}".format(hotKey["desc"]))

    pc.showWindow(UINAME)

def showHelp():
    pc.showHelp("https://docs.google.com/document/d/1q_aRS0SVRLwTaLVA8Zm6DHvS6vEcjPFptFu--1kXoe0/pub", absolute=True)

def menu():
    #Create Toonkit Menu
    if pc.menu("tkMainMenu", query=True, exists=True):
        pc.deleteUI("tkMainMenu", menu=True)

    gMainWindow = pc.mel.eval("string $parent = $gMainWindow")
    tkMainMenu = pc.menu("tkMainMenu", label="Toonkit", parent=gMainWindow, tearOff=True)

    pc.menuItem(label="Rebuild menu", parent=tkMainMenu, command="TKuserSetup.menu()")
    pc.menuItem(divider=True)

    oscarmodulepath = locationModule.OscarModuleLocation()
    mainMenuPath = os.path.join(oscarmodulepath, "tkMenu")
    tkMenus.generateMenu(tkMainMenu, mainMenuPath, False)

    #General/Version
    pc.menuItem(divider=True, parent=tkMainMenu)
    pc.menuItem(label="Install default hotkeys", parent=tkMainMenu, command="TKuserSetup.setHotKeys()")
    pc.menuItem(label="Hotkeys info", parent=tkMainMenu, command=hotKeyMap)
    pc.menuItem(divider=True, parent=tkMainMenu)
    pc.menuItem(label="Help (" + VERSIONINFO + ")", parent=tkMainMenu, command="TKuserSetup.showHelp()")

#print "Done Initializing Python Toonkit's core library (menu creation deferred)"
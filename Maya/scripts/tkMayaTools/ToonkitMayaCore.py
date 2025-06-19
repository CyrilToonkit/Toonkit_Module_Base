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
import os

import pymel.core as pc

import locationModule
import Toonkit_Core.tkCore as tc
from Toonkit_Core import tkLogger
from Toonkit_Core.tkToolOptions.tkOptions import Options
from tkMayaTools.tkMayaTool import MayaTool as Tool

import tkMayaCore as tkc
import tkMenus

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.5.97.1"

MENU_NAME = "tkMainMenu"

COMMAND_FORMAT = "tk{0}_C"
TK_PROJECT_NAME = "TK_PROJECT_NAME"

HOTKEYS =   {
                #SI Style
                "ResetAllTransforms":
                    {"key":"R" , "ctrl":True , "alt":False, "mel":False,
                        "desc":"Reset All Transforms",
                        "code":"import tkMayaCore as tkc;tkc.executeFromSelection('resetAll')"
                    },
                "Outliner":
                    {"key":"_" , "ctrl":False , "alt":False, "mel":True,
                        "desc":"Show Outliner",
                        "code":"OutlinerWindow"
                    },
                "ComponentEditor":
                    {"key":"e" , "ctrl":True , "alt":False, "mel":True,
                        "desc":"Show Component editor",
                        "code":"tearOffPanel \"Component Editor\" \"componentEditorPanel\" true"
                    },
                "NodeEditor":
                    {"key":"(" , "ctrl":False , "alt":False, "mel":True,
                        "desc":"Show Node editor",
                        "code":"nodeEditorWindow"
                    },
                "ToVertices":
                    {"key":"T" , "ctrl":True , "alt":False, "mel":True,
                        "desc":"Vertices selection",
                        "code":"changeSelectMode -object;changeSelectMode -component;setComponentPickMask \"Point\" true;setComponentPickMask \"Facet\" false;setComponentPickMask \"Line\" false;"
                    },
                "ToFaces":
                    {"key":"U" , "ctrl":True , "alt":False, "mel":True,
                        "desc":"Faces selection",
                        "code":"changeSelectMode -object;changeSelectMode -component;setComponentPickMask \"Point\" false;setComponentPickMask \"Facet\" true;setComponentPickMask \"Line\" false;"
                    },
                "ToEdges":
                    {"key":"Y" , "ctrl":True , "alt":False, "mel":True,
                        "desc":"Edges selection",
                        "code":"changeSelectMode -object;changeSelectMode -component;setComponentPickMask \"Point\" false;setComponentPickMask \"Facet\" false;setComponentPickMask \"Line\" true;"
                    },

                #Tools
                "showSIBAR":
                    {"key":"W" , "ctrl":True , "alt":False, "mel":False,
                        "desc":"Toggle SIBar",
                        "code":"import tkMayaSIBar as tksi;tksi.toggleUI()"
                    },
                "showSynopTiK":
                    {"key":"C" , "ctrl":True , "alt":False, "mel":False,
                        "desc":"Show SynopTiK view",
                        "code":"import tkMayaCore as tkc;tkc.showSynopTiK()"
                    },
                "showAnimPicker":
                    {"key":"X" , "ctrl":True , "alt":False, "mel":False,
                        "desc":"Show AnimPicker",
                        "code":"import tkAnimPicker;tkAnimPicker.show()"
                    },
                "toggleAnimPicker":
                    {"key":"Q" , "ctrl":True , "alt":False, "mel":False,
                        "desc":"Toggle AnimPicker",
                        "code":"import tkAnimPicker;tkAnimPicker.toggle()"
                    },
                "showSkinpaster":
                    {"key":"A" , "ctrl":True , "alt":False, "mel":True,
                        "desc":"Show qaSkinPaster",
                        "code":"qa_skinPasterUI"
                    },
                "showSkinner":
                    {"key":"E" , "ctrl":True , "alt":False, "mel":False,
                        "desc":"Show Principal Skinner",
                        "code":"import tkSkinner;tkSkinner.showUI()"
                    },
                "selectConstraining":
                    {"key":">" , "ctrl":True , "alt":False, "mel":False,
                        "desc":"Select objects constraing selection",
                        "code":"import pymel.core as pc;import tkMayaCore as tkc;tkc.selectConstraining(pc.selected()[0]) if len(pc.selected()) > 0 else False"
                    },
                "selectConstrained":
                    {"key":"<" , "ctrl":True , "alt":False, "mel":False,
                        "desc":"Select objects constrained to selection",
                        "code":"import pymel.core as pc;import tkMayaCore as tkc;tkc.selectConstrained(pc.selected()[0]) if len(pc.selected()) > 0 else False"
                    },
                "searchInTkMenu":
                    {"key":"f" , "ctrl":True , "alt":False, "mel":False,
                        "desc":"Show toonkit menu search tool",
                        "code":"tkc.showSearch()"
                    },
                "showDisplayEditor":
                    {"key": "V", "ctrl":True, "alt":False,"mel":False,
                        "desc":"Show Display Editor",
                        "code": "import tkDisplayEditor;tkDisplayEditor.toggleUI()"
                    },
                "showOscarParamEditor":
                    {"key": "B", "ctrl":True, "alt":False,"mel":False,
                        "desc":"Show Oscar Param Editor",
                        "code": "import tkOscarParamEditor;tkOscarParamEditor.toggleUI()"
                    }
            }

class ToonkitMayaCore(Tool):
    def __init__(self, inContext=None, inDebug=False):
        tkLogger.info("Toonkit Maya Core {0} initializing...".format(VERSIONINFO))

        super(ToonkitMayaCore, self).__init__(inName="ToonkitMayaCore", inDescription="Toonkit's Maya base library",
            inUsage="", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.boundPort = -1

        self.options = Options()

        # OPTIONS : inName, inValue, inDescription=DEFAULT_DESC, inNiceName=None, inOptional=False, inCategory=None
        #Configuration
        self.options.addOption("project", "demo", None, "Project name", False, "Configuration")
        self.options.addOption("alternateProjectsPath", "", "Commat separated list of alternate project paths", "Alternate Projects Path", False, "Configuration")
        self.options.addOption("mayaroot", os.path.join("C:\\", "Program Files", "Autodesk", "Maya2013", "bin"), "Maya installation root directory", "Maya root", False, "Configuration")
        self.options.addOption("mayapath", os.path.join("C:\\", "Program Files", "Autodesk", "Maya2013", "bin", "maya.exe"), "Maya executable path", "Maya path", False, "Configuration")
        self.options.addOption("mayabatchpath", os.path.join("C:\\", "Program Files", "Autodesk", "Maya2013", "bin", "mayabatch.exe"), "Maya batch path", "Maya batch path", False, "Configuration")
        self.options.addOption("hidemenu", False, "Hide Toonkit menu", "Hide menu", False, "Configuration")
        self.options.addOption("hookmayabatch", True, "Intercep a mayabatch call to execute a python script given as argument", "Hook mayabatch", False, "Configuration")
        self.options.addOption("logLevel", 2, "Set the logging value","Log Level :", False, "Logs.Level", inValues=["VERBOSE", "DEBUG", "INFO", "WARNING", "ERROR"])
        self.options.addOption("logFile", False, None, " ", False, "Logs.File")
        self.options.addOption("logPath", "ToonKit", None, "Log to File :", False, "Logs.File")

        self.options.addOption("hookDagMenuProc", True, "Override Maya 'dagMenuProc'", "Override Maya 'dagMenuProc'", False, "Configuration")

        #Hotkeys
        self.options.addOption("ResetAllTransformsKey", "R", None, "Key", False, "HotKeys.ResetAllTransforms")
        self.options.addOption("ResetAllTransformsCtrl", True, None, "Ctrl", False, "HotKeys.ResetAllTransforms")
        self.options.addOption("ResetAllTransformsAlt", False, None, "Alt", False, "HotKeys.ResetAllTransforms")

        self.options.addOption("OutlinerKey", "_", None, "Key", False, "HotKeys.Outliner")
        self.options.addOption("OutlinerCtrl", False, None, "Ctrl", False, "HotKeys.Outliner")
        self.options.addOption("OutlinerAlt", False, None, "Alt", False, "HotKeys.Outliner")

        self.options.addOption("ComponentEditorKey", "e", None, "Key", False, "HotKeys.ComponentEditor")
        self.options.addOption("ComponentEditorCtrl", True, None, "Ctrl", False, "HotKeys.ComponentEditor")
        self.options.addOption("ComponentEditorAlt", False, None, "Alt", False, "HotKeys.ComponentEditor")

        self.options.addOption("NodeEditorKey", "(", None, "Key", False, "HotKeys.NodeEditor")
        self.options.addOption("NodeEditorCtrl", False, None, "Ctrl", False, "HotKeys.NodeEditor")
        self.options.addOption("NodeEditorAlt", False, None, "Alt", False, "HotKeys.NodeEditor")

        self.options.addOption("ToVerticesKey", "T", None, "Key", False, "HotKeys.ToVertices")
        self.options.addOption("ToVerticesCtrl", True, None, "Ctrl", False, "HotKeys.ToVertices")
        self.options.addOption("ToVerticesAlt", False, None, "Alt", False, "HotKeys.ToVertices")

        self.options.addOption("ToFacesKey", "U", None, "Key", False, "HotKeys.ToFaces")
        self.options.addOption("ToFacesCtrl", True, None, "Ctrl", False, "HotKeys.ToFaces")
        self.options.addOption("ToFacesAlt", False, None, "Alt", False, "HotKeys.ToFaces")

        self.options.addOption("ToEdgesKey", "Y", None, "Key", False, "HotKeys.ToEdges")
        self.options.addOption("ToEdgesCtrl", True, None, "Ctrl", False, "HotKeys.ToEdges")
        self.options.addOption("ToEdgesAlt", False, None, "Alt", False, "HotKeys.ToEdges")

        self.options.addOption("showSIBARKey", "W", None, "Key", False, "HotKeys.showSIBAR")
        self.options.addOption("showSIBARCtrl", True, None, "Ctrl", False, "HotKeys.showSIBAR")
        self.options.addOption("showSIBARAlt", False, None, "Alt", False, "HotKeys.showSIBAR")

        self.options.addOption("showSynopTiKKey", "C", None, "Key", False, "HotKeys.showSynopTiK")
        self.options.addOption("showSynopTiKCtrl", True, None, "Ctrl", False, "HotKeys.showSynopTiK")
        self.options.addOption("showSynopTiKAlt", False, None, "Alt", False, "HotKeys.showSynopTiK")

        self.options.addOption("showAnimPickerKey", "X", None, "Key", False, "HotKeys.showAnimPicker")
        self.options.addOption("showAnimPickerCtrl", True, None, "Ctrl", False, "HotKeys.showAnimPicker")
        self.options.addOption("showAnimPickerAlt", False, None, "Alt", False, "HotKeys.showAnimPicker")

        self.options.addOption("toggleAnimPickerKey", "Q", None, "Key", False, "HotKeys.toggleAnimPicker")
        self.options.addOption("toggleAnimPickerCtrl", True, None, "Ctrl", False, "HotKeys.toggleAnimPicker")
        self.options.addOption("toggleAnimPickerAlt", False, None, "Alt", False, "HotKeys.toggleAnimPicker")

        self.options.addOption("showSkinpasterKey", "A", None, "Key", False, "HotKeys.showSkinpaster")
        self.options.addOption("showSkinpasterCtrl", True, None, "Ctrl", False, "HotKeys.showSkinpaster")
        self.options.addOption("showSkinpasterAlt", False, None, "Alt", False, "HotKeys.showSkinpaster")

        self.options.addOption("showSkinnerKey", "E", None, "Key", False, "HotKeys.showSkinner")
        self.options.addOption("showSkinnerCtrl", True, None, "Ctrl", False, "HotKeys.showSkinner")
        self.options.addOption("showSkinnerAlt", False, None, "Alt", False, "HotKeys.showSkinner")

        self.options.addOption("selectConstrainingKey", ">", None, "Key", False, "HotKeys.selectConstraining")
        self.options.addOption("selectConstrainingCtrl", True, None, "Ctrl", False, "HotKeys.selectConstraining")
        self.options.addOption("selectConstrainingAlt", False, None, "Alt", False, "HotKeys.selectConstraining")

        self.options.addOption("selectConstrainedKey", "<", None, "Key", False, "HotKeys.selectConstrained")
        self.options.addOption("selectConstrainedCtrl", True, None, "Ctrl", False, "HotKeys.selectConstrained")
        self.options.addOption("selectConstrainedAlt", False, None, "Alt", False, "HotKeys.selectConstrained")

        self.options.addOption("searchInTkMenuKey", "f", None, "Key", False, "HotKeys.searchInTkMenu")
        self.options.addOption("searchInTkMenuCtrl", True, None, "Ctrl", False, "HotKeys.searchInTkMenu")
        self.options.addOption("searchInTkMenuAlt", False, None, "Alt", False, "HotKeys.searchInTkMenu")

        self.options.addOption("showDisplayEditorKey", "V", None, "Key", False, "HotKeys.showDisplayEditor")
        self.options.addOption("showDisplayEditorCtrl", True, None, "Ctrl", False, "HotKeys.showDisplayEditor")
        self.options.addOption("showDisplayEditorAlt", False, None, "Alt", False, "HotKeys.showDisplayEditor")

        self.options.addOption("showOscarParamEditorKey", "B", None, "Key", False, "HotKeys.showOscarParamEditor")
        self.options.addOption("showOscarParamEditorCtrl", True, None, "Key", False, "HotKeys.showOscarParamEditor")
        self.options.addOption("showOscarParamEditorAlt", False, None, "Key", False, "HotKeys.showOscarParamEditor")


        savedOption = Options(inPath=self.getOptionsPath())
        for key, value in savedOption.items():
            if key in self.options.keys():
                tkLogger.debug("The option '" +key+ "' already exists, his value is set to " + str(value))
                self.options[key] = value
            elif not key in self.options.keys():
                tkLogger.warning("The options'" + key + "' is not in base options !" )
        del savedOption
        self.options.path = self.getOptionsPath()
        
        self.options.addSavedCallback(self.saved)
        if not self.options.isSaved():
            self.saveOptions()

        projectVEnv(self)
        self.options.addChangedCallback(self.optionChanged)
        setLoggingLevel(self)
        setLoggingOptions(self)


    def getOptionsPath(self):
        return os.path.abspath(os.path.join(locationModule.get(), os.pardir, os.pardir, "Preferences", "{0}.json".format(type(self).__name__)))

    def getToolsRepos(self):
        return ["Toonkit_Core.tkToolOptions", "tkMayaTools"]

    def saved(self):
        tc.getTool().options.save()

    def optionChanged(self, *args, **kwargs):
        self.logDebug("{0} changed ({1} => {2})".format(kwargs["option"].name, kwargs["old"], kwargs["new"]))

        if kwargs["option"].name == "logFile":
            setLoggingOptions(self)

        if kwargs["option"].name == "logLevel":
            setLoggingLevel(self)

        elif kwargs["option"].name == "project":
            # Try to create a projet with this new project Name
            project = tc.setProject(dccName = "maya", inName=kwargs["new"]) # setProjec can faild and return None if it was never init.
            if project:
                tkLogger.debug("Requested project: {0}. Created project : {1}.".format(kwargs["new"], project.name))
                tkLogger.debug("Do tkCore project are the same as tkMayaTool project : "+ str(project.name == kwargs["new"]))
                if project.name != kwargs["new"]:
                    self.options["project"] = project.name
                    pc.evalDeferred(self.showPrefs)
                else:
                    # Set tkCoreTool to preserve sync with tkMayaCoreTool
                    tc.getTool().options["project"] = kwargs["new"]
            else:
                pc.evalDeferred(self.showPrefs)

        elif kwargs["option"].name == "alternateProjectsPath":
            tc.getTool().options["alternateProjectsPath"] = kwargs["new"]

        elif kwargs["option"].name == "hidemenu":
            if kwargs["new"]:
                self.hideMenu()
            else:
                self.showMenu()

        elif kwargs["option"].name == "hookDagMenuProc":
            if kwargs["new"]:
                print ("Si on passe l'override a True")
            else:
                print ("Si on passe l'override a False")

        elif "HotKeys." in kwargs["option"].category:
            self.setHotKeys()

    def reload(self, *args):
        """
        try:
            #Force interpreter reset
            eval("reload(tkc)")
        except:
            pass
        """

        #Pre-load needed plug-ins first, as it's a pre-requisite
        NEEDEDPLUGINS = {   "extractDeltas.py":False, "tkResPlaneNode.mll":False, "tkSoftIKNode.mll":False,
                            "tkSpreadDeformNode.mll":False, "tkSpringNode.mll":False, "tkWheelNode.mll":False,
                            "ngSkinTools.mll":False, "radialBlendShape.mll":False, "fStretch.mll":False,
                            "tkMathNodes.mll":False, "tkProjectNode.mll":False,
                            "setPointPosition.py":False, "setSkinWeight":False}

        for k in NEEDEDPLUGINS:
            try:
                pc.loadPlugin( k, quiet=True )
                NEEDEDPLUGINS[k] = True
                #print "Toonkit plugin %s loaded" % k
            except:
                pass
                #print("Can't load Toonkit plugin %s, this could be by design..." % k)

        if not self.options["hidemenu"]:
            pc.evalDeferred(self.showMenu)

    def showMenu(self, *args):
        if pc.menu(MENU_NAME, query=True, exists=True):
            pc.deleteUI(MENU_NAME, menu=True)

        gMainWindow = pc.mel.eval("string $parent = $gMainWindow")
        tkMainMenu = pc.menu(MENU_NAME, label="Toonkit", parent=gMainWindow, tearOff=True)

        pc.menuItem(label="Rebuild menu", parent=tkMainMenu, command=self.reload)
        pc.menuItem(label="Search...", parent=tkMainMenu, command=tkc.showSearch)
        pc.menuItem(divider=True)

        oscarmodulepath = locationModule.OscarModuleLocation()
        mainMenuPath = os.path.join(oscarmodulepath, "tkMenu")

        tkMenus.generateMenu(tkMainMenu, mainMenuPath, False, tkc.HELP_LIST)

        #General/Version
        pc.menuItem(divider=True, parent=tkMainMenu)
        pc.menuItem(label="Toolkit options...", parent=tkMainMenu, command=self.showPrefs)
        pc.menuItem(label="Load Context Menu", parent=tkMainMenu,ann="Open a RMB menu once before.", command="pc.mel.eval(\"source \\\"" +  os.path.join(oscarmodulepath, "dagMenuProc.mel").replace("\\", "/") + "\\\"\")")
        pc.menuItem(label="Install default hotkeys", parent=tkMainMenu, command=self.setHotKeys)

        helpText = "Toolkit help (v" + self.version + ")"
        if self.boundPort != -1:
            helpText += " ({0})".format(self.boundPort)

        pc.menuItem(label=helpText, parent=tkMainMenu, command=showHelp)
        

    def hideMenu(self):
        if pc.menu(MENU_NAME, query=True, exists=True):
            pc.deleteUI(MENU_NAME, menu=True)

    def setHotKeys(self, *args):
        #starting from maya 2016, we now have different "hotKey sets"
        if pc.versions.current() >= 201600:
            if pc.hotkeySet("Toonkit_KeySet", exists=True):
                pc.hotkeySet("Toonkit_KeySet", edit=True, delete=True)
            pc.hotkeySet( "Toonkit_KeySet", current=True )

        #Refer to options and HOTKEYS constant
        categorizedOptions = self.getCategorizedOptions()

        for categ, options in categorizedOptions.items():
            if categ and categ.startswith("HotKeys."):
                hotkeyName = categ.split(".")[-1]
                if hotkeyName in HOTKEYS:
                    hotKey=HOTKEYS[hotkeyName]
                    setHotKey(COMMAND_FORMAT.format(hotkeyName),
                        self.options[hotkeyName+"Key"],
                        self.options[hotkeyName+"Ctrl"],
                        self.options[hotkeyName+"Alt"],
                        hotKey["code"], hotKey["desc"], hotKey["mel"])
                else:
                    pc.warning("Wrong hotkey definition {0}".format(hotkeyName))

#TOP LEVEL METHODS AND CONSTANTS FROM TKUserSetup
def showHelp(*args):
    pc.showHelp("https://docs.google.com/document/d/1q_aRS0SVRLwTaLVA8Zm6DHvS6vEcjPFptFu--1kXoe0/pub", absolute=True)

def setHotKey(inName, inShortCut, inCtrlMod=False, inAltMod=False, code="print 'HelloWorld'", desc="", mel=False):
    #print "setHotKey", inName, inShortCut, inCtrlMod, inAltMod, code, desc, mel

    #clear existing hotkey
    pc.hotkey(keyShortcut=inShortCut, ctrlModifier=inCtrlMod, altModifier=inAltMod, name='')
    #create named command for custom tool
    #For some reason you need to run the python tool command through a python command in mel
    pc.nameCommand(inName, ann=desc, c=code if mel else "python(\""+ code +"\");", default=False)
    #assign it a hotkey
    pc.hotkey( keyShortcut=inShortCut, ctrlModifier=inCtrlMod, altModifier=inAltMod, name=inName)

def projectVEnv(inTool):
    project = os.environ.get(TK_PROJECT_NAME)
    if project is None:
        return

    pickerPath = os.path.join(locationModule.get(), "anim_picker", "Picker_Files", project)

    if os.path.isdir(pickerPath):
        inTool.options["project"] = project
    else:
        pc.warning("Can't find a project named '{0}', loading '{1}' instead".format(project, inTool.options["project"]))


def setLoggingLevel(tool):
    if not tool.options["logLevel"] is None:
        level = tool.options["logLevel"]
        if level == 0:
            level = -1
        tkLogger.setLevel(level * 10)

def setLoggingOptions(tool):
    if tool.options["logFile"] == True:
        formatDict = {"path":"\\".join(locationModule.get().split("\\")[:-2]) + "\\Logs\\",
                        "pid":str(os.getpid()),
                        "name":tool.options["logPath"]}
        path = "{path}\\{pid}_{name}.log".format(**formatDict)
        tkLogger.setLogsFiles(path)
        tkLogger.debug("TkLog is now bound to file :%s" %path)
    elif tool.options["logFile"] is False:
        tkLogger.removeHandlers()
        tkLogger.debug("TkLog is now unbound to file")
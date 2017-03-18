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

import subprocess
import os
import os.path
import re
import xml.dom.minidom as minidom

import pymel.core as pc
import pymel.core.system as pmsys

import zvRadialBlendShape
import tkMayaSIBar as tksi
import tkMayaCore as tkc
import tkSIGroups
import tkSpring
import tkRig
import tkDevHelpers
import tkBatcher
import tkParseMA
import tkPoseScaler
import tkOutfits
import tkPalette
import locationModule
import mayaexecpythonfile
import tkBlendShapes
import tkSym
import tkSkinner
import tkWeightsFilters
import anim_picker.tkAnimPicker
import tkTagTool
import tkConfo
import tkMenus

skinToolsAvailable = True

try:
    from ngSkinTools.ui.mainwindow import MainWindow
except:
    print "Can't load skinning Toolkit, this could be by design..."
    skinToolsAvailable = False

__author__ = "Cyril GIBAUD - Toonkit"

UINAME = "tkMenuToolsUI"

UITAG = None

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

print "Initializing Toonkit's core library (%s)" % tkc.VERSIONINFO

oscarmodulepath = locationModule.OscarModuleLocation()
#we arrived in "Scripts" folder, go up one step
oscarmodulepath = os.path.join(os.path.split(oscarmodulepath)[:-1])[0]

#Oscar may not be available
oscarAvailable = True
#SynoptiK may not be available
synoptikAvailable = True
#MimeTiK may not be available
mimetikAvailable = True
#SpringManager may not be available
springManagerAvailable = True
#PosesMaker may not be available
posesMakerAvailable = True
#CompareGeo may not be available
compareGeoAvailable = True

OSCARPATH = oscarmodulepath + "\\Standalones\\OSCAR\\OscarEditor.exe"
SYNOPTIKPATH = tkc.SYNOPTIKPATH
MIMETIKPATH = tkc.MIMETIKPATH
SPRINGMANAGERPATH = oscarmodulepath + "\\Standalones\\SpringManager\\SpringManager.exe"
POSESMAKERPATH = oscarmodulepath + "\\Standalones\\PosesMaker\\PosesMaker.exe"
COMPAREGEOPATH = oscarmodulepath + "\\Standalones\\CompareGeo\\CompareGeo.exe"

VERSIONINFO = tkc.VERSIONINFO + " [Toonkit - Prod]"

NEEDEDPLUGINS = {"extractDeltas.py":False, "tkResPlaneNode.mll":False, "tkSoftIKNode.mll":False, "tkSpreadDeformNode.mll":False, "tkSpringNode.mll":False, "tkWheelNode.mll":False, "ngSkinTools.mll":False, "radialBlendShape.mll":False}

#Pre-load needed plug-ins first, as it's a pre-requisite
for k in NEEDEDPLUGINS:
    try:
        pc.loadPlugin( k, quiet=True )
        NEEDEDPLUGINS[k] = True
        print "Toonkit plugin %s loaded" % k
    except:
        print("Can't load Toonkit plugin %s, this could be by design..." % k)

if oscarAvailable:
    oscarAvailable = os.path.isfile(OSCARPATH)

if synoptikAvailable:
    synoptikAvailable = os.path.isfile(SYNOPTIKPATH)

if mimetikAvailable:
    mimetikAvailable = os.path.isfile(MIMETIKPATH)

if posesMakerAvailable:
    posesMakerAvailable = os.path.isfile(POSESMAKERPATH)

if compareGeoAvailable:
    compareGeoAvailable = os.path.isfile(COMPAREGEOPATH)

PROJECT_DEFINITION_PATH = oscarmodulepath + "\\Standalones\\OSCAR\\Data\\Projects\\Projects.xml"

#Todo : implement this at Oscar project level
SERVER_PATH_SUBST = ("Z:\\Toonkit\\","\\\\NHAMDS\\Toonkit\\ToonKit\\")

def showNgSkinTools(*args):
    MainWindow.open()

def smoothSkin(*args):
    tkWeightsFilters.smooth()

def sharpenSkin(*args):
    tkWeightsFilters.sharpen()

def hardenSkin(*args):
    tkWeightsFilters.harden()

def qaSkinPaster(*args):
    pc.mel.eval("qa_skinPasterUI")

def abSymMesh(*args):
    pc.mel.eval("abSymMesh")

def showZvRadialBS(*args):
    zvRadialBlendShape.zvRadialBlendShape()

def oscarOnClick(launchOscar=True, mock=False, hook=False):
    if launchOscar:
        commandLine = OSCARPATH

        if mock:
            commandLine += " mock"
        if hook:
            commandLine += " hook"

        subprocess.Popen(commandLine)

def synoptikOnClick():
    tkc.showSynopTiK()

def mimetikOnClick():
    subprocess.Popen(MIMETIKPATH)

def springManagerOnClick():
    subprocess.Popen(SPRINGMANAGERPATH)

def posesMakerOnClick():
    subprocess.Popen(POSESMAKERPATH)

def compareGeoOnClick():
    subprocess.Popen(COMPAREGEOPATH)

def getValuesFromOtherScene(*inArgs):
    sel = pc.ls(sl=True)

    if len(sel) == 0:
        pc.error("Please select some objects")

    maFile = pc.fileDialog2(caption="Select the .ma reference file", fileFilter="Maya ascii (*.ma)(*.ma)", dialogStyle=2, fileMode=1)
    if maFile == None:
        print "getValuesFromOtherScene aborted"
        return

    tkParseMA.setValuesFromOtherScene( pc.ls(sl=True), maFile)

def extractDeltas():
    sel = pc.ls(sl=True)
    result = None
    if len(sel) == 2:
        if tkc.getSkinCluster(sel[0]) != None:
            result = pc.extractDeltas(s=sel[0].name(), c=sel[1].name())
        else:
            pc.error("Extract deltas : WRONG INPUTS !\nFirst selected mesh must have a skinCluster.")
    else:
        pc.error("Extract deltas : WRONG INPUTS !\nPlease select skinned mesh first, then undeformed ('freezed') corrective mesh.")

    if result != None:
        print "Corrective blendshape created : " + result
    else:
        pc.error("Extract deltas : UNKNOWN ERROR !\nSomething unexpected went wrong...")

def applySpreadDeforms():
    sel = pc.ls(sl=True)
    result = None
    if len(sel) >= 3:
        curves = sel[:len(sel) - 2]
        refCurve = sel[-2]
        refParent = sel[-1]

        #Verify inputs
        for crv in curves:
            shp = crv.getShape()
            if shp == None or shp.type() != "nurbsCurve":
                pc.error("Spread Deform : WRONG INPUTS !\nDeformed objects must be nurbsCurves.")

        shp = refCurve.getShape()
        if shp == None or shp.type() != "nurbsCurve":
            pc.error("Spread Deform : WRONG INPUTS !\nReference object must be a nurbsCurve.")

        if tkc.getSkinCluster(refCurve) == None:
            pc.error("Spread Deform : WRONG INPUTS !\nReference curve must be skinned (before last selected object).")

        if refParent.type() != "transform":
            pc.error("Spread Deform : WRONG INPUTS !\nReference parent must be a transform node.")

        tkc.applySpreadDeforms(curves, refCurve, refParent)
    else:
        pc.error("Spread Deform : WRONG INPUTS !\nPlease select any number of curves to be deformed, then the reference curve with skinCluster and reference parent for skinned curve.")

def rigInclude():
    ref = ""
    sel = pc.ls(sl=True, transforms=True)
    if len(sel) > 0:
        ref = sel[0].name()
    fileRslt = pc.fileDialog2(caption="Select a rig to include", fileFilter="Maya ascii (*.ma)(*.ma)", dialogStyle=2, fileMode=1)
    if fileRslt != None:
        fileRslt = fileRslt[0]
        oldName = os.path.split(fileRslt)[-1].split(".")[0]
        result = pc.promptDialog(
                title="Include Rig",
                message="Rig included in '%s'" % ("Scene root" if ref=="" else ref) + "\nRig Name:",
                text=tkc.getUniqueName(oldName),
                button=['OK', 'Cancel'],
                defaultButton='OK',
                cancelButton='Cancel',
                dismissString='Cancel')
        if result == 'OK':
            newName = pc.promptDialog(query=True, text=True)
            tkRig.importRig(fileRslt, newName, ref)

def rigFbx():
    rslt = pc.confirmDialog( title='Fbx setup', message="Creating a fbx will modify your scene (make sure it's properly saved), proceed ?", button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
    if rslt == "Yes":
        fileRslt = pc.fileDialog2(caption="Save your fbx export", fileFilter="Fbx (*.fbx)(*.fbx)", dialogStyle=2)
        if fileRslt != None:
            fileRslt = fileRslt[0]
            tkRig.plotRigAndExport(fileRslt);

def transferShading():
    refFileRslt = pc.fileDialog2(caption="Select the ref model (texture ?)", fileFilter="Maya ascii (*.ma)(*.ma)", dialogStyle=2, fileMode=1)
    if refFileRslt == None:
        print "transferShading aborted"
        return
        
    targetFileRslt = pc.fileDialog2(caption="Select the target model (uvs ?)", fileFilter="Maya ascii (*.ma)(*.ma)", dialogStyle=2, fileMode=1)
    if targetFileRslt == None:
        print "transferShading aborted"
        return
        
    tkRig.updateShading(refFileRslt[0], targetFileRslt[0])

def transferShadingInPlace():
    tkRig.updateShadingInPlace(refFileRslt[0], targetFileRslt[0])

def replaceDeformers():
    sel = pc.ls(sl=True)
    if len(sel) > 1:
        newDef = sel[-1]
        oldDefs = sel[:-1]

        tkc.replaceDeformers(oldDefs, newDef)
    else:
        pc.error("Please select at least two objects, old deformer(s) first, then new deformer !")

def selectDeformers():
    tkc.selectDeformers(pc.ls(sl=True))

def byPassNode():
    sel = pc.ls(sl=True)
    if len(sel) > 0:
        inObj=sel[0]
        ancestor = None
        if len(sel) > 1:
            ancestor=sel[1]

        tkRig.byPassNode(inObj, ancestor)
    else:
        pc.error("Please select at least one object (Ctrl from node to bypass), then eventually an ancestor node !")

def gator(*args):#I'll take strictCopy:bool, matchMatrices:bool
    sel = pc.ls(sl=True)
    if len(sel) > 1:
        strictCopy = False
        if len(args) > 1:
            strictCopy = args[1]
        copyMatrices = False
        if len(args) > 2:
            copyMatrices = args[2]

        tkc.gator(sel[:-1], sel[-1], copyMatrices, strictCopy)
    else:
        pc.warning("Please select at least two objects (any number of meshes to receive weights, then a \"Reference\" mesh) !")

def gatorClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    gator(True, pc.checkBox("gatorOptionStrict",query=True, value=True), pc.checkBox("gatorOptionMatch",query=True, value=True))

def gatorOption(*args):
    global UINAME
    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("gatorOptionWD", title='Gator')
    
    colLayout = pc.columnLayout()

    pc.text(label='Select any number of meshes to match first, then the ref mesh')

    pc.checkBox("gatorOptionStrict", label='Strict copy (weights array)', value=False)
    pc.checkBox("gatorOptionMatch", label='Match bind poses', value=False)
    pc.button(label='Apply', c=gatorClick, width=177)

    pc.showWindow(UINAME)

def setRefPoses(*args):
    sel = pc.selected()

    if len(sel) == 0:
        pc.warning("Please select deformer(s) (influence(s)), geometries or skinCluster(s) to reset bind poses !")
        return

    if sel[0].type() == "joint":
        tkc.setRefPoses(sel, inSkins=None)
    elif sel[0].type() == "skinCluster":
        setRefPoses(None, sel)
    else:
        skins = []
        for selNode in sel:
            skin = tkc.getSkinCluster(selNode)
            if skin != None:
                skins.append(skin)

        if len(skins) == 0:
            pc.warning("No skinCLusters found on selected objects !")
            return

        tkc.setRefPoses(None, skins)

def equilibrateSkin(*args):
    tkc.equilibrateSelPointsWeights()

def equilibrateSkinClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    strPrefixes = pc.textFieldGrp("equilibrateSkinOptionPrefixes",query=True, text=True)
    prefixes = ["Left","Right"]
    splitPrefixes = strPrefixes.split(",")
    if splitPrefixes[0] != "":
        prefixes[0] = splitPrefixes[0]
    if len(splitPrefixes) > 1 and splitPrefixes[1] != "" and splitPrefixes[1] != prefixes[0]:
        prefixes[1] = splitPrefixes[1]

    tkc.equilibrateSelPointsWeights(pc.checkBox("equilibrateSkinOptionRightToLeft", query=True, value=False), inPrefixes = prefixes)

def equilibrateSkinOption(*args):
    global UINAME
    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("equilibrateSkinOptionWD", title='EquilibrateSkin')
    
    colLayout = pc.columnLayout()

    pc.text(label='Select center loop points of a skinned mesh')

    pc.checkBox("equilibrateSkinOptionRightToLeft", label='Right to left', value=False)
    pc.textFieldGrp("equilibrateSkinOptionPrefixes", label='Prefixes', text="Left,Right")
    pc.button(label='Apply', c=equilibrateSkinClick, width=177)

    pc.showWindow(UINAME)

def tkSymUI(*args):
    tkSym.showUI()

def copyBS(*args):#I'll take strictCopy:bool, matchMatrices:bool
    sel = pc.ls(sl=True)
    if len(sel) > 1:
        source = sel[-1]
        targets = sel[:-1]
        sources = pc.ls(pc.listHistory(source, gl=True, pdo=True, lf=True, f=False, il=2), type="blendShape")
        if len(sources) == 0:
            pc.warning("Cannot find BlendShape node on {0}".format(source))
            return
        for target in targets:
            for source in sources:
                tkBlendShapes.copyBS(source.name(), target.name())
    else:
        pc.warning("Please select at least two objects (any number of meshes to receive blendShapes, then a \"Reference\" mesh) !")

def copyBSClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    copyBS(True, )

def copyBSOption(*args):
    print "NOT IMPLEMENTED"
    return

    global UINAME
    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("gatorOptionWD", title='Gator')
    
    colLayout = pc.columnLayout()

    pc.text(label='Select any number of meshes to match first, then the ref mesh')

    pc.checkBox("gatorOptionStrict", label='Strict copy (weights array)', value=False)
    pc.checkBox("gatorOptionMatch", label='Match bind poses', value=False)
    pc.button(label='Apply', c=gatorClick, width=177)

    pc.showWindow(UINAME)

def matchPointPositions(*args):#I'll take scope:string(All, LeftOnly, RightOnly), treshold:float
    print "matchPointPositions(", args
    sel = pc.ls(sl=True)
    if len(sel) > 1:
        sided = False
        rightToLeft=False
        treshold=2.0

        if len(args) > 1:
            if args[1] == "Right only":
                sided = True
                rightToLeft = True
            elif args[1] == "Left only":
                sided = True

        if len(args) > 2:
            treshold = args[2]

        for selObj in sel[:-1]:
            tkBlendShapes.matchPointPositions(sel[-1], selObj, sided, rightToLeft, treshold)

    else:
        pc.error("Please select at least two objects (any number of meshes to receive point positions, then a \"Reference\" mesh) !")

def matchPointPositionsClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    matchPointPositions(True, pc.optionMenu("matchOptionScope",query=True, value=True), pc.floatSliderGrp("matchOptionTreshold",query=True, value=True))

def matchPointPositionsOption(*args):
    global UINAME
    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("matchPointPositionsOptionWD", title='Match point positions')
    
    colLayout = pc.columnLayout()

    pc.text(label='Select any number of meshes to match first, then the ref mesh')

    pc.optionMenu("matchOptionScope", label='Scope')
    pc.menuItem("All", label="All")
    pc.menuItem("LeftOnly", label="Left only")
    pc.menuItem("RightOnly", label="Right only")
    pc.floatSliderGrp("matchOptionTreshold", label='Center treshold', field=True,pre=2, minValue=0.0, maxValue=5.0, fieldMinValue=0.0, fieldMaxValue=1000000, value=2.0)

    pc.button(label='Apply', c=matchPointPositionsClick, width=177)

    pc.showWindow(UINAME)

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

def getOscarProject():
    project = {}

    try:
        doc = minidom.parse(PROJECT_DEFINITION_PATH)
        
        project = {"name":doc.getElementsByTagName("CurrentProject")[0].firstChild.nodeValue}
        pathsElem = doc.getElementsByTagName("string")
        
        for pathElem in pathsElem:
            fullPath = pathElem.firstChild.nodeValue
            projPath, projDir = os.path.split(pathElem.firstChild.nodeValue)
            if projDir == project["name"]:
                project["path"] = fullPath
    except:
        pass
            
    if not "path" in project:
        pc.warning("Cannot detect current Oscar project !!")
        project = None
    else:
        tkc.PROJECT_INFO = project

    return project

def duplicateClean(*args):#I'll take muteDeformers:bool
    muteDeformers = False

    if len(args) > 1:
        muteDeformers = args[1]

    selObjs = pc.ls(sl=True)

    for selObj in selObjs:
        tkBlendShapes.duplicateAndClean(selObj.name(), "$REF_dupe", muteDeformers)

def duplicateCleanClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    duplicateClean(True, pc.checkBox("duplicateCleanOptionMute",query=True, value=True))

def duplicateCleanOption(*args):
    global UINAME

    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("duplicateCleanOptionWD", title='Duplicate Clean')
        
    colLayout = pc.columnLayout()

    pc.checkBox("duplicateCleanOptionMute", label='Mute Deformers', value=False)
    pc.button(label='Apply', c=duplicateCleanClick, width=177)

    pc.showWindow(UINAME)

def editTargetsClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    if UITAG == None or not pc.objExists(UITAG):
        pc.warning("No blendShape node given !")
        return

    target = pc.optionMenu("editTargetsTargets",query=True, value=True)
    shape = tkBlendShapes.editTarget(UITAG, target, corrective=None)

    if shape != None:
        pc.select(shape, replace=True)

def editAllTargetsClick(*args):
    if UITAG == None or not pc.objExists(UITAG):
        pc.warning("No blendShape node given !")
        return

    allTargets = tkBlendShapes.editTargets(UITAG)

    if len(allTargets) > 0:
        pc.select(allTargets, replace=True)

def removeTargetsClick(*args):
    if not pc.control(UINAME, query=True, exists=True):
        return

    if UITAG == None or not pc.objExists(UITAG):
        pc.warning("No blendShape node given !")
        return

    target = pc.optionMenu("editTargetsTargets",query=True, value=True)
    source = tkBlendShapes.getSource(UITAG)

    shape = tkBlendShapes.editTarget(UITAG, target)
    pc.blendShape(UITAG, edit=True, rm=True, target=[source, 2, target, 1])
    pc.delete(shape)
    pc.select(source, replace=True)
    editTargets()

def editTargets(*args):
    bs = None

    selObjs = pc.ls(sl=True)

    for selObj in selObjs:
        if selObj.type() != "blendShape":
            bsOps = pc.ls(pc.listHistory(selObj, gl=True, pdo=True, lf=True, f=False, il=2), type="blendShape")
            if len(bsOps) > 0:
                bs = bsOps[0].name()
        else:
            bs = selObj.name()

    if bs == None:
        pc.warning("No blendShape found in selection !")
        return

    global UINAME
    global UITAG

    UITAG = bs

    if pc.control(UINAME, query=True, exists=True):
        pc.deleteUI(UINAME, control=True)

    UINAME = pc.window("editTargetsWD", title='Edit blendShape targets')

    colLayout = pc.columnLayout()

    arrayAttrs = pc.listAttr("{0}.weight".format(bs), multi=True)

    pc.optionMenu("editTargetsTargets", label='Targets')
    for arrayAttr in arrayAttrs:
        pc.menuItem(arrayAttr, label=arrayAttr)

    pc.rowLayout(numberOfColumns=3)
    pc.button(label='Edit Target', c=editTargetsClick, width=128)
    pc.button(label='Edit all targets', c=editAllTargetsClick, width=128)
    pc.button(label='Remove Target', c=removeTargetsClick, width=128)

    pc.showWindow(UINAME)

def cleanTargets(*args):
    selObjs = pc.ls(sl=True)

    for selObj in selObjs:
        if selObj.type() != "blendShape":
            bsOps = pc.ls(pc.listHistory(selObj, gl=True, pdo=True, lf=True, f=False, il=2), type="blendShape")
            for bsOp in bsOps:
                tkBlendShapes.cleanUpBlendShapeWeights(bsOp.name())
        else:
            tkBlendShapes.cleanUpBlendShapeWeights(selObj.name())

def removeUnknown(*args):
    tkc.removeUnknownNodes()

def removeUnused(*args):
    tkc.deleteUnusedNodes()

def showPoseScaler(*args):
    tkPoseScaler.showUI()

def exportAnim(*args):
    tkRig.exportAnim(inObjects=None, inPath=None)

def importAnim(*args):
    result = pc.promptDialog(
            title="Import Anim",
            message="If you want to change destination namespace, give it here",
            text="",
            button=['OK', 'Remove old', 'Cancel'],
            defaultButton='OK',
            cancelButton='Cancel',
            dismissString='Cancel')
    if result == 'OK' or result == 'Remove old':
        namespace = None
        if result == 'OK':
            namespace = pc.promptDialog(query=True, text=True)

        tkRig.importAnim(swapNamespace=namespace)

def reskin(*args):
    tkc.reSkin(pc.selected())

def exportSkinnings(*args):
    inPath = None
    inPath = pc.fileDialog2(caption="Save your envelopes", fileFilter="Text file (*.txt)(*.txt)", dialogStyle=2, fileMode=0)

    if inPath != None and len(inPath) > 0:
        inPath = inPath[0]

        tkc.storeSkins(pc.selected(), inPath)

def importSkinnings(*args):
    inPath = None
    inPath = pc.fileDialog2(caption="Load your envelopes", fileFilter="Text file (*.txt)(*.txt)", dialogStyle=2, fileMode=1)

    if inPath != None and len(inPath) > 0:
        inPath = inPath[0]

        tkc.loadSkins(inPath, pc.selected())

def tkAnimPickerRebuild(*args):
    anim_picker.tkAnimPicker.show(True)

def getLongestName(inNode):
    return inNode.fullPath() if isinstance(inNode, pc.nodetypes.DagNode) else inNode.name()

def showOverrides(*args):
    selObjs = pc.ls(sl=True)

    selArray = [getLongestName(selObj) for selObj in selObjs]

    layersAdjusts = tkOutfits.getAllLayersAdjustments()

    objectsOverrides = {}

    for layersAdjust in layersAdjusts.keys():
        for objectAdjust in layersAdjusts[layersAdjust].keys():
            overrides = layersAdjusts[layersAdjust][objectAdjust]
            for key in overrides.keys():
                if key == None:
                    continue

                if not objectAdjust in objectsOverrides:
                    objectsOverrides[objectAdjust] = {}

                if not layersAdjust in objectsOverrides[objectAdjust]:
                    objectsOverrides[objectAdjust][layersAdjust] = {}

                objectsOverrides[objectAdjust][layersAdjust][key] = overrides[key]

    for objectAdjust in objectsOverrides.keys():
        if len(selObjs) == 0 or objectAdjust in selArray:
            obj = pc.PyNode(objectAdjust)
            print "\r\n *** {0} ***".format(obj.name())
            for layerAdjust in objectsOverrides[objectAdjust]:
                print " - {0}".format(layerAdjust)
                overrides = objectsOverrides[objectAdjust][layerAdjust]
                for override in overrides.keys():
                    print "   - {0}.{1} : {2}".format(obj.name(), override, overrides[override])

def showOutfits(*args):
    tkOutfits.showUI()

def showPalette(*args):
    tkPalette.showUI()

def selDupes(*args):
    namesDic = tkc.getDuplicates(inLog=True)

    dupObjs = []
    for name in namesDic:
        dupObjs.extend(namesDic[name])

    pc.select(dupObjs)

def filterDupes(*args):
    namesDic = tkc.getDuplicates(pc.selected(), inLog=True)

    dupObjs = []
    for name in namesDic:
        dupObjs.extend(namesDic[name], inLog=True)

    pc.select(dupObjs)

def renameDupes(*args):
    tkc.renameDuplicates(inLog=True)

def renameSelDupes(*args):
    tkc.renameDuplicates(pc.selected(), inLog=True)

def lock(*args):
    pc.lockNode(pc.selected(), lock=True)

def unlock(*args):
    pc.lockNode(pc.selected(), lock=False)

def showOrphans(*args):
    orphans = tkOutfits.getLayerOrphanMeshes("*:layer_*")
    if len(orphans) > 0:
        message = 'Some geometries are visible by default, but are not present in any layer :\r\n' + "\r\n".join([orphan.name() for orphan in orphans]) + "\r\n See log for object list !"
        rslt = pc.confirmDialog( title='Geometries not present in any layer', message=message, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
        pc.select(orphans, replace=True)
        print "\r\n" + message + "\r\n"

def menu():
    #Perform a deferred loading for Oscar modules
    global oscarAvailable
    try: 
        import LaunchMayaServer
    except ImportError, e:
        oscarAvailable = False
        pc.warning("Oscar modules could not be loaded (%s)!" % str(e))

    #Create Toonkit Menu
    if pc.menu("tkMainMenu", query=True, exists=True):
        pc.deleteUI("tkMainMenu", menu=True)

    gMainWindow = pc.mel.eval("string $parent = $gMainWindow")
    tkMainMenu = pc.menu("tkMainMenu", label="Toonkit", parent=gMainWindow, tearOff=True)

    pc.menuItem(label="Rebuild menu", parent=tkMainMenu, command="TKuserSetup.menu()")
    pc.menuItem(divider=True)

    mainMenuPath = os.path.join(oscarmodulepath, "scripts", "tkMenu")
    tkMenus.generateMenu(tkMainMenu, mainMenuPath, False)

    commonScriptsPath = "Z:\\Toonkit\\RnD\\Scripts\\Maya\\"
    serverCommonScriptsPath = commonScriptsPath.replace(SERVER_PATH_SUBST[0], SERVER_PATH_SUBST[1])

    if (os.path.isdir(serverCommonScriptsPath) or os.path.isdir(commonScriptsPath)) or oscarAvailable:
        pc.menuItem(divider=True, parent=tkMainMenu)

        if os.path.isdir(serverCommonScriptsPath) or os.path.isdir(commonScriptsPath):
            tkCommonMenu = pc.menuItem("tkCommonMenu", label="Scripts", parent=tkMainMenu, subMenu=True, tearOff=True)
            tkMenus.generateMenu(tkCommonMenu, commonScriptsPath)

        if oscarAvailable:
            proj = getOscarProject()
            if proj != None:
                tkProjectMenu = pc.menuItem("tkProjectMenu", label="Project : '{0}'".format(proj["name"]), parent=tkMainMenu, subMenu=True, tearOff=True)
                tkMenus.generateMenu(tkProjectMenu, os.path.join(proj["path"], "Scripts", "Maya"))

    #General/Version
    pc.menuItem(divider=True, parent=tkMainMenu)
    pc.menuItem(label="Install default hotkeys", parent=tkMainMenu, command="TKuserSetup.setHotKeys()")
    pc.menuItem(label="Hotkeys info", parent=tkMainMenu, command=hotKeyMap)
    pc.menuItem(divider=True, parent=tkMainMenu)
    pc.menuItem(label="Help (" + VERSIONINFO + ")", parent=tkMainMenu, command="TKuserSetup.showHelp()")

print "Done Initializing Python Toonkit's core library (menu creation deferred)"
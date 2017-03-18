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
DevHelpers
"""
import time
import re
import types
import os
import inspect

import pymel.core as pc

import tkMayaCore as tkc
import tkSIGroups
import tkSpring
import tkRig

__author__ = "Cyril GIBAUD - Toonkit"

MODULES = [tkc, tkSIGroups, tkSpring, tkRig]

NODESNAMES = "defaultRenderGlobals, miDefaultOptions, mentalrayGlobals, miDefaultFramebuffer"
STOREDATTRIBUTES = {}
UNFOUNDNODES = []

FORBIDDENATTRS = ["publishedNodeInfo", "instObjGroups", "InstObjGroups", "renderLayerInfo"]

def get_default_args(func):
    """
    returns a dictionary of arg_name:default_values for the input function
    """
    args, varargs, keywords, defaults = inspect.getargspec(func)
    if defaults != None and len(defaults) > 0:
        return dict(zip(reversed(args), reversed(defaults)))

    return {}

def getMethods():
    methods = {}

    for module in MODULES:
        objdir = dir(module)
        for key in objdir:
            func = module.__dict__.get(key)
            if isinstance(func, types.FunctionType):
                methods[module.__name__ + "." + func.__name__] = func

    return methods

def filterMethods(inStr="", inDocs=True):
    methods = getMethods()
    filteredMethods = {}

    regexes = []
    splitStr = inStr.split(",")

    for split in splitStr:
        if split != "" and split != "*" and split != ".":
            regexes.append(re.compile("^" + split.replace("*",".*") + "$", re.I))

    if len(regexes) > 0:
        for methodKey in methods.keys():
            methodName = methodKey.split(".")[1]
            for reg in regexes:
                if reg.search(methodName) or (inDocs and methods[methodKey].__doc__ != None and reg.search(str(methods[methodKey].__doc__).replace("\r", "").replace("\n", ""))):
                    filteredMethods[methodKey] = methods[methodKey]
                    break
    
    return filteredMethods

#################################################################################
#   monitorAttrChanges
#################################################################################

def getAttr(inInstance, inMethodName, inDefault="None"):
    if hasattr(inInstance,inMethodName):
        method = getattr(inInstance,inMethodName)
        if callable(method):
            return method()
    return inDefault

def objectInfo(*inArgs):
    sel = pc.ls(sl=True)

    if len(sel) > 0:
        obj = sel[0]
        print "name : %s, type : %s, nodeType : %s, dagPath %s" % (obj.name(), obj.type(), obj.nodeType(), getAttr(obj, "fullPath"))

def storeAttrs(inAdd=False):
    global STOREDATTRIBUTES
    global UNFOUNDNODES

    UNFOUNDNODES = []
    if not inAdd:
        STOREDATTRIBUTES = {}

    splitNames = NODESNAMES.split(",")

    for splitName in splitNames:
        name = splitName.strip()
        if pc.objExists(name):
            lstAttrs = pc.listAttr(name, scalarAndArray=True)
            for attr in lstAttrs:
                valid=True
                for forbiddenAttr in FORBIDDENATTRS:
                    if forbiddenAttr in attr:
                        valid = False
                        break

                if valid:
                    STOREDATTRIBUTES[name +"."+ attr] = pc.getAttr(name +"."+ attr)
        else:
            UNFOUNDNODES.append(name)

def compareAttrs(inUpdate=True):
    global STOREDATTRIBUTES

    changes = []

    for attr in STOREDATTRIBUTES.keys():
        oldVal = STOREDATTRIBUTES[attr]
        newVal = pc.getAttr(attr)

        if oldVal != newVal:
            changes.append((attr, oldVal, newVal))

        if inUpdate:
            STOREDATTRIBUTES[attr] = newVal

    return changes

def log():
    if len(STOREDATTRIBUTES) > 0:
        print "Attributes dictionary at %s" % time.strftime('%X %x %Z')
        print "-------------------------------------------"
        for key in STOREDATTRIBUTES.keys():
            print key.ljust(50) + " : %s" % str(STOREDATTRIBUTES[key])
    else:
        print "Attributes dictionary is empty at %s" % time.strftime('%X %x %Z')
    print ""

def logChanges(inChanges):
    if len(inChanges) > 0:
        print "Changes at %s" % time.strftime('%X %x %Z')
        print "-------------------------------------------"
        for attr_oldVal_newVal in inChanges:
            print "- " + attr_oldVal_newVal[0].ljust(40) + "%s => %s" % (attr_oldVal_newVal[1], attr_oldVal_newVal[2])
    else:
        print "No changes at %s" % time.strftime('%X %x %Z')
    print ""

def monitorAttrChangesUI(*inArgs):
    """
    UI for monitorAttrChanges
    """
    # check to see if window exists
    if (pc.window('monitorAttrChangesUI', q=True, exists=True)):
        pc.deleteUI('monitorAttrChangesUI')
    myUI = pc.window('monitorAttrChangesUI', title='Monitor attribute changes', widthHeight=(260, 260))
    colLayout = pc.columnLayout( adjustableColumn=True )

    pc.rowLayout(numberOfColumns=2, adjustableColumn2=2)
    pc.text("Nodes :")
    pc.textField("monitorAttrChangesNodesCB", text=NODESNAMES, cc=textChanged )
    pc.setParent(colLayout)
    
    pc.rowLayout(numberOfColumns=2, adjustableColumn2=1)
    pc.button("Store", command=storeClicked)
    pc.checkBox("monitorAttrChangesAddCB", label="Add", value=False)
    pc.setParent(colLayout)

    pc.rowLayout(numberOfColumns=2, adjustableColumn2=1)
    pc.button("Compare", command=compareClicked)
    pc.checkBox("monitorAttrChangesUpdateCB", label="Update", value=True)
    pc.setParent(colLayout)
    pc.button("Log current values", command=logClicked)

    pc.showWindow(myUI)

#CALLBACKS

def textChanged(*inArgs):
    global NODESNAMES
    NODESNAMES = pc.textField("monitorAttrChangesNodesCB", query=True, text=True)

def storeClicked(*inArgs):
    global STOREDATTRIBUTES
    global UNFOUNDNODES

    storeAttrs(pc.checkBox("monitorAttrChangesAddCB", query=True, value=True))

def compareClicked(*inArgs):
    changes = compareAttrs(pc.checkBox("monitorAttrChangesUpdateCB", query=True, value=True))
    logChanges(changes)

def logClicked(*inArgs):
    log()

#################################################################################
#   devMate
#################################################################################

def UIVisChanged(args):
    #Defer the execution in case hidiung is temporary (docking/undocking)
    pc.evalDeferred("tkDevHelpers.cleanIfHidden()")

def cleanIfHidden():
    if pc.window('devMateUI', q=True, exists=True):
       if not pc.control("devMateDockControl", query=True, visible=True):
            pc.deleteUI('devMateUI')
            pc.deleteUI('devMateDockControl')

def devMateUI(*inArgs):
    if (pc.window('devMateUI', q=True, exists=True)):
        pc.deleteUI('devMateUI')

    dirname, filename = os.path.split(os.path.abspath(__file__))
    ui = pc.loadUI(uiFile=dirname + "\\UI\\tkDevMate.ui")
    pc.showWindow(ui)

    pc.setParent(u=1)
    dockLayout = pc.paneLayout(configuration='single')

    dockName = pc.dockControl("devMateDockControl", allowedArea='all', area='top', floating=False, content=dockLayout, label="Dev' Mate", vcc=UIVisChanged)
    pc.control(ui, e=True, parent=dockLayout)

    filtersChanged()

def filtersChanged():
    cmds = filterMethods(pc.textField("tkDMFiltersTB", query=True, text=True))
    
    pc.textScrollList("tkDMFunctionsLB", edit=True, removeAll=True)

    cmdskeys = cmds.keys()
    cmdskeys = sorted(cmdskeys)

    for cmd in cmdskeys:
        pc.textScrollList("tkDMFunctionsLB", edit=True, append=cmd)

def printValue(inValue):
    if isinstance(inValue, str):
        return "\"%s\"" % inValue

    return str(inValue)

def functionSelChanged():

    #"%s(%s)" % (methodKey, ",".join(methods[methodKey].func_code.co_varnames))] = 

    sel = pc.textScrollList("tkDMFunctionsLB", query=True, selectItem=True)

    if sel != None and len(sel) > 0:
        methods = filterMethods(pc.textField("tkDMFiltersTB", query=True, text=True), pc.checkBox("tkDMDocCB", query=True, value=True))

        if sel[0] in methods:
            args, varargs, keywords, defaults = inspect.getargspec(methods[sel[0]])
            defaults = get_default_args(methods[sel[0]])

            argsArray =  []
            for argName in args:
                if argName in defaults:
                    argsArray.append("%s=%s" % (argName, printValue(defaults[argName])))
                else:
                    argsArray.append(argName)
            strContent = "#import %s\r\n" % sel[0].split(".")[0]
            strContent += "%s(%s)\r\n\r\n'''\r\n" % (sel[0], ",".join(argsArray))
            strContent += "Documentation : \r\n" + str(methods[sel[0]].__doc__) + "\r\n\r\n"
            strContent += "'''\r\n"
            pc.textField("tkDMFunctionsLE", edit=True, text=strContent)

def docChanged():
    filtersChanged()
    functionSelChanged()
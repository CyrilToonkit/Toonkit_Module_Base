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
from functools import partial
import os
import re

import pymel.core as pc

import tkMayaCore as tkc
import mayaexecpythonfile

__author__ = "Cyril GIBAUD - Toonkit"

SEP = False#Indicates if last item was a separator

SUFFIX_OPTIONBOX = "_optionBox"
SUFFIX_SUBMENU = "_subMenu"
SUFFIX_EXTERNALMENU = "_externalMenu"

MENUFORMAT_REG = re.compile('((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))')
MENUFORMAT_REPLACE = {
    "VARPARO":"(",
    "VARPARC":")",
    "VARBRAO":"{",
    "VARBRAC":"}",
    "VARQUO":"'",
    "VARQUOD":"\"",
    "VARDOT":"."
}

#Todo : implement this at Oscar project level
SERVER_PATH_SUBST = ("Z:\\Toonkit\\","\\\\NHAMDS\\Toonkit\\ToonKit\\")

def menuFormat(in_rawName, inLocal=False, inServer=False):
    formattedName = in_rawName

    if '.' in formattedName:
        formattedName, ext = os.path.splitext(formattedName)

    for searchStr, replaceStr in MENUFORMAT_REPLACE.iteritems():
        formattedName = formattedName.replace(searchStr, replaceStr)

    digits = 0
    #strip digits in first or second position
    if formattedName[0].isdigit():
        digits = 1
    elif len(formattedName) > 1 and formattedName[1].isdigit():
        digits = 2

    if digits > 0:
        while digits < (len(formattedName) - 1) and formattedName[digits].isdigit():
            digits += 1

        formattedName = formattedName[digits:]

    #strip separation characters
    seps = ["-","_"," "]
    formattedName = formattedName.strip("".join(seps))

    #Un-camelCase
    formattedName = MENUFORMAT_REG.sub(r" \1", formattedName).lower()
    
    #Remove underscores
    formattedName = formattedName.replace("_", " ")

    #Upper first letter
    formattedName = formattedName[0].upper() + formattedName[1:]

    if inLocal:
        formattedName += (" (local override)" if inServer else " (local only)")

    return formattedName

def executeScript(in_path):
    try:
        mayaexecpythonfile.execpythonfile(in_path)
    except Exception as e:
        pc.warning("Cannot execute script from " + in_path + " : " + str(e))

def executeScriptClick(*args):
    executeScript(args[0])

def executeScriptClick(*args):
    executeScript(args[0])

def executeSubScriptClick(*args):
    tkc.executeCode(args[0], functionName="do", args=[args[1]])

def generateDynamicItems(in_parentMenuItem, in_scriptPath, inLocal=False, inServer=False):
    code = None
    with open(in_scriptPath, 'r') as content_file:
        code = content_file.read()

    if code == None:
        pc.warning("Dynamic menu {0} failed!".format(in_scriptPath))

    items = tkc.executeCode(code, functionName="get")

    if items == None or len(items) == 0:
        pc.warning("Dynamic menu {0} returned no items !".format(in_scriptPath))
        return

    elementName, elementExt = os.path.splitext(os.path.split(in_scriptPath)[-1])
    elementName = elementName.replace(SUFFIX_SUBMENU, "")
    if pc.menuItem(elementName + "Menu", exists=True):
        pc.deleteUI(elementName + "Menu")

    tkSubMenu = pc.menuItem(elementName + "Menu", label=menuFormat(elementName, inLocal, inServer), parent=in_parentMenuItem, subMenu=True, tearOff=True)
    for item in items:
        subElementName, subElementExt = os.path.splitext(item[0])
        subElementName = subElementName.replace("/", "\\").replace("\\", "_")
        pc.menuItem(subElementName + "Item", label=item[0], parent=tkSubMenu, aob=True, command=partial(executeSubScriptClick,code, item[1]))

def generateExternalMenu(in_parentMenuItem, in_scriptPath, inLocal=False, inServer=False):
    code = None
    with open(in_scriptPath, 'r') as content_file:
        code = content_file.read()

    if code == None:
        pc.warning("External menu {0} failed!".format(in_scriptPath))

    folderPath = tkc.executeCode(code, functionName="get")

    if folderPath == None or not isinstance(folderPath, basestring or folderPath == "" ):
        pc.warning("External menu {0} returned invalid value '{1}', must be a string representing a folder absolute path ' !".format(in_scriptPath, folderPath))
        return

    if not os.path.isdir(folderPath):
        pc.warning("External menu {0}, folder not found '{1}' !".format(in_scriptPath, folderPath))
        return

    elementName, elementExt = os.path.splitext(os.path.basename(in_scriptPath))
    elementName = elementName[:-len(SUFFIX_EXTERNALMENU)]
    if pc.menuItem(elementName + "Menu", exists=True):
        pc.deleteUI(elementName + "Menu")

    tkSubMenu = pc.menuItem(elementName + "Menu", label=menuFormat(elementName, inLocal, inServer), parent=in_parentMenuItem, subMenu=True, tearOff=True)
    generateMenu(tkSubMenu, folderPath)

def generateMenu(in_parentMenuItem, in_scriptsPath, in_checkServer=True):
    global SEP#Indicates if last item was a separator

    alternatePath = in_scriptsPath.replace(SERVER_PATH_SUBST[0], SERVER_PATH_SUBST[1])

    elementsDic = {}

    if os.path.isdir(in_scriptsPath) or not in_checkServer or os.path.isdir(alternatePath):
        elements = os.listdir(in_scriptsPath) if os.path.isdir(in_scriptsPath) else []

        for element in elements:
            if (element.endswith(".pyc") and (element[:-4]+".py") in elementsDic) or (element.endswith(".py") and (element[:-3]+".pyc") in elementsDic):
                continue
            elementsDic[element] = [os.path.join(in_scriptsPath, element)]

        if in_checkServer and alternatePath != in_scriptsPath:
            alternateElements = os.listdir(alternatePath) if os.path.isdir(alternatePath) else []
            for alternateElement in alternateElements:
                if not alternateElement in elementsDic:
                    if (alternateElement.endswith(".pyc") and (alternateElement[:-4]+".py") in elementsDic) or (alternateElement.endswith(".py") and (alternateElement[:-3]+".pyc") in elementsDic):
                        continue
                    elements.append(alternateElement)
                    elementsDic[alternateElement] = [os.path.join(alternatePath, alternateElement)]
                else:
                    elementsDic[alternateElement].append(os.path.join(alternatePath, alternateElement))

        elements = elementsDic.keys()
        elements.sort(key=lambda x:x.lower())

        for element in elements:
            elementName, elementExt = os.path.splitext(element)
            if element.endswith(SUFFIX_OPTIONBOX+elementExt):
                continue

            fullpath = elementsDic[element][0]

            local = False
            server = True
            
            if in_checkServer:
                local = fullpath.startswith(SERVER_PATH_SUBST[0])
                server = fullpath.startswith(SERVER_PATH_SUBST[1]) or len(elementsDic[element]) > 1
            
            if "__" in elementName:#Separator
                if not SEP:
                    matchObj = re.match(".*_([A-Za-z]+).*", elementName)
                    if matchObj:
                        pc.menuItem(divider=True, parent=in_parentMenuItem, label=menuFormat(matchObj.groups()[-1], False, True))
                    else:
                        pc.menuItem(divider=True, parent=in_parentMenuItem)
                SEP=True

            elif element.endswith(SUFFIX_SUBMENU+elementExt):#dynamic subMenu (ends with SUFFIX_SUBMENU)
                generateDynamicItems(in_parentMenuItem, fullpath, local, server)

            elif element.endswith(SUFFIX_EXTERNALMENU+elementExt):#external subMenu (ends with SUFFIX_EXTERNALMENU)
                generateExternalMenu(in_parentMenuItem, fullpath, local, server)

            elif os.path.isdir(fullpath):#subMenu (Directory)
                if pc.menuItem(elementName + "Menu", exists=True):
                    pc.deleteUI(elementName + "Menu")

                tkSubMenu = pc.menuItem(elementName + "Menu", label=menuFormat(element, local, server), parent=in_parentMenuItem, subMenu=True, tearOff=True)
                generateMenu(tkSubMenu, fullpath, in_checkServer)
                SEP=False

            else:#menuItem or optionBox (file)
                if pc.menuItem(elementName + SUFFIX_OPTIONBOX, exists=True):
                    pc.deleteUI(elementName + SUFFIX_OPTIONBOX)
                if pc.menuItem(elementName + "Item", exists=True):
                    pc.deleteUI(elementName + "Item")

                #menuItem (file)
                pc.menuItem(elementName + "Item", label=menuFormat(element, local, server), parent=in_parentMenuItem, aob=True, command=partial(executeScriptClick, fullpath))
                optionBox = elementName + SUFFIX_OPTIONBOX+elementExt
                if optionBox in elements:#optionBox (file)
                    pc.menuItem(elementName + "OptionBox", optionBox=True, command=partial(executeScriptClick, elementsDic[optionBox][0]))
                SEP=False
"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Author : Stephane Bonnot - Parallel Dev
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
import maya.cmds as cmds
import tkMayaCore as tkc
from functools import partial

__author__ = "Mickael Garcia - Toonkit"

CTXMENU_FLAG = "tkContextMenu"

DEFAULT_CTX = {
    "name":        "Hello world",
    "code":        "print 'Hello world'",
    "condition":   None,
    "inherit":     None,
    "inheritRecur":False,
}
GLOBAL_DICT = {}

# Function call at right click
def add_items(parent, inObject):
    """Function called at right click to add custom items in sepcified context.
    Parameters:
        parent (str) : Parent's name of the UI maya object's of the dag menu.
        inObject (str) : Object name mouse hovered or selected.
    Return: Create custom items menu on dag menu.
    """
    selection = cmds.ls(sl=True, ap=True)
    try:
        selection.remove(inObject)
    except:pass
    global GLOBAL_DICT
    GLOBAL_DICT.clear()
    for x in selection:
        GLOBAL_DICT[x] = getContextMenus(x)[1]

    keys, menusDict = getContextMenus(inObject)
    for itemName, subItems in keys:
        create_item(itemName, parent, menusDict, subItems)

def create_item(itemName, parent, inDict, subItems):
    """Recurcive function to create dag items menu in right context.
    Parameters:
        itemName (str) : Parameter name.
        inDict (dict) : Data of all parameter of contextMenus.
    Return: Create custom items menu on dag menu corresponding of all parameters.
    """
    if inDict[itemName]["inherit"]:
        objectName, propertyName = inDict[itemName]["inherit"].split(".")
        try:
            inheritRecur = inDict[itemName]["inheritRecur"]
            keys, menusDict =  getContextMenus(objectName)
            inDict[itemName] = menusDict[itemName]
            menusDict.update(inDict)
            inDict = menusDict
            if inheritRecur:
                subItems = get_heritage_subItems(keys, propertyName)
        except:
            inDict[itemName]["code"] = "print\"No code here\""
            cmds.warning("The menuItem '{0}' failed to find heritage property '{1}' on '{2}' node".format(inDict[itemName]["name"], propertyName, objectName))
    isSubMenu = len(subItems) > 0
    for value in GLOBAL_DICT.values():
        try:
            inDict[itemName]["code"] += "\n" + value[itemName]["code"]
        except: pass
    condition = 1
    if inDict[itemName]["condition"]:
        condition = eval(inDict[itemName]["condition"])
    if condition == True:
        subMenu_Parent = cmds.menuItem(p=parent, l=inDict[itemName]["name"], sm = isSubMenu, c=inDict[itemName]["code"] )

    if isSubMenu:
        for subItem in subItems:
            create_item(subItem[0], subMenu_Parent, inDict, subItem[1])
        cmds.setParent(parent, m=True)

def get_heritage_subItems(keys, propertiesName):
    """Get all subitems of the giver properties (Recurcive function).
    Parameters:
        keys (list): herarchique view of parameters.
        propertiesName (str): Properties name to find children.
    return:
        Returne (list) : List of hierarchique items childs of propertiesName
    """
    for key in keys:
        if propertiesName == key[0]:
            return key[1]
        else:
            get_heritage_subItems(key, propertiesName)


def getValidObjectName(inText):
    # To do to excape none maya name 
    return inText


def writeContextMenu(inObject, **kwargs):
    """Write properties of context Menus
    Parameters: 
        inObject (str): Object name to attache property
    Returne (str): returne the name of the created node."""
    ctxProp = inObject

    if not CTXMENU_FLAG in inObject.name():
        ctxProp = tkc.getProperty(inObject, CTXMENU_FLAG) or tkc.addProperty(inObject, CTXMENU_FLAG)


    prop = tkc.addProperty(ctxProp, getValidObjectName(kwargs["name"]))

    tkc.decorate(prop, kwargs)
    
    return prop

def readContextMenuProp(inProperty, inDefaultValues=DEFAULT_CTX):
    """# Read Context Menu propertys on property
    Parameters:
        inProperty (str): Property transform node
    Return (dict): Return all properties of the property node with the default value for non-declared properties"""
    inObject = tkc.getNode(inProperty)
    decoration = tkc.readDecoration(inObject)
    
    if len(decoration) == 0:
        return None
    dic = inDefaultValues.copy()
    dic.update(decoration)
    
    return dic

# Read 
def getContextMenus(inObject):
    """
    return value structure :
        keys = [("Visibilities",
                    ("Hide", ()),
                    ("Show", ())
                ),
                ("Swicth", ())]
    """
    inObject = tkc.getNode(inObject)
    ctxProp = inObject
    ns = tkc.getNamespace(inObject)
    
    if not CTXMENU_FLAG in inObject.name():
        ctxProp = tkc.getProperty(inObject, CTXMENU_FLAG)
        
    if ctxProp is None:
        return ([], {})

    properties = tkc.getProperties(ctxProp)
    
    keys = []
    MenuDict = {}
    
    for prop in properties:
        ctx = readContextMenuProp(prop)
        ctx["code"] = ctx["code"].replace("$NS", ns)
        if ctx["condition"]:
            ctx["condition"] = ctx["condition"].replace("$NS", ns)
        if ctx["inherit"]:
            ctx["inherit"] = ctx["inherit"].replace("$NS", ns)
        if not ctx is None:
            subKeys, subDict = getContextMenus(prop)
            keys.append((ctx["name"], subKeys))
            MenuDict[ctx["name"]] = ctx
            MenuDict.update(subDict)
            
    return (keys, MenuDict)
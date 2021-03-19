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

# Function call at right click
def add_items(parent, inObject):
    keys, menusDict = getContextMenus(inObject)
    for itemName, subItems in keys:
        nameSpace = str(tkc.getNode(inObject).namespace())# TO DO : Can be execute in getContextMenus to optimise
        create_item(itemName, parent, menusDict, subItems)


def create_item(itemName, parent, inDict, subItems):
        code = inDict[itemName]["code"]
        isSubMenu = len(subItems) > 0
        subMenu_Parent = cmds.menuItem(p=parent, l=inDict[itemName]["name"], sm = isSubMenu, c=code )
        if isSubMenu:
            for subItem in subItems:
                create_item(subItem[0], subMenu_Parent, inDict, subItem[1])
            cmds.setParent(parent, m=True)
        

def get_namespace(inObject):
    if not tkc.CONST_NSSEP in inObject:
        return ""
    else:
        return  tkc.CONST_NSSEP.join(inObject.split(tkc.CONST_NSSEP)[:-1]) + tkc.CONST_NSSEP

def getValidObjectName(inText):
    # To do to excape none maya name 
    return inText


def writeContextMenu(inObject, **kwargs):
    # Write properties of context Menus
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
    Return:
        dic (dict): Return all properties of the property node with the default value for non-declared properties"""
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
    
    if not CTXMENU_FLAG in inObject.name():
        ctxProp = tkc.getProperty(inObject, CTXMENU_FLAG)
        
    if ctxProp is None:
        return ([], {})

    properties = tkc.getProperties(ctxProp)
    
    keys = []
    MenuDict = {}
    
    for prop in properties:
        ctx = readContextMenuProp(prop)
        ctx["code"] = ctx["code"].replace("$NS", tkc.getNamespace(inObject))
        print ctx
        if not ctx is None:
            subKeys, subDict = getContextMenus(prop)
            keys.append((ctx["name"], subKeys))
            MenuDict[ctx["name"]] = ctx
            MenuDict.update(subDict)
            
    return (keys, MenuDict)
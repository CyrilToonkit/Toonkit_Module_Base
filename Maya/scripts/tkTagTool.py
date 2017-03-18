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

import pymel.core as pc

__author__ = "Cyril GIBAUD - Toonkit"

UINAME = "tagToolUI"

def getObjectsWithNotes():
    return [attr.node() for attr in pc.ls(["*:*.notes" ,"*.notes"])]

""" DEPRECATED
def getMeshesT():
    meshes = pc.ls(["*", "*:*"], type="mesh")
    
    meshesT = []
    
    for mesh in meshes:
        meshT = mesh.getParent()
        if not meshT in meshesT:
            meshesT.append(meshT)
            
        if pc.attributeQuery("notes", node=mesh, exists=True):
            note = mesh.notes.get()
            if note != "":
                pc.warning("Notes on mesh shape '{0}', maybe it needs to be written on the tranform node ?".format(mesh.name()))
    return meshesT
"""

def getTags(inObjects=None, inTags=None):
    if inObjects == None:
        inObjects = getObjectsWithNotes()
    else:
        if not isinstance(inObjects, list):
            inObjects = [inObjects]

    tags = {}
    
    for meshT in inObjects:
        if pc.attributeQuery("notes", node=meshT, exists=True):
            notes = meshT.notes.get().split(",")
            for note in notes:
                if note == "" or (inTags != None and (inTags != note and not note in inTags)):
                    continue
                if not (note in tags):
                    tags[note] = []
                tags[note].append(meshT.name())
        
    return tags

def printTags(inObjects=None, inTags=None):
    if inObjects == None:
        inObjects = getObjectsWithNotes()

    if inTags == None:
        inTags = getTags(inObjects)

    print "\n".join(["{0} : '{1}'".format(k, ",".join(v)) for k,v in inTags.iteritems()])

def setTags(inObject, inTagsStr):
    if not pc.attributeQuery("notes", node=inObject, exists=True):
        pc.addAttr(inObject, sn="nts", ln="notes", dt="string")
    inObject.notes.set(inTagsStr)

def addTags(inObjects=None, inTags=None):
    if inObjects == None:
        inObjects = pc.selected()

    if not isinstance(inTags, list):
        inTags = [inTags]
            
    for inObject in inObjects:
        modified=False
        tags = getTags(inObject).keys()
        for inTag in inTags:
            if not inTag in tags:
                tags.append(inTag)
                modified=True
        
        if modified:
            setTags(inObject, ",".join(tags))

def removeTags(inObjects=None, inTags=None):
    if inObjects == None:
        inObjects = pc.selected()

    if not isinstance(inTags, list):
        inTags = [inTags]
            
    for inObject in inObjects:
        modified=False
        tags = getTags(inObject).keys()
        for tag in tags:
            if tag in inTags:
                tags.remove(tag)
                modified=True
        
        if modified:
            setTags(inObject, ",".join(tags))

def addTagClick(*args):
    addTags(inTags=args[0])
    showUI()

def addCustomTagClick(*args):
    addTags(inTags=pc.textFieldGrp(args[0], query=True, text=True))
    showUI()

def removeTagClick(*args):
    removeTags(inTags=args[0])
    showUI()

def showUI(*args):
    if (pc.window(UINAME, q=True, exists=True)):
        pc.deleteUI(UINAME)
    
    tags = getTags()
    
    ttWindow = pc.window(UINAME, title="Tag Tool", width=150)

    pc.frameLayout(label="Add tags", collapsable=True)
    pc.columnLayout()
    row = pc.rowLayout(numberOfColumns=3)
    pc.button( label='Add "nfr"', command=partial(addTagClick, "nfr"))
    pc.button( label='Add "model_low"', command=partial(addTagClick, "model_low"))
    pc.button( label='Add "hd"', command=partial(addTagClick, "hd"))
    
    pc.setParent(upLevel=True)
    row = pc.rowLayout(numberOfColumns=2)
    pc.button( label='Add custom tag', command=partial(addCustomTagClick, "TagToolCustomTag"))
    pc.textFieldGrp("TagToolCustomTag", label='Custom tag', text="MyTag")
    
    pc.setParent(upLevel=True)
    frame = pc.frameLayout(label="Edit tags", collapsable=True)
    for tag, objects in tags.iteritems():
        pc.rowLayout(numberOfColumns=2, parent=frame)
        pc.button( label='Select "{0}"'.format(tag), command="pc.select([{0}])".format(",".join(["'{0}'".format(obj) for obj in objects])))
        pc.button( label='Remove "{0}" tag on selection'.format(tag), command=partial(removeTagClick, tag))

    pc.showWindow(ttWindow)
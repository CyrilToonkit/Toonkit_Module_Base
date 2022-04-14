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

def getTags(inObjects=None, inTags=None):
    if inObjects == None:
        inObjects = getObjectsWithNotes()
    else:
        if not isinstance(inObjects, list):
            inObjects = [inObjects]

    tags = {}
    
    for meshT in inObjects:
        if pc.attributeQuery("notes", node=meshT, exists=True):
            notes = meshT.notes.get()
            if notes is None:
                continue
            notes = notes.split(",")
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

    print ("\n".join(["{0} : '{1}'".format(k, ",".join(v)) for k,v in inTags.items()]))

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
        tags = list(getTags(inObject).keys())
        for inTag in inTags:
            if not inTag in tags:
                print(tags)
                print(getTags(inObject))
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
        tags = list(getTags(inObject).keys())
        for tag in tags:
            if tag in inTags:
                tags.remove(tag)
                modified=True
        
        if modified:
            setTags(inObject, ",".join(tags))

def saveTags(inTags, inPath):
    with open(inPath, "w") as f:
        f.write(str(inTags))

def loadTags(inPath, inApply=False):
    content = ""
    tags = {}
    
    try:
        with open(inPath) as f:
            content = f.read()
        
        if len(content) > 0:
            tags = eval(content)
            
        if inApply:
            applyTags(tags)
    except:
        pc.warning("Can't read {0} as a tag file !".format(inPath))

    return tags

def applyTags(inTags):
    defects=0
    for tagValue, tagObjs in inTags.items():
        for tagObj in tagObjs:
            baseName = tagObj.split(":")[-1]
            candidates = [tagObj, "*:"+baseName]
            if baseName != tagObj:
                candidates.append(baseName)
            tagCandidates = pc.ls(candidates)

            if len(tagCandidates) == 0:
                defects += 1
                pc.warning("{0} cannot be found !".format(baseName))
                continue

            addTags([tagCandidates[0]], tagValue)

    return defects == 0

def loadClick(*args):
    choosenFile = pc.fileDialog2(caption="Select your tags file", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=1)

    if choosenFile != None and len(choosenFile) > 0:
        loadTags(choosenFile[0], inApply=True)
        showUI()
    else:
        pc.warning("No file selected !")

def saveClick(*args):
    choosenFile = pc.fileDialog2(caption="Save your tags file", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=0)

    if choosenFile != None and len(choosenFile) > 0:
        saveTags(getTags(), choosenFile[0])
    else:
        pc.warning("No file selected !")

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

    pc.columnLayout()

    row = pc.rowLayout(numberOfColumns=2)
    pc.button( label='Load...', command=loadClick)
    pc.button( label='Save...', command=saveClick)
    pc.setParent(upLevel=True)

    pc.frameLayout(label="Add tags", collapsable=True)
    pc.columnLayout()
    row = pc.rowLayout(numberOfColumns=4)
    pc.button( label='Add "nfr"', command=partial(addTagClick, "nfr"))
    pc.button( label='Add "LD"', command=partial(addTagClick, "LD"))
    pc.button( label='Add "MD"', command=partial(addTagClick, "MD"))
    pc.button( label='Add "HD"', command=partial(addTagClick, "HD"))
    
    pc.setParent(upLevel=True)
    row = pc.rowLayout(numberOfColumns=2)
    pc.button( label='Add custom tag', command=partial(addCustomTagClick, "TagToolCustomTag"))
    pc.textFieldGrp("TagToolCustomTag", label='Custom tag', text="MyTag")
    
    pc.setParent(upLevel=True)
    frame = pc.frameLayout(label="Edit tags", collapsable=True)
    for tag, objects in tags.items():
        pc.rowLayout(numberOfColumns=2, parent=frame)
        pc.button( label='Select "{0}"'.format(tag), command="pc.select([{0}])".format(",".join(["'{0}'".format(obj) for obj in objects])))
        pc.button( label='Remove "{0}" tag on selection'.format(tag), command=partial(removeTagClick, tag))
    
    pc.showWindow(ttWindow)
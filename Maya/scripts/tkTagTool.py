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
import tkMayaCore as tkc
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

def getOSCARTags():
    tagsParams = pc.ls("*_Root_OSCAR_Attributes.GenerationTags")
    allTags = {}
    for tagParam in tagsParams:
        tagValue = tagParam.get()
        tagsValue = tagValue.split(",")
        for tag in tagsValue:
            if not tag in allTags.keys():
                allTags[tag] = [tagParam.node().getParent().name()]
            else:
                allTags[tag].append(tagParam.node().getParent().name())

    return allTags

def getAllTags():
    modTags = getTags()
    oscarTags = getOSCARTags()
    allTags = {}

    for key, value in modTags.items():
        if not key in allTags.keys():
            allTags[key] = value
        else:
            allTags[key] += value
            
    for key, value in oscarTags.items():
        if not key in allTags.keys():
            allTags[key] = value
        else:
            allTags[key] += value
    
    return allTags

def allButCurrentTag(inTag, allTags, exclusif=False):
    if inTag not in allTags.keys():
        pc.error("The given tag does not exist !")
    
    toDelete = []
    if not exclusif:    
        for key, value in allTags.items():
            if key != inTag:
                for obj in value:
                    if obj not in allTags[inTag]:
                        toDelete.append(obj)
    elif exclusif is True:
        meshs = list(set([x.getParent() for x in pc.ls(type="mesh")]))
        for mesh in meshs:
            if mesh not in allTags[inTag]:
                toDelete.append(mesh.name())
        for key, value in allTags.items():
            if key != inTag:
                for obj in value:
                    if obj not in allTags[inTag]:
                        toDelete.append(obj)
        toDelete = list(set(toDelete))
    return toDelete

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

class showUI():
    def __init__(self):
        if (pc.window(UINAME, q=True, exists=True)):
            pc.deleteUI(UINAME)
        
    
        ttWindow = pc.window(UINAME, title="Tag Tool", width=150)

        pc.columnLayout()

        row = pc.rowLayout(numberOfColumns=4)
        pc.button( label='Load...', command=self.loadClick)
        pc.button( label='Save...', command=self.saveClick)
        self.modTagsCb = pc.checkBox(label = "Mod Tags", value = True, cc=self.updateUI)
        self.oscarTagsCb = pc.checkBox(label = "Oscar Tags", value = False, cc=self.updateUI)
        pc.setParent(upLevel=True)

        pc.frameLayout(label="Add tags", collapsable=True)
        pc.columnLayout()
        row = pc.rowLayout(numberOfColumns=4)
        pc.button( label='Add "nfr"', command=partial(self.addTagClick, "nfr"))
        pc.button( label='Add "LD"', command=partial(self.addTagClick, "LD"))
        pc.button( label='Add "MD"', command=partial(self.addTagClick, "MD"))
        pc.button( label='Add "HD"', command=partial(self.addTagClick, "HD"))
        
        pc.setParent(upLevel=True)
        row = pc.rowLayout(numberOfColumns=2)
        pc.button( label='Add custom tag', command=partial(self.addCustomTagClick, "TagToolCustomTag"))
        self.textfield = pc.textFieldGrp("TagToolCustomTag", label='Custom tag', text="MyTag")
        
        pc.setParent(upLevel=True)
        self.frame = pc.frameLayout(label="Edit tags", collapsable=True)

        self.updateUI()
        pc.showWindow()

    def updateUI(self, *args):
        self.tags = None
        if pc.checkBox(self.modTagsCb, value=True, q=True) and pc.checkBox(self.oscarTagsCb, value=True, q=True):
            self.tags = getAllTags()
        elif pc.checkBox(self.modTagsCb, value=True, q=True) and not pc.checkBox(self.oscarTagsCb, value=True, q=True):
            self.tags = getTags()
        elif not pc.checkBox(self.modTagsCb, value=True, q=True) and pc.checkBox(self.oscarTagsCb, value=True, q=True):
            self.tags = getOSCARTags()

        childeElements = pc.frameLayout(self.frame, q=True, childArray=True)
        if childeElements:
            pc.deleteUI(childeElements)
        for tag, objects in self.tags.items():
            pc.rowLayout(numberOfColumns=5, parent=self.frame)
            pc.button( label='Select "{0}"'.format(tag), command=partial(self.selectClicked, tag))
            pc.button( label='Remove "{0}" tag on selection'.format(tag), command=partial(self.removeTagClick, tag))
            pc.button( label='Select all no ' + tag, command=partial(self.selectButCurrentTag, tag))
            pc.button( label='Select all but ' + tag, command=partial(self.selectAllButCurrentTag, tag))

    def selectClicked(self, tag, *args):
        getModifier = pc.getModifiers()
        multiSelect = False
        if getModifier == 1:
            multiSelect = True
        pc.select(self.tags[tag], add = multiSelect)
        
    def loadClick(self, *args):
        choosenFile = pc.fileDialog2(caption="Select your tags file", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=1)

        if choosenFile != None and len(choosenFile) > 0:
            loadTags(choosenFile[0], inApply=True)
            self.updateUI()
        else:
            pc.warning("No file selected !")

    def saveClick(self, *args):
        choosenFile = pc.fileDialog2(caption="Save your tags file", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=0)

        if choosenFile != None and len(choosenFile) > 0:
            saveTags(getTags(), choosenFile[0])
        else:
            pc.warning("No file selected !")

    def addTagClick(self, *args):
        addTags(inTags=args[0])
        self.updateUI()

    def addCustomTagClick(self, *args):
        addTags(inTags=pc.textFieldGrp(args[0], query=True, text=True))
        self.updateUI()

    def removeTagClick(self, *args):
        removeTags(inTags=args[0])
        self.updateUI()

    def selectButCurrentTag(self, tag, *args):
        pc.select(allButCurrentTag(tag, self.tags))
    
    def selectAllButCurrentTag(self, tag, *args):
        pc.select(allButCurrentTag(tag, self.tags, exclusif=True))
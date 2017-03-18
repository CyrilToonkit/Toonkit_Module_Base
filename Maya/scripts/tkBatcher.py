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
Maya scene batcher
"""

import subprocess
import os
import re

import pymel.core as pc
import maya.cmds as mc

import tkMayaCore as tkc
import tkProjects.tkContext as tkContext

__author__ = "Cyril GIBAUD - Toonkit"

RESULTS = {}

def doBatch(inBatchName, inPath, inCode, inSimulate=False, inForce=False, inSaveFile=False, inSavePath=""):
    dirname, filename = os.path.split(os.path.abspath(inPath))
    rawFilename = os.path.splitext(filename)[0]

    lastStatus = None
    logDir = os.path.join(dirname, rawFilename + "_Batches")
    logFile = os.path.join(logDir, inBatchName + ".ko")

    if not os.path.isdir(logDir) and not inSimulate:
        os.mkdir(logDir)
    else:
        if os.path.isfile(os.path.join(logDir, inBatchName + ".ko")):
            lastStatus = False
            os.remove(os.path.join(logDir, inBatchName + ".ko"))
        if os.path.isfile(os.path.join(logDir, inBatchName + ".ok")):
            lastStatus = True
            if inForce:
                os.remove(os.path.join(logDir, inBatchName + ".ok"))

    code = "import maya.cmds\r\n"
    code += "def batcherDoBatch(fileName, filePath, saveFilePath=ur\""+inSavePath+"\", saveFile="+str(inSaveFile)+", success=True, pathVariables="+str(RESULTS[inPath])+"):\r\n"
    code += "    print 'Batch "+inBatchName+" begins'\r\n"
    code += "    try:\r\n"
    code += "        maya.cmds.file(filePath, open=True, force=True)\r\n"
    code += "\r\n".join(["        " + line.rstrip("\r") for line in inCode.split("\n")]) + "\r\n"
    code += "    except Exception, e:\r\n"
    code += "        print 'Exception  : '+str(e)\r\n"
    code += "        success = False\r\n"
    code += "    if success and saveFile:\r\n"
    if inSimulate:
        code += "        print 'Simulation : file would have been saved to', saveFilePath\r\n"
    else:
        code += "        print 'saving', saveFilePath\r\n"
        code += "        maya.cmds.file(rename=saveFilePath)\r\n"
        code += "        maya.cmds.file(save=True, force=True)\r\n"
    code += "    if success:\r\n"
    code += "        print 'Success'\r\n"
    code += "    else:\r\n"
    code += "        print 'Failure'\r\n"
    code += "    return success\r\n"

    if not inSimulate:
        code = code.replace("print(", "printBatch(")

        codeLines = code.split("\r\n")

        for i in range(len(codeLines)):
            codeLine = codeLines[i]

            matchObj = re.match(".*print (.+).*", codeLine)
            if matchObj != None:
                """
                print "code\r\n",codeLine
                print "search",matchObj.group(0).lstrip()
                print "replace","printBatch(" + matchObj.group(1) + ")\r"
                """
                codeLines[i] = codeLine.replace(matchObj.group(0).lstrip(), "printBatch(" + matchObj.group(1) + ")")

        code = "\r\n".join(codeLines)
    
        code += "def printBatch(*arguments):\r\n"
        code += "    print(','.join([str(s) for s in arguments]))\r\n"
        code += "    fo = open('"+logFile.replace("\\", "\\\\")+"', 'a')\r\n"
        code += "    for argument in arguments:\r\n"
        code += "        fo.write(argument + '\\r\\n')\r\n"
        code += "    fo.close()\r\n"

        print "code",code

    if lastStatus and not inForce:
        print ""
        print " --- SKIPPED '{0}' on {1}, already executed successfully".format(inBatchName, filename)
        return None

    print ""
    print " --- START {3} '{0}' on {1} ({2}) ---".format(inBatchName, filename, inPath, "Batch" if not inSimulate else "Simulation")
    if lastStatus == None:
        print " - Never executed before"
    else:
        print " - Already executed, with result :", lastStatus
    print ""

    result = tkc.executeCode(code, strlng=1, functionName="batcherDoBatch", args=[rawFilename, inPath])

    if not inSimulate and result:
        os.rename(logFile, logFile.replace(".ko", ".ok"))

    print " --- END {3} '{0}' on {1} ({2})---".format(inBatchName, filename, "SUCCESS" if result else "FAILURE", "Batch" if not inSimulate else "Simulation")

    return result

def collectNodes():
    selOnly = mc.checkBox("batcherSelectionCB", query=True, value=True)

    nodesText = None

    if selOnly:
        nodesText = mc.textScrollList("batcherNodesLB", query=True, selectItem=True)
    else:
        nodesText = mc.textScrollList("batcherNodesLB", query=True, allItems=True)

    return [n.split("(")[1][:-1] for n in nodesText]

def getSavePath(inPattern, filePath, fileName, pathVariables):
    code = "def batcherGetPath(BATCHERVARfilePath, BATCHERVARfileName, BATCHERVARpathVariables):"
    code +="    return " + inPattern.replace("#","BATCHERVAR")
    return tkc.executeCode(code, strlng=1, functionName="batcherGetPath", args=[filePath, fileName, pathVariables])

def batcherSimClick(*args):
    batchName = mc.textField("batcherNameLE", query=True, text=True)
    nodes = collectNodes()
    code = mc.textField("batcherCodeLE", query=True, text=True)
    force = not mc.checkBox("batcherSkipCB", query=True, value=True)
    savefile = mc.checkBox("batcherSaveByDefaultCB", query=True, value=True)
    
    mc.control("batcherProgressBar", edit=True, visible=True)

    mc.progressBar( "batcherProgressBar",
    edit=True,
    beginProgress=True,
    isInterruptable=True,
    status="Executing " + batchName,
    maxValue=len(nodes))

    for node in nodes:
        variables = RESULTS[node]
        dirname, filename = os.path.split(os.path.abspath(node))
        savefilePath = getSavePath(mc.textField("batcherSavepathLE", query=True, text=True), node, filename.split(".")[0], variables)

        doBatch(batchName, node, code, True, force, savefile, savefilePath)
        pc.progressBar("batcherProgressBar", edit=True, step=1)

    mc.progressBar("batcherProgressBar", edit=True, endProgress=True)
    mc.control("batcherProgressBar", edit=True, visible=False)

def batcherDoBatchClick(*args):
    batchName = mc.textField("batcherNameLE", query=True, text=True)
    nodes = collectNodes()
    code = mc.textField("batcherCodeLE", query=True, text=True)
    force = not mc.checkBox("batcherSkipCB", query=True, value=True)
    savefile = mc.checkBox("batcherSaveByDefaultCB", query=True, value=True)

    mc.control("batcherProgressBar", edit=True, visible=True)

    mc.progressBar( "batcherProgressBar",
    edit=True,
    beginProgress=True,
    isInterruptable=True,
    status="Executing " + batchName,
    maxValue=len(nodes))

    successes = []
    failures = []
    skips = []

    for node in nodes:
        variables = RESULTS[node]
        dirname, filename = os.path.split(os.path.abspath(node))
        savefilePath = getSavePath(mc.textField("batcherSavepathLE", query=True, text=True), node, filename.split(".")[0], variables)

        result = doBatch(batchName, node, code, False, force, savefile, savefilePath)
        if result == None:
            skips.append(node)
        elif result:
            successes.append(node)
        else:
            failures.append(node)

        pc.progressBar("batcherProgressBar", edit=True, step=1)

    mc.progressBar("batcherProgressBar", edit=True, endProgress=True)
    mc.control("batcherProgressBar", edit=True, visible=False)

    print "{0} failed, {1} succeeded, {2} skipped".format(len(failures), len(successes), len(skips))
    if len(failures) > 0:
        print "failed : " + ",".join(failures)
    if len(successes) > 0:
        print "succeeded : " + ",".join(successes)
    if len(skips) > 0:
        print "skipped : " + ",".join(skips)

def batcherOpenClick(*args):
    dirname, filename = os.path.split(os.path.abspath(__file__))
    rawFilename = os.path.splitext(filename)[0]

    startingDirectory = os.path.join(dirname, rawFilename + "_Batches")

    pyFilePath = mc.fileDialog2(caption="Select a .py batch file", fileFilter="Python (*.py)(*.py)", startingDirectory=startingDirectory, dialogStyle=2, fileMode=1)
    if pyFilePath == None:
        return

    content = ""

    with open(pyFilePath[0]) as pyFile:
        content = pyFile.read()

    dirname, filename = os.path.split(os.path.abspath(pyFilePath[0]))

    mc.textField("batcherNameLE", edit=True, text=filename.split(".")[0])
    mc.textField("batcherCodeInputLE", edit=True, text=content)

def batcherSelectSuccessClick(*args):
    batchName = mc.textField("batcherNameLE", query=True, text=True)
    nodesText = mc.textScrollList("batcherNodesLB", query=True, allItems=True)

    success = []

    for nodeText in nodesText:
        path = nodeText.split("(")[1][:-1]
        dirname, filename = os.path.split(path)
        rawFilename = os.path.splitext(filename)[0]

        if os.path.isfile(os.path.join(dirname, rawFilename + "_Batches", batchName + ".ok")):
            success.append(nodeText)

    mc.textScrollList("batcherNodesLB", edit=True, deselectAll=True)

    if len(success) > 0:
        mc.textScrollList("batcherNodesLB", edit=True, selectItem=success)

def batcherSelectFailureClick(*args):
    batchName = mc.textField("batcherNameLE", query=True, text=True)
    nodesText = mc.textScrollList("batcherNodesLB", query=True, allItems=True)

    failure = []

    for nodeText in nodesText:
        path = nodeText.split("(")[1][:-1]
        dirname, filename = os.path.split(path)
        rawFilename = os.path.splitext(filename)[0]

        if os.path.isfile(os.path.join(dirname, rawFilename + "_Batches", batchName + ".ko")):
            failure.append(nodeText)

    mc.textScrollList("batcherNodesLB", edit=True, deselectAll=True)

    if len(failure) > 0:
        mc.textScrollList("batcherNodesLB", edit=True, selectItem=failure)

def batcherSelectNoneClick(*args):
    batchName = mc.textField("batcherNameLE", query=True, text=True)
    nodesText = mc.textScrollList("batcherNodesLB", query=True, allItems=True)

    none = []

    for nodeText in nodesText:
        path = nodeText.split("(")[1][:-1]
        dirname, filename = os.path.split(path)
        rawFilename = os.path.splitext(filename)[0]

        if not os.path.isfile(os.path.join(dirname, rawFilename + "_Batches", batchName + ".ok")) and not os.path.isfile(os.path.join(dirname, rawFilename + "_Batches", batchName + ".ko")):
            none.append(nodeText)

    mc.textScrollList("batcherNodesLB", edit=True, deselectAll=True)

    if len(none) > 0:
        mc.textScrollList("batcherNodesLB", edit=True, selectItem=none)

def batcherOpenSelectedClick(*args):
    nodesText = mc.textScrollList("batcherNodesLB", query=True, selectItem=True)
    if nodesText != None and len(nodesText) > 0:
        path = nodesText[0].split("(")[1][:-1]
        mc.file(path, open=True, force=True)

def batcherExploreSelectedClick(*args):
    nodesText = mc.textScrollList("batcherNodesLB", query=True, selectItem=True)
    if nodesText != None and len(nodesText) > 0:
        path = nodesText[0].split("(")[1][:-1]
        subprocess.Popen(r'explorer /select,"'+path+'"')

def connectControls():
    #mc.textField("batcherPathLE", edit=True, cc=initUI)
    mc.button("batcherRefreshPathBT", edit=True, c=initUI)
    
    mc.button("batcherSimBT", edit=True, c=batcherSimClick)
    mc.button("batcherDoBatchBT", edit=True, c=batcherDoBatchClick)
    mc.button("batcherOpenBT", edit=True, c=batcherOpenClick)

    mc.button("batcherSelectSuccessBT", edit=True, c=batcherSelectSuccessClick)
    mc.button("batcherSelectFailureBT", edit=True, c=batcherSelectFailureClick)
    mc.button("batcherSelectNoneBT", edit=True, c=batcherSelectNoneClick)

    mc.button("batcherOpenSelectedCB", edit=True, c=batcherOpenSelectedClick)
    mc.button("batcherExploreSelectedCB", edit=True, c=batcherExploreSelectedClick)

def initUI(*args):
    global RESULTS
    mc.textScrollList("batcherNodesLB", edit=True, removeAll=True)
    RESULTS = {}

    results = tkContext.collectPath(pc.textField("batcherPathLE", query=True, text=True))
    for result in results:
        fullPath = result[0]
        folderName,fileName = os.path.split(fullPath)
        RESULTS[fullPath] = result[1]
        pc.textScrollList("batcherNodesLB", edit=True, append="{0} ({1})".format(fileName, fullPath))

def showUI(*args):
    if (mc.window('tkBatcherUI', q=True, exists=True)):
        mc.deleteUI('tkBatcherUI')

    dirname, filename = os.path.split(os.path.abspath(__file__))
    ui = mc.loadUI(uiFile=dirname + "\\UI\\tkNodesBatcher.ui")
    mc.showWindow(ui)

    connectControls()

    initUI()

    mc.textField("batcherCodeLE", edit=True, visible=False)
    mc.control("batcherProgressBar", edit=True, visible=False)
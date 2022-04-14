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
import tempfile

import pymel.core as pc
import maya.cmds as mc

import tkMayaCore as tkc
import locationModule
import Toonkit_Core.tkProjects.tkContext as tkContext
from Toonkit_Core.tkToolOptions.tkOptions import Options

__author__ = "Cyril GIBAUD - Toonkit"

RESULTS = {}

def doBatch(inBatchName, inPath, inCode, inSimulate=False, inForce=False, inSaveFile=False, inSavePath="", inVariables=None, inLogDirPath=None, inLoadRefs=True):

    if inVariables is None:
        inVariables = RESULTS[inPath]

    dirname, filename = os.path.split(os.path.abspath(inPath))
    rawFilename = os.path.splitext(filename)[0]

    lastStatus = None

    logFilePath = os.path.join(inLogDirPath, inBatchName + ".ko")

    if not os.path.isdir(inLogDirPath) and not inSimulate:
        os.mkdir(inLogDirPath)
    else:
        if os.path.isfile(os.path.join(inLogDirPath, inBatchName + ".ko")):
            lastStatus = False
            os.remove(os.path.join(inLogDirPath, inBatchName + ".ko"))
        if os.path.isfile(os.path.join(inLogDirPath, inBatchName + ".ok")):
            lastStatus = True
            if inForce:
                os.remove(os.path.join(inLogDirPath, inBatchName + ".ok"))

    loadRefsSentence = ", loadReferenceDepth='none'" if not inLoadRefs else ""

    code = "import maya.cmds\r\n"
    code += "def batcherDoBatch(fileName, filePath, saveFilePath=r\""+inSavePath+"\", saveFile="+str(inSaveFile)+", success=True, pathVariables="+str(inVariables)+"):\r\n"
    code += "    print ('Batch "+inBatchName+" begins')\r\n"
    code += "    try:\r\n"
    code += "        maya.cmds.file(filePath, open=True"+loadRefsSentence+", force=True, prompt=False)\r\n"
    code += "\r\n".join(["        " + line.rstrip("\r") for line in inCode.split("\n")]) + "\r\n"
    code += "    except Exception as e:\r\n"
    code += "        print ('Exception  : '+str(e))\r\n"
    code += "        success = False\r\n"
    code += "    if success and saveFile:\r\n"
    if inSimulate:
        code += "        print ('Simulation : file would have been saved to', saveFilePath)\r\n"
    else:
        code += "        print ('saving', saveFilePath)\r\n"
        code += "        maya.cmds.file(rename=saveFilePath)\r\n"
        code += "        maya.cmds.file(save=True, force=True)\r\n"
    code += "    if success:\r\n"
    code += "        print ('Success')\r\n"
    code += "    else:\r\n"
    code += "        print ('Failure')\r\n"
    code += "    return success\r\n"

    if not inSimulate:
        code = code.replace("print(", "printBatch(")

        codeLines = code.split("\r\n")

        for i in range(len(codeLines)):
            codeLine = codeLines[i]

            matchObj = re.match(".*print (.+).*", codeLine)
            if matchObj != None:
                """
                print ("code\r\n",codeLine)
                print ("search",matchObj.group(0).lstrip())
                print ("replace","printBatch(" + matchObj.group(1) + ")\r")
                """
                codeLines[i] = codeLine.replace(matchObj.group(0).lstrip(), "printBatch(" + matchObj.group(1) + ")")

        code = "\r\n".join(codeLines)
    
        code += "def printBatch(*arguments):\r\n"
        code += "    print (','.join([str(s) for s in arguments]))\r\n"
        code += "    fo = open('"+logFilePath.replace("\\", "\\\\")+"', 'a')\r\n"
        code += "    for argument in arguments:\r\n"
        code += "        fo.write(argument + '\\r\\n')\r\n"
        code += "    fo.close()\r\n"


    if lastStatus and not inForce:
        print ("")
        print (" --- SKIPPED '{0}' on {1}, already executed successfully".format(inBatchName, filename))
        return None

    print ("")
    print (" --- START {3} '{0}' on {1} ({2}) ---".format(inBatchName, filename, inPath, "Batch" if not inSimulate else "Simulation"))
    if lastStatus == None:
        print (" - Never executed before")
    else:
        print (" - Already executed, with result :", lastStatus)
    print ("")

    result = tkc.executeCode(code, strlng=1, functionName="batcherDoBatch", args=[rawFilename, inPath])

    if not inSimulate and result:
        os.rename(logFilePath, logFilePath.replace(".ko", ".ok"))

    print (" --- END {3} '{0}' on {1} ({2})---".format(inBatchName, filename, "SUCCESS" if result else "FAILURE", "Batch" if not inSimulate else "Simulation"))

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
    code = "import os\r\n"
    code += "def batcherGetPath(BATCHERVARfilePath, BATCHERVARfileName, BATCHERVARpathVariables):\r\n"
    code +="    return " + inPattern.replace("#","BATCHERVAR")
    return tkc.executeCode(code, strlng=1, functionName="batcherGetPath", args=[filePath, fileName, pathVariables])

def getLogPath(inPattern, filePath, fileName, pathVariables):
    code = "import os\r\n"
    code += "def batcherGetPath(BATCHERVARfilePath, BATCHERVARfileName, BATCHERVARpathVariables):\r\n"
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
        savefilePath = getSavePath(mc.textField("batcherSavepathLE", query=True, text=True), node, os.path.splitext(filename)[0], variables)
        logFilePath = getLogPath(mc.textField("batcherLogSavepathLE", query=True, text=True), node, os.path.splitext(filename)[0], variables)
        loadRefs = mc.checkBox("batcherLoadReferencesCB", query=True, value=True)

        doBatch(batchName, node, code, True, force, savefile, savefilePath, variables, logFilePath, loadRefs)
        pc.progressBar("batcherProgressBar", edit=True, step=1)

    mc.progressBar("batcherProgressBar", edit=True, endProgress=True)
    mc.control("batcherProgressBar", edit=True, visible=False)

def batcherDoBatchClick(*args):
    batchName = mc.textField("batcherNameLE", query=True, text=True)
    nodes = collectNodes()
    code = mc.textField("batcherCodeLE", query=True, text=True)
    force = not mc.checkBox("batcherSkipCB", query=True, value=True)
    savefile = mc.checkBox("batcherSaveByDefaultCB", query=True, value=True)
    savePath = mc.textField("batcherSavepathLE", query=True, text=True)
    logPath = mc.textField("batcherLogSavepathLE", query=True, text=True)
    loadRefs = mc.checkBox("batcherLoadReferencesCB", query=True, value=True)

    batcherDoBatches(nodes, RESULTS, batchName, code, force, savefile, savePath, logPath, "batcherProgressBar", 0, loadRefs)

def batcherDoMayaBatchClick(*args):
    batchName = mc.textField("batcherNameLE", query=True, text=True)
    nodes = collectNodes()
    code = mc.textField("batcherCodeLE", query=True, text=True)
    force = not mc.checkBox("batcherSkipCB", query=True, value=True)
    savefile = mc.checkBox("batcherSaveByDefaultCB", query=True, value=True)
    savePath = mc.textField("batcherSavepathLE", query=True, text=True)
    logPath = mc.textField("batcherLogSavepathLE", query=True, text=True)
    loadRefs = mc.checkBox("batcherLoadReferencesCB", query=True, value=True)

    batcherDoBatches(nodes, RESULTS, batchName, code, force, savefile, savePath, logPath, "batcherProgressBar", 1, loadRefs)

def batcherDoBatches(nodes, variables, batchName, code, force, savefile, savePath, logPath, inProgressBar=None, inMode=0, inLoadRefs=True):
    if inProgressBar is not None:
        mc.control(inProgressBar, edit=True, visible=True)

        mc.progressBar( inProgressBar,
        edit=True,
        beginProgress=True,
        isInterruptable=True,
        status="Executing " + batchName,
        maxValue=len(nodes))

    successes = []
    failures = []
    skips = []

    for node in nodes:
        thisVariables = variables[node]
        dirname, filename = os.path.split(os.path.abspath(node))
        savefilePath = getSavePath(savePath, node, os.path.splitext(filename)[0], thisVariables)
        logFilePath = getLogPath(logPath, node, os.path.splitext(filename)[0], thisVariables)
        result = None

        if inMode == 0:
            result = doBatch(batchName, node, code, False, force, savefile, savefilePath, thisVariables, logFilePath, inLoadRefs)
        else:
            #Save the variables we need to options
            optionsDic = {
                "batchName":batchName,
                "node":node,
                "code":code,
                "simulate":False,
                "force":force,
                "saveFile":savefile,
                "savefilePath":savefilePath,
                "variables":thisVariables,
                "logpath":logFilePath
                }

            tmpFile = tempfile.NamedTemporaryFile(prefix='tkBatcher',suffix='.json', delete=False)
            tmpFileName = tmpFile.name

            try:
                Options(optionsDic).save(tmpFile)

                coreOptions = tkc.getTool().options

                #Call mayabatch tkBatcherDo.py tmpFile.name
                scriptPath = os.path.join(locationModule.OscarModuleLocation(), "tkBatcherDo.py")

                cmdLine = "\"{0}\" {1} {2}".format(coreOptions["mayabatchpath"], scriptPath, tmpFile.name)
                p = subprocess.Popen(cmdLine, shell=True, stdout = subprocess.PIPE)
                stdout, stderr = p.communicate()
                result = "Toonkit mayabatcher : result True" in stdout
                #print "p.returncode",p.returncode
                #print "stdout",stdout
                #print "stderr",stderr
            except Exception as e:
                print ("Error : Can't execute batch : {0} ({1})".format(batchName, e) )
            finally:
                os.remove(tmpFileName)

        if result == None:
            skips.append(node)
        elif result:
            successes.append(node)
        else:
            failures.append(node)

        if inProgressBar is not None:
            pc.progressBar(inProgressBar, edit=True, step=1)

    if inProgressBar is not None:
        mc.progressBar(inProgressBar, edit=True, endProgress=True)
        mc.control(inProgressBar, edit=True, visible=False)

    print ("{0} failed, {1} succeeded, {2} skipped".format(len(failures), len(successes), len(skips)))
    if len(failures) > 0:
        print ("failed : " + ",".join(failures))
    if len(successes) > 0:
        print ("succeeded : " + ",".join(successes))
    if len(skips) > 0:
        print ("skipped : " + ",".join(skips))

def batcherSaveClick(*args):
    oldPath = mc.textField("batcherFilePathLE", query=True, text=True)
    dirname, filename = os.path.split(oldPath)

    startingDirectory = dirname

    pyFilePath = mc.fileDialog2(caption="Save a .py batch file", fileFilter="Python (*.py)(*.py)", startingDirectory=oldPath, dialogStyle=1, fileMode=0)
    if pyFilePath == None:
        return

    with open(pyFilePath[0], "w") as pyFile:
        pyFile.write(mc.textField("batcherCodeLE", query=True, text=True))
    
    dirname, filename = os.path.split(pyFilePath[0])

    optionsPath = os.path.join(dirname, filename.replace(".py",".json"))

    options = Options()
    options["path"] = mc.textField("batcherPathLE", query=True, text=True)
    options["selection"] = mc.checkBox("batcherSelectionCB", query=True, value=True)
    options["saveByDefault"] = mc.checkBox("batcherSaveByDefaultCB", query=True, value=True)
    options["savePath"] = mc.textField("batcherSavepathLE", query=True, text=True)
    options["skip"] = mc.checkBox("batcherSkipCB", query=True, value=True)
    options["logSavePath"] = mc.textField("batcherLogSavepathLE", query=True, text=True)
    options["loadRefs"] = mc.checkBox("batcherLoadReferencesCB", query=True, value=True)

    options.save(optionsPath)

    mc.textField("batcherNameLE", edit=True, text=os.path.splitext(filename)[0])
    mc.textField("batcherFilePathLE", edit=True, text=pyFilePath[0])

def batcherInit(inPath):
    content = ""

    with open(inPath) as pyFile:
        content = pyFile.read()

    dirname, filename = os.path.split(os.path.abspath(inPath))

    mc.textField("batcherNameLE", edit=True, text=os.path.splitext(filename)[0])
    mc.textField("batcherCodeInputLE", edit=True, text=content)
    mc.textField("batcherFilePathLE", edit=True, text=inPath)

    optionsPath = os.path.join(dirname, filename.replace(".py",".json"))
    if os.path.isfile(optionsPath):
        options = Options(inPath=optionsPath)
        mc.textField("batcherPathLE", edit=True, text=options["path"])
        mc.checkBox("batcherSelectionCB", edit=True, value=options["selection"])
        mc.checkBox("batcherSaveByDefaultCB", edit=True, value=options["saveByDefault"])
        mc.textField("batcherSavepathLE", edit=True, text=options["savePath"])
        mc.checkBox("batcherSkipCB", edit=True, value=options["skip"])
        mc.textField("batcherLogSavepathLE", edit=True, text=options["logSavePath"])
        if "loadRefs" in options:
            mc.checkBox("batcherLoadReferencesCB", edit=True, value=options["loadRefs"])

    initUI()

def batcherOpenClick(*args):
    oldPath = mc.textField("batcherFilePathLE", query=True, text=True)
    dirname, filename = os.path.split(oldPath)

    startingDirectory = dirname

    pyFilePath = mc.fileDialog2(caption="Select a .py batch file", fileFilter="Python (*.py)(*.py)", startingDirectory=startingDirectory, dialogStyle=1, fileMode=1)
    if pyFilePath == None or len(pyFilePath) == 0:
        return

    batcherInit(pyFilePath[0])

def batcherSelectSuccessClick(*args):
    batchName = mc.textField("batcherNameLE", query=True, text=True)
    nodesText = mc.textScrollList("batcherNodesLB", query=True, allItems=True)

    success = []

    for nodeText in nodesText:
        path = nodeText.split("(")[1][:-1]
        dirname, filename = os.path.split(path)
        logDirPath = getLogPath(mc.textField("batcherLogSavepathLE", query=True, text=True), path, os.path.splitext(filename)[0], RESULTS[path])
        logFilePath = os.path.join(logDirPath, mc.textField("batcherNameLE", query=True, text=True) + ".ok")

        if os.path.isfile(logFilePath):
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
        logDirPath = getLogPath(mc.textField("batcherLogSavepathLE", query=True, text=True), path, os.path.splitext(filename)[0], RESULTS[path])
        logFilePath = os.path.join(logDirPath, mc.textField("batcherNameLE", query=True, text=True) + ".ko")

        if os.path.isfile(logFilePath):
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
        logDirPath = getLogPath(mc.textField("batcherLogSavepathLE", query=True, text=True), path, os.path.splitext(filename)[0], RESULTS[path])
        logFilePathRoot = os.path.join(logDirPath, mc.textField("batcherNameLE", query=True, text=True))
        logFilePath = logFilePathRoot + ".ok"
        logFilePath2 = logFilePathRoot + ".ko"

        if not os.path.isfile(logFilePath) and not os.path.isfile(logFilePath2):
            none.append(nodeText)

    mc.textScrollList("batcherNodesLB", edit=True, deselectAll=True)

    if len(none) > 0:
        mc.textScrollList("batcherNodesLB", edit=True, selectItem=none)

def batcherOpenSelectedClick(*args):
    nodesText = mc.textScrollList("batcherNodesLB", query=True, selectItem=True)
    if nodesText != None and len(nodesText) > 0:
        path = nodesText[0].split("(")[1][:-1]
        mc.file(path, open=True, force=True)

def batcherImportSelectedClick(*args):
    nodesText = mc.textScrollList("batcherNodesLB", query=True, selectItem=True)
    if nodesText != None and len(nodesText) > 0:
        for nodeText in nodesText:
            path = nodeText.split("(")[1][:-1]
            mc.file(path, i=True, force=True)

def batcherReferenceSelectedClick(*args):
    nodesText = mc.textScrollList("batcherNodesLB", query=True, selectItem=True)
    if nodesText != None and len(nodesText) > 0:
        for nodeText in nodesText:
            path = nodeText.split("(")[1][:-1]
            pc.system.createReference(path, namespace=os.path.splitext(os.path.basename(path))[0])

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

def batcherExportFilesClick(*args):
    if RESULTS is None or len(RESULTS) == 0:
        pc.warning("No results yet !")
        return

    choosenFile = mc.fileDialog2(caption="Export you file list", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=0)

    if choosenFile != None and len(choosenFile) > 0:
        choosenFile = choosenFile[0]

        with open(choosenFile, "w") as f:
            f.write("\r\n".join([pc.textField("batcherPathLE", query=True, text=True)] + RESULTS.keys()))

def batcherImportFilesClick(*args):
    choosenFile = mc.fileDialog2(caption="Select your file list", fileFilter="text file (*.txt)(*.txt)", dialogStyle=1, fileMode=1)

    if choosenFile != None and len(choosenFile) > 0:
        global RESULTS
        mc.textScrollList("batcherNodesLB", edit=True, removeAll=True)
        RESULTS = {}

        choosenFile = choosenFile[0]

        content = None

        with open(choosenFile) as f:
            content = f.readlines()

        if not content is None and len(content) > 0:
            pattern=None
            if "{" in content[0]:
                pattern = content.pop(0).rstrip("\r\n")
            pc.textField("batcherPathLE", edit=True, text=pattern or "{filePath}")

            for line in content:
                fullPath = line.rstrip("\r\n")
                folderName,fileName = os.path.split(fullPath)

                variables = {}
                if pattern is None:
                    RESULTS[fullPath] = {"filePath":fullPath}
                    pc.textScrollList("batcherNodesLB", edit=True, append="{0} ({1})".format(fileName, fullPath))
                elif(tkContext.match(pattern, fullPath, inVariables=variables)):
                    RESULTS[fullPath] = variables

def connectControls():
    #mc.textField("batcherPathLE", edit=True, cc=initUI)
    mc.button("batcherRefreshPathBT", edit=True, c=initUI)
    
    mc.button("batcherSimBT", edit=True, c=batcherSimClick)
    mc.button("batcherDoBatchBT", edit=True, c=batcherDoBatchClick)
    mc.button("batcherDoMayaBatchBT", edit=True, c=batcherDoMayaBatchClick)
    mc.button("batcherOpenBT", edit=True, c=batcherOpenClick)
    mc.button("batcherSaveBT", edit=True, c=batcherSaveClick)
    mc.button("batcherSelectSuccessBT", edit=True, c=batcherSelectSuccessClick)
    mc.button("batcherSelectFailureBT", edit=True, c=batcherSelectFailureClick)
    mc.button("batcherSelectNoneBT", edit=True, c=batcherSelectNoneClick)

    mc.button("batcherOpenSelectedCB", edit=True, c=batcherOpenSelectedClick)
    mc.button("batcherImportSelectedBT", edit=True, c=batcherImportSelectedClick)
    mc.button("batcherReferenceSelectedBT", edit=True, c=batcherReferenceSelectedClick)
    mc.button("batcherExploreSelectedCB", edit=True, c=batcherExploreSelectedClick)

    mc.button("batcherExportFilesBT", edit=True, c=batcherExportFilesClick)
    mc.button("batcherImportFilesBT", edit=True, c=batcherImportFilesClick)

    

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

def showUI(inPath=None):
    if (mc.window('tkBatcherUI', q=True, exists=True)):
        mc.deleteUI('tkBatcherUI')

    dirname, filename = os.path.split(os.path.abspath(__file__))
    ui = mc.loadUI(uiFile=dirname + "\\UI\\tkNodesBatcher.ui")
    mc.showWindow(ui)

    connectControls()

    initUI()

    mc.textField("batcherCodeLE", edit=True, visible=False)
    mc.control("batcherProgressBar", edit=True, visible=False)

    if not inPath is None:
        batcherInit(inPath)

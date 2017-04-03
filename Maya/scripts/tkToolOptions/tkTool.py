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
import os
from functools import partial

import pymel.core as pc

import locationModule
from functools import partial
from tkOptions import Options 

__author__ = "Cyril GIBAUD - Toonkit"

DEBUG_PREFIX = "DEBUG"
WARNING_PREFIX = "WARNING"

class Tool(object):
    """
    Base class for tools, encapsulating tkOptions instance
    """

    def __init__(self, inName="newTool", inDescription="", inUsage="", inVersion="0.0.0.0", inContext=None, inDebug=False, inOptions=Options()):
        self.name = inName
        self.description = inDescription
        self.usage = inUsage
        self.version = inVersion
        self.context = inContext
        self.debug = inDebug
        self.opts = inOptions

        self.arguments = []

    def getFullName(self):
        return "{0} v{1}".format(self.name, self.version)

    #####################################################
    #                 LOGGING                           #
    #####################################################

    def log(self, *args, **kwargs):
        inPrefix = ""
        if "inPrefix" in kwargs:
            inPrefix = kwargs["inPrefix"]

        print ((inPrefix + " ") if len(inPrefix) > 0 else "") + "{0} : {1}".format(self.name, " ".join([str(arg) for arg in args]))

    def logDebug(self, *args):
        if not self.debug:
            return

        self.log(*args, inPrefix=DEBUG_PREFIX)

    def warning(self, *args, **kwargs):
        self.log(*args, inPrefix=WARNING_PREFIX)

    #####################################################
    #                 OPTIONS                           #
    #####################################################

    def getOptionsPath(self):
        return os.path.abspath(os.path.join(locationModule.get(), os.pardir, os.pardir, "Preferences", "{0}.json".format(self.name)))

    def saveOptions(self):
        if self.opts.path is None:
            self.opts.path = self.getOptionsPath()

        return self.opts.save()

    def loadOptions(self):
        if self.opts.path is None:
            self.opts.path = self.getOptionsPath()

        return self.opts.load()

    def defaultOptions(self):
        for option in self.opts.options:
            self.opts[option.name] = option.defaultValue
            


    #####################################################
    #                 EXECUTION                         #
    #####################################################

    def getArguments(self, *args, **kwargs):
        defaults = [v if not k in kwargs else kwargs[k] for k, v in self.opts.iteritems()]
        for i in range(len(args)):
            if len(defaults) > i:
                defaults[i] = args[i]

        return defaults

    def executeUI(self, *args):
        self.execute()

    def execute(self, *args, **kwargs):
        self.arguments = self.getArguments(*args, **kwargs)
        self.logDebug("Executing {0} ({1})".format(self.getFullName(), ",".join([str(obj) for obj in self.arguments])))

    #####################################################
    #                 UI                                #
    #####################################################
    def getWindowName(self):
        return "{0}UI".format(self.name)

    def checkBoxValueChanged(self, inControlName, inOptionName, uiArg):
        self.opts[inOptionName] = pc.checkBox(inControlName, query=True, value=True)

    def createOptionItem(self, inOption):
        if inOption.type == "bool":
            return pc.checkBox(inOption.name, label=inOption.niceName, value=self.opts[inOption.name], cc=partial(self.checkBoxValueChanged, inOption.name, inOption.name))
        else:
            self.warning("Option {0} have unmanaged type {1}, no item created !".format(inOption.name, inOption.type))

    def saveOptionsUI(self, *args):
        self.saveOptions()

    def defaultOptionsUI(self, *args):
        self.defaultOptions()

    def buildWindow(self, inExecutable=True):
        uiName = self.getWindowName()
        if pc.control(uiName, query=True, exists=True):
            pc.deleteUI(uiName, control=True)

        uiName = pc.window(uiName, title=self.getFullName())

        colLayout = pc.columnLayout()

        if len(self.description) > 0:
            pc.text(label=self.description)

        if len(self.usage) > 0:
            pc.text(label=self.usage)

        for option in self.opts.options:
            self.createOptionItem(option)

        pc.rowLayout(numberOfColumns=3 if inExecutable else 2)
        if inExecutable:
            pc.button(label='Apply', c=self.executeUI)
        pc.button(label='Save options', c=self.saveOptionsUI)
        pc.button(label='Default options', c=self.defaultOptionsUI)

        return uiName

    def showPrefs(self, *args):
        window = self.buildWindow(False)
        pc.showWindow(window)

    def showUI(self, *args):
        window = self.buildWindow(True)
        pc.showWindow(window)
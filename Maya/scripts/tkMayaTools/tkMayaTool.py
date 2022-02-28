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
import six
basestring = six.string_types

import Toonkit_Core.tkToolOptions.tkTool as tkTool
from Toonkit_Core.tkToolOptions.tkOptions import Options
from Toonkit_Core.tkToolOptions.tkTool import Tool

import locationModule
import pymel.core as pc

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.0.0.0"

def addShelfButton(inLabel, inCode, inDCode=None, inImage=None, inShelf=None):
    if inShelf is None:
        inShelf = pc.mel.eval("$currentShelf = `tabLayout -q -st $gShelfTopLevel`")

    if inImage is None:
        inImage = "pythonFamily.png"

    pc.setParent(inShelf)

    pc.shelfButton(label=inLabel, imageOverlayLabel=inLabel, command=inCode, dcc=inDCode, image=inImage)
    pc.mel.eval("shelfTabRefresh")

class MayaTool(Tool):
    def log(self, *args, **kwargs):
        if kwargs.get("inPrefix") == tkTool.WARNING_PREFIX :
            pc.warning(tkTool.WARNING_PREFIX + " {0} : {1}".format(self.name, " ".join([str(arg) for arg in args])))
            return

        super(MayaTool, self).log(*args, **kwargs)

    #####################################################
    #                 OPTIONS                           #
    #####################################################

    def getOptionsPath(self):
        return os.path.abspath(os.path.join(locationModule.get(), os.pardir, os.pardir, "Preferences", "{0}.json".format(type(self).__name__)))

    #####################################################
    #                 EXECUTION                         #
    #####################################################

    def getExecuteCode(self, *args):
        arguments = self.getArguments(*args)

        strArgumentsLst = []

        for argument in arguments:
            strArgumentsLst.append("'{0}'".format(argument) if isinstance(argument, basestring) else str(argument))

        className = self.__class__.__name__
        return "tkc.getTool().getChildTool('{0}').execute({1})".format(className, ",".join(strArgumentsLst))

    def getShowUICode(self, *args):
        className = self.__class__.__name__
        return "tkc.getTool().getChildTool('{0}').showUI()".format(className)

    def addToShelf(self, *args):
        className = self.__class__.__name__

        code = self.getExecuteCode(*args)

        addShelfButton(self.name, self.getExecuteCode(*args), self.getShowUICode(*args))

    #####################################################
    #                 UI                                #
    #####################################################

    def checkBoxValueChanged(self, inControlName, inOptionName, uiArg):
        self.options[inOptionName] = pc.checkBox(inControlName, query=True, value=True)

    def textValueChanged(self, inControlName, inOptionName, uiArg):
        self.options[inOptionName] = pc.textFieldGrp(inControlName, query=True, text=True)

    def intValueChanged(self, inControlName, inOptionName, uiArg):
        self.options[inOptionName] = pc.intSliderGrp(inControlName, query=True, value=True)
        
    def floatValueChanged(self, inControlName, inOptionName, uiArg):
        self.options[inOptionName] = pc.floatSliderGrp(inControlName, query=True, value=True)

    def setOptionItem(self, inOption):
        if inOption.type == "bool":
            return pc.checkBox(inOption.name, edit=True, value=self.options[inOption.name])
        elif inOption.type == "str":
            return pc.textFieldGrp(inOption.name, edit=True, text=self.options[inOption.name])
        elif inOption.type == "int":
            return pc.intSliderGrp(inOption.name, edit=True, value=self.options[inOption.name])
        elif inOption.type == "float":
            return pc.floatSliderGrp(inOption.name, edit=True, value=self.options[inOption.name])
        else:
            self.warning("Option {0} have unmanaged type {1}, no item set !".format(inOption.name, inOption.type))

    def createOptionItem(self, inOption):
        if inOption.type == "bool":
            return pc.checkBox(inOption.name, label=inOption.niceName, value=self.options[inOption.name], cc=partial(self.checkBoxValueChanged, inOption.name, inOption.name))
        elif inOption.type == "str":
            return pc.textFieldGrp(inOption.name, label=inOption.niceName, text=self.options[inOption.name], columnAlign=[1, "left"], adjustableColumn=2, cc=partial(self.textValueChanged, inOption.name, inOption.name) )
        elif inOption.type == "int":
            return pc.intSliderGrp(inOption.name, label=inOption.niceName, field=True, value=self.options[inOption.name], minValue=inOption.min, maxValue=inOption.max, fieldMinValue=-1000000, fieldMaxValue=1000000, columnAlign=[1, "left"], adjustableColumn=3, cc=partial(self.intValueChanged, inOption.name, inOption.name) )
        elif inOption.type == "float":
            return pc.floatSliderGrp(inOption.name, label=inOption.niceName, field=True, value=self.options[inOption.name], minValue=inOption.min, maxValue=inOption.max, fieldMinValue=-1000000.0, fieldMaxValue=1000000.0, pre = 3, columnAlign=[1, "left"], adjustableColumn=3, cc=partial(self.floatValueChanged, inOption.name, inOption.name) )
        else:
            self.warning("Option {0} have unmanaged type {1}, no item created !".format(inOption.name, inOption.type))

    def buildWindow(self, inExecutable=True):
        uiName = self.getWindowName()
        if pc.control(uiName, query=True, exists=True):
            pc.deleteUI(uiName, control=True)

        uiName = pc.window(uiName, title=self.getFullName())

        colLayout = pc.columnLayout(adjustableColumn=True)

        if len(self.description) > 0:
            pc.text(label=self.description, align="left")

        if len(self.usage) > 0:
            pc.text(label=self.usage, align="left")

        categorizedOptions = self.getCategorizedOptions()

        parentCateg = None
        for categ, options in categorizedOptions.items():

            if len(categorizedOptions) > 1:
                categ = tkTool.DEFAULT_CATEGORY if not categ else categ
                if "." in categ:
                    categs = categ.split(".")
                    if categs[-2] != parentCateg:
                        pc.setParent(colLayout)
                        pc.frameLayout( label=categs[-2], collapsable=True)
                        parentCateg = categs[-2]
                    pc.text(label=" - "+categs[-1], align="left")
                    pc.rowLayout(numberOfColumns=len(options))
                else:
                    pc.frameLayout( label=categ, collapsable=True)

            for option in options:
                self.createOptionItem(option)
            pc.setParent("..")

        pc.setParent(colLayout)

        pc.rowLayout(numberOfColumns=4 if inExecutable else 2)
        if inExecutable:
            pc.button(label='Apply', c=self.executeUI)
        pc.button(label='Save options', c=self.saveOptionsUI)
        pc.button(label='Default options', c=self.defaultOptionsUI)
        if inExecutable:
            pc.button(label='Add to shelf', c=self.addToShelf)
        return uiName

    def showPrefs(self, *args):
        window = self.buildWindow(False)
        pc.showWindow(window)

    def showUI(self, *args):
        window = self.buildWindow(True)
        pc.showWindow(window)
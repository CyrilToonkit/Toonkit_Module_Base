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

from tkOptions import Options
from tkMayaTool import MayaTool as Tool

import pymel.core as pc
import tkNodeling as tkn

__author__ = "Cyril GIBAUD - Toonkit"

VERSIONINFO = "1.0.0.0"

class ExpressionsToNodes(Tool):
    def __init__(self, inContext=None, inDebug=False):
        super(ExpressionsToNodes, self).__init__(inName="Expressions to nodes", inDescription="Convert expressions to utility nodes",
            inUsage="Type an arbitrary expression or select one or more expressions to convert", inVersion=VERSIONINFO, inContext=inContext, inDebug=inDebug, inOptions=None)

        self.options = Options(inPath=self.getOptionsPath())
        self.options.addOption("Expression", "", "Expression to evaluate", "Expression")
        self.options.addOption("RemoveUnused", True, "Remove unused nodes after graphing", "RemoveUnused")

        if not self.options.isSaved():
            self.saveOptions()

    def execute(self, *args, **kwargs):
        super(ExpressionsToNodes, self).execute(*args, **kwargs)

        expressions = [node for node in pc.ls(sl=True) if node.type() == "expression"]
        if len(expressions) > 0:
            for expr in expressions:
                exprName = expr.name()
                exprString = expr.getString()
                nodes = tkn.convertExpression(expr, self.arguments[1])[0]
                allNodes = []
                for curNodes in nodes:
                    allNodes.extend(nodes)

                self.log("Expression '{0}' ({1}) converted to :\n[{2}]".format(exprName, exprString.replace(os.linesep, ""),
                                ",".join(["'{0}'".format(n.name()) for n in allNodes])))
        else:
            if self.arguments[0] != "":
                nodes = tkn.compileNodes(self.arguments[0], self.arguments[1])
                self.log("Expression '{0}' converted to :\n[{1}]".format(self.arguments[0],
                                ",".join(["'{0}'".format(n.name()) for n in nodes])))
            else:
                self.warning("Please type an arbitrary expression or select one or more expressions to convert !")
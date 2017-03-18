"""
------------------------- LICENCE INFORMATION -------------------------------
    This file is part of Toonkit Module Lite, Python Maya library and module.
    Authors : Cyril GIBAUD - Toonkit, Stephane Bonnot - Parallel Dev
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
Python helper to manage external python files in maya 
"""

import sys
import os

__author__ = "Cyril GIBAUD - Toonkit, Stephane Bonnot - Parallel Dev"

def execpythonfile(fullpath):
	"""
	Executes a python file out of maya script path by adding file path to sys.path
	based on tweaks by Ryan Trowbridge 
	fullpath must be given ( ex: c:/MyCode/MyFile.py )
	"""
	dir = os.path.dirname(fullpath)
	# Check if the file dirrectory already exists in the sys.path array
	paths = sys.path
	pathfound = 0
	if dir in paths:
		pathfound = 1
		#print dir + " already in sys.path..."
	# If the dirrectory is not part of sys.path add it
	if not pathfound:
		#print dir + " added to sys.path !!"
		sys.path.append(dir)
	fileName = os.path.splitext(os.path.basename(fullpath))[0]
	if not fileName in globals():
		exec('import ' + fileName) in globals()
	else:
		exec('reload( ' + fileName + ' )') in globals()

	if not pathfound:
		sys.path.remove(dir)

#execpythonfile("Z:/Toonkit/RnD/Src/GitRepo/oscar/src/Python/Oscar/LaunchMayaServer.py")
import os
import sys

currentPath = os.path.dirname(__file__)
if not os.path.exists(currentPath):
    raise IOError("The source path '"+currentPath+"' does not exist!")
    
if currentPath not in sys.path:
    sys.path.insert(0, currentPath)
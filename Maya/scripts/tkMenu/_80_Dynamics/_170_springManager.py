import subprocess
import locationModule
import os

path = locationModule.OscarModuleLocation()
#we arrived in "Scripts" folder, go up one step
path = os.path.join(os.path.split(path)[:-1][0])
path = os.path.join(path, "Standalones", "SpringManager", "SpringManager.exe")

subprocess.Popen(path)
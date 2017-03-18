import pymel.core as pc
import os
import subprocess

def get():
    items=[]
    subMenuItems = []
    files = pc.optionVar(query="RecentFilesList")
    if isinstance(files, list):
        for item in files:
            baseName = os.path.dirname(item)
            if not baseName in items:
                items.append(baseName)
                subMenuItems.append((baseName, baseName))

    return subMenuItems

def do(inItem):
    subprocess.Popen(r'explorer /select,"'+inItem.replace("/","\\")+'"')
import pymel.core as pc
import os
import subprocess

def get():
    items=[]
    subMenuItems = []
    files = pc.optionVar(query="RecentFilesList")
    if isinstance(files, list):
        for item in files:
            items.append(item)
            subMenuItems.append((item, item))

    return subMenuItems

def do(inItem):
    subprocess.Popen(r'explorer /select,"'+inItem.replace("/","\\")+'"')
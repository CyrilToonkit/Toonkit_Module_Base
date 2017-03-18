import pymel.core as pc
import os

def get():
    subMenuItems = []
    files = pc.optionVar(query="RecentFilesList")
    if isinstance(files, list):
        for item in files:
            subMenuItems.append((item, item))

    return subMenuItems

def do(inItem):
    pc.system.importFile(inItem, namespace=os.path.splitext(os.path.basename(inItem))[0])
    #pc.system.createReference(inItem)
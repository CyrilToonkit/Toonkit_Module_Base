"""
Import pose from ".txt" file saved with "Export Pose" feature
"""
import tkRig
import pymel.core as pc

result = pc.promptDialog(
        title="Import Pose",
        message="If you want to change destination namespace, give it here",
        text="",
        button=['OK', 'Remove old', 'Cancel'],
        defaultButton='OK',
        cancelButton='Cancel',
        dismissString='Cancel')
if result == 'OK' or result == 'Remove old':
    namespace = None
    if result == 'OK':
        namespace = pc.promptDialog(query=True, text=True)
        if len(namespace) == 0:
            namespace = None
    else:
        namespace = ""

    tkRig.importSimplePose(inNs=namespace)
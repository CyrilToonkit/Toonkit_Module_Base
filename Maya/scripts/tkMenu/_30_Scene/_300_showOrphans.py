import pymel.core as pc
import tkOutfits

def getLongestName(inNode):
    return inNode.fullPath() if isinstance(inNode, pc.nodetypes.DagNode) else inNode.name()

orphans = tkOutfits.getLayerOrphanMeshes("*:layer_*")
if len(orphans) > 0:
    message = 'Some geometries are visible by default, but are not present in any layer :\r\n' + "\r\n".join([orphan.name() for orphan in orphans]) + "\r\n See log for object list !"
    rslt = pc.confirmDialog( title='Geometries not present in any layer', message=message, button=['OK'], defaultButton='OK', cancelButton='OK', dismissString='OK' )
    pc.select(orphans, replace=True)
    print "\r\n" + message + "\r\n"
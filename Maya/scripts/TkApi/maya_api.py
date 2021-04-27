import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma


def get_api_nodes(names, dag_path=True):
    api_nodes = []
    for name in names:
        sellist = om.MGlobal.getSelectionListByName( name )

        if dag_path:
            api_nodes.append(sellist.getDagPath(0))
        else:
            api_nodes.append(sellist.getDependNode(0))
    return api_nodes

def get_deformer_set_components(names):

    skin_node = oma.MFnSkinCluster(get_api_nodes([names], dag_path=False)[0])
    meshNode = skin_node.getOutputGeometry()[0]
    meshVerItFn = om.MItMeshVertex(meshNode)
    indices = range(meshVerItFn.count())

    singleIdComp = om.MFnSingleIndexedComponent()
    vertexComp = singleIdComp.create(om.MFn.kMeshVertComponent)
    singleIdComp.addElements( indices )

    return vertexComp


def get_components_from_selection_list(inInfSel):
    inf_components = inInfSel.getComponent(0)[1]
    return inf_components


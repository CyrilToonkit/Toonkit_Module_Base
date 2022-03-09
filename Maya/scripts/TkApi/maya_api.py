import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.cmds as cmds


def get_api_nodes(names, dag_path=True):
    api_nodes = []
    if not isinstance(names, list):
        names = [names]
        
    for name in names:
        sellist = om.MGlobal.getSelectionListByName( name )

        if dag_path:
            api_nodes.append(sellist.getDagPath(0))
        else:
            api_nodes.append(sellist.getDependNode(0))
    return api_nodes

def get_deformer_set_components(names):
    skin_node = oma.MFnSkinCluster(get_api_nodes(names, False)[0])
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

def get_weights_data(inTransformNode = None, inSkinCluster=None, inInfluence = None):
    """
        Method  that returns the skin data from the given skinCluster deformer. It uses API2.0 to retrieve the weighs.
        It will return the classic linear weights for all the influences, the dual quaternion weights and a list of
        influences (str) in the logical order.
        Args:
            inSkinCLuster: (str) String name of skinCluster Node
            inTransformNode: (str) String name of the transform node of a deformed object

        Returns: (orderedDictionary) orderedDictionary with all the influences, the classic linear weights for all of
        them and the dual quaternion weights
    """
    # Argument base conditions
    if inTransformNode is None:
        inTransformNode = cmds.ls(sl=True, ap=True)
        if len(inTransformNode) > 0:
            inTransformNode = inTransformNode[0]
            if cmds.objectType(inTransformNode) != "transform":
                inTransformNode = None
            else:
                inSkinCluster = [x for x in cmds.listHistory(inTransformNode) if cmds.objectType(x) == "skinCluster"][0]
        else:
            inTransformNode = None
    if inSkinCluster is None:
        if inTransformNode is None:
            inSkinCluster = cmds.ls(sl=True, ap=True)
            if len(inSkinCluster) > 0:
                inSkinCluster = inSkinCluster[0]
                if cmds.objectType(inSkinCluster) != "skinCluster":
                    inSkinCluster = None
                else:
                    inTransformNode = cmds.skinCluster(inSkinCluster, q=1, g=1)[0]
        else:
            inSkinCluster = [x for x in cmds.listHistory(inTransformNode) if cmds.objectType(x) == "skinCluster"][0]
    elif inTransformNode is None and inSkinCluster is not None:
        inTransformNode = cmds.skinCluster(inSkinCluster, q=1, g=1)[0]
    if inTransformNode is None and inSkinCluster is None:
        raise TypeError ("You must give at least a transform node or a skinCluster node !")
    

    
    skinNode = oma.MFnSkinCluster(get_api_nodes(inSkinCluster, False)[0])
    # components = get_deformer_set_components(inSkinCluster)
    components = om.MObject()
    transformDagPath = get_api_nodes(inTransformNode)[0]
    
    skinData = {}
    infObjs = [inf.partialPathName() for inf in skinNode.influenceObjects()]
    if inInfluence:
        if not isinstance(inInfluence, int):
            inInfluenceIndex = infObjs.index(inInfluence)
        skinData["influences"] = [inInfluence]
        skinData["classic_linear"] = skinNode.getWeights(transformDagPath ,components, inInfluenceIndex)
        #skinData["dual_quaternion"] = []
    elif inInfluence is None:
        skinData["influences"] = [inf.partialPathName() for inf in skinNode.influenceObjects()]
        skinData['classic_linear'] = skinNode.getWeights(transformDagPath, components)[0]
        #skinData['dual_quaternion'] = skinNode.getBlendWeights(transformDagPath, components)

    return skinData

def getPointPositions(inObjectName, worldSpace = False):
        pointsPositions = []
        if worldSpace:
            Mspace = om.MSpace.kWorld
        else:
            Mspace = om.MSpace.kObject
        
        targetDagPath = get_api_nodes(inObjectName)[0]
        targetDagPathShape = targetDagPath.extendToShape()
        if targetDagPath.apiType() == 296: # 269 is the id of kMesh object from maya api
            target_mPointArray = om.MFnMesh(targetDagPathShape).getFloatPoints(Mspace)
        elif targetDagPath.apiType() == 294: # 294 is the id of kNurbsSurface object from maya api
            target_mPointArray = om.MFnNurbsSurface(targetDagPathShape).cvPositions(Mspace)
        elif targetDagPath.apiType() == 267: # 267 is the id of kNurbsCurve object from maya api
            target_mPointArray = om.MFnNurbsCurve(targetDagPathShape).cvPositions(Mspace)

        for poses in target_mPointArray:
            pointsPositions.append((poses[0], poses[1], poses[2]))
        return pointsPositions
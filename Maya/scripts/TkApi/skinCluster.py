import maya.api.OpenMaya as om
import maya.api.OpenMayaAnim as oma
import maya.cmds as cmds
import maya_api as maya_api
import collections

class Deformer(object):
    def __init__(self, name, deformed_shape, *args, **kwargs):
        self.name = name
        self.deformed_shape = deformed_shape

class SkinCluster(Deformer):
    def __init__(self, *args, **kwargs):
        super(SkinCluster, self).__init__(*args, **kwargs)

    @property
    def weights(self):
        """
        Property  that returns the skin data from the given skinCluster deformer. It uses API2.0 to retrieve the weighs.
        It will return the classic linear weights for all the influences, the dual quaternion weights and a list of
        influences (str) in the logical order.

        Returns: (orderedDictionary) orderedDictionary with all the influences, the classic linear weights for all of
        them and the dual quaternion weights

        """
        skin_node = oma.MFnSkinCluster(maya_api.get_api_nodes([self.name], dag_path=False)[0])
        mesh_dag_path = maya_api.get_api_nodes([self.deformed_shape])[0]
        components = maya_api.get_deformer_set_components(self.name)

        skin_data = collections.OrderedDict()
        skin_data['influences'] = [inf.partialPathName() for inf in skin_node.influenceObjects()]
        skin_data['classic_linear'] = skin_node.getWeights(mesh_dag_path, components)[0]
        skin_data['dual_quaternion'] = skin_node.getBlendWeights(mesh_dag_path, components)

        return skin_data
    
    def set_weights(self, classic_linear=False, dual_quaternion=False, weight_list=None, influence=None,
                    influence_weight=None):
        """
        Method that set weights using Maya API 2.0. It will set weights depending on the arguments passed. Passing an
        influence and its influence weight, works like a flood values on that influence.
        Args:
            classic_linear: (Bool) If True if will assign the weights as classic linear
            dual_quaternion: (Bool) If True will assign the weights as dual quaternion
            weight_list: (list) Weights to be assigned
            influence: (str) Name of the influence
            influence_weight: (float) Value to assign to the influence vertices for the passed influence.

        Returns:

        """
        mesh_geo = cmds.skinCluster(self.name, q=1, g=1)
        skin_node = oma.MFnSkinCluster(maya_api.get_api_nodes([self.name], dag_path=False)[0])
        mesh_dag_path = maya_api.get_api_nodes(mesh_geo)[0]
        components = maya_api.get_deformer_set_components(self.name)

        if weight_list is not None:
            weight_list = om.MDoubleArray(weight_list)

        if classic_linear:
            influence_indices = om.MIntArray([i for i in range(len(skin_node.influenceObjects()))])
            skin_node.setWeights(mesh_dag_path, components, influence_indices, weight_list)
        if dual_quaternion:
            skin_node.setBlendWeights(mesh_dag_path, components, weight_list)
        if influence is not None:
            inf_index = [i for i, inf in enumerate(skin_node.influenceObjects()) if inf.partialPathName() == influence][
                0]
            inf_sel = skin_node.getPointsAffectedByInfluence(maya_api.get_api_nodes([influence])[0])
            inf_components = maya_api.get_components_from_selection_list(inf_sel[0])
            skin_node.setWeights(mesh_dag_path, inf_components, inf_index, influence_weight)

    @property
    def influences(self):
        """
        Property that returns the influence objects of the skinCLuster in logical order
        Returns: (list)

        """
        skin_node = oma.MFnSkinCluster(maya_api.get_api_nodes([self.name], dag_path=False)[0])
        return [inf.partialPathName() for inf in skin_node.influenceObjects()]

    @property
    def classic_linear_weights(self):
        """
        Returns a list with the classic linear weights of the skinCluster for all the influences
        Returns: (list)

        """
        return self.weights['classic_linear']

    @property
    def dual_quaternion(self):
        """
        Returns a list with the dual quaternion weights
        Returns: (list)

        """
        return self.weights['dual_quaternion']

    def get_influence_weights(self, influence=None):
        """
        Method that allos the user to get the classic linear weights of a specific influence
        Args:
            influence: (str) Influence name

        Returns: (list) weights for that influence

        """
        if influence is not None:
            mesh_geo = cmds.skinCluster(self.name, q=1, g=1)
            skin_node = oma.MFnSkinCluster(maya_api.get_api_nodes([self.name], dag_path=False)[0])
            mesh_dag_path = maya_api.get_api_nodes(mesh_geo)[0]
            components = maya_api.get_deformer_set_components(self.name)
            inf_index = [i for i, inf in enumerate(skin_node.influenceObjects()) if inf.partialPathName() == influence]
            return list(skin_node.getWeights(mesh_dag_path, components, inf_index[0]))

    def swap_influences(self, inf1=None, inf2=None):
        """
        Method that allows the user to swap the weights between influences.
        Args:
            inf1: (str) Name of a skin influence
            inf2: (str) Name of a skin influence

        Returns: (bool) False if any of the influences is None or True if the action is performed correctly

        """

        if inf1 is None or inf2 is None:
            return False

        mesh_geo = cmds.skinCluster(self.name, q=1, g=1)
        skin_node = oma.MFnSkinCluster(maya_api.get_api_nodes([self.name], dag_path=False)[0])
        mesh_dag_path = maya_api.get_api_nodes(mesh_geo)[0]
        components = maya_api.get_deformer_set_components(self.name)
        all_weights = skin_node.getWeights(mesh_dag_path, components)[0]
        influences = [inf.partialPathName() for inf in skin_node.influenceObjects()]

        inf1_index = [i for i, inf in enumerate(skin_node.influenceObjects()) if inf.partialPathName() == inf1][0]
        inf1_weights = skin_node.getWeights(mesh_dag_path, components, inf1_index)

        inf2_index = [i for i, inf in enumerate(skin_node.influenceObjects()) if inf.partialPathName() == inf2][0]
        inf2_weights = skin_node.getWeights(mesh_dag_path, components, inf2_index)

        vtx_per_inf = len(all_weights) / len(influences)

        for i in range(vtx_per_inf):
            all_weights[(i * len(influences)) + inf1_index] = inf2_weights[i]
            all_weights[(i * len(influences)) + inf2_index] = inf1_weights[i]

        self.set_weights(classic_linear=True, weight_list=all_weights)
        return True

    def combine_influences(self, target_influence=None, source_influences=None):
        """
        Method that combines influences into one.
        Args:
            target_influence: (str) Skin influence where all the weights are going to be added
            source_influences: (str) Skin influences to merge into the target influence

        Returns: (bool) True if the action is performed correctly

        """

        if isinstance(source_influences, str):
            source_influences = [source_influences]

        mesh_geo = cmds.skinCluster(self.name, q=1, g=1)
        skin_node = oma.MFnSkinCluster(maya_api.get_api_nodes([self.name], dag_path=False)[0])
        mesh_dag_path = maya_api.get_api_nodes(mesh_geo)[0]
        components = maya_api.get_deformer_set_components(self.name)

        all_weights = skin_node.getWeights(mesh_dag_path, components)[0]
        influences = [inf.partialPathName() for inf in skin_node.influenceObjects()]
        vtx_per_inf = len(all_weights) / len(influences)

        target_index = \
            [i for i, inf in enumerate(skin_node.influenceObjects()) if inf.partialPathName() == target_influence][0]
        target_weights = weights.Weights(skin_node.getWeights(mesh_dag_path, components, target_index))

        combined_indices = list()
        for source_influence in source_influences:
            inf_index = \
                [i for i, inf in enumerate(skin_node.influenceObjects()) if inf.partialPathName() == source_influence][
                    0]
            inf_weights = skin_node.getWeights(mesh_dag_path, components, inf_index)
            target_weights = weights.Weights(target_weights.__add__(list(inf_weights)))
            combined_indices.append(inf_index)
        for i in range(vtx_per_inf):
            all_weights[(i * len(influences)) + target_index] = target_weights[i]
            for ci in combined_indices:
                all_weights[(i * len(influences)) + ci] = 0.0

        self.set_weights(classic_linear=True, weight_list=all_weights)
        return True

    def copy_vertex_weight_to_vertices(self, source_vertex=None, target_vertices=None):
        """
        Method that copy the influence values from a given vertex into a list of vertices
        Args:
            source_vertex: (int) Vertex index to copy the weights from
            target_vertices: (int or list) Vertices indices to paste the weights

        Returns: (bool)

        """
        if isinstance(source_vertex, int):
            source_vertex = [source_vertex]

        if isinstance(target_vertices, int):
            target_vertices = [target_vertices]
        else:
            cmds.error('Source vertex argument is not an int')
            return False

        mesh_geo = cmds.skinCluster(self.name, q=1, g=1)
        skin_node = oma.MFnSkinCluster(maya_api.get_api_nodes([self.name], dag_path=False)[0])
        mesh_dag_path = maya_api.get_api_nodes(mesh_geo)[0]
        components = maya_api.get_deformer_set_components(self.name)

        all_weights = skin_node.getWeights(mesh_dag_path, components)[0]

        all_influences = skin_node.influenceObjects()

        weights_matrix = list()
        for i, inf in enumerate(all_influences):
            weights_matrix.append(list(skin_node.getWeights(mesh_dag_path, components, i)))

        for source in source_vertex:
            vtx_weights = list()
            for i in range(len(all_influences)):
                vtx_weights.append(weights_matrix[i][source])

            for j in range(len(all_influences)):
                for target in target_vertices:
                    weights_matrix[j][target] = vtx_weights[j]

        vtx_per_inf = (len(all_weights) / len(all_influences))
        weight_list = list()

        for j in range(vtx_per_inf):
            for x in range(len(all_influences)):
                weight_list.append(weights_matrix[x][j])

        self.set_weights(classic_linear=True, weight_list=weight_list)
        return True

    def get_vertex_weights(self, vertices=None):
        """
        Method that returns the weights per vertex
        Args:
            vertices: (int or list) Vertices indices to retrieve from the weights

        Returns: (tuple (orderedDictionary, list)) Returns a tuple with the vertex and weights as an orderedDictionary
         and a list of the influences in logical order

        """
        if isinstance(vertices, int):
            vertices = [vertices]

        if not isinstance(vertices, list):
            cmds.error('Vertices argument needs to be an int or a list')
            return False

        vertices_data = collections.OrderedDict()

        mesh_geo = cmds.skinCluster(self.name, q=1, g=1)
        skin_node = oma.MFnSkinCluster(maya_api.get_api_nodes([self.name], dag_path=False)[0])
        mesh_dag_path = maya_api.get_api_nodes(mesh_geo)[0]
        components = maya_api.get_deformer_set_components(self.name)

        all_influences = skin_node.influenceObjects()

        weights_matrix = list()
        for i, inf in enumerate(all_influences):
            weights_matrix.append(list(skin_node.getWeights(mesh_dag_path, components, i)))

        for vtx in vertices:
            vtx_weights = list()
            for i in range(len(all_influences)):
                vtx_weights.append(weights_matrix[i][vtx])
            vertices_data[vtx] = vtx_weights

        return (vertices_data, all_influences)

    def set_vertex_weights(self, vertices=None, vertices_weights=None):
        """
        Method that assign vertex weights to some determined vertices.
        Args:
            vertices: (int or list) vertices indices. If None, it will use all the vertex passed in te vertices_weights
            data.
            vertices_weights: (tuple (orderedDictionary, list)) a tuple with the vertex and weights as an
            orderedDictionary and a list of the influences in logical order

        Returns: (bool)

        """
        target_vertices = None
        if isinstance(vertices, int):
            target_vertices = [vertices]
        if isinstance(vertices, list):
            target_vertices = vertices
        if vertices is None:
            target_vertices = vertices_weights[0].keys()

        if not isinstance(target_vertices, list):
            cmds.error('Vertices argument needs to be an int, list, or None to evaluate the vertices_weights stored data')
            return False

        mesh_geo = cmds.skinCluster(self.name, q=1, g=1)
        skin_node = oma.MFnSkinCluster(maya_api.get_api_nodes([self.name], dag_path=False)[0])
        mesh_dag_path = maya_api.get_api_nodes(mesh_geo)[0]
        components = maya_api.get_deformer_set_components(self.name)
        all_weights = skin_node.getWeights(mesh_dag_path, components)[0]
        all_influences = skin_node.influenceObjects()

        skn_inf_names = [inf.partialPathName() for inf in skin_node.influenceObjects()]
        data_inf_names = [inf.partialPathName() for inf in vertices_weights[1]]

        weights_matrix = list()
        for i, inf in enumerate(all_influences):
            weights_matrix.append(list(skin_node.getWeights(mesh_dag_path, components, i)))

        for i in range(len(all_influences)):
            for target in target_vertices:
                if target not in vertices_weights[0].keys():
                    cmds.warning('Vertex {} data not found. Can not set this vertex weights.'.format(target))
                else:
                    vtx_weights = vertices_weights[0][target]
                    weights_matrix[i][target] = vtx_weights[data_inf_names.index(skn_inf_names[i])]

        vtx_per_inf = (len(all_weights) / len(all_influences))
        weight_list = list()

        for j in range(vtx_per_inf):
            for x in range(len(all_influences)):
                weight_list.append(weights_matrix[x][j])

        self.set_weights(classic_linear=True, weight_list=weight_list)
        return True

from GraphInterface import GraphInterface
from Node import Node


class DiGraph(GraphInterface):
    """This class implement GraphInterface abstract class that represents an interface of a graph."""

    def __init__(self, **kwargs):
        """
        Each DiGraph contain dictionary of his nodes, and each node contain his edges.
        In addition each DiGraph holds the number of edges in the graph and a mode counter (mc)
        that represent the number of changes (add node, add edge, remove node or remove edge) in the graph.
        """
        self.nodes = dict()
        self.__mc = 0
        self.__num_of_edges = 0

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        :return: The number of vertices in this graph
        """
        return len(self.nodes.keys())

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        :return: The number of edges in this graph
        """
        return self.__num_of_edges

    def get_all_v(self) -> dict:
        """
        Return a dictionary of all the nodes in the Graph,
        each node is represented using a pair (node_id, Node).
        :return: dictionary of all the nodes in the Graph
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        Return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (key, edge weight)
        :return: return a dictionary of all the nodes connected to (into) node_id
        """
        if self.nodes.get(id1) is None:
            raise Exception('Node {} is not exist in the graph'.format(id1))
        return self.nodes.get(id1).get_connections_in()

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        Return a dictionary of all the nodes connected from node_id ,
        each node is represented using a pair (key, edge weight)
        :return: return a dictionary of all the nodes connected from node_id
        """
        if self.nodes.get(id1) is None:
            raise Exception('Node {} is not exist in the graph'.format(id1))
        return self.nodes.get(id1).get_connections_out()

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC increased.
        :return: The current version of this graph.
        """
        return self.__mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        :param: id1: The start node of the edge
        :param: id2: The end node of the edge
        :param: weight: The weight of the edge (positive weight)
        :return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists, the method simply does nothing
        Note2: If the weight is not positive the method raises an exception
        """
        if self.nodes.get(id1) is None or self.nodes.get(id2) is None:
            return False
        if id2 in self.get_node(id1).get_connections_out().keys():
            return False
        if weight < 0:
            raise Exception('Edge weight must be positive')
        if id1 == id2:
            return False
        self.nodes.get(id1).add_neighbor_out(id2, weight)
        self.nodes.get(id2).add_neighbor_in(id1, weight)
        self.__mc += 1
        self.__num_of_edges += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        :param: node_id: The node ID
        :param: pos: The position of the node
        :return: True if the node was added successfully, False o.w.
        Note: if the node id already exists, the method simply does nothing
        """
        if node_id in self.nodes:
            return False
        n = Node(node_id, pos)
        self.nodes[node_id] = n
        self.__mc += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        If there are edges that go in or out from this node, they will also be removed.
        :param: node_id: The node ID
        :return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists, the method simply does nothing
        """
        if node_id not in self.nodes.keys():
            return False
        removed_node = self.nodes[node_id]
        keys = ()
        for x in removed_node.get_connections_out().keys():
            keys += (x,)
        [self.remove_edge(node_id, x) for x in keys]
        keys = ()
        for x in removed_node.get_connections_in().keys():
            keys += (x,)
        [self.remove_edge(x, node_id) for x in keys]
        del self.nodes[node_id]
        self.__mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        :param: node_id1: The start node of the edge
        :param: node_id2: The end node of the edge
        :return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists, the method simply does nothing
        """
        if self.nodes.get(node_id1) is None or self.nodes.get(node_id2) is None:
            return False
        if node_id2 not in self.nodes.get(node_id1).get_connections_out():
            return False
        del self.nodes.get(node_id1).get_connections_out()[node_id2]
        del self.nodes.get(node_id2).get_connections_in()[node_id1]
        self.__mc += 1
        self.__num_of_edges -= 1
        return True

    def get_node(self, node_id: int) -> Node:
        """
        Return the node by his key (node_id).
        :param node_id: this node key
        :return: the node by his key.
        """
        if node_id not in self.nodes.keys():
            raise Exception('Node {} is not exist in the graph'.format(node_id))
        return self.nodes[node_id]

    def as_dict(self):
        """
        Return the graph as dictionary {"Edges": ...., "Nodes": ....}
        :return: the graph as dictionary
        """
        m_dict = {}
        node_list = []
        edge_list = []
        for k, v in self.nodes.items():
            node_list.append(v.as_dict_node())
            for i in range(len(v.as_dict_edge())):
                edge_list.append(v.as_dict_edge()[i])
        m_dict["Edges"] = edge_list
        m_dict["Nodes"] = node_list

        return m_dict

    def __str__(self) -> str:
        s = ''
        for key, value in self.nodes.items():
            s += str(key) + ' : ' + str(value) + '\n'
        return s

    def __eq__(self, other):
        if self is other:
            return True
        if other is None or self.__class__ is not other.__class__:
            return False
        return self.nodes.__eq__(other.nodes) and self.e_size() == other.e_size()

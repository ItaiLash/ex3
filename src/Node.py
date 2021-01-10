class Node:
    """
    This class represent a node (vertex).
    """

    def __init__(self, k: int = None, loc: tuple = None, **kwargs):
        """
        Each node contain dew fields:
        key: node_id.
        location: node's position represent as 3DPoint.
        ni_out: a dictionary that holds all the "edges" that connected from this node,
        each edge is represented using a pair (key, edge weight).
        ni_in: a dictionary that holds all the "edges" that connected to this node,
        each edge is represented using a pair (key, edge weight)
        """
        self.__key = k
        self.__location = loc
        self.__ni_out = {}
        self.__ni_in = {}

    def add_neighbor_out(self, neighbor_id: int, weight: float) -> None:
        """
        Add "edge" that connected from this node (node_id ---> neighbor_id).
        :param neighbor_id: dest node key
        :param weight: edge's weight
        """
        self.__ni_out[neighbor_id] = weight

    def add_neighbor_in(self, neighbor_id: int, weight: float) -> None:
        """
        Add "edge" that connected to this node (neighbor_id ---> node_id).
        :param neighbor_id: dest node key
        :param weight: edge's weight
        """
        self.__ni_in[neighbor_id] = weight

    def get_connections_out(self) -> dict:
        """
        Return a dictionary that holds all the "edges" that connected from this node,
        each edge is represented using a pair (key, edge weight).
        :return: dictionary (key, edge weight).
        """
        return self.__ni_out

    def get_connections_in(self) -> dict:
        """
        Return a dictionary that holds all the "edges" that connected to this node,
        each edge is represented using a pair (key, edge weight).
        :return: dictionary (key, edge weight).
        """
        return self.__ni_in

    def get_key(self) -> int:
        """
        Return this node key.
        :return: key
        """
        return self.__key

    def get_location(self) -> tuple:
        """
        Return this node location as a 3DPoint (x, y, z).
        :return: this node location
        """
        return self.__location

    def set_location(self, location: tuple) -> None:
        """
        Allows to add location to this node.
        This method used for load and plot graphs that their nodes have no position.
        :param location: the new position of this node
        """
        self.__location = location

    def as_dict_node(self):
        """
        Return the node as dictionary {"pos": "x", "y", "z", "id": key}
        :return: the node as dictionary
        """
        loc_as_str = str(self.get_location())
        m_dict = {"pos": loc_as_str[1:-1], "id": self.get_key()}
        return m_dict

    def as_dict_edge(self):
        """
        Return the edge as dictionary {"src": src node_id, "w": edge weight, "dest": dest node_id}
        :return: the edge as dictionary
        """
        l_list = []
        for k, v in self.get_connections_out().items():
            m_dict = {"src": int(self.get_key()), "w": float(v), "dest": int(k)}
            l_list.append(m_dict)
        return l_list

    def __repr__(self):
        return str([self.get_key()])

    def __str__(self) -> str:
        return "Node: id: " + str(self.__key) + ' neighbors: ' + str(self.__ni_out)

    def __eq__(self, o: object) -> bool:
        if self is o:
            return True
        if o is None or self.__class__ is not o.__class__:
            return False
        other = o
        return self.__key == other.__key and self.__location.__eq__(other.__location) and self.__ni_in.__eq__(
            other.__ni_in) and self.__ni_out.__eq__(other.__ni_out)
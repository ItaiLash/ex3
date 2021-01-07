from GraphInterface import GraphInterface
from Node import Node


class DiGraph(GraphInterface):
    num_of_edges = 0
    mc = 0

    def __init__(self, **kwargs):
        self.nodes = dict()

    def v_size(self) -> int:
        return len(self.nodes.keys())

    def e_size(self) -> int:
        return DiGraph.num_of_edges

    def get_all_v(self) -> dict:
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        if self.nodes.get(id1) is None:
            raise Exception('Node {} is not exist in the graph'.format(id1))
        return self.nodes.get(id1).get_connections_in()

    def all_out_edges_of_node(self, id1: int) -> dict:
        if self.nodes.get(id1) is None:
            raise Exception('Node {} is not exist in the graph'.format(id1))
        return self.nodes.get(id1).get_connections_out()

    def get_mc(self) -> int:
        return DiGraph.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if self.nodes.get(id1) is None or self.nodes.get(id2) is None:
            return False
        self.nodes.get(id1).add_neighbor_out(id2, weight)
        self.nodes.get(id2).add_neighbor_in(id1, weight)
        DiGraph.mc += 1
        DiGraph.num_of_edges +=1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self.nodes:
            return False
        n = Node(node_id, pos)
        self.nodes[node_id] = n
        DiGraph.mc += 1
        return True

    def remove_node(self, node_id: int) -> bool:
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
        DiGraph.mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if self.nodes.get(node_id1) is None or self.nodes.get(node_id2) is None:
            return False
        if node_id2 not in self.nodes.get(node_id1).get_connections_out():
            return False
        del self.nodes.get(node_id1).get_connections_out()[node_id2]
        del self.nodes.get(node_id2).get_connections_in()[node_id1]
        DiGraph.mc += 1
        DiGraph.num_of_edges -= 1
        return True

    def __str__(self) -> str:
        s = ''
        for key, value in self.nodes.items():
            s += str(key) + ' : ' + str(value) + '\n'
        return s

    def as_dict(self):
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


if __name__ == '__main__':

    g = DiGraph()
    g.add_node(0, (1, 1, 1))
    g.add_node(1, (2, 2, 2))
    g.add_node(2, (1, 1, 3))
    g.add_node(3, (1, 1, 4))
    g.add_node(4, (1, 1, 5))
    g.add_edge(0,1,4.5)
    g.add_edge(1,2,2.5)
    g.add_edge(4,0,1.5)
    g.add_node(1,(1,2,3))
    print(g.get_all_v())
    print(g.__str__())
    print(g.e_size())
    print(g.v_size())
    print(g.all_in_edges_of_node(1))
    print(g.all_out_edges_of_node(1))
    print(g.get_mc())
    # g.remove_node(0)
    # g.remove_node(2)
    # g.remove_node(2)
    # g.remove_edge(3,4)
    print(g.__str__())
    print(g.get_mc())
    print('**************************')
    print(g.as_dict())





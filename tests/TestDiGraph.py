from unittest import TestCase
from src.DiGraph import DiGraph
from src.Node import Node


class Test(TestCase):

    def setUp(self):
        # graph creator, |V|=7, |E|=18
        self.graph = DiGraph()
        for i in range(7):
            self.graph.add_node(i)
        self.graph.add_edge(0, 1, 1)
        self.graph.add_edge(0, 2, 1)
        self.graph.add_edge(0, 3, 1)
        self.graph.add_edge(0, 4, 1)
        self.graph.add_edge(0, 5, 1)
        self.graph.add_edge(0, 6, 1)
        self.graph.add_edge(1, 0, 1)
        self.graph.add_edge(1, 2, 1)
        self.graph.add_edge(2, 1, 1)
        self.graph.add_edge(2, 4, 1)
        self.graph.add_edge(3, 4, 1)
        self.graph.add_edge(3, 5, 1)
        self.graph.add_edge(4, 1, 1)
        self.graph.add_edge(4, 2, 1)
        self.graph.add_edge(4, 3, 1)
        self.graph.add_edge(5, 0, 1)
        self.graph.add_edge(5, 2, 1)
        self.graph.add_edge(5, 4, 1)

    def test_v_size(self):
        self.assertEqual(7, self.graph.v_size())
        # add new node
        self.assertTrue(self.graph.add_node(7))
        self.assertEqual(8, self.graph.v_size())
        # add existing node
        self.assertFalse(self.graph.add_node(0))
        self.assertEqual(8, self.graph.v_size())

    def test_e_size(self):
        self.assertEqual(18, self.graph.e_size())
        # add new edge
        self.assertTrue(self.graph.add_edge(6, 5, 1))
        self.assertEqual(19, self.graph.e_size())
        # add edge that already exists in the graph
        self.assertFalse(self.graph.add_edge(0, 1, 1))
        self.assertEqual(19, self.graph.e_size())

    def test_get_all_v(self):
        nodes = {0: Node(0), 1: Node(1), 2: Node(2), 3: Node(3), 4: Node(4), 5: Node(5), 6: Node(6)}
        self.assertEqual(nodes.__repr__(), self.graph.get_all_v().__repr__())

    def test_all_in_edges_of_node(self):
        self.assertEqual({1: 1, 5: 1}, self.graph.all_in_edges_of_node(0))
        self.graph.add_node(7)
        self.assertEqual({}, self.graph.all_in_edges_of_node(7))

        self.assertRaises(Exception, self.graph.all_in_edges_of_node, 10)

    def test_all_out_edges_of_node(self):
        self.assertEqual({1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1}, self.graph.all_out_edges_of_node(0))
        self.assertEqual({0: 1, 2: 1}, self.graph.all_out_edges_of_node(1))
        self.assertEqual({}, self.graph.all_out_edges_of_node(6))

        self.assertRaises(Exception, self.graph.all_in_edges_of_node, 10)

    def test_get_mc(self):
        self.assertEqual(25, self.graph.get_mc())
        # remove node with edges
        self.assertTrue(self.graph.remove_node(0))
        # mc+=9 , remove node: 1, remove edges out of node 0: 5, remove edges in to node 0: 2
        self.assertEqual(34, self.graph.get_mc())

    def test_add_edge(self):
        self.assertEqual(18, self.graph.e_size())
        # add new edge
        self.assertTrue(self.graph.add_edge(6, 5, 1))
        self.assertEqual(19, self.graph.e_size())
        self.assertEqual(26, self.graph.get_mc())
        # add edge that already exists in the graph
        self.assertFalse(self.graph.add_edge(0, 1, 1))
        # add edge between nodes that does not exists in the graph
        self.assertFalse(self.graph.add_edge(0, 10, 1))
        self.assertFalse(self.graph.add_edge(10, 0, 1))
        self.assertFalse(self.graph.add_edge(10, 11, 1))
        self.assertEqual(19, self.graph.e_size())
        self.assertEqual(26, self.graph.get_mc())

    def test_add_node(self):
        self.assertEqual(7, self.graph.v_size())
        # add new node
        self.assertTrue(self.graph.add_node(7))
        self.assertEqual(8, self.graph.v_size())
        self.assertEqual(26, self.graph.get_mc())
        # add existing node
        self.assertFalse(self.graph.add_node(0))
        self.assertEqual(8, self.graph.v_size())
        self.assertEqual(26, self.graph.get_mc())

    def test_remove_node(self):
        self.assertEqual(7, self.graph.v_size())
        # remove node
        self.assertTrue(self.graph.remove_node(6))
        self.assertEqual(6, self.graph.v_size())
        self.assertEqual(27, self.graph.get_mc())
        # remove node that does not exists in the graph
        self.assertFalse(self.graph.remove_node(10))
        self.assertEqual(6, self.graph.v_size())
        self.assertEqual(27, self.graph.get_mc())

    def test_remove_edge(self):
        self.assertEqual(18, self.graph.e_size())
        # remove edge
        self.assertTrue(self.graph.remove_edge(1, 2))
        self.assertEqual(17, self.graph.e_size())
        self.assertEqual(26, self.graph.get_mc())
        # remove edge that does not exists in the graph
        self.assertFalse(self.graph.remove_edge(1, 6))
        self.assertEqual(17, self.graph.e_size())
        self.assertEqual(26, self.graph.get_mc())

    def test_get_node(self):
        node_0 = self.graph.nodes.get(0)
        self.assertEqual(node_0, self.graph.get_node(0))
        self.assertRaises(Exception, self.graph.get_node, 10)

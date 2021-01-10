import random
from unittest import TestCase

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
from numpy import inf


class TestGraphAlgo(TestCase):

    def setUp(self):
        self.graph = None
        self.ga = GraphAlgo()

    def test_load_from_json(self):
        self.assertTrue(self.ga.load_from_json("../data/G_10_80_0.json"))
        self.assertTrue(self.ga.load_from_json("../data/G_10_80_1.json"))
        self.assertTrue(self.ga.load_from_json("../data/G_10_80_2.json"))

    def test_save_to_json(self):
        self.ga.load_from_json("../data/G_10_80_0.json")
        self.assertTrue(self.ga.save_to_json("graph1.json"))
        self.ga.load_from_json("../data/G_10_80_1.json")
        self.assertTrue(self.ga.save_to_json("graph2.json"))
        self.ga.load_from_json("../data/G_10_80_2.json")
        self.assertTrue(self.ga.save_to_json("graph3.json"))

    def test_shortest_path(self):
        self.ga.graph = graph_2

        self.assertEqual("(6, [1, 2, 4, 3, 5, 0, 6])", str(self.ga.shortest_path(1, 6)))
        self.assertEqual("(2, [3, 5, 0])", str(self.ga.shortest_path(3, 0)))
        self.assertEqual("(0, [2])", str(self.ga.shortest_path(2, 2)))
        # no path
        no_path = (inf, [])
        self.assertEqual(no_path, self.ga.shortest_path(6, 1))
        # shortest path between nodes that one or more of the nodes does not exist in the graph
        self.assertRaises(Exception, self.ga.shortest_path, (10, 1))
        self.assertRaises(Exception, self.ga.shortest_path, (1, 10))
        self.assertRaises(Exception, self.ga.shortest_path, (9, 10))

    def test_connected_component(self):
        self.ga.graph = graph_3
        for i in range(0, 10):
            for j in range(10):
                if j in range(3):
                    self.assertEqual([2, 1, 0], self.ga.connected_component(j))
                if j in range(3, 5):
                    self.assertEqual([4, 3], self.ga.connected_component(j))
                if j in range(5, 7):
                    self.assertEqual([j], self.ga.connected_component(j))
                if j in range(8, 11):
                    self.assertEqual([8, 9, 7], self.ga.connected_component(j))

    def test_connected_components(self):
        self.ga.graph = graph_2
        self.assertEqual([[1, 2, 4, 3, 5, 0], [6]], self.ga.connected_components())
        self.ga.graph = graph_3
        self.assertEqual([[8, 9, 7], [5], [6], [2, 1, 0], [4, 3]], self.ga.connected_components())

    def test_plot_graph(self):
        # plot graph without positions
        self.ga.graph = graph_2
        self.ga.plot_graph()
        # plot graph with position
        self.ga.graph = graph_3
        self.ga.plot_graph()


# graph creator, |V|=7, |E|=19
graph_2 = DiGraph()
for i in range(7):
    graph_2.add_node(i)
graph_2.add_edge(0, 1, 1)
graph_2.add_edge(0, 2, 1)
graph_2.add_edge(0, 3, 1)
graph_2.add_edge(0, 4, 1)
graph_2.add_edge(0, 5, 1)
graph_2.add_edge(0, 6, 1)
graph_2.add_edge(1, 0, 8)
graph_2.add_edge(1, 2, 1)
graph_2.add_edge(1, 6, 9)
graph_2.add_edge(2, 1, 1)
graph_2.add_edge(2, 4, 1)
graph_2.add_edge(3, 4, 1)
graph_2.add_edge(3, 5, 1)
graph_2.add_edge(4, 1, 1)
graph_2.add_edge(4, 2, 1)
graph_2.add_edge(4, 3, 1)
graph_2.add_edge(5, 0, 1)
graph_2.add_edge(5, 2, 1)
graph_2.add_edge(5, 4, 1)

# graph creator, |V|=10, |E|=12
graph_3 = DiGraph()

graph_3.add_node(0, (2, 14, 0))
graph_3.add_node(1, (3, 11, 0))
graph_3.add_node(2, (4, 12, 0))
graph_3.add_node(3, (2, 8, 0))
graph_3.add_node(4, (1, 6, 0))
graph_3.add_node(5, (5, 8, 0))
graph_3.add_node(6, (7, 8, 0))
graph_3.add_node(7, (1, 3, 0))
graph_3.add_node(8, (3, 4, 0))
graph_3.add_node(9, (2, 1, 0))


graph_3.add_edge(0, 2, 1)
graph_3.add_edge(1, 0, 1)
graph_3.add_edge(2, 1, 1)
graph_3.add_edge(1, 3, 1)
graph_3.add_edge(3, 4, 1)
graph_3.add_edge(4, 3, 1)
graph_3.add_edge(5, 6, 1)
graph_3.add_edge(7, 4, 1)
graph_3.add_edge(7, 8, 1)
graph_3.add_edge(8, 9, 1)
graph_3.add_edge(9, 7, 1)
graph_3.add_edge(9, 8, 1)



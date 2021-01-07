import random
from numpy import inf
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from typing import List
import json
import Node
import networkx as nx
import matplotlib.pyplot as plt


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, digraph: DiGraph = None):
        self.graph = digraph

    def get_graph(self) -> DiGraph:
        return self.graph

    # def load_from_json(self, file_name: str) -> bool:
    #     g = DiGraph()
    #     with open(file_name, "r") as f:
    #         graph_dict = json.load(f)
    #         for k, v in graph_dict.items():
    #             i = 0
    #             args = []
    #             for nodeK,nodeV in v.items():
    #                 if i < 2:
    #                     args.append(nodeV)
    #                 i += 1
    #             g.add_node(*args)
    #         for k, v in graph_dict.items():
    #             for dest, w in v.get("_Node__ni_out").items():
    #                 g.add_edge(int(k), int(dest), w)
    #     self.graph = g

    def load_from_json(self, file_name: str) -> bool:
        g = DiGraph()
        with open(file_name, "r") as f:
            graph_dict = json.load(f)
            for i in graph_dict.get("Nodes"):
                if "pos" in i:
                    pos = ()
                    for d in i.get("pos"):
                        pos.__add__(tuple(d))
                    g.add_node(int(i.get("id")), pos)
                else:
                    x = random.uniform(0, 10)
                    y = random.uniform(0, 10)
                    g.add_node(int(i.get("id")), (x, y, 0))
            for i in graph_dict.get("Edges"):
                g.add_edge(int(i.get("src")), int(i.get("dest")), float(i.get("w")))
        self.graph = g

    def save_to_json(self, file_name: str) -> bool:
        try:
            with open(file_name, "w") as f:
                json.dump(self.graph, default=lambda o: o.as_dict(), indent=4, fp=f)
        except IOError as e:
            print(e)

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if self.graph.nodes.get(id1) is None:
            raise Exception('Node {} is not exist in the graph'.format(id1))
        if self.graph.nodes.get(id2) is None:
            raise Exception('Node {} is not exist in the graph'.format(id2))
        if id1 == id2:
            return 0, [id1]
        return self.dijkstra(id1, id2)

    def dijkstra(self, src, dest) -> (float, list):
        distances = {node: inf for node in self.graph.nodes.keys()}
        previous_nodes = {node: None for node in self.graph.nodes.keys()}
        distances[src] = 0
        # vertices = self.vertices.copy()
        nodes = [x for x in self.graph.nodes.keys()]
        while nodes:
            # 3. Select the unvisited node with the smallest distance,
            # it's current node now.
            current_node = min(nodes, key=lambda vertex: distances[vertex])
            # 6. Stop, if the smallest distance
            # among the unvisited nodes is infinity.
            if distances[current_node] == inf:
                break

            # 4. Find unvisited neighbors for the current node
            # and calculate their distances through the current node.
            for neighbour, w in self.graph.nodes.get(current_node).get_connections_out().items():
                alternative_route = distances[current_node] + w

                # Compare the newly calculated distance to the assigned
                # and save the smaller one.
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_nodes[neighbour] = current_node

            # 5. Mark the current node as visited
            # and remove it from the unvisited set.
            nodes.remove(current_node)

        path, current_node = [], dest
        while previous_nodes[current_node] is not None:
            path.append(current_node)
            current_node = previous_nodes[current_node]
        if path:
            path.append(current_node)
        path.reverse()
        return distances[dest], path

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC
        """
        if id1 not in self.graph.get_all_v().keys():
            raise Exception('Node {} is not exist in the graph'.format(id1))
        l = self.SCC
        for i in l:
            if id1 in i:
                return i

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC
        """
        return self.SCC

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """


    def DFSUtil(self, g: DiGraph, n: int, visited: dict, l: list):
        visited[n] = True
        l.append(n)
        # Recur for all the vertices adjacent to this vertex
        for k, v in g.all_out_edges_of_node(n).items():
            if not visited.get(k):
                self.DFSUtil(g, k, visited, l)

    def fillOrder(self, n, visited, stack):
        # Mark the current node as visited
        visited[n] = True
        # Recur for all the vertices adjacent to this vertex
        for k, v in self.graph.all_out_edges_of_node(n).items():
            if not visited.get(k):
                self.fillOrder(k, visited, stack)
        stack = stack.append(n)

    def Transpose(self):
        g = DiGraph()
        for k, v in self.graph.get_all_v().items():
            g.add_node(k, v.get_location())
        for k, v in g.get_all_v().items():
            for dest, w in self.graph.all_in_edges_of_node(k).items():
                g.add_edge(k, dest, w)
        return g

    @property
    def SCC(self):
        stack = []
        visited = {}
        for k in self.graph.get_all_v():
            visited[k] = False
        # Fill vertices in stack according to their finishing
        # times
        for i in visited:
            if not visited.get(i):
                self.fillOrder(i, visited, stack)

            # Create a reversed graph
        g_transpose = self.Transpose()

        # Mark all the vertices as not visited (For second DFS)
        visited = {}
        for k in self.graph.get_all_v():
            visited[k] = False

        # Now process all vertices in order defined by Stack
        the_list = []
        while stack:
            scc_list = []
            n = stack.pop()
            if not visited.get(n):
                self.DFSUtil(g_transpose, n, visited, scc_list)
                the_list.append(scc_list)
        return the_list


if __name__ == '__main__':
    g = DiGraph()
    g.add_node(0, (2,2,2))
    g.add_node(1, (2, 2, 2))
    g.add_node(2, (1, 1, 3))
    g.add_node(3, (1, 1, 4))
    g.add_node(4, (1, 1, 5))
    g.add_edge(0, 1, 1.5)
    g.add_edge(1, 2, 2.5)
    g.add_edge(2, 0, 1)
    g.add_edge(4, 0, 1.5)
    g.add_edge(4, 3, 1.5)

    g.add_node(1, (1, 2, 3))
    g.add_edge(0, 2, 3)

    ga = GraphAlgo()
    ga.load_from_json('DiGraphTry.json')

    #ga.load_from_json('../data/T0.json')
    #ga.load_from_json('../src/DiGraph.json')
    #ga.save_to_json('DiGraphTry.json')
    #ga.load_from_json('DiGraph.json')
    print(str(ga.graph))
    print(ga.get_graph().get_all_v())
    print(ga.shortest_path(0, 0))
    print(ga.shortest_path(0, 2))
    ga.graph.add_node(10)
    print(str(ga.graph))

    print('\n', str(ga.graph))

    print(ga.connected_components())
    print(ga.connected_component(0))

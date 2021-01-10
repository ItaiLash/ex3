import random
from numpy import inf
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from typing import List
import json

import matplotlib.pyplot as plt


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, digraph: DiGraph = None):
        self.graph = digraph

    def get_graph(self) -> DiGraph:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        gra = DiGraph()
        with open(file_name, "r") as f:
            graph_dict = json.load(f)
            for i in graph_dict.get("Nodes"):
                if "pos" in i and len(i.get("pos")) > 0:
                    pos = []
                    pos_as_str = i.get("pos")
                    arr = pos_as_str.split(',')
                    for j in arr:
                        pos.append(float(j))
                    gra.add_node(int(i.get("id")), tuple(pos))
                else:
                    x = random.uniform(0, 100)
                    y = random.uniform(0, 100)
                    gra.add_node(int(i.get("id")), (x, y, 0))
            for i in graph_dict.get("Edges"):
                gra.add_edge(int(i.get("src")), int(i.get("dest")), float(i.get("w")))
        self.graph = gra
        return True

    def save_to_json(self, file_name: str) -> bool:
        try:
            with open(file_name, "w") as f:
                json.dump(self.graph, default=lambda o: o.as_dict(), indent=4, fp=f)
        except IOError as e:
            print(e)
            return False
        return True

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
        scc = self.SCC
        for i in scc:
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
        for node in self.graph.get_all_v().values():
            if node.get_location() is None:
                loc_x = random.uniform(0, 100)
                loc_y = random.uniform(0, 100)
                location = (loc_x, loc_y, 0)
                node.set_location(location)
            x, y, z = node.get_location()
            plt.plot(x, y, markersize=30, marker='.', color='red')
            plt.text(x, y, str(node.get_key()), color='black', fontsize=10)
            for dest_id, w in self.graph.all_out_edges_of_node(node.get_key()).items():
                dest = self.graph.get_node(dest_id)
                if dest.get_location() is None:
                    loc_x2 = random.uniform(0, 100)
                    loc_y2 = random.uniform(0, 100)
                    location = (loc_x2, loc_y2, 0)
                    dest.set_location(location)
                x2, y2, z2 = dest.get_location()
                plt.annotate("", xy=(x, y), xytext=(x2, y2), arrowprops=dict(arrowstyle="<-"))
                # mid_x = (x+x2)/2
                # mid_y = (y+y2)/2
                # plt.text(mid_x, mid_y, str(w)[0:4], color='black', fontsize=10)
        plt.show()

    def dfs(self, gra: DiGraph, n: int, visited: dict, stack: list):
        local_stack = [n]  # create local_stack with starting vertex
        while local_stack:  # while local_stack is not empty
            v = local_stack[-1]  # peek top of local_stack
            if visited[v]:  # if already seen
                v = local_stack.pop()  # done with this node, pop it from local_stack
                if visited[v] == 1:  # if GRAY, finish this node
                    visited[v] = 2  # BLACK, done
                    stack.append(v)
            else:  # seen for first time
                visited[v] = 1  # GRAY: discovered
                for k in gra.all_out_edges_of_node(v).keys():  # for all neighbor (v, w)
                    if not visited[k]:  # if not seen
                        local_stack.append(k)

    def transpose(self):
        gra = DiGraph()
        for k, v in self.graph.get_all_v().items():
            gra.add_node(k, v.get_location())
        for k, v in gra.get_all_v().items():
            for dest, w in self.graph.all_in_edges_of_node(k).items():
                gra.add_edge(k, dest, w)
        return gra

    @property
    def SCC(self):
        stack = []
        visited = {}
        for k in self.graph.get_all_v():
            visited[k] = 0

        # Fill vertices in stack according to their finishing
        # times
        for i in visited:
            if not visited.get(i):
                self.dfs(self.graph, i, visited, stack)

            # Create a reversed graph
        g_transpose = self.transpose()

        # Mark all the vertices as not visited (For second DFS)
        visited = {}
        for k in self.graph.get_all_v():
            visited[k] = 0

        # Now process all vertices in order defined by Stack
        the_list = []
        while stack:
            scc_list = []
            n = stack.pop()
            if not visited.get(n):
                self.dfs(g_transpose, n, visited, scc_list)
                the_list.append(scc_list)
        return the_list

    def __eq__(self, other):
        if self is other:
            return True
        if other is None or self.__class__ is not other.__class__:
            return False
        return self.graph.__eq__(other.graph)


if __name__ == '__main__':
    g = DiGraph()
    # g.add_node(0, (1, 1, 1))
    # g.add_node(1, (2, 2, 2))
    # g.add_node(2, (1, 1, 3))
    # g.add_node(3, (1, 1, 4))
    # g.add_node(4, (1, 1, 5))
    # g.add_edge(0, 1, 1.5)
    # g.add_edge(1, 2, 2.5)
    # g.add_edge(2, 0, 1)
    # g.add_edge(4, 0, 1.5)
    # g.add_edge(4, 3, 1.5)

    # g.add_node(1, (1, 2, 3))
    # g.add_edge(0, 2, 3)
    #
    ga = GraphAlgo(g)
    # ga.load_from_json('DiGraphTry.json')

    # ga.load_from_json('../data/T0.json')
    ga.load_from_json('../data/G_30000_240000_2.json')
    # ga.save_to_json('DiGraphTry.json')
    # ga.load_from_json('DiGraph.json')
    # print(str(ga.graph))
    # print(ga.get_graph().get_all_v())
    # print(ga.shortest_path(0, 0))
    print(ga.shortest_path(0, 100))
    # ga.graph.add_node(10)
    # print(str(ga.graph))

    # print('\n', str(ga.graph))

    print(ga.connected_components())
    print(ga.connected_component(0))
    # ga.plot_graph()

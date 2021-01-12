import heapq
import random
from numpy import inf
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from typing import List
import json
import matplotlib.pyplot as plt


class GraphAlgo(GraphAlgoInterface):
    """This class implement GraphAlgoInterface abstract class that represents an interface of a graph."""

    def __init__(self, digraph: DiGraph = None):
        """
        Each GraphAlgo contain a DiGraph on which the algorithm works on.
        :param digraph:
        """
        self.graph = digraph

    def get_graph(self) -> DiGraph:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
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
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        try:
            with open(file_name, "w") as f:
                json.dump(self.graph, default=lambda o: o.as_dict(), indent=4, fp=f)
        except IOError as e:
            print(e)
            return False
        return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm.
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, the path as a list
        """
        if self.graph.nodes.get(id1) is None:
            raise Exception('Node {} is not exist in the graph'.format(id1))
        if self.graph.nodes.get(id2) is None:
            raise Exception('Node {} is not exist in the graph'.format(id2))
        if id1 == id2:
            return 0, [id1]
        return self.dijkstra(id1, id2)

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC
        """
        if id1 not in self.graph.get_all_v().keys():
            raise Exception('Node {} is not exist in the graph'.format(id1))
        return self.SCC(id1)

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: a list all SCCs
        """
        return self.SCC()

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
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

    def dijkstra(self, src, dest) -> (float, list):
        """
        This method based on Dijkstra's algorithm.
        Dijkstra's algorithm is an algorithm for finding the shortest paths between nodes in a graph.
        In other words it finds the shortest paths between the source node and the destination node.
        The method stored a distance dictionary represent each node weight, in the beginning initialized to infinity.
        In each step the method update his current distance from the source node.
        In addition it stored a dictionary represent each node "father", meaning the node through which we
        discovered this node.
        Update the source node weight to be 0 and push him into a queue.
        Pop the node with the minimum weight from the queue.
        Visit each one of this nodes neighbors:
        Check if his current weight is more then the distance between the node and the source node,
        if so, update his weight and updates his "father" to be the node's id from which he came to.
        After going through all the neighbors of the node,
        If the current node that pop out from the queue is the destination node we finish.
        Otherwise repeat these steps until the queue is empty.
        If the dest node weight is infinity it means there is no path between src node and dest node,
        return infinity and empty list.
        Otherwise returns the weight of the dest node that represent the distance between the two nodes,
        return the path between them and the distance.
        Complexity: O((|V|+|E|)log|V|), |V|=number of nodes, |E|=number of edges.
        :param: src  - the source node_info
        :param: dest - the destination node_info
        :return: the shortest path between the two nodes and the path between them,
        and infinity if there is no path like this.
        """
        distances = {node: inf for node in self.graph.nodes.keys()}
        previous_nodes = {src: -1}
        distances[src] = 0
        queue = []
        heapq.heappush(queue, (0, src))
        while queue:
            current_node = heapq.heappop(queue)[1]
            if distances[current_node] == inf:
                break
            for neighbour, w in self.graph.nodes.get(current_node).get_connections_out().items():
                alternative_route = distances[current_node] + w
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_nodes[neighbour] = current_node
                    heapq.heappush(queue, (distances[neighbour], neighbour))
                if current_node == dest:
                    break

        path, current_node = [], dest
        if distances[dest] == inf:
            return inf, []
        while current_node != -1:
            path.insert(0, current_node)
            current_node = previous_nodes[current_node]

        return distances[dest], path

    def dfs(self, gra: DiGraph, n: int, visited: dict, stack: list):
        """
        This method based on DFS algorithm.
        Depth-first search (DFS) is an algorithm for traversing or searching graph data structures.
        The algorithm starts at the root node and explores as far as possible along each branch before backtracking.
        First, the method create local stack and insert the root node inside it.
        While local_stack is not empty:
        peek the node that in the top of the local stack.
        If his status is 0, meaning it discover for the first time, update his status to 1.
        Visit each one of this node neighbors and if the neighbor status is 0, insert it into the local stack.
        If his status is 1 or 2, pop this node from the local stack and update his status to 2,
        and insert this node to the stack.
        At the end, the stack contain all the nodes discover from the "root" node (n).
        :param gra: a DiGraph
        :param n: the node_id from which the method begins the search
        :param visited: a dictionary represent the node status, 0, 1 or 2.
        :param stack: a list that will be updated during the method.
        """
        local_stack = [n]
        while local_stack:
            v = local_stack[-1]
            if visited[v]:
                v = local_stack.pop()
                if visited[v] == 1:
                    visited[v] = 2
                    stack.append(v)
            else:
                visited[v] = 1
                for k in gra.all_out_edges_of_node(v).keys():
                    if not visited[k]:
                        local_stack.append(k)

    def transpose(self):
        """
        Return transpose graph.
        Meaning each edge in the original graph transpose (src-->dest)-->(src<--dest).
        :return:
        """
        gra = DiGraph()
        for k, v in self.graph.get_all_v().items():
            gra.add_node(k, v.get_location())
        for k, v in gra.get_all_v().items():
            for dest, w in self.graph.all_in_edges_of_node(k).items():
                gra.add_edge(k, dest, w)
        return gra

    def SCC(self, key=None):
        """
        This method based on Kosaraju's algorithm in iterative way.
        First, call dfs on the original graph to fill the stack in order of each node finish time.
        Then compute this graph transpose.
        Last, call dfs on the transpose graph, but in the main loop, consider nodes in order of decreasing
        finishing time(as computed in the first dfs).
        In the last call for the dfs it return a list of scc.
        :return: a List of lists represents all the strongly connected component in the graph.
        """
        stack = []
        visited = {}
        for k in self.graph.get_all_v():
            visited[k] = 0
        for i in visited:
            if not visited.get(i):
                self.dfs(self.graph, i, visited, stack)

        g_transpose = self.transpose()

        visited = {}
        for k in g_transpose.get_all_v():
            visited[k] = 0

        the_list = []
        while stack:
            scc_list = []
            n = stack.pop()
            if not visited.get(n):
                self.dfs(g_transpose, n, visited, scc_list)
                the_list.append(scc_list)
                if key is not None and key in scc_list:
                    return scc_list
        return the_list

    def __eq__(self, other):
        if self is other:
            return True
        if other is None or self.__class__ is not other.__class__:
            return False
        return self.graph.__eq__(other.graph)

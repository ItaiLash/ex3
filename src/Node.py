class Node:

    def __init__(self, k: int = None, loc: tuple = None, **kwargs):
        self.__key = k
        self.__location = loc
        self.__ni_out = {}
        self.__ni_in = {}
        self.d_time = 0
        self.f_time = 0

    def add_neighbor_out(self, neighbor_id: int, weight: float) -> None:
        self.__ni_out[neighbor_id] = weight

    def add_neighbor_in(self, neighbor_id: int, weight: float) -> None:
        self.__ni_in[neighbor_id] = weight

    def get_connections_out(self) -> dict:
        return self.__ni_out

    def get_connections_in(self) -> dict:
        return self.__ni_in

    def get_key(self) -> int:
        return self.__key

    def get_weight(self, neighbor_id: int) -> float:
        return self.__ni_out[neighbor_id]

    def get_location(self) -> tuple:
        return self.__location

    def set_location(self, location: tuple) -> None:
        self.__location = location

    def __repr__(self):
        return str([self.get_key()])

    def __str__(self) -> str:
        return "Node: id: " + str(self.__key) + ' neighbors: ' + str(self.__ni_out)

    def as_dict_node(self):
        l = str(self.get_location())
        m_dict = {"pos": l[1:-1], "id": self.get_key()}
        return m_dict

    def as_dict_edge(self):
        l_list = []
        for k, v in self.get_connections_out().items():
            m_dict = {"src": int(self.get_key()), "w": float(v), "dest": int(k)}
            l_list.append(m_dict)
        return l_list


if __name__ == '__main__':
    a = (1, 1, 1)
    n = Node(0, a)
    n.add_neighbor_in(1, 3.5)
    n.add_neighbor_out(2, 1.7)
    n.add_neighbor_out(4, 0.5)
    print(n.__str__())
    print(n.as_dict_node())
    print(n.get_connections_in())

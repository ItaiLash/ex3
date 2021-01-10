class Node:

    def __init__(self, k: int = None, loc: tuple = None, **kwargs):
        self.__key = k
        self.__location = loc
        self.__ni_out = {}
        self.__ni_in = {}

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
        loc_as_str = str(self.get_location())
        m_dict = {"pos": loc_as_str[1:-1], "id": self.get_key()}
        return m_dict

    def as_dict_edge(self):
        l_list = []
        for k, v in self.get_connections_out().items():
            m_dict = {"src": int(self.get_key()), "w": float(v), "dest": int(k)}
            l_list.append(m_dict)
        return l_list

    def __eq__(self, o: object) -> bool:
        if self is o:
            return True
        if o is None or self.__class__ is not o.__class__:
            return False
        other = o
        return self.__key == other.__key and self.__location.__eq__(other.__location) and self.__ni_in.__eq__(
            other.__ni_in) and self.__ni_out.__eq__(other.__ni_out)


if __name__ == '__main__':
    a = (1, 1, 1)
    n = Node(0, a)
    n2 = Node(0, (1, 1, 1))
    print("eq:", n.__eq__(n2))
    n.add_neighbor_in(1, 3.5)
    n.add_neighbor_out(2, 1.7)
    n.add_neighbor_out(4, 0.5)
    n2.add_neighbor_in(1, 3.5)
    n2.add_neighbor_out(2, 1.7)
    print("eq:", n.__eq__(n2))
    n2.add_neighbor_out(4, 0.5)
    print("eq:", n.__eq__(n2))

    print(n.__str__())
    print(n.as_dict_node())
    print(n.get_connections_in())
    b = {1: 1, 2: 2}
    c = {1: 1, 2: 2}
    print(c.__eq__(b))

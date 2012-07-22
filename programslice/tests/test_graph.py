import unittest2
from programslice.graph import Graph
from programslice.graph import Node


class TestGraph(unittest2.TestCase):

    def setUp(self):
        self.graph = Graph()

    def test_add(self):
        self.graph.add(Node(1))
        self.graph.add(Node(2))
        self.assertEqual([1, 2], self.graph.edges())

        self.graph.add(Node(3))
        self.assertEqual(3, len(self.graph))
        self.assertEqual([1, 2, 3], self.graph.edges())

    def test_connect(self):
        self.graph.add(Node(1))
        self.graph.add(Node(2))
        self.graph.connect(1, 2)
        self.assertEqual([2], [x.lineno for x in self.graph[1]])

        self.graph.connect(2, 1)
        self.assertEqual([1], [x.lineno for x in self.graph[2]])

    def test_edges(self):
        self.graph.add(Node(1))
        self.graph.add(Node(2))

        result = self.graph.edges()
        self.assertEqual([1, 2], result)

    def test_slice_forward(self):
        for i in range(1, 12):
            self.graph.add(Node(i))

        self.graph.connect(1, 10)
        self.graph.connect(1, 6)
        self.graph.connect(2, 11)
        self.graph.connect(2, 7)
        self.graph.connect(2, 3)
        self.graph.connect(3, 5)
        self.graph.connect(3, 8)
        self.graph.connect(3, 4)
        self.graph.connect(4, 5)
        self.graph.connect(6, 6)
        self.graph.connect(6, 10)
        self.graph.connect(7, 7)
        self.graph.connect(8, 8)
        self.graph.connect(8, 5)
        self.graph.connect(8, 7)

        result = self.graph.find_path(2)
        self.assertEqual([2, 3, 4, 5, 7, 8, 11], result)

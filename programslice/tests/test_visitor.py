import ast
import os.path
import programslice.visitor
import unittest2 as unittest


class TestLineDependencyVisitor(unittest.TestCase):

    def setUp(self):
        self.visitor = programslice.visitor.LineDependencyVisitor()

    def load_testdata(self, filename):
        filepath = os.path.join(os.path.dirname(__file__),
                                'testdata', filename)
        node = ast.parse(open(filepath, 'r').read(), filepath)
        return node

    def test_visit_FunctionDef(self):
        node = self.load_testdata('function.py')
        self.visitor.visit(node)
        graph1, graph2 = self.visitor.graphs[2:]
        self.assertEqual(4, len(self.visitor.graphs))
        self.assertEqual('main', graph1.name)
        self.assertEqual('innerfunc', graph2.name)
        self.assertEqual([17, 19, 20], graph2.slice_forward(17))

    def test_visit_Call(self):
        node = self.load_testdata('function.py')
        self.visitor.visit(node)
        graph = self.visitor.graphs[0]
        self.assertEqual([5, 6, 7, 10, 11], graph.slice_forward(5))

    def test_visit_While(self):
        node = self.load_testdata('binsearch.py')
        self.visitor.visit(node)
        graph = self.visitor.get_graph_for(12)
        expected = [12, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        self.assertEqual(expected, graph.slice_forward(12))

        expected = [18, 20, 22]
        self.assertEqual(expected, graph.slice_forward(18))


class TestVisitorFunctional(unittest.TestCase):

    def test_get_graph_for(self):
        visitor = programslice.visitor.LineDependencyVisitor()
        graph1 = programslice.graph.Graph('function1')
        graph1.add(3)
        graph1.add(5)
        graph1.add(11)

        graph2 = programslice.graph.Graph('function2')
        graph2.add(12)
        graph2.add(13)
        graph2.add(15)
        visitor.graphs = [graph1, graph2]

        self.assertEqual('function1', visitor.get_graph_for(4).name)
        self.assertEqual('function2', visitor.get_graph_for(12).name)
        self.assertEqual(None, visitor.get_graph_for(2))

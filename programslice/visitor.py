import ast
import programslice.graph
from collections import deque


class LineDependencyVisitor(ast.NodeVisitor):
    """
    A visitor which creates a data dependency graph.

    Note: I've called it LineDependencyVisitor, as currently what
    matters are dependencies between lines of code. This is determined
    by simply using the occurences of variables in their lines as the
    graphs edges. This is not very precise, but makes of a nice
    prototype to play with the vim integration.
    """

    def __init__(self):
        self.graphs = []
        self.current_graph = None
        self.stack = deque()
        self.variables = {}

    def get_graph_for(self, lineno):
        """
        Returns a graph, which visited the given lineno
        """
        for graph in self.graphs:
            if lineno >= graph.first and lineno <= graph.last:
                return graph

    def visit_FunctionDef(self, node):
        graph = programslice.graph.Graph(
            'function {0}:{1}'.format(node.name, node.lineno))
        self.stack.appendleft(graph)
        [self.visit(x) for x in ast.iter_child_nodes(node)]
        self.reset()

    def visit_Name(self, node):
        self.variables.setdefault(node.id, deque()).append(node.lineno)

    def reset(self):
        graph = self.stack.popleft()
        for key, linenumbers in self.variables.items():
            while linenumbers:
                lineno = linenumbers.popleft()
                if lineno not in graph.edges:
                    graph.add(lineno)
                if linenumbers:
                    graph.connect(lineno, linenumbers[0])
        self.graphs.append(graph)

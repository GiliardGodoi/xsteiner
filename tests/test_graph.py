import pytest
from xsteiner.graph.graph import Graph
from xsteiner.graph.edge import Edge

@pytest.fixture
def empty_graph():
    return Graph()

@pytest.fixture
def small_graph():
    g = Graph()
    g.add_node(1)
    g.add_node(2)
    g.add_edge(1, 2, weight=5)
    return g

@pytest.fixture
def medium_graph():
    g = Graph()
    nodes = range(1, 21)
    for node in nodes:
        g.add_node(node)

    edges = [
        (1, 2, 3), (2, 3, 4), (3, 4, 5), (4, 5, 6), (5, 6, 7),
        (6, 7, 8), (7, 8, 9), (8, 9, 10), (9, 10, 11), (10, 11, 12),
        (11, 12, 13), (12, 13, 14), (13, 14, 15), (14, 15, 16), (15, 16, 17),
        (16, 17, 18), (17, 18, 19), (18, 19, 20), (19, 20, 21), (20, 1, 32)
    ]

    for edge in edges:
        g.add_edge(*edge)

    return g

@pytest.mark.parametrize('graph,node,expected',[
            ('empty_graph', 1, 1),
            ('empty_graph', 'B', 1),
            ('empty_graph', sum, 1),
            ('medium_graph', 100, 21),
            ('small_graph', 'C', 3)
        ])
def test_add_node_to_empty_graph(graph, node, expected, request):
    graph = request.getfixturevalue(graph)
    graph.add_node(node)
    assert len([n for n in graph.nodes()]) == expected
    assert node in [n for n in graph.nodes()]

def test_add_none_as_node(empty_graph):
    with pytest.raises(ValueError):
        empty_graph.add_node(None)

def test_add_an_already_existing_node(small_graph):
    small_graph.add_node(3)
    with pytest.raises(ValueError):
        small_graph.add_node(2)

@pytest.mark.parametrize('graph,node,expected',[
    ('small_graph', 2, True),
    ('small_graph', 5, False),
    ('small_graph', 'X', False),
    ('small_graph', None, False)
])
def test_has_node(graph, node, expected, request):
    graph = request.getfixturevalue(graph)
    assert graph.has_node(node) == expected

def test_add_edge(empty_graph):

    empty_graph.add_edge(1, 2, 80)
    empty_graph.add_edge(2, 3, 0)
    empty_graph.add_edge(2, 3, 1)
    empty_graph.add_edge(2, 5, 20)
    empty_graph.add_edge(1, 4, 5)

    edges = [e for e in empty_graph.adjacents_edges(2)]
    assert sum(e.weight for e in edges) == 101

    edges = [e for e in empty_graph.edges()]
    assert len(edges) == 5

@pytest.mark.parametrize('graph_fixture,edge,expected',[
    ('empty_graph',  Edge(4, 5, 9),    False),
    ('small_graph',  Edge(1, 2, 5),    True),
    ('small_graph',  Edge(1, 2, None), False),
    ('medium_graph', Edge(12, 13, 14), True),
    ('medium_graph', Edge(12, 13, 15), False),
])
def test_has_edge_with_edge_obj(graph_fixture, edge, expected, request):
    graph = request.getfixturevalue(graph_fixture)
    assert graph.has_edge(edge) == expected


@pytest.mark.parametrize('graph_fixture,edge,expected',[
    ('empty_graph',  (4, 5, 9),    False),
    ('small_graph',  (1, 2, 5),    True),
    ('small_graph',  (1, 2),       False),
    ('medium_graph', (12, 13, 14), True),
    ('medium_graph', (12, 13, 15), False),
    ('medium_graph', (12, 13),     False),
])
def test_has_edge_with_args(graph_fixture, edge, expected, request):
    graph = request.getfixturevalue(graph_fixture)
    assert graph.has_edge(*edge) == expected

def test_has_edge_raising_exception(small_graph):
    with pytest.raises(ValueError):
        small_graph.has_edge(2)

@pytest.mark.skip(reason="Test not implemented yet")
def test_remove_edge():
    assert False, 'Something went wrong!'

@pytest.mark.skip(reason="Test not implemented yet")
def test_graphs_that_share_edges():
    assert False

def test_adjacents_edges(medium_graph):
    u = 20
    edges = [edge for edge in medium_graph.adjacents_edges(u)]
    assert len(edges) == 2

    vertices = [edge.x if edge.y == u else edge.y for edge in edges]
    assert 1 in vertices
    assert 19 in vertices

    weights = [edge.weight for edge in edges]
    assert sum(weights) == 53
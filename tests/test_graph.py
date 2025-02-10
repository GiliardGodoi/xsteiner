import pytest
from xsteiner.graph.graph import Graph
from xsteiner.graph.edge import Edge

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


def test_adjacency(medium_graph):
    cyclic = medium_graph
    start = 1
    assert cyclic.has_node(start)
    adjs = [v for v in cyclic.adjacents(start)]
    assert len(adjs) == 2
    assert 20 in adjs
    assert 2 in adjs


def test_add_edge_with_args(empty_graph):

    empty_graph.add_edge(1, 2, 80)
    empty_graph.add_edge(2, 3, 0)
    empty_graph.add_edge(2, 3, 1)
    empty_graph.add_edge(2, 5, 20)
    empty_graph.add_edge(1, 4, 5)

    edges = [e for e in empty_graph.adjacents_edges(2)]
    assert sum(e.weight for e in edges) == 101

    edges = [e for e in empty_graph.edges()]
    assert len(edges) == 5

def test_add_edges_from_list_of_edges(empty_graph, list_edges):
    for edge in list_edges:
        empty_graph.add_edge(edge)
    assert len(list_edges) == len([e for e in empty_graph.edges()])


@pytest.mark.parametrize('graph,node,expected',[
    ('small_graph', 2, True),
    ('small_graph', 5, False),
    ('small_graph', 'X', False),
    ('small_graph', None, False)
])
def test_has_node(graph, node, expected, request):
    graph = request.getfixturevalue(graph)
    assert graph.has_node(node) == expected


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

def test_degree_method(star_graph):
    leafs = [v for v in star_graph.nodes() if star_graph.degree(v) == 1]
    assert len(leafs) == 8
    assert star_graph.degree(20) == 8
    with pytest.raises(ValueError):
        star_graph.degree(101)
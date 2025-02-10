import pytest
import os
from pathlib import Path
from xsteiner.graph.edge import Edge
from xsteiner.graph.graph import Graph
from xsteiner.utils.steinlib import steinlib_parser
from xsteiner.utils.orlib import orlib_parser

@pytest.fixture
def steinlib_file():
    return Path('datasets', 'cc10-2p.stp')

@pytest.fixture
def bigger():
    return steinlib_parser(Path('datasets', 'cc10-2p.stp'))

@pytest.fixture
def orlib_file():
    return Path('datasets', 'steinb2.txt')

@pytest.fixture
def orlib_graph(orlib_file):
    return orlib_parser(orlib_file)

@pytest.fixture
def empty_graph():
    return Graph()

@pytest.fixture
def cyclic():
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

@pytest.fixture
def list_edges():
    return [
            Edge(4, 5, 9),
            Edge(1, 2, 5),
            Edge(1, 2, None),
            Edge(12, 13, 14),
            Edge(12, 13, 15),
        ]


@pytest.fixture
def star_graph():
    g = Graph()
    center = 20
    weights = [9, 8, 1, 0, 3, 6, 7, 15]
    for i, w in enumerate(weights, start=1):
        g.add_edge(i, center, w)
    return g

@pytest.fixture
def small_graph():
    g = Graph()
    g.add_node(1)
    g.add_node(2)
    g.add_edge(1, 2, 5)
    return g
import pytest
import os
from pathlib import Path
from xsteiner.graph.graph import SteinerGraphProblemInstance, Graph
from xsteiner.graph.edge import Edge
from xsteiner.utils.orlib import orlib_parser

@pytest.fixture
def filepath():
    return Path('datasets', 'steinb2.txt')

@pytest.fixture
def steiner_graph(filepath):
    graph = orlib_parser(filepath)
    return graph

def test_dataset_existence(filepath):
    assert os.path.exists(filepath)

def test_if_steiner_problem_is_graph():
    assert issubclass(SteinerGraphProblemInstance, Graph)

def test_orlib_parser(filepath):
    graph = orlib_parser(filepath)
    assert isinstance(graph, SteinerGraphProblemInstance)
    assert graph.nro_nodes == 50
    assert graph.nro_edges == 63
    assert graph.nro_terminals == 13
    assert type(graph.terminals) == set
    assert not (graph.terminals == {})
    assert hasattr(graph, 'update_terminals')

def test_edges_classes(steiner_graph):
    assert all(isinstance(edge, Edge) for edge in steiner_graph.edges())

def test_number_of_edges(steiner_graph):
    for i, _ in enumerate(steiner_graph.edges(), start=1):
        pass
    assert i == steiner_graph.nro_edges

def test_number_of_nodes(steiner_graph):
    for i, _ in enumerate(steiner_graph.nodes(), start=1):
        pass
    assert i == steiner_graph.nro_nodes

def test_number_of_terminal_nodes(steiner_graph):
    for i, _ in enumerate(steiner_graph.terminals, start=1):
        pass
    assert i == steiner_graph.nro_terminals

def test_update_terminals(steiner_graph):
    assert type(steiner_graph.terminals) == set
    assert not (steiner_graph.terminals == {})
    with pytest.raises(ValueError):
        steiner_graph.update_terminals(set()) # empty set
    assert steiner_graph.terminals != set()
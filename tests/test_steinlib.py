import pytest
import os
from pathlib import Path
from xsteiner.graph.graph import SteinerGraphProblemInstance
from xsteiner.graph.edge import Edge
from xsteiner.utils.steinlib import steinlib_parser, PUC


@pytest.fixture
def filepath():
    return Path('datasets', 'cc10-2p.stp')

@pytest.fixture
def steiner_graph(filepath):
    return steinlib_parser(filepath)

def test_dataset_existence(filepath):
    assert os.path.exists(filepath)

def test_steinlib_parser(filepath):
    steiner = steinlib_parser(filepath)
    assert isinstance(steiner, SteinerGraphProblemInstance)
    assert steiner.nro_nodes == 1024
    assert steiner.nro_edges == 5120
    assert steiner.nro_terminals == 135
    assert isinstance(steiner.terminals, set)
    assert len(steiner.terminals) != 0
    assert len(steiner.terminals) == steiner.nro_terminals
    assert hasattr(steiner, 'update_terminals')

def test_path_not_found():
    filepath = Path('xyz', 'dky.stp')
    with pytest.raises(FileNotFoundError):
        steinlib_parser(filepath)

def test_edges_classes(steiner_graph):
    assert all(isinstance(edge, Edge) for edge in steiner_graph.edges())

def test_sum_of_edges_weight(steiner_graph):
    assert sum(edge.weight for edge in steiner_graph.edges())

def test_counting_edges(steiner_graph):
    counter = 0
    for _ in steiner_graph.edges(): counter += 1
    assert steiner_graph.nro_edges == counter

def test_counting_nodes(steiner_graph):
    counter = 0
    for _ in steiner_graph.nodes(): counter += 1
    assert steiner_graph.nro_nodes == counter

def test_counting_terminals(steiner_graph):
    assert len(steiner_graph.terminals) == steiner_graph.nro_terminals

def test_update_terminals(steiner_graph):
    assert hasattr(steiner_graph, 'update_terminals')
    assert isinstance(steiner_graph.terminals, set)
    assert not (len(steiner_graph.terminals) == 0)
    with pytest.raises(ValueError):
        steiner_graph.update_terminals(set()) # empty set
    assert steiner_graph.terminals != set()

def test_puc_problem_instances():
    assert len(PUC) == 50
    assert all(isinstance(p, tuple)  for p in PUC)
    assert all(isinstance(p[0], str) for p in PUC)
    assert all(isinstance(p[1], int) for p in PUC)
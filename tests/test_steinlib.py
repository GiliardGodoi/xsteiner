import pytest
import os
from pathlib import Path
from xsteiner.graph.graph import SteinerGraphProblemInstance
from xsteiner.graph.edge import Edge
from xsteiner.utils.steinlib import steinlib_parser, PUC


def test_dataset_existence(steinlib_file):
    assert os.path.exists(steinlib_file)

def test_steinlib_parser(steinlib_file):
    steiner = steinlib_parser(steinlib_file)
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

def test_edges_classes(bigger):
    assert all(isinstance(edge, Edge) for edge in bigger.edges())

def test_sum_of_edges_weight(bigger):
    assert sum(edge.weight for edge in bigger.edges())

def test_counting_edges(bigger):
    counter = 0
    for _ in bigger.edges(): counter += 1
    assert bigger.nro_edges == counter

def test_counting_nodes(bigger):
    counter = 0
    for _ in bigger.nodes(): counter += 1
    assert bigger.nro_nodes == counter

def test_counting_terminals(bigger):
    assert len(bigger.terminals) == bigger.nro_terminals

def test_update_terminals(bigger):
    assert hasattr(bigger, 'update_terminals')
    assert isinstance(bigger.terminals, set)
    assert not (len(bigger.terminals) == 0)
    with pytest.raises(ValueError):
        bigger.update_terminals(set()) # empty set
    assert bigger.terminals != set()

def test_puc_problem_instances():
    assert len(PUC) == 50
    assert all(isinstance(p, tuple)  for p in PUC)
    assert all(isinstance(p[0], str) for p in PUC)
    assert all(isinstance(p[1], int) for p in PUC)
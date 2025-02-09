import pytest
import os
from pathlib import Path
from xsteiner.graph.graph import SteinerGraphProblemInstance, Graph
from xsteiner.graph.edge import Edge
from xsteiner.utils.orlib import (
    STEIN_B,
    STEIN_C,
    STEIN_D,
    STEIN_E,
    problems_class,
    generate_all_filenames,
    orlib_parser
)

@pytest.fixture
def filepath():
    return Path('datasets', 'steinb2.txt')

@pytest.fixture
def steiner_graph(filepath):
    return orlib_parser(filepath)

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
    counter = 0
    for _ in steiner_graph.terminals: counter += 1
    assert steiner_graph.nro_terminals == counter

def test_update_terminals(steiner_graph):
    assert hasattr(steiner_graph, 'update_terminals')
    assert isinstance(steiner_graph.terminals, set)
    assert not (len(steiner_graph.terminals) == 0)
    with pytest.raises(ValueError):
        steiner_graph.update_terminals(set()) # empty set
    assert steiner_graph.terminals != set()

@pytest.mark.parametrize('problems,key',[
    (STEIN_B, 'B'), (STEIN_C, 'c'), (STEIN_D, 'D'), (STEIN_E, 'e')
])
def test_stein_classes(problems, key):

    filenames = [f for f in generate_all_filenames(key)]

    assert len(problems) == len(filenames)
    assert all( p[0] == f for p, f in zip(problems, filenames))
    assert all( p[1] > 0 for p in problems)
    assert all( type(p) == tuple for p in problems)
    assert all( type(p[0]) == str for p in problems)
    assert all( type(p[1]) == int for p in problems)

def test_stein_classes_others():
    assert len(problems_class['others']) == 3
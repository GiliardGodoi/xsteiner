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

def test_dataset_existence(orlib_file):
    assert os.path.exists(orlib_file)

def test_if_steiner_problem_is_graph():
    assert issubclass(SteinerGraphProblemInstance, Graph)

def test_orlib_parser(orlib_file):
    graph = orlib_parser(orlib_file)
    assert isinstance(graph, SteinerGraphProblemInstance)
    assert graph.nro_nodes == 50
    assert graph.nro_edges == 63
    assert graph.nro_terminals == 13
    assert type(graph.terminals) == set
    assert not (graph.terminals == {})


def test_edges_classes(orlib_graph):
    assert all(isinstance(edge, Edge) for edge in orlib_graph.edges())

def test_sum_of_edges_weight(orlib_graph):
    assert sum(edge.weight for edge in orlib_graph.edges())

def test_counting_edges(orlib_graph):
    counter = 0
    for _ in orlib_graph.edges(): counter += 1
    assert orlib_graph.nro_edges == counter

def test_counting_nodes(orlib_graph):
    counter = 0
    for _ in orlib_graph.nodes(): counter += 1
    assert orlib_graph.nro_nodes == counter

def test_counting_terminals(orlib_graph):
    counter = 0
    for _ in orlib_graph.terminals: counter += 1
    assert orlib_graph.nro_terminals == counter

def test_update_terminals(orlib_graph):
    assert hasattr(orlib_graph, 'update_terminals')
    assert isinstance(orlib_graph.terminals, set)
    assert not (len(orlib_graph.terminals) == 0)
    with pytest.raises(ValueError):
        orlib_graph.update_terminals(set()) # empty set
    assert orlib_graph.terminals != set()

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
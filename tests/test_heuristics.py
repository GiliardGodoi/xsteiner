import os
import pytest
import random
from xsteiner.graph.graph import Graph, SteinerGraphProblemInstance
from xsteiner.graph.heuristics import (
    shortest_path_steiner_tree,
    shortest_path_with_origin,
    shortest_path_origin_prim,
    pruning_minimum_spanning_tree,
    pruning_kruskal_minimum_spanning_tree
)
from xsteiner.utils.orlib import (
    orlib_parser
)
from pathlib import Path

@pytest.fixture
def steiner():
    return orlib_parser(Path('datasets', 'steinb2.txt'))

def test_shortest_path_steiner_tree(steiner:SteinerGraphProblemInstance):
    node = 5
    total_weight = sum(edge.weight for edge in steiner.edges())
    assert steiner.has_node(node)

    tree, cost = shortest_path_steiner_tree(steiner, node, steiner.terminals)
    assert 0 < cost <= total_weight
    assert isinstance(tree, Graph)
    assert all(tree.has_node(t) for t in steiner.terminals)


def test_shortest_path_with_origin(steiner:SteinerGraphProblemInstance):

    node = 5
    total_weight = sum(edge.weight for edge in steiner.edges())
    assert steiner.has_node(node)

    tree, cost = shortest_path_with_origin(steiner, node, steiner.terminals)

    assert 0 < cost <= total_weight
    assert isinstance(tree, Graph)
    assert all(tree.has_node(t) for t in steiner.terminals)

def test_shortest_path_origin_prim(steiner:SteinerGraphProblemInstance):
    node = 5
    total_weight = sum(edge.weight for edge in steiner.edges())
    assert steiner.has_node(node)

    tree, cost = shortest_path_origin_prim(steiner,node,steiner.terminals)
    assert 0 < cost <= total_weight
    assert isinstance(tree, Graph)
    assert all(tree.has_node(t) for t in steiner.terminals)


def test_pruning_minimum_spanning_tree(steiner:SteinerGraphProblemInstance):

    node = 5
    total_weight = sum(edge.weight for edge in steiner.edges())
    assert steiner.has_node(node)

    tree, cost = pruning_minimum_spanning_tree(steiner,node,steiner.terminals)
    assert 0 < cost <= total_weight
    assert isinstance(tree, Graph)
    assert all(tree.has_node(t) for t in steiner.terminals)

def test_pruning_kruskal_minimum_spanning_tree(steiner:SteinerGraphProblemInstance):
    node = 5
    total_weight = sum(edge.weight for edge in steiner.edges())
    assert steiner.has_node(node)

    tree, cost = pruning_kruskal_minimum_spanning_tree(steiner, steiner.terminals)
    assert 0 < cost <= total_weight
    assert isinstance(tree, Graph)
    assert all(tree.has_node(t) for t in steiner.terminals)

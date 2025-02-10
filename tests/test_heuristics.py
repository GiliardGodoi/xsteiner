import os
import pytest
import random
from xsteiner.graph.graph import Graph, SteinerGraphProblemInstance
from xsteiner.graph.heuristics import (
    shortest_path_steiner_tree,
    shortest_path_with_origin,
    shortest_path_origin_prim,
    pruning_prim_minimum_spanning_tree,
    pruning_kruskal_minimum_spanning_tree,
    pruning_tree
)


def test_shortest_path_steiner_tree(orlib_graph:SteinerGraphProblemInstance):
    node = 5
    total_weight = sum(edge.weight for edge in orlib_graph.edges())
    assert orlib_graph.has_node(node)

    tree, cost = shortest_path_steiner_tree(orlib_graph, node, orlib_graph.terminals)
    assert 0 < cost <= total_weight
    assert isinstance(tree, Graph)
    assert all(tree.has_node(t) for t in orlib_graph.terminals)


def test_shortest_path_with_origin(orlib_graph:SteinerGraphProblemInstance):

    node = 5
    total_weight = sum(edge.weight for edge in orlib_graph.edges())
    assert orlib_graph.has_node(node)

    tree, cost = shortest_path_with_origin(orlib_graph, node, orlib_graph.terminals)

    assert 0 < cost <= total_weight
    assert isinstance(tree, Graph)
    assert all(tree.has_node(t) for t in orlib_graph.terminals)

def test_shortest_path_origin_prim(orlib_graph:SteinerGraphProblemInstance):
    node = 5
    total_weight = sum(edge.weight for edge in orlib_graph.edges())
    assert orlib_graph.has_node(node)

    tree, cost = shortest_path_origin_prim(orlib_graph,node,orlib_graph.terminals)
    assert 0 < cost <= total_weight
    assert isinstance(tree, Graph)
    assert all(tree.has_node(t) for t in orlib_graph.terminals)


def test_pruning_minimum_spanning_tree(orlib_graph:SteinerGraphProblemInstance):

    node = 5
    total_weight = sum(edge.weight for edge in orlib_graph.edges())
    assert orlib_graph.has_node(node)

    tree, cost = pruning_prim_minimum_spanning_tree(orlib_graph,node,orlib_graph.terminals)
    assert 0 < cost <= total_weight
    assert isinstance(tree, Graph)
    assert all(tree.has_node(t) for t in orlib_graph.terminals)

def test_pruning_kruskal_minimum_spanning_tree(orlib_graph:SteinerGraphProblemInstance):
    node = 5
    total_weight = sum(edge.weight for edge in orlib_graph.edges())
    assert orlib_graph.has_node(node)

    tree, cost = pruning_kruskal_minimum_spanning_tree(orlib_graph, orlib_graph.terminals)
    assert 0 < cost <= total_weight
    assert isinstance(tree, Graph)
    assert all(tree.has_node(t) for t in orlib_graph.terminals)

def test_pruning_tree(bigger:SteinerGraphProblemInstance):

    tree = pruning_tree(bigger, 5, bigger.terminals)

    assert all(tree.has_node(t) for t in bigger.terminals)

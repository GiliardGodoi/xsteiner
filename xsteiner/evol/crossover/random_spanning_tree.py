import random
from xsteiner.graph.graph import (
    Graph,
    SteinerGraphProblemInstance
)
from xsteiner.graph.operators import (
    union,
    pruning_tree
)
from xsteiner.graph.trees.minimum_spanning import (
    prim_spanning_tree,
    kruskal_spanning_tree,
    boruvka_spanning_tree
)
from xsteiner.graph.trees.random_spanning import (
    prim_random_spanning_tree,
    kruskal_random_spanning_tree,
    boruvka_random_spanning_tree,
    random_walk_spanning_tree
)

class PrimRSTCrossover:

    def __init__(self, stpg:SteinerGraphProblemInstance):
        self.terminals = stpg.terminals.copy()

    def __call__(self, red: Graph, blue: Graph, p_prune=1.0, p_greedy=0.0):
        graph = union(red, blue)
        if (p_greedy != 0) and (random.random() < p_greedy) :
            tree = prim_spanning_tree(graph)
        else:
            tree = prim_random_spanning_tree(graph)

        if random.random() < p_prune:
            tree = pruning_tree(tree, self.terminals)
        return tree


class KruskalRSTCrossover:
    def __init__(self, stpg:SteinerGraphProblemInstance):
        self.terminals = stpg.terminals.copy()

    def __call__(self, red: Graph, blue: Graph, p_prune=1.0, p_greedy=0.0):

        graph = union(red, blue)
        if (p_greedy != 0) and (random.random() < p_greedy) :
            tree = kruskal_spanning_tree(graph)
        else:
            tree = kruskal_random_spanning_tree(graph)

        if random.random() < p_prune:
            tree = pruning_tree(tree, self.terminals)

        return tree


class BoruvkaRSTCrossover:
    def __init__(self, stpg:SteinerGraphProblemInstance):
        self.terminals = stpg.terminals.copy()

    def __call__(self, red: Graph, blue: Graph, p_prune=1.0, p_greedy=0.0):

        graph = union(red, blue)
        if (p_greedy != 0) and (random.random() < p_greedy) :
            tree = boruvka_spanning_tree(graph)
        else:
            tree = boruvka_random_spanning_tree(graph)

        if random.random() < p_prune:
            tree = pruning_tree(tree, self.terminals)

        return tree

class RandomWalkRSTCrossover:

    def __init__(self, stpg:SteinerGraphProblemInstance):
        self.terminals = stpg.terminals.copy()

    def __call__(self, red: Graph, blue: Graph, p_prune=1.0, p_greedy=None):

        graph = union(red, blue)
        tree = random_walk_spanning_tree(graph)
        if random.random() < p_prune:
            tree = pruning_tree(tree, self.terminals)

        return tree
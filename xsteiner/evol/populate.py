from random import (
    choice,
    random
)
from xsteiner.graph.graph import (
    Graph,
    SteinerGraphProblemInstance
)
from xsteiner.graph.operators import pruning_tree
from xsteiner.graph.trees.random_spanning import (
    prim_random_spanning_tree,
    kruskal_random_spanning_tree,
    boruvka_random_spanning_tree
)

class PrimRSTPopulation:
    """
    Generates a random spanning trees from Steiner Graph Problem Instance using the Prim Random Spanning Tree (PrimRST) algorithm.

    Attributes:
        stpg (SteinerGraphProblemInstance): The Steiner Graph Problem Instance.
        terminals (list): The list of terminal nodes in the Steiner Graph Problem Instance.
    Methods:
        __call__(self, *args, p_prune=1.0):
            Generates a random spanning tree using PrimRST algorithm and prunes it with probability p_prune.
    """

    def __init__(self, stpg:SteinerGraphProblemInstance):
        self.stpg = stpg
        self.terminals = stpg.terminals

    def __call__(self,*args, p_prune=1.0):
        stpg = self.stpg
        tree = prim_random_spanning_tree(stpg)
        if random() > p_prune:
            tree = pruning_tree(tree, self.terminals)
        return tree


class KruskalRSTPopulation:
    """
    Generates random spanning trees from a Steiner Graph Problem Instance using the Kruskal Random Spanning Tree (KruskalRST) algorithm.
    Attributes:
        stpg (SteinerGraphProblemInstance): The Steiner Graph Problem Instance.
        terminals (list): The list of terminal nodes in the Steiner Graph Problem Instance.
    Methods:
        __call__(self, *args, p_prune=1.0, **kwds):
            Generates a random spanning tree using the KruskalRST algorithm and prunes it with probability p_prune.
    """

    def __init__(self, stpg:SteinerGraphProblemInstance):
        self.stpg = stpg
        self.terminals = stpg.terminals

    def __call__(self,*args, p_prune=1.0, **kwds):
        stpg = self.stpg
        tree = kruskal_random_spanning_tree(stpg)
        if random() > p_prune:
            tree = pruning_tree(tree, self.terminals)
        return tree

class BoruvkaRSTPolulation:
    """
    Generates random spanning trees from a Steiner Graph Problem Instance using the Boruvka Random Spanning Tree (BoruvkaRST) algorithm.
    Attributes:
        stpg (SteinerGraphProblemInstance): The Steiner Graph Problem Instance.
        terminals (list): The list of terminal nodes in the Steiner Graph Problem Instance.
    Methods:
        __call__(self, *args, p_prune=1.0, **kwds):
            Generates a random spanning tree using the BoruvkaRST algorithm and prunes it with probability p_prune.
    """

    def __init__(self, stpg:SteinerGraphProblemInstance):
        self.stpg = stpg
        self.terminals = stpg.terminals

    def __call__(self,*args, p_prune=1.0):
        stpg = self.stpg
        tree = boruvka_random_spanning_tree(stpg)
        if random() > p_prune:
            tree = pruning_tree(tree, self.terminals)
        return tree

class RandomWalkRSPPopulation:
    """
    Generates random spanning trees from a Steiner Graph Problem Instance using a Random Walk algorithm.
    Attributes:
        stpg (SteinerGraphProblemInstance): The Steiner Graph Problem Instance.
        terminals (list): The list of terminal nodes in the Steiner Graph Problem Instance.
    Methods:
        __call__(self, *args, p_prune=1.0, **kwds):
            Generates a random spanning tree using a random walk algorithm and prunes it with probability p_prune.
    """

    def __init__(self, stpg:SteinerGraphProblemInstance):
        self.stpg = stpg
        self.terminals = stpg.terminals

    def __call__(self, p_prune=1.0):
        """
        Attributes:
            p_prune (float): The probability of pruning the generated tree.

        Observation:
            This code does not run the function from the module `random_walk_spanning_tree` from the module `xsteiner.graph.trees.random_spanning` for optimization purposes.
            The stop criterion in the while loop based on terminal nodes runs faster
            than one based on all nodes from the stpg instance.
        """
        stpg = self.stpg
        tree = Graph()
        special_nodes = set(self.terminals)
        v = special_nodes.pop()
        while special_nodes:
            edge = choice([e for e in stpg.adjacents_edges(v)])
            u = edge.adj(v)
            if not tree.has_node(u):
                tree.add_edge(edge)
                special_nodes.discard(u)
            v = u

        if random() > p_prune:
            tree = pruning_tree(tree)

        return tree
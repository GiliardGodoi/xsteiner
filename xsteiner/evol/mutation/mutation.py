import random
from xsteiner.disjointset.disjointset import DisjointSet
from xsteiner.graph.graph import (
    Graph,
    SteinerGraphProblemInstance
)
from xsteiner.graph.operators import induced_subgraph, pruning_tree
from xsteiner.graph.trees.random_spanning import (
    prim_random_spanning_tree,
    kruskal_random_spanning_tree,
    boruvka_random_spanning_tree,
    random_walk_spanning_tree
)

class ShuffleEdges:
    '''
    Generates a spanning tree from an induced subgraph and optionally pruning it.
    The mutation process involves the following steps:

    1. An induced subgraph is created from the input tree using the Steiner tree problem graph (stpg).
    2. A spanning tree is generated from the induced subgraph.
    3. If a randomly generated number is less than p_prune, the spanning tree is pruned using the terminal nodes.
    '''

    def __init__(self, stpg:SteinerGraphProblemInstance, spanning_method='prim'):
        """
        Initializes the mutation instance for a Steiner Graph Problem.
        Args:
            stpg (SteinerGraphProblemInstance): The Steiner graph problem instance.
            spanning_method (str, optional): The method to generate the spanning tree.
                Options are:
                - 'prim': Uses Prim RST algorithm.
                - 'kruskal': Uses Kruskal RST algorithm.
                - 'boruvka': Uses Boruvka RST algorithm.
                - 'random_walk': Uses a random walk algorithm.
                Defaults to 'prim'.
        Raises:
            ValueError: If an unknown method is provided.
        """

        self.terminals = stpg.terminals.copy()
        self.spanning_method = spanning_method

        if self.spanning_method == 'prim':
            self.spanning_tree_func = prim_random_spanning_tree

        elif self.spanning_method == 'kruskal':
            self.spanning_tree_func = kruskal_random_spanning_tree

        elif self.spanning_method == 'boruvka':
            self.spanning_tree_func = boruvka_random_spanning_tree

        elif self.spanning_method == 'random_walk':
            self.spanning_tree_func = random_walk_spanning_tree

        else:
            raise ValueError(f"Unknown method: {self.spanning_method}")

    def __call__(self, tree:Graph, p_prune=0.0):
        """
        Call the mutation operator for a given tree.
        Args:
            tree (Graph): The input graph to be mutated.
            p_prune (float, optional): Probability of pruning the tree. Defaults to 0.0.
            *args: Additional arguments.
            **kwds: Additional keyword arguments.
        Returns:
            Graph: The mutated tree.
        """

        subgraph = induced_subgraph(tree, self.stpg)
        tree = self.spanning_tree_func(subgraph)

        if random.random() < p_prune:
            tree = pruning_tree(tree, self.terminals)

        return tree


class ReplaceRandomEdge:

    def __init__(self, stpg:SteinerGraphProblemInstance):
        self.stpg = stpg
        self.terminals = stpg.terminals.copy()

    def __call__(self, tree:Graph, n_replace=3, p_prune=0.0):

        edges = list(tree.edges())
        if not (1 <= n_replace <= len(edges)):
            raise ValueError(f'Number of replaceable edge should be between 1 and {len(edges)}. Value: {n_replace=}')

        to_remove = set(random.sample(edges, k=n_replace))
        assert len(to_remove) == n_replace

        ds = DisjointSet()
        offspring = Graph()

        for v in tree.nodes():
            ds.make_set(v)
            offspring.add_node(v)

        for edge in tree.edges():
            if edge not in to_remove:
                offspring.add_edge(edge)
                ds.union(edge.x, edge.y)

        counter = 0
        subedges = (e
                    for e in self.stpg.edges()
                    if (tree.has_node(e.x))
                    and (tree.has_node(e.y))
                    and (not offspring.has_edge(e))
                ) # end
        for edge in subedges:
            if ds.find(edge.x) == ds.find(edge.y):
                continue
            elif offspring.has_edge(edge):
                # continue
                assert False, 'A função não deveria cair nessa condição'
            else:
                offspring.add_edge(edge)
                ds.union(edge.x, edge.y)
                counter += 1
            if counter >= n_replace:
                break

        if counter < n_replace:
            for edge in to_remove:
                if ds.find(edge.x) != ds.find(edge.y):
                    offspring.add_edge(edge)
                    ds.union(edge.x, edge.y)
                    counter += 1
                if counter >= n_replace:
                    break

        if random.random() < p_prune:
            offspring = pruning_tree(offspring, self.terminals)

        return offspring


def random_key_path(T:Graph, G:Graph):
    pass

class RandomKeyPath:

    def __init__(self, stpg:SteinerGraphProblemInstance):
        self.stpg = stpg

    def __call__(self,tree:Graph):
        pass


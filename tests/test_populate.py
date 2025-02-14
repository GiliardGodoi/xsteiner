
from xsteiner.disjointset.disjointset import DisjointSet
from xsteiner.graph.graph import (
    Graph,
    SteinerGraphProblemInstance,
)
from xsteiner.evol.populate import (
    PrimRSTPopulation,
    KruskalRSTPopulation,
    RandomWalkRSPPopulation,
    BoruvkaRSTPolulation
)

def test_kruskal_random_spanning_tree(bigger:SteinerGraphProblemInstance):
    generator = KruskalRSTPopulation(bigger)
    trees = [generator(p_prune=1.0) for _ in range(10)]
    assert len(trees) == 10


def test_prim_random_spanning_tree(bigger:SteinerGraphProblemInstance):
    generator = PrimRSTPopulation(bigger)
    trees = [generator(p_prune=1.0) for _ in range(10)]
    assert trees

def test_random_walk_spanning_tree(bigger:SteinerGraphProblemInstance):
    generator = RandomWalkRSPPopulation(bigger)
    trees = [generator(p_prune=1.0) for _ in range(10)]
    assert trees

#
def test_boruvka_random_spanning_tree(bigger:SteinerGraphProblemInstance):
    generator = BoruvkaRSTPolulation(bigger)
    trees = [generator(p_prune=1.0) for _ in range(10)]
    assert trees
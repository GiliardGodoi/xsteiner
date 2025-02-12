from operator import attrgetter
from xsteiner.graph.graph import Graph

def normalize(population, key='cost'):

    higher_cost_individual = max(population, key=attrgetter(key))
    for individual in population:
        individual.fitness = higher_cost_individual.cost - individual.cost

    return population

def evaluate_tree(tree: Graph):
    total = sum(e.weight for e in tree.edges())
    return total
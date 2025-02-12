from random import choices
from operator import attrgetter

def roullete(individuals, n_parents=None, weighted=True):

    if not n_parents: n_parents = len(individuals)

    if weighted:
        fitnesses = [p.fitness for p in individuals if p.is_evaluated()]
    else:
        fitnesses = None

    return choices(individuals, weights=fitnesses, k=n_parents)

def tournament(individuals,
               n_competitors=2,
               maximize=True,
               n_parents=None,
               key_attr='fitness'
            ):

    if not n_parents:
        n_parents = len(individuals)

    assert n_competitors < len(individuals) // 4, f"you must set less than {(len(individuals) // 4)} competitors for {len(individuals)} individuals"

    contest = max if maximize else min

    selected = list()
    while len(selected) < n_parents:
        competitors = choices(individuals, k=n_competitors)
        selected.append(contest(competitors, key=attrgetter(key_attr)))

    return selected
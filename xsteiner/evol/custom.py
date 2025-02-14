import itertools as it
from copy import copy
from evol.population import BasePopulation
from evol.utils import select_arguments
from typing import (
    Any,
    Callable,
    Generator,
    Iterable,
    List,
    Optional,
    Sequence,
    Union
)
from xsteiner.evol.individual import Individual

def custom_offspring_generator( parents: List[Individual],
                                parent_picker: Callable[..., Union[Individual, Sequence]],
                                combiner: Callable[..., Any],
                                **kwargs
                            ) -> Generator[Individual]:

    while True:
        selected_parents = parent_picker(parents, **kwargs)
        if isinstance(selected_parents, Individual):
            chromosomes = (selected_parents.chromosome,)
        else:
            chromosomes = tuple(individual.chromosome for individual in selected_parents)
        # Create children
        combined = combiner(*chromosomes, **kwargs)
        if isinstance(combined, Generator):
            for child in combined:
                yield Individual(chromosome=child)
        else:
            yield Individual(chromosome=combined)



class CustomPopulation(BasePopulation):
    """Population of Individuals

    :param chromosomes: Iterable of initial chromosomes of the Population.
    :param eval_function: Function that reduces a chromosome to a fitness.
    :param maximize: If True, fitness will be maximized, otherwise minimized.
        Defaults to True.
    :param generation: Generation of the Population. This is incremented after
        each breed call. Defaults to 0.
    :param intended_size: Intended size of the Population. The population will
        be replenished to this size by .breed(). Defaults to the number of
        chromosomes provided.
    :param checkpoint_target: Target for the serializer of the Population. If
        a serializer is provided, this target is ignored. Defaults to None.
    :param serializer: Serializer for the Population. If None, a new
        SimpleSerializer is created. Defaults to None.
    :param concurrent_workers: If > 1, evaluate individuals in {concurrent_workers}
        separate processes. If None, concurrent_workers is set to n_cpus. Defaults to 1.
    """

    def __init__(self,
                 chromosomes: Iterable,
                 eval_function: Callable[..., float],
                 maximize: bool = True,
                 generation: int = 0,
                 intended_size: Optional[int] = None,
                 checkpoint_target: Optional[str] = None,
                 serializer=None,
                 concurrent_workers: Optional[int] = 1):
        super().__init__(chromosomes=[],
                         eval_function=eval_function,
                         checkpoint_target=checkpoint_target,
                         concurrent_workers=concurrent_workers,
                         maximize=maximize,
                         generation=generation,
                         intended_size=intended_size,
                         serializer=serializer)

        self.individuals = [Individual(chromosome=chromosome) for chromosome in chromosomes]

    def __copy__(self):
        result = self.__class__(chromosomes=[],
                                eval_function=self.eval_function,
                                maximize=self.maximize,
                                serializer=self.serializer,
                                intended_size=self.intended_size,
                                generation=self.generation,
                                concurrent_workers=1)  # Prevent new pool from being made
        result.individuals = [copy(individual) for individual in self.individuals]
        result.concurrent_workers = self.concurrent_workers
        result.pool = self.pool
        result.documented_best = self.documented_best
        result.id = self.id
        return result

    def evaluate(self, lazy: bool = False):
        """Evaluate the individuals in the population.

        This evaluates the fitness of all individuals. If lazy is True, the
        fitness is only evaluated when a fitness value is not yet known. In
        most situations adding an explicit evaluation step is not needed, as
        lazy evaluation is implicitly included in the operations that need it
        (most notably in the survive operation).

        :param lazy: If True, do no re-evaluate the fitness if the fitness is known.
        :return: self
        """
        if self.pool:
            f = self.eval_function  # We cannot refer to self in the map
            scores = self.pool.map(lambda i: i.fitness if (i.fitness and lazy) else f(i.chromosome), self.individuals)
            for individual, fitness in zip(self.individuals, scores):
                individual.fitness = fitness
        else:
            for individual in self.individuals:
                individual.evaluate(eval_function=self.eval_function, lazy=lazy)
        self._update_documented_best()
        return self

    def breed(self,
            parent_picker: Callable[..., Sequence[Individual]],
            combiner: Callable,
            population_size: Optional[int] = None,
            **kwargs) -> BasePopulation:
        if population_size:
            self.intended_size = population_size
        offspring = custom_offspring_generator(parents=self.individuals,
                                        parent_picker=select_arguments(parent_picker),
                                        combiner=select_arguments(combiner),
                                        **kwargs)
        self.individuals += list(it.islice(offspring, self.intended_size - len(self.individuals)))
        self.generation += 1
        return self
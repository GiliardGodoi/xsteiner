import random
from typing import (
    Callable,
    Any,
    Optional
)

class Individual:
    """
    Represents an individual in an evolutionary algorithm.
    Attributes:
        _instance_count (int): Class variable to keep track of the number of instances created.
        _forma (any): The representation of the individual.
        _cost (float or None): The cost associated with the individual, initially None.
        _fitness (float or None): The fitness value of the individual, initially None.
        id (int): Sequential identifier for the individual instance.
    Methods:
        get_instance_count(): Class method to get the current instance count.
        cost: Property to get or set the cost of the individual.
        fitness: Property to get or set the fitness of the individual.
        forma: Property to get or set the representation of the individual.
        tree: Property to get or set the representation of the individual (alias for forma).
        evaluate(eval_func, *args, **kargs): Evaluates the individual using the provided evaluation function.
        is_evaluated(): Checks if the individual has been evaluated.
    """

    _instance_count = 0

    def __init__(self, chromosome: Any, fitness: Optional[float] = None):
        self._chromosome = chromosome
        self._cost = fitness
        self._fitness = fitness
        self.age = 0
        Individual._instance_count += 1
        self.id = Individual._instance_count

    def __repr__(self):
        return f"<individual id:{self.id} fitness:{self.fitness}>"

    @classmethod
    def from_dict(cls, data: dict) -> 'Individual':
        """Load an Individual from a dictionary.

        :param data: Dictionary containing the keys 'age', 'chromosome', 'fitness' and 'id'.
        :return: Individual
        """
        result = cls(chromosome=data['chromosome'], fitness=data['fitness'])
        result.age = data['age']
        result.id = data['id']
        return result

    @classmethod
    def get_instance_count(cls):
        return cls._instance_count

    def __post_evaluate(self, result: float):
        self.fitness = result

    @property
    def cost(self):
        if self._cost is None:
            raise ValueError(f'Individual not evaluated yet. Id: {self.seq_id}')
        return self._cost

    @cost.setter
    def cost(self, value):
        self._cost = value
        self._fitness = value

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, value):
        self._fitness = value

    @property
    def chromosome(self):
        return self._chromosome

    @chromosome.setter
    def chromosome(self, value):
        self._chromosome = value
        self._cost = None
        self._fitness = None

    @property
    def tree(self):
        return self._chromosome

    @tree.setter
    def chromosome(self, value):
        self._chromosome = value
        self._cost = None
        self._fitness = None

    def evaluate(self, eval_function, *args, lazy=False, **kargs):
        self._cost = eval_function(self._chromosome, *args, **kargs)
        self._fitness = self._cost

    def is_evaluated(self):
        return not (self._cost is None)

    def mutate(self, mutate_function: Callable[..., Any], probability: float = 1.0, **kwargs):
        """Mutate the chromosome of the individual.

        :param mutate_function: Function that accepts a chromosome and returns a mutated chromosome.
        :param probability: Probability that the individual mutates.
            The function is only applied in the given fraction of cases.
            Defaults to 1.0.
        :param kwargs: Arguments to pass to the mutation function.
        """
        if probability == 1.0 or random.random() < probability:
            self.chromosome = mutate_function(self.chromosome, **kwargs)

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

    def __init__(self, representation):
        self._forma = representation
        self._cost = None
        self._fitness = None
        Individual._instance_count += 1
        self.seq_id = Individual._instance_count

    @classmethod
    def get_instance_count(cls):
        return cls._instance_count

    @property
    def cost(self):
        if self._cost is None:
            raise ValueError(f'Individual not evaluated yet. Id: {self.seq_id}')
        return self._cost

    @cost.setter
    def cost(self, value):
        self._cost = value

    @property
    def fitness(self):
        if self._fitness is None:
            raise ValueError(f'Individual not evaluated yet. Id: {self.seq_id}')
        return self.__fitness

    @fitness.setter
    def fitness(self, value):
        self._fitness = value

    @property
    def forma(self):
        return self._forma

    @forma.setter
    def forma(self, value):
        self._forma = value
        self._cost = None
        self._fitness = None

    @property
    def tree(self):
        return self._forma

    @tree.setter
    def forma(self, value):
        self._forma = value
        self._cost = None
        self._fitness = None

    def evaluate(self, eval_func, *args, **kargs):
        self._cost = eval_func(self._forma, *args, **kargs)
        self._fitness = self._cost

    def is_evaluated(self):
        return not (self._cost is None)
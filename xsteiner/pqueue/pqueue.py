# -*- coding: utf-8 -*-
from heapq import heapify, heappop, heappush
import itertools


class PriorityQueue:
    """
    Priority Queue implementation

    There is a tradeoff between speed and memory.

    In this implementations we've choosed the solution presented in official documentation for heapq module.
    More details in <https://docs.python.org/3/library/heapq.html>

    """

    def __init__(self):
        self.queue = list()
        heapify(self.queue)
        self.REMOVED = "<removed>"
        self.entries_finder = dict()
        self.counter = itertools.count()

    def __contains__(self, label):
        return label in self.entries_finder

    def __len__(self):
        return len(self.entries_finder)

    def __bool__(self):
        return bool(self.entries_finder)

    def __str__(self):
        return f"PQueue({len(self.queue)})"

    def push(self, priority, item):
        """
        Insere um elemento na fila de prioridade.
        @paramns: priority <int> e item <vértice> do grafo
        """

        if item in self.entries_finder:
            self.__mark_remove(item)

        seq = next(self.counter)
        entry = [priority, seq, item]
        self.entries_finder[item] = entry
        heappush(self.queue, entry)
        return item

    def pop(self):
        """
        Retorna o menor <item> elemento da fila de prioridade.
        """
        while self.queue:
            # priority, seq, item = heappop(self.queue)
            priority, _, item = heappop(self.queue)
            if item is not self.REMOVED:
                del self.entries_finder[item]
                return priority, item

    def __mark_remove(self, item):
        entry = self.entries_finder.pop(item)
        entry[-1] = self.REMOVED  ## marca a última posição como REMOVED

    def empty(self):
        return len(self.entries_finder) == 0

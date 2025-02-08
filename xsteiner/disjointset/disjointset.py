# -*- coding: utf-8 -*-
"""
A Python implementation for the disjoint set data structure.
"""
from collections import defaultdict


class Subset:
    def __init__(self, vertice, rank=0):
        self.parent = vertice
        self.rank = rank


class DisjointSet:
    def __init__(self):
        self.subsets = defaultdict()

    def __contains__(self, item):
        return item in self.subsets

    def __len__(self):
        return len(self.subsets)

    def __bool__(self):
        return bool(self.subsets)

    def __link__(self, v, u):
        if self.subsets[u].rank > self.subsets[v].rank:
            self.subsets[v].parent = self.subsets[u].parent

        elif self.subsets[v].rank > self.subsets[u].rank:
            self.subsets[u].parent = self.subsets[v].parent

        else:
            self.subsets[v].parent = u
            self.subsets[u].rank += 1

    def make_set(self, item):
        if item in self.subsets:
            raise ValueError(f"Key <{item!r}> already exist")

        self.subsets[item] = Subset(item)
        return item

    def find(self, item):
        if item not in self.subsets:
            raise ValueError(f"There is no subset for {item}")

        if self.subsets[item].parent != item:
            self.subsets[item].parent = self.find(self.subsets[item].parent)

        return self.subsets[item].parent

    def union(self, a, b):
        self.__link__(self.find(a), self.find(b))

    def get_sets(self):

        disjointed = defaultdict(set)
        for key in self.subsets.keys():
            parent = self.find(key)
            disjointed[parent].add(key)

        return disjointed

    def parents_components(self):
        components = defaultdict(set)
        for key in self.subsets.keys():
            parent = self.find(key)
            components[parent].add(key)

        return components

    def disjoint_components(self):
        components = self.parents_components()
        return list(components.values())

    def parents(self):
        return set([self.find(item) for item in self.subsets.keys()])

    def item_component(self, item):
        if item not in self.subsets:
            raise ValueError(f"There is no subset for {item}")

        component = set([item])
        for key in self.subsets.keys():
            if self.find(item) == self.find(key):
                component.add(key)

        return component
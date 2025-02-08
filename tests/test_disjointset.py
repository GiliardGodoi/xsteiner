from xsteiner.disjointset import DisjointSet

import random
import pytest
from pytest import fixture, mark
from string import ascii_uppercase as symbols
from itertools import combinations, product


@fixture
def example():
    return DisjointSet()


def test_contains_method(example):

    assert not ("A" in example)

    example.make_set("A")

    assert "A" in example
    assert not (1 in example)


def test_len_method(example):
    assert len(example) == 0

    for i in range(100):
        example.make_set(i)

    assert len(example) == 100

    i = 0
    for j in range(i + 1, 100):
        example.union(i, j)
        i = j

    assert len(example) == 100


def test_bool_method(example):

    assert not bool(example)

    for i in range(1, 101):  # arbitrary values
        j = example.make_set(i)
        assert i == j

    assert bool(example)


@mark.parametrize("number_elements", [100, 10_000, 100_000])
def test_make_set_method(number_elements):
    dset = DisjointSet()

    for i in range(number_elements):
        dset.make_set(i)

    assert len(dset) == number_elements


def test_insert_an_element_again(example):

    elements = list()
    for i in range(10_000):
        elements.append(i)
        example.make_set(i)

    random_elemnt = random.choice(elements)

    with pytest.raises(ValueError):
        example.make_set(random_elemnt)


@mark.parametrize("number_elements", [100, 10_000, 100_000])
def test_union_method_with_numeric_values(number_elements):
    dset = DisjointSet()

    max_range = number_elements + 1

    for i in range(1, max_range):  # arbitrary values
        j = dset.make_set(i)
        assert i == j

    i = 2
    for j in range((i + 2), max_range, 2):
        dset.union(i, j)  # even numbers
        i = j

    i = 1
    for j in range((i + 2), max_range, 2):
        dset.union(i, j)  # even numbers
        i = j

    assert len(dset) == number_elements

    random_element = 4

    assert random_element in dset, f"{random_element=} should be in the disjoint set"
    assert not (max_range in dset), "this value shouldn't belong to disjoint set"

    flatted_sets = dset.get_sets()

    assert len(flatted_sets) == 2

    assert dset.find(24) % 2 == 0
    assert dset.find(25) % 2 == 1


def test_union_with_string_values(example):

    elements = list()
    for letters in combinations(symbols, 3):
        key = "".join(letters)
        example.make_set(key)
        elements.append(key)

    assert len(example) == len(elements)

    random.shuffle(elements)

    counter = 0
    for a, b in product(elements, repeat=2):
        counter += 1
        if a[0] == b[0]:
            example.union(a, b)

    assert len(example.get_sets()) == (len(symbols) - 2)


def test_union_with_tuple_values(example):

    elements = list()
    for key in combinations(symbols, 3):
        example.make_set(key)
        elements.append(key)

    assert len(example) == len(elements)

    random.shuffle(elements)

    counter = 0
    for a, b in product(elements, repeat=2):
        counter += 1
        if a[0] == b[0]:
            example.union(a, b)

    assert len(example.get_sets()) == (len(symbols) - 2)

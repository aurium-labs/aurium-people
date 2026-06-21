"""Profiles collection: indexing, iteration, subset extraction, edge cases."""

import pytest

from aurium_people import Profiles, Profile


def test_len_and_indexing():
    people = Profiles(3, seed=1)
    assert len(people) == 3
    assert isinstance(people[0], Profile)
    assert people[1] is people[1]  # stable references


def test_iteration():
    people = Profiles(4, seed=2)
    names = [p.first_name for p in people]
    assert len(names) == 4
    assert all(isinstance(n, str) for n in names)


def test_only_returns_list_of_dicts():
    people = Profiles(3, seed=5)
    subset = people.only("first_name", "email")
    assert len(subset) == 3
    for row in subset:
        assert set(row.keys()) == {"first_name", "email"}


def test_to_list_full_serialization():
    people = Profiles(2, seed=8)
    rows = people.to_list()
    assert len(rows) == 2
    assert "first_name" in rows[0]
    assert "ssn" in rows[0]


def test_empty_batch():
    people = Profiles(0, seed=1)
    assert len(people) == 0
    assert list(people) == []
    assert people.only("first_name") == []


def test_negative_count_raises():
    with pytest.raises(ValueError):
        Profiles(-1, seed=1)


def test_unknown_field_raises():
    p = Profile(seed=1)
    with pytest.raises(ValueError):
        p.only("not_a_field")


def test_repr():
    people = Profiles(2, seed=9)
    assert "count=2" in repr(people)
    assert "seed=9" in repr(people)

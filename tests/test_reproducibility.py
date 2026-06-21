"""Reproducibility: seeded profiles and batches must be deterministic."""

from aurium_people import Profile, Profiles


def test_same_seed_same_profile():
    a = Profile(seed=42).to_dict()
    b = Profile(seed=42).to_dict()
    assert a == b


def test_different_seeds_different_profile():
    a = Profile(seed=1).to_dict()
    b = Profile(seed=2).to_dict()
    assert a != b


def test_unseeded_profiles_differ():
    # Two unseeded profiles should (with overwhelming probability) differ.
    a = Profile().to_dict()
    b = Profile().to_dict()
    assert a != b


def test_batch_reproducible():
    a = Profiles(10, seed=7).to_list()
    b = Profiles(10, seed=7).to_list()
    assert a == b


def test_batch_seeds_offset_so_profiles_differ():
    people = Profiles(5, seed=100)
    names = [p.first_name for p in people]
    # The 5 profiles should not all be identical.
    assert len(set(names)) > 1


def test_seed_property():
    assert Profiles(3, seed=5).seed == 5
    assert Profiles(3).seed is None

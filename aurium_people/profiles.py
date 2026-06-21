"""The ``Profiles`` collection — a batch of coherent profiles.

``Profiles(count, seed=...)`` eagerly generates ``count`` coherent profiles.
The collection behaves like a list (indexing, iteration, len) and supports
subset extraction via ``.only()``.

Reproducibility: when ``seed`` is set, profile ``i`` is generated with seed
``seed + i``, so the whole batch is reproducible.
"""

from typing import Iterator

from .profile import Profile

__all__ = ["Profiles"]


class Profiles:
    """A collection of generated ``Profile`` instances.

        >>> people = Profiles(5, seed=10)
        >>> len(people)
        5
        >>> people[0].first_name
        'Maria'
        >>> people.only("first_name", "email")[0]
        {'first_name': 'Maria', 'email': 'maria.smith23@gmail.com'}

    Args:
        count: Number of profiles to generate.
        seed: Optional base seed for reproducibility. Profile ``i`` uses seed
            ``seed + i``. None = random (non-reproducible).
        **gen_kwargs: Forwarded to ``Profile`` (e.g. ``min_age``, ``max_age``,
            ``force_employment_status``).
    """

    def __init__(self, count: int, seed: int | None = None, **gen_kwargs) -> None:
        if count < 0:
            raise ValueError(f"count must be non-negative, got {count}")

        self._seed = seed
        self._profiles: list[Profile] = [
            Profile(seed=(None if seed is None else seed + i), **gen_kwargs)
            for i in range(count)
        ]

    @property
    def seed(self) -> int | None:
        """The base seed (None if unseeded)."""
        return self._seed

    def __getitem__(self, index: int) -> Profile:
        return self._profiles[index]

    def __iter__(self) -> Iterator[Profile]:
        return iter(self._profiles)

    def __len__(self) -> int:
        return len(self._profiles)

    def only(self, *fields: str) -> list[dict]:
        """Return a list of dicts, each containing only the requested fields.

        Applied across every profile in the collection.
        """
        return [p.only(*fields) for p in self._profiles]

    def to_list(self) -> list[dict]:
        """Serialize every profile to a dict."""
        return [p.to_dict() for p in self._profiles]

    def __repr__(self) -> str:
        return f"Profiles(count={len(self)}, seed={self._seed!r})"

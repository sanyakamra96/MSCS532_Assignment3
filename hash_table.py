"""Separate-chaining hash table with universal hashing for integer keys.

Supports integer keys (including negative integers) and arbitrary Python values.
A randomized member of h_{a,b}(k) = ((a*k + b) mod p) mod m is selected on init.
"""
from __future__ import annotations

import random
from typing import Any


class ChainedHashTable:
    PRIME = 2**61 - 1

    def __init__(self, capacity: int = 8, max_load: float = 0.75,
                 seed: int | None = None) -> None:
        if capacity < 1:
            raise ValueError("capacity must be positive")
        if not 0 < max_load < 1:
            raise ValueError("max_load must be between 0 and 1")
        self._minimum_capacity = capacity
        self._buckets: list[list[tuple[int, Any]]] = [[] for _ in range(capacity)]
        self._size = 0
        self._max_load = max_load
        rng = random.Random(seed)
        self._a = rng.randrange(1, self.PRIME)
        self._b = rng.randrange(self.PRIME)

    def __len__(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        return len(self._buckets)

    @property
    def load_factor(self) -> float:
        return self._size / self.capacity

    def _index(self, key: int) -> int:
        if not isinstance(key, int):
            raise TypeError("keys must be integers")
        return ((self._a * key + self._b) % self.PRIME) % self.capacity

    def _resize(self, new_capacity: int) -> None:
        old_buckets = self._buckets
        self._buckets = [[] for _ in range(new_capacity)]
        for bucket in old_buckets:
            for key, value in bucket:
                self._buckets[self._index(key)].append((key, value))

    def insert(self, key: int, value: Any) -> None:
        bucket = self._buckets[self._index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return
        if (self._size + 1) / self.capacity > self._max_load:
            self._resize(self.capacity * 2)
            bucket = self._buckets[self._index(key)]
        bucket.append((key, value))
        self._size += 1

    def search(self, key: int) -> Any:
        for existing_key, value in self._buckets[self._index(key)]:
            if existing_key == key:
                return value
        raise KeyError(key)

    def delete(self, key: int) -> None:
        bucket = self._buckets[self._index(key)]
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket.pop(i)
                self._size -= 1
                if self.capacity > self._minimum_capacity and self.load_factor < 0.20:
                    self._resize(max(self._minimum_capacity, self.capacity // 2))
                return
        raise KeyError(key)

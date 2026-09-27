"""Randomized and first-pivot deterministic three-way quicksort implementations.

Three-way partitioning keeps duplicate-heavy inputs efficient.  Both functions
return sorted copies and do not mutate the input sequence.
"""
from __future__ import annotations

import random
from typing import Sequence, TypeVar

T = TypeVar("T")


def _quicksort(values: Sequence[T], *, randomized: bool, seed: int | None = None) -> list[T]:
    arr = list(values)
    rng = random.Random(seed)
    if len(arr) < 2:
        return arr

    # An explicit stack avoids Python's recursion limit on adversarial inputs.
    stack = [(0, len(arr) - 1)]
    while stack:
        lo, hi = stack.pop()
        while lo < hi:
            pivot = arr[rng.randint(lo, hi)] if randomized else arr[lo]
            lt, i, gt = lo, lo, hi
            while i <= gt:
                if arr[i] < pivot:
                    arr[lt], arr[i] = arr[i], arr[lt]
                    lt += 1
                    i += 1
                elif arr[i] > pivot:
                    arr[i], arr[gt] = arr[gt], arr[i]
                    gt -= 1
                else:
                    i += 1
            # Process the smaller side first; stack the larger one.
            left = (lo, lt - 1)
            right = (gt + 1, hi)
            left_size = left[1] - left[0] + 1
            right_size = right[1] - right[0] + 1
            if left_size < right_size:
                if right[0] < right[1]:
                    stack.append(right)
                lo, hi = left
            else:
                if left[0] < left[1]:
                    stack.append(left)
                lo, hi = right
    return arr


def randomized_quicksort(values: Sequence[T], seed: int | None = None) -> list[T]:
    """Return a sorted copy, choosing each pivot uniformly at random."""
    return _quicksort(values, randomized=True, seed=seed)


def deterministic_quicksort(values: Sequence[T]) -> list[T]:
    """Return a sorted copy, choosing the first element of each subarray."""
    return _quicksort(values, randomized=False)

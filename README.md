# MSCS532 Assignment 3 — Algorithm Efficiency and Scalability

**Student:** Sanya Kamra  
**Course:** MSCS-532 Algorithms and Data Structures

This repository contains implementations and analysis of randomized Quicksort, first-element-pivot deterministic Quicksort, and a separate-chaining hash table with integer keys.

## Requirements

Python 3.10+; standard library only (no pip dependencies).

## Project files

- `quicksort.py` — both three-way Quicksort implementations.
- `hash_table.py` — chaining hash table with randomized universal-style hashing and resizing.
- `benchmark.py` — reproducible four-distribution, five-size, five-trial comparison.
- `test_algorithms.py` — correctness and edge-case unit tests.
- `results/timings.csv` — recorded experimental measurements.
- `REPORT.md` — theoretical derivation, results table, interpretation and references.

## Run on macOS or any terminal

```bash
python3 -m unittest -v
python3 benchmark.py
```

The benchmark overwrites `results/timings.csv` with measurements from your own machine; it prints means for both versions to the terminal. `python3` can be replaced with `python` if that is how Python is installed.

## Basic use

```python
from quicksort import randomized_quicksort, deterministic_quicksort
from hash_table import ChainedHashTable

print(randomized_quicksort([4, 2, 4, 1], seed=532))  # [1, 2, 4, 4]
print(deterministic_quicksort([4, 2, 4, 1]))     # [1, 2, 4, 4]

h = ChainedHashTable(seed=532)
h.insert(42, "answer")
print(h.search(42))  # answer
h.insert(42, "updated")
h.delete(42)
```

## Findings

Randomized Quicksort has expected Theta(n log n) runtime on distinct keys; first-element pivot selection is vulnerable to input ordering. Three-way partitioning makes both versions efficient on duplicate-heavy data. The hash table has expected Theta(1 + alpha) lookup, insert and delete operations under simple uniform hashing, with alpha = entries / buckets and occasional Theta(n) rehashing during growth or shrinkage. See `REPORT.md` for the full analysis and measurements.

**Notes:** The hash table intentionally supports integer keys only. Run `benchmark.py` on your own computer if you want timing results reflecting that hardware. The included CSV was generated in a separate execution environment.

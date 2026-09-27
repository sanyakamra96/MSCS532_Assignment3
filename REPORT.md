# Assignment 3: Understanding Algorithm Efficiency and Scalability

**Course:** MSCS-532 Algorithms and Data Structures  
**Student:** Sanya Kamra  
**Project:** Randomized Quicksort and Hashing with Chaining

## 1. Randomized Quicksort: Implementation

`quicksort.py` implements randomized and deterministic Quicksort. The randomized version chooses an index uniformly from the **current** subarray using `randint(lo, hi)`. The deterministic version takes the first element of the subarray. Both versions use Dutch-national-flag (three-way) partitioning: elements less than the pivot, equal to the pivot, and greater than the pivot. The implementations return new lists, preserve their inputs, handle empty/singleton lists, duplicates and negative values, and use an explicit stack rather than recursive Python calls. Each partition scans its subarray in linear time. The explicit stack, with the smaller partition processed immediately, uses O(log n) auxiliary stack space; the copied input uses O(n) additional space.

## 2. Why Randomized Quicksort Has Expected O(n log n) Time

Assume initially that the n input keys are distinct. Label the sorted keys z_1 < z_2 < ... < z_n. Define X_ij as 1 if z_i and z_j are compared directly by the algorithm, and 0 otherwise. The two keys are compared exactly when the first pivot selected from the rank interval [i, j] is one of those two keys. Because pivots are uniformly selected, P(X_ij = 1) = 2/(j-i+1). By linearity of expectation, the expected number of comparisons is:

E[C_n] = sum_{1 <= i < j <= n} E[X_ij]
       = sum_{i<j} 2/(j-i+1)
       = 2 sum_{d=1}^{n-1} (n-d)/(d+1)
       = 2(n+1)H_n - 4n,

where H_n = sum_{k=1}^n 1/k is the nth harmonic number. Since H_n = Theta(log n), E[C_n] = Theta(n log n). Each partition performs linear work in the subarray length, so this also establishes expected Theta(n log n) runtime under the standard unit-cost comparison model. Equivalently, one can write E[T(n)] = (1/n) sum_{k=0}^{n-1}(E[T(k)] + E[T(n-k-1)]) + Theta(n), which solves to Theta(n log n).

**Important implementation nuance:** The exact comparison-count formula above is for the conventional distinct-key, two-way comparison model. Our three-way implementation makes additional branch comparisons per inspected element, but has the same expected Theta(n log n) complexity for distinct keys. Three-way partitioning can do better when many keys are equal. Randomization does **not** eliminate the quadratic worst case: consistently extreme pivots still yield O(n²) runtime, although that pivot pattern becomes unlikely on large distinct-key arrays.

## 3. Empirical Quicksort Comparison

### Method

`benchmark.py` generates distinct random arrays sampled without replacement, increasing arrays, decreasing arrays, and arrays with ten possible values. Sizes are 100, 500, 1,000, 2,000, and 4,000. Five timed trials run for each size/distribution/algorithm combination. The same input is used for both algorithms within each trial, and outputs are asserted equal to Python's `sorted`. The script records mean, median, minimum and maximum wall-clock duration in milliseconds using `time.perf_counter_ns`. Input generation and correctness verification are **outside** the measured interval. Random number generators use fixed seeds, although execution times still depend on CPU and system load.

### Recorded results: mean runtime in milliseconds

| Distribution | n | Randomized | First-element deterministic |
|---|---:|---:|---:|
| Random | 100 | 0.2033 | 0.1418 |
| Random | 500 | 1.1947 | 0.9207 |
| Random | 1,000 | 2.7784 | 2.3669 |
| Random | 2,000 | 6.1305 | 5.1771 |
| Random | 4,000 | 13.3665 | 11.2119 |
| Sorted | 100 | 0.1840 | 0.2095 |
| Sorted | 500 | 1.1270 | 2.1483 |
| Sorted | 1,000 | 2.6552 | 6.3664 |
| Sorted | 2,000 | 5.8700 | 18.2254 |
| Sorted | 4,000 | 13.6247 | 52.9568 |
| Reverse | 100 | 0.2284 | 0.7825 |
| Reverse | 500 | 1.7114 | 23.3570 |
| Reverse | 1,000 | 3.3046 | 79.2380 |
| Reverse | 2,000 | 6.5269 | 369.8218 |
| Reverse | 4,000 | 16.5627 | 1453.1326 |
| Repeated | 100 | 0.0932 | 0.0634 |
| Repeated | 500 | 0.3444 | 0.3010 |
| Repeated | 1,000 | 1.0813 | 0.9005 |
| Repeated | 2,000 | 1.4180 | 1.0436 |
| Repeated | 4,000 | 2.1658 | 2.2737 |

The complete recorded data, including medians and ranges, are in `results/timings.csv`.

### Interpretation

For randomly ordered **distinct** inputs, both versions generally exhibit n log n scaling. The deterministic version is somewhat faster in this measurement because selecting a random pivot adds random-number-generator overhead and the random inputs do not systematically disadvantage the first-pivot choice. This does not mean deterministic first-pivot Quicksort has a better worst-case bound.

For sorted and reverse-sorted arrays, deterministic first-pivot choice can create highly unbalanced partitions. Reverse-sorted arrays show the clearest quadratic-like growth in this benchmark: at n = 4,000, deterministic execution takes about 1,453 ms versus 16.56 ms for randomized execution. **The deterministic sorted-array timings are less extreme than a textbook naive first-pivot Quicksort:** in-place three-way partitioning rearranges values during scanning, so it can disrupt the initial order of recursive subproblems. It remains sensitive to input ordering, but its exact timings depend on partition implementation.

Repeated-element arrays are fast with *both* variants because three-way partitioning removes the entire equal-key group from further partitioning. The standard distinct-key analysis therefore does not predict their exact runtime. Small samples, interpreter overhead, timing noise, and the randomized pivot's extra work can reverse small timing differences; reproducibility is improved by five trials and reporting both mean and median, but stronger claims would require larger trials and additional machines.

## 4. Hashing with Chaining: Implementation

`hash_table.py` implements a hash table for **integer keys**, including negative keys, with arbitrary Python values. Each bucket is a Python list of `(key, value)` pairs. The initialized hash function is selected at random from the family

h_(a,b)(k) = ((a k + b) mod p) mod m,

where p = 2^61 - 1, a is uniform in {1,...,p-1}, b is uniform in {0,...,p-1}, and m is the current number of buckets. This is based on a universal hashing construction over integer keys considered modulo p; keys congruent modulo p cannot be distinguished by this hash family. The reduction to arbitrary m can also introduce small distribution differences. A prime modulus larger than the expected bounded key universe is preferable when strict theoretical universality assumptions are required.

- `insert(key, value)`: updates an existing key or appends a new pair.
- `search(key)`: returns the associated value or raises `KeyError` when absent, distinguishing absence from a stored `None`.
- `delete(key)`: removes a key or raises `KeyError` when absent.

The table doubles the bucket count **before** a new insertion would exceed a 0.75 load factor. It halves the bucket count when the load factor falls below 0.20, subject to the initial minimum capacity. On resize, stored entries are rehashed because m changes; all original key-value associations remain intact.

## 5. Expected Complexity and Load Factor

Define the load factor alpha = n/m, where n is the number of stored entries and m is the number of bucket slots. Under **simple uniform hashing**, each key is equally likely to be hashed to any of the m slots independently of the other keys. Expected chain length is alpha.

| Operation | Expected runtime without resizing | Explanation |
|---|---|---|
| Search, unsuccessful | Theta(1 + alpha) | Hash the key and scan its chain, whose expected length is alpha. |
| Search, successful | Theta(1 + alpha) | Hash and scan until the matching pair is encountered. |
| Insert, new key | Theta(1 + alpha) | Search for an existing key, then append to the chain. |
| Insert, existing key | Theta(1 + alpha) | Find and update the matching pair. |
| Delete | Theta(1 + alpha) | Search for the matching pair and remove it from its chain. |

A resize costs Theta(n + m_new) time to allocate buckets and rehash all entries. This is an **occasional worst-case cost**, not a constant-time guarantee per operation. Geometric growth (doubling) distributes that cost across many insertions, giving expected **amortized** O(1) insertion when alpha is bounded and ordinary hashing assumptions hold. A small load factor reduces average chain length at the cost of more unused memory; a large load factor saves memory but increases expected search and deletion time. Shrink and grow thresholds are separated to avoid repeatedly resizing near a single threshold (resize thrashing).

The theoretical O(1 + alpha) claim relies on the hashing assumptions. It does not provide a worst-case guarantee: if all keys fall into one chain, lookup/deletion can take O(n). Randomly selecting a hash function mitigates predictable collisions for a suitable key universe, but does not prevent maliciously chosen or congruent-mod-p keys from colliding.

## 6. Conclusion

Random pivot selection improves robustness against input-order patterns for distinct keys, while adding modest runtime overhead on already random arrays. Three-way partitioning is particularly beneficial for repeated keys. Separate chaining supports expected constant-time dictionary operations when the load factor remains bounded, at the cost of O(n) individual resize events and extra bucket memory. Together, these experiments show why algorithm choice requires both asymptotic analysis and implementation-aware measurements.

## References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press.

Python Software Foundation. (n.d.). *time — Time access and conversions*. https://docs.python.org/3/library/time.html

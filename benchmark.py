"""Reproducible quicksort benchmark. Saves results/timings.csv."""
import csv
import random
import statistics
import time
from pathlib import Path
from quicksort import randomized_quicksort, deterministic_quicksort

SIZES = (100, 500, 1000, 2000, 4000)
TRIALS = 5
DISTRIBUTIONS = ("random", "sorted", "reverse", "repeated")
OUTPUT = Path(__file__).resolve().parent / "results" / "timings.csv"


def make_input(distribution: str, size: int, rng: random.Random) -> list[int]:
    if distribution == "random":
        return rng.sample(range(size * 20), size)
    if distribution == "sorted":
        return list(range(size))
    if distribution == "reverse":
        return list(range(size - 1, -1, -1))
    if distribution == "repeated":
        return [rng.randrange(10) for _ in range(size)]
    raise ValueError(distribution)


def main() -> None:
    rng = random.Random(532)
    OUTPUT.parent.mkdir(exist_ok=True)
    records = []
    for distribution in DISTRIBUTIONS:
        for size in SIZES:
            measurements = {"randomized": [], "deterministic": []}
            for trial in range(TRIALS):
                values = make_input(distribution, size, rng)
                expected = sorted(values)
                for name, sort in (("randomized", randomized_quicksort),
                                   ("deterministic", deterministic_quicksort)):
                    start = time.perf_counter_ns()
                    result = sort(values, seed=trial + 532) if name == "randomized" else sort(values)
                    elapsed_ms = (time.perf_counter_ns() - start) / 1_000_000
                    assert result == expected, (distribution, size, name)
                    measurements[name].append(elapsed_ms)
            for name, times in measurements.items():
                records.append({"distribution": distribution, "n": size,
                                "algorithm": name, "trials": TRIALS,
                                "mean_ms": round(statistics.mean(times), 5),
                                "median_ms": round(statistics.median(times), 5),
                                "min_ms": round(min(times), 5),
                                "max_ms": round(max(times), 5)})
            print(f"{distribution:8s} n={size:5d} randomized={statistics.mean(measurements['randomized']):9.4f} ms deterministic={statistics.mean(measurements['deterministic']):9.4f} ms")
    with OUTPUT.open("w", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    print(f"Saved {OUTPUT}")


if __name__ == "__main__":
    main()

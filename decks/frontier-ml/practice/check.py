"""Run: python check.py answers.py [exercise]. Uses independent test fixtures."""
import argparse
import importlib.util
import math
from pathlib import Path


def close(a, b):
    if isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b))
    if isinstance(b, str):
        return a == b
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-10)


fixtures = {
    "cross_entropy": [
        (([1000, 1000], 1), math.log(2)), (([-1000, 1000], 0), 2000),
        (([2, 2 + math.log(3)], 1), math.log(4/3))],
    "merge_stats": [
        (((2, 3, 2), (1, 6, 0)), (3, 4, 8)),
        (((0, 0, 0), (5, 9, 2)), (5, 9, 2)),
        (((4, 10, 5), (4, 0, 1)), (8, 5, 206))],
    "attention": [
        (([0], [[2], [3]], [[1, 5], [3, 7]], [1, 1]), [2, 6]),
        (([1000], [[2], [2]], [[1], [3]], [0, 0]), [0]),
        (([1000], [[1], [1]], [[8], [3]], [0, 1]), [3]),
        (([math.sqrt(2), 0], [[0, 0], [math.log(3), 0]], [[2], [6]], [1, 1]), [5])],
    "token_loss": [(([6, 10], [2, 5]), 16/7), (([0, 5], [0, 2]), 2.5),
                   (([0, 0], [0, 0]), ValueError)],
    "gae": [
        (([1, 2], [0, 0], [0, 0], [False, True], [False, True], 0.9, 0.5), [1.9, 2]),
        (([0, 3], [2, 1], [4, 100], [False, True], [True, True], 0.5, 1), [0, 2]),
        (([1], [2], [5], [False], [False], 0.8, 0), [3])],
    "ppo_term": [
        ((math.log(1.4), 0, 2, 0.2), 2.4), ((math.log(1.4), 0, -2, 0.2), -2.8),
        ((math.log(0.5), 0, -2, 0.2), -1.6), ((-2, -2, 1, 0.1), 1)],
    "dpo_loss": [
        ((-3, -5, -3, -5, 0.1), math.log(2)),
        ((-1000, 0, 0, 0, 1), 1000),
        ((-1, -3, -2, -2, 0.5), math.log1p(math.exp(-1)))],
    "pass_at_k": [((5, 2, 2), 0.7), ((4, 0, 3), 0), ((4, 2, 4), 1)],
    "kv_bytes": [(([16, 17, 0], 2, 3, 4, 2, 16), 48*96),
                 (([8192], 32, 8, 128, 2, 1), 2**30), (([], 2, 2, 2, 2, 4), 0)],
    "decoding_frontier": [
        (([("A", 8, 3, 10), ("B", 9, 3, 10), ("C", 7, 1, 10),
           ("D", 10, 1, 15), ("E", 9, 3, 9)], 10), ["B", "C", "E"]),
        (([("A", 1, 1, 2)], 1), [])],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("submission", type=Path)
    parser.add_argument("exercise", nargs="?", choices=fixtures)
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("submission", args.submission)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for name in [args.exercise] if args.exercise else fixtures:
        func = getattr(module, name)
        for i, (inputs, expected) in enumerate(fixtures[name], 1):
            try:
                actual = func(*inputs)
            except ValueError:
                if expected is ValueError:
                    continue
                raise
            if expected is ValueError or not close(actual, expected):
                raise SystemExit(f"{name} case {i}: expected {expected!r}, got {actual!r}")
        print(f"{name}: {len(fixtures[name])} cases passed")


if __name__ == "__main__":
    main()

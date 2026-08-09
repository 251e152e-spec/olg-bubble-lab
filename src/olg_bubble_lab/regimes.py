"""Generators for R*_t / G regime sequences used to explore the
bubble-necessity frequency condition.

All generators return a list of log ratios ``x_t = log(R*_t / G)``,
which is the natural input for :mod:`olg_bubble_lab.conditions`.
"""

from __future__ import annotations

import math
from collections.abc import Sequence


def from_rates(r_star: Sequence[float], g: float) -> list[float]:
    """Convert a sequence of raw autarkic rates R*_t into log ratios log(R*_t/G)."""
    if g <= 0:
        raise ValueError("g must be positive")
    return [math.log(r / g) for r in r_star]


def periodic_regime(
    r_high: float, r_low: float, g: float, n_high: int, n_low: int, n_periods: int
) -> list[float]:
    """Alternate n_high periods of R*_H then n_low periods of R*_L, repeated.

    This mirrors the two-value regime toy model (R*_H > n > R*_L) used
    to build intuition for the frequency condition.
    """
    if n_high <= 0 or n_low <= 0 or n_periods <= 0:
        raise ValueError("n_high, n_low and n_periods must be positive")
    block = [r_high] * n_high + [r_low] * n_low
    r_star = block * n_periods
    return from_rates(r_star, g)


def diverging_blocks(r_high: float, r_low: float, g: float, n_blocks: int) -> list[float]:
    """Diverging block-length counterexample: L,H block lengths 1,1,2,2,3,3,...

    This sequence satisfies the Cesaro (log-average) condition but
    violates the K-uniform frequency condition for any fixed K, since
    block lengths grow without bound. Useful as a regression test for
    the two conditions disagreeing.
    """
    if n_blocks <= 0:
        raise ValueError("n_blocks must be positive")
    r_star: list[float] = []
    for block_len in range(1, n_blocks + 1):
        r_star += [r_low] * block_len
        r_star += [r_high] * block_len
    return from_rates(r_star, g)


def from_csv(path: str, column: str = "R_star", g_column: str = "G") -> list[float]:
    """Load a rate sequence from a CSV file with columns R_star and G.

    If the CSV has a constant G column, a single scalar is inferred;
    otherwise a pointwise log ratio log(R_star_t / G_t) is computed.
    """
    import csv

    r_values: list[float] = []
    g_values: list[float] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            r_values.append(float(row[column]))
            g_values.append(float(row[g_column]))
    if not r_values:
        raise ValueError(f"no data rows found in {path}")
    return [math.log(r / g) for r, g in zip(r_values, g_values)]

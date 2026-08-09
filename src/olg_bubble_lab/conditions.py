"""Numerical checks for the bubble-necessity conditions used in the
frequency/recurrence framing of non-stationary OLG economies.

Given a sequence of log growth-rate ratios

    x_t := log(R*_t / G)

(where R*_t is the autarkic interest rate at date t and G is the
population/technology growth rate), this module checks two conditions:

1. The K-uniform frequency condition:
       there exist K in N and gamma > 0 such that for all t,
           (1/K) * sum_{j=0}^{K-1} x_{t+j} <= -gamma

2. The Cesaro (log-average) condition:
       the running average (1/T) * sum_{t=1}^{T} x_t is eventually
       bounded away from 0 from above, i.e. trends non-positive
       in the long run (a necessary but, on its own, insufficient
       condition for bubble existence).

Both checks operate on *finite* sequences, so they are best read as
"the condition holds on this window of observed data", not as a
proof of an infinite-horizon property.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class FrequencyCheckResult:
    """Result of checking the K-uniform frequency condition."""

    holds: bool
    k: int
    gamma: float
    worst_window_start: int
    worst_window_average: float

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        verdict = "satisfied" if self.holds else "NOT satisfied"
        return (
            f"Frequency condition (K={self.k}, gamma={self.gamma:.4g}) "
            f"{verdict}; worst K-window starts at t={self.worst_window_start} "
            f"with average {self.worst_window_average:.4g}"
        )


@dataclass(frozen=True)
class CesaroCheckResult:
    """Result of checking the Cesaro / log-average condition."""

    holds: bool
    final_average: float
    running_average: list[float]

    def __str__(self) -> str:  # pragma: no cover - cosmetic
        verdict = "satisfied" if self.holds else "NOT satisfied"
        return f"Cesaro condition {verdict}; running average -> {self.final_average:.4g}"


def _validate_sequence(x: Sequence[float]) -> None:
    if len(x) == 0:
        raise ValueError("sequence must be non-empty")


def check_frequency_condition(
    x: Sequence[float], k: int, gamma: float = 0.0
) -> FrequencyCheckResult:
    """Check the K-uniform frequency condition on a finite sequence.

    For every valid window start t (0 <= t <= len(x) - k), the average
    of x over the window [t, t+k) must be <= -gamma. If gamma is not
    supplied, the largest gamma for which the condition holds is
    reported implicitly via ``worst_window_average`` (its negative is
    the tightest feasible gamma).

    Raises
    ------
    ValueError
        If ``x`` is empty or ``k`` is not a positive integer no larger
        than ``len(x)``.
    """
    _validate_sequence(x)
    if k <= 0:
        raise ValueError("k must be a positive integer")
    if k > len(x):
        raise ValueError("k cannot exceed the length of the sequence")

    n = len(x)
    window_averages = []
    for t in range(n - k + 1):
        window_avg = sum(x[t : t + k]) / k
        window_averages.append((t, window_avg))

    worst_start, worst_avg = max(window_averages, key=lambda pair: pair[1])
    holds = worst_avg <= -gamma

    return FrequencyCheckResult(
        holds=holds,
        k=k,
        gamma=gamma,
        worst_window_start=worst_start,
        worst_window_average=worst_avg,
    )


def best_gamma_for_k(x: Sequence[float], k: int) -> float:
    """Return the tightest gamma >= 0 for which the K-window condition holds.

    This is simply the negative of the worst (largest) K-window average.
    A non-positive return value means no gamma > 0 works for this K.
    """
    result = check_frequency_condition(x, k, gamma=0.0)
    return -result.worst_window_average


def find_minimal_k(
    x: Sequence[float], gamma: float, k_max: int | None = None
) -> int | None:
    """Search for the smallest K for which the frequency condition holds
    with the given gamma. Returns None if no such K <= k_max is found.
    """
    _validate_sequence(x)
    upper = k_max if k_max is not None else len(x)
    upper = min(upper, len(x))
    for k in range(1, upper + 1):
        if check_frequency_condition(x, k, gamma).holds:
            return k
    return None


def check_cesaro_condition(x: Sequence[float], tol: float = 1e-9) -> CesaroCheckResult:
    """Check whether the running (Cesaro) average of x trends non-positive.

    The condition is judged to "hold" if the final running average is
    <= tol. This is a necessary-but-not-sufficient condition for bubble
    necessity under the frequency framing: it can hold even when the
    K-uniform frequency condition fails (see the diverging-block
    counterexample in ``regimes.diverging_blocks``).
    """
    _validate_sequence(x)
    running_average: list[float] = []
    running_sum = 0.0
    for i, value in enumerate(x, start=1):
        running_sum += value
        running_average.append(running_sum / i)

    final_average = running_average[-1]
    holds = final_average <= tol

    return CesaroCheckResult(
        holds=holds, final_average=final_average, running_average=running_average
    )

"""Illustrative simulation of a candidate bubble's log price path.

This is a *pedagogical* simulation, not a full equilibrium solver: it
tracks the cumulative log-growth factor

    log(p_t / p_0) = sum_{s=1}^{t} x_s,    x_s = log(R*_s / G)

which is the natural quantity the frequency and Cesaro conditions make
statements about. Whether the K-uniform frequency condition holds is
reflected in whether this cumulative path is pulled back down
regularly enough to stay bounded, versus drifting to +infinity when
only the (insufficient) Cesaro condition holds.
"""

from __future__ import annotations

from collections.abc import Sequence


def cumulative_log_price(x: Sequence[float], p0: float = 1.0) -> list[float]:
    """Return the price path p_0, p_1, ..., p_T implied by log ratios x."""
    if p0 <= 0:
        raise ValueError("p0 must be positive")
    import math

    path = [p0]
    cumulative = 0.0
    for value in x:
        cumulative += value
        path.append(p0 * math.exp(cumulative))
    return path

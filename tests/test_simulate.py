import math

import pytest

from olg_bubble_lab.simulate import cumulative_log_price


def test_cumulative_log_price_starts_at_p0() -> None:
    path = cumulative_log_price([0.0, 0.0, 0.0], p0=3.0)
    assert path[0] == pytest.approx(3.0)


def test_cumulative_log_price_length() -> None:
    path = cumulative_log_price([0.1, 0.2, -0.1])
    assert len(path) == 4  # p0 plus one entry per step


def test_cumulative_log_price_matches_manual_exponential() -> None:
    x = [math.log(2.0), math.log(0.5)]
    path = cumulative_log_price(x, p0=1.0)
    assert path[1] == pytest.approx(2.0)
    assert path[2] == pytest.approx(1.0)


def test_cumulative_log_price_rejects_nonpositive_p0() -> None:
    with pytest.raises(ValueError):
        cumulative_log_price([0.0], p0=0.0)

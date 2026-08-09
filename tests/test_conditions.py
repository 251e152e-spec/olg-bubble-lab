import math

import pytest

from olg_bubble_lab.conditions import (
    best_gamma_for_k,
    check_cesaro_condition,
    check_frequency_condition,
    find_minimal_k,
)
from olg_bubble_lab.regimes import diverging_blocks, periodic_regime


def test_frequency_condition_holds_for_strongly_negative_sequence() -> None:
    x = [-1.0] * 10
    result = check_frequency_condition(x, k=2, gamma=0.5)
    assert result.holds is True
    assert result.worst_window_average == pytest.approx(-1.0)


def test_frequency_condition_fails_for_positive_sequence() -> None:
    x = [1.0] * 10
    result = check_frequency_condition(x, k=2, gamma=0.0)
    assert result.holds is False


def test_frequency_condition_rejects_empty_sequence() -> None:
    with pytest.raises(ValueError):
        check_frequency_condition([], k=1)


def test_frequency_condition_rejects_k_too_large() -> None:
    with pytest.raises(ValueError):
        check_frequency_condition([1.0, 2.0], k=3)


def test_frequency_condition_rejects_nonpositive_k() -> None:
    with pytest.raises(ValueError):
        check_frequency_condition([1.0, 2.0], k=0)


def test_periodic_regime_satisfies_frequency_condition() -> None:
    # R*_H = 1.5, R*_L = 0.5, G = 1.0: strongly negative on average
    x = periodic_regime(r_high=1.5, r_low=0.5, g=1.0, n_high=1, n_low=1, n_periods=20)
    result = check_frequency_condition(x, k=2, gamma=0.01)
    assert result.holds is True


def test_diverging_blocks_violate_frequency_condition_for_fixed_k() -> None:
    # Block lengths grow without bound, so any fixed K is eventually
    # swallowed by an all-H window.
    x = diverging_blocks(r_high=2.0, r_low=0.5, g=1.0, n_blocks=6)
    result = check_frequency_condition(x, k=3, gamma=0.01)
    assert result.holds is False


def test_diverging_blocks_still_satisfy_cesaro_condition() -> None:
    # log(2.0) and log(0.5) are symmetric (+/- log 2), and blocks are
    # equal length on each side, so the running average should trend
    # toward 0 (satisfying the <=0 Cesaro condition) even though the
    # frequency condition fails.
    x = diverging_blocks(r_high=2.0, r_low=0.5, g=1.0, n_blocks=10)
    result = check_cesaro_condition(x, tol=1e-6)
    assert result.holds is True
    assert result.final_average == pytest.approx(0.0, abs=1e-6)


def test_best_gamma_for_k_matches_manual_computation() -> None:
    x = [-2.0, -2.0, -2.0, -2.0]
    gamma = best_gamma_for_k(x, k=2)
    assert gamma == pytest.approx(2.0)


def test_find_minimal_k_finds_expected_window() -> None:
    x = [1.0, -3.0, 1.0, -3.0, 1.0, -3.0]
    k = find_minimal_k(x, gamma=0.1, k_max=4)
    assert k is not None
    result = check_frequency_condition(x, k=k, gamma=0.1)
    assert result.holds is True


def test_find_minimal_k_returns_none_when_infeasible() -> None:
    x = [1.0, 1.0, 1.0]
    k = find_minimal_k(x, gamma=0.1)
    assert k is None


def test_cesaro_condition_fails_for_drifting_positive_sequence() -> None:
    x = [0.1] * 50
    result = check_cesaro_condition(x)
    assert result.holds is False
    assert result.final_average == pytest.approx(0.1)


def test_cesaro_running_average_length_matches_input() -> None:
    x = [math.log(1.2), math.log(0.8), math.log(1.1)]
    result = check_cesaro_condition(x)
    assert len(result.running_average) == len(x)

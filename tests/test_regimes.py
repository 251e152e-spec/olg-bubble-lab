import csv
import math
from pathlib import Path

import pytest

from olg_bubble_lab.regimes import diverging_blocks, from_csv, from_rates, periodic_regime


def test_from_rates_computes_log_ratio() -> None:
    x = from_rates([2.0, 0.5], g=1.0)
    assert x == pytest.approx([math.log(2.0), math.log(0.5)])


def test_from_rates_rejects_nonpositive_g() -> None:
    with pytest.raises(ValueError):
        from_rates([1.0], g=0.0)


def test_periodic_regime_length_and_pattern() -> None:
    x = periodic_regime(r_high=2.0, r_low=0.5, g=1.0, n_high=2, n_low=1, n_periods=3)
    assert len(x) == (2 + 1) * 3
    # first block: H, H, L
    assert x[0] == pytest.approx(math.log(2.0))
    assert x[1] == pytest.approx(math.log(2.0))
    assert x[2] == pytest.approx(math.log(0.5))


def test_periodic_regime_rejects_invalid_lengths() -> None:
    with pytest.raises(ValueError):
        periodic_regime(1.0, 1.0, 1.0, n_high=0, n_low=1, n_periods=1)


def test_diverging_blocks_length() -> None:
    x = diverging_blocks(r_high=2.0, r_low=0.5, g=1.0, n_blocks=4)
    # block lengths 1+1, 2+2, 3+3, 4+4 = 2*(1+2+3+4) = 20
    assert len(x) == 20


def test_diverging_blocks_rejects_nonpositive_n_blocks() -> None:
    with pytest.raises(ValueError):
        diverging_blocks(1.0, 1.0, 1.0, n_blocks=0)


def test_from_csv_reads_pointwise_rates(tmp_path: Path) -> None:
    csv_path = tmp_path / "rates.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["R_star", "G"])
        writer.writerow([2.0, 1.0])
        writer.writerow([0.5, 1.0])
    x = from_csv(str(csv_path))
    assert x == pytest.approx([math.log(2.0), math.log(0.5)])


def test_from_csv_rejects_empty_file(tmp_path: Path) -> None:
    csv_path = tmp_path / "empty.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["R_star", "G"])
    with pytest.raises(ValueError):
        from_csv(str(csv_path))

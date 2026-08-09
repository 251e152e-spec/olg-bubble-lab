"""Matplotlib visualizations for regime sequences and price paths."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from .conditions import check_cesaro_condition
from .simulate import cumulative_log_price


def plot_regime_and_price(
    x: Sequence[float],
    output_path: str | Path,
    title: str = "OLG regime sequence and implied price path",
) -> Path:
    """Plot the log-ratio regime sequence, its running (Cesaro) average,
    and the implied cumulative price path, stacked in three panels.
    Saves a vector PDF (or whatever format the extension implies) and
    returns the resolved path.
    """
    output_path = Path(output_path)
    cesaro = check_cesaro_condition(x)
    price_path = cumulative_log_price(x)

    fig, axes = plt.subplots(3, 1, figsize=(7, 8), sharex=False)

    t = list(range(len(x)))
    axes[0].step(t, x, where="mid", color="tab:blue")
    axes[0].axhline(0.0, color="gray", linewidth=0.8, linestyle="--")
    axes[0].set_ylabel(r"$x_t = \log(R^*_t / G)$")
    axes[0].set_title(title)

    axes[1].plot(t, cesaro.running_average, color="tab:orange")
    axes[1].axhline(0.0, color="gray", linewidth=0.8, linestyle="--")
    axes[1].set_ylabel("running (Cesaro) average")

    axes[2].plot(range(len(price_path)), price_path, color="tab:green")
    axes[2].set_ylabel(r"implied price $p_t$")
    axes[2].set_xlabel("t")

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    return output_path

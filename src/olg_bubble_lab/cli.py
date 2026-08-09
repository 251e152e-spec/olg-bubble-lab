"""Command-line interface for olg-bubble-lab.

Examples
--------
Check a periodic regime for the frequency condition::

    olg-bubble check-periodic --r-high 1.2 --r-low 0.8 --g 1.0 \\
        --n-high 2 --n-low 3 --n-periods 10 --k 5 --gamma 0.01

Plot a diverging-block counterexample::

    olg-bubble plot-diverging --r-high 1.2 --r-low 0.8 --g 1.0 \\
        --n-blocks 8 --output diverging.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import click

from . import conditions, regimes, visualize


@click.group()
@click.version_option()
def main() -> None:
    """olg-bubble-lab: check and visualize OLG bubble-necessity conditions."""


@main.command("check-periodic")
@click.option("--r-high", type=float, required=True, help="High-regime autarkic rate R*_H")
@click.option("--r-low", type=float, required=True, help="Low-regime autarkic rate R*_L")
@click.option("--g", type=float, required=True, help="Growth rate G")
@click.option("--n-high", type=int, required=True, help="Length of each high-regime block")
@click.option("--n-low", type=int, required=True, help="Length of each low-regime block")
@click.option("--n-periods", type=int, required=True, help="Number of high/low blocks to repeat")
@click.option("--k", type=int, required=True, help="Window length K to test")
@click.option("--gamma", type=float, default=0.0, show_default=True, help="Required margin gamma")
def check_periodic(
    r_high: float,
    r_low: float,
    g: float,
    n_high: int,
    n_low: int,
    n_periods: int,
    k: int,
    gamma: float,
) -> None:
    """Check the frequency and Cesaro conditions on a periodic H/L regime."""
    x = regimes.periodic_regime(r_high, r_low, g, n_high, n_low, n_periods)
    freq_result = conditions.check_frequency_condition(x, k, gamma)
    cesaro_result = conditions.check_cesaro_condition(x)
    click.echo(str(freq_result))
    click.echo(str(cesaro_result))


@main.command("check-diverging")
@click.option("--r-high", type=float, required=True)
@click.option("--r-low", type=float, required=True)
@click.option("--g", type=float, required=True)
@click.option("--n-blocks", type=int, required=True, help="Number of diverging L/H block pairs")
@click.option("--k", type=int, required=True, help="Window length K to test")
@click.option("--gamma", type=float, default=0.0, show_default=True)
def check_diverging(
    r_high: float, r_low: float, g: float, n_blocks: int, k: int, gamma: float
) -> None:
    """Check the diverging-block counterexample sequence (1,1,2,2,3,...)."""
    x = regimes.diverging_blocks(r_high, r_low, g, n_blocks)
    freq_result = conditions.check_frequency_condition(x, k, gamma)
    cesaro_result = conditions.check_cesaro_condition(x)
    click.echo(str(freq_result))
    click.echo(str(cesaro_result))


@main.command("plot-periodic")
@click.option("--r-high", type=float, required=True)
@click.option("--r-low", type=float, required=True)
@click.option("--g", type=float, required=True)
@click.option("--n-high", type=int, required=True)
@click.option("--n-low", type=int, required=True)
@click.option("--n-periods", type=int, required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
def plot_periodic(
    r_high: float, r_low: float, g: float, n_high: int, n_low: int, n_periods: int, output: Path
) -> None:
    """Plot a periodic H/L regime and its implied price path."""
    x = regimes.periodic_regime(r_high, r_low, g, n_high, n_low, n_periods)
    path = visualize.plot_regime_and_price(x, output, title="Periodic regime")
    click.echo(f"saved: {path}")


@main.command("plot-diverging")
@click.option("--r-high", type=float, required=True)
@click.option("--r-low", type=float, required=True)
@click.option("--g", type=float, required=True)
@click.option("--n-blocks", type=int, required=True)
@click.option("--output", type=click.Path(path_type=Path), required=True)
def plot_diverging(r_high: float, r_low: float, g: float, n_blocks: int, output: Path) -> None:
    """Plot the diverging-block counterexample and its implied price path."""
    x = regimes.diverging_blocks(r_high, r_low, g, n_blocks)
    path = visualize.plot_regime_and_price(x, output, title="Diverging-block counterexample")
    click.echo(f"saved: {path}")


@main.command("check-csv")
@click.option("--path", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--r-column", default="R_star", show_default=True)
@click.option("--g-column", default="G", show_default=True)
@click.option("--k", type=int, required=True)
@click.option("--gamma", type=float, default=0.0, show_default=True)
def check_csv(path: Path, r_column: str, g_column: str, k: int, gamma: float) -> None:
    """Check the frequency and Cesaro conditions on a CSV-provided rate sequence."""
    x = regimes.from_csv(str(path), column=r_column, g_column=g_column)
    freq_result = conditions.check_frequency_condition(x, k, gamma)
    cesaro_result = conditions.check_cesaro_condition(x)
    click.echo(str(freq_result))
    click.echo(str(cesaro_result))


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())

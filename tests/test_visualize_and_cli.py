from pathlib import Path

from click.testing import CliRunner

from olg_bubble_lab.cli import main
from olg_bubble_lab.regimes import periodic_regime
from olg_bubble_lab.visualize import plot_regime_and_price


def test_plot_regime_and_price_creates_file(tmp_path: Path) -> None:
    x = periodic_regime(r_high=1.5, r_low=0.5, g=1.0, n_high=2, n_low=2, n_periods=4)
    output = tmp_path / "plot.pdf"
    result_path = plot_regime_and_price(x, output)
    assert result_path == output
    assert output.exists()
    assert output.stat().st_size > 0


def test_cli_check_periodic_runs_successfully() -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "check-periodic",
            "--r-high",
            "1.5",
            "--r-low",
            "0.5",
            "--g",
            "1.0",
            "--n-high",
            "1",
            "--n-low",
            "1",
            "--n-periods",
            "10",
            "--k",
            "2",
            "--gamma",
            "0.01",
        ],
    )
    assert result.exit_code == 0
    assert "Frequency condition" in result.output
    assert "Cesaro condition" in result.output


def test_cli_check_diverging_runs_successfully() -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "check-diverging",
            "--r-high",
            "2.0",
            "--r-low",
            "0.5",
            "--g",
            "1.0",
            "--n-blocks",
            "6",
            "--k",
            "3",
        ],
    )
    assert result.exit_code == 0


def test_cli_plot_periodic_creates_file(tmp_path: Path) -> None:
    runner = CliRunner()
    output = tmp_path / "out.pdf"
    result = runner.invoke(
        main,
        [
            "plot-periodic",
            "--r-high",
            "1.5",
            "--r-low",
            "0.5",
            "--g",
            "1.0",
            "--n-high",
            "2",
            "--n-low",
            "2",
            "--n-periods",
            "3",
            "--output",
            str(output),
        ],
    )
    assert result.exit_code == 0
    assert output.exists()

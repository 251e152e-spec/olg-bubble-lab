"""olg-bubble-lab: check and visualize OLG bubble-necessity frequency conditions."""

from .conditions import (
    CesaroCheckResult,
    FrequencyCheckResult,
    best_gamma_for_k,
    check_cesaro_condition,
    check_frequency_condition,
    find_minimal_k,
)
from .regimes import diverging_blocks, from_csv, from_rates, periodic_regime
from .simulate import cumulative_log_price

__all__ = [
    "CesaroCheckResult",
    "FrequencyCheckResult",
    "best_gamma_for_k",
    "check_cesaro_condition",
    "check_frequency_condition",
    "cumulative_log_price",
    "diverging_blocks",
    "find_minimal_k",
    "from_csv",
    "from_rates",
    "periodic_regime",
]

__version__ = "0.1.0"

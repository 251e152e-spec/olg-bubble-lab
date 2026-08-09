"""Reproduce the verification figure used in the accompanying report.

Compares, at a fixed window K=2, how the frequency condition behaves on
(1) a periodic H/L regime versus (2) the diverging-block counterexample
(1,1,2,2,3,3,...), and shows how the minimal K needed for the diverging
sequence grows without bound as more blocks are added.

Run with:  python examples/verification.py
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from olg_bubble_lab import (
    check_frequency_condition,
    diverging_blocks,
    find_minimal_k,
    periodic_regime,
)

R_HIGH, R_LOW, G = 1.5, 0.3, 1.0
GAMMA = 0.1
K_FIXED = 2
K_CAP = 10


def main() -> None:
    n_list = list(range(1, 14))

    diverging_pass = []
    periodic_pass = []
    for n in n_list:
        xd = diverging_blocks(R_HIGH, R_LOW, G, n_blocks=n)
        diverging_pass.append(
            1 if check_frequency_condition(xd, k=K_FIXED, gamma=GAMMA).holds else 0
        )
        xp = periodic_regime(R_HIGH, R_LOW, G, n_high=1, n_low=1, n_periods=n)
        periodic_pass.append(
            1 if check_frequency_condition(xp, k=K_FIXED, gamma=GAMMA).holds else 0
        )

    diverging_min_k: list[int | None] = []
    for n in n_list:
        xd = diverging_blocks(R_HIGH, R_LOW, G, n_blocks=n)
        diverging_min_k.append(find_minimal_k(xd, gamma=GAMMA, k_max=min(K_CAP, len(xd))))

    print("n:", n_list)
    print(f"diverging pass (K={K_FIXED}):", diverging_pass)
    print(f"periodic  pass (K={K_FIXED}):", periodic_pass)
    print(f"diverging min K (cap {K_CAP}):", diverging_min_k)

    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))

    axes[0].step(n_list, diverging_pass, where="mid", label="diverging blocks", color="tab:red")
    axes[0].step(
        n_list, periodic_pass, where="mid", label="periodic H/L", color="tab:blue", linestyle="--"
    )
    axes[0].set_ylim(-0.2, 1.2)
    axes[0].set_yticks([0, 1])
    axes[0].set_yticklabels(["fails", "holds"])
    axes[0].set_xlabel("n (n_blocks / n_periods)")
    axes[0].set_title(f"Frequency condition at fixed K={K_FIXED}, gamma={GAMMA}")
    axes[0].legend(fontsize=8, loc="center right")

    axes[1].plot(
        n_list, [k if k else float("nan") for k in diverging_min_k], "o-", color="tab:red"
    )
    axes[1].set_xlabel("n (n_blocks)")
    axes[1].set_ylabel(f"minimal K found (search capped at {K_CAP})")
    axes[1].set_title("Diverging blocks: minimal K grows with n")

    fig.tight_layout()
    fig.savefig("examples/verification_min_k.pdf")
    print("saved examples/verification_min_k.pdf")


if __name__ == "__main__":
    main()

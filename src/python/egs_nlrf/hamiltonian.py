"""Quantum domain: H = H_0 + alpha_Phi * O_Phi."""

from __future__ import annotations

import numpy as np

from egs_nlrf.lattice import delta_v_phi


def rydberg_energy_cm(n: int, R_inf: float = 109737.31568549) -> float:
    """Standard hydrogenic level (cm^-1), H_0 baseline."""
    return -R_inf / (n ** 2)


def egs_correction_cm(
    n: int,
    alpha_phi: float,
    phi: float = 1.618033988749895,
) -> float:
    """
    Exploratory O_Phi correction: geometric residual scaled by Phi^n lattice proximity.
    Vanishes as alpha_phi -> 0.
    """
    if alpha_phi == 0.0:
        return 0.0
    # Model postulate: small oscillatory correction on log-scale coordinates
    x = np.log(max(n, 1)) / np.log(phi)
    return alpha_phi * np.sin(2.0 * np.pi * x) * 1e-3


def corrected_transition_cm(
    n_upper: int,
    n_lower: int,
    alpha_phi: float,
    phi: float = 1.618033988749895,
) -> float:
    e_u = rydberg_energy_cm(n_upper) + egs_correction_cm(n_upper, alpha_phi, phi)
    e_l = rydberg_energy_cm(n_lower) + egs_correction_cm(n_lower, alpha_phi, phi)
    return abs(e_u - e_l)


def hydrogen_transition_series(
    n_lower: int = 2,
    n_max: int = 10,
    alpha_phi: float = 0.0,
) -> np.ndarray:
    """Balmer-like series frequencies (cm^-1)."""
    return np.array(
        [corrected_transition_cm(n, n_lower, alpha_phi) for n in range(n_lower + 1, n_max + 1)]
    )

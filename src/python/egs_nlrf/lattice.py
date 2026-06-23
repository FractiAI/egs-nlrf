"""Appendix A: boundary-lattice potential on L_n = Phi^n."""

from __future__ import annotations

import numpy as np

from egs_nlrf import A0_BOHR, PHI_EGS


def lattice_radius(n: int, phi: float = PHI_EGS, a0: float = A0_BOHR) -> float:
    return a0 * (phi ** n)


def delta_v_phi(
    r: np.ndarray,
    q: float = 1.0,
    phi: float = PHI_EGS,
    a0: float = A0_BOHR,
    n_min: int = -3,
    n_max: int = 6,
    eps0: float = 8.8541878128e-12,
) -> np.ndarray:
    """
    delta V_Phi(r) = (q / 4 pi eps0 r) sum_n Phi^{-n} Theta(r - a0 Phi^n)
    """
    pref = q / (4.0 * np.pi * eps0)
    v = np.zeros_like(r, dtype=np.float64)
    for n in range(n_min, n_max + 1):
        rn = a0 * (phi ** n)
        cn = phi ** (-n)
        v += cn * (r >= rn).astype(np.float64)
    return pref * v / np.maximum(r, 1e-30)


def radial_density_delta(
    r: np.ndarray,
    q: float = 1.0,
    phi: float = PHI_EGS,
    a0: float = A0_BOHR,
    n_min: int = -3,
    n_max: int = 6,
) -> np.ndarray:
    """Discrete lattice density contribution (smoothed delta comb)."""
    rho = np.zeros_like(r, dtype=np.float64)
    for n in range(n_min, n_max + 1):
        rn = a0 * (phi ** n)
        cn = phi ** (-n)
        sigma = 0.02 * rn
        rho += cn * q * np.exp(-0.5 * ((r - rn) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))
    return rho

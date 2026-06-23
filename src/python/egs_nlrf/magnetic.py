"""Appendix B: magnetic topology phase functional."""

from __future__ import annotations

import numpy as np

from egs_nlrf import PHI_EGS


def vector_potential_phi(
    r: np.ndarray,
    phi0: float = 1.0,
    phi: float = PHI_EGS,
    n_terms: int = 5,
    gamma: np.ndarray | None = None,
) -> np.ndarray:
    """|A_phi| magnitude along azimuthal component model."""
    if gamma is None:
        gamma = np.ones(n_terms) / n_terms
    a = np.zeros_like(r, dtype=np.float64)
    for n, gn in enumerate(gamma[:n_terms]):
        a += gn * np.cos(2.0 * np.pi * r / (phi ** n))
    return (phi0 / (2.0 * np.pi * np.maximum(r, 1e-12))) * a


def aharonov_bohm_phase(
    m: int,
    phi: float = PHI_EGS,
    phi0: float = 1.0,
    n_terms: int = 5,
    gamma: np.ndarray | None = None,
) -> float:
    """oint A_phi . dr on circle R = a0 Phi^m (Appendix B)."""
    if gamma is None:
        gamma = np.ones(n_terms) / n_terms
    total = 0.0
    for n, gn in enumerate(gamma[:n_terms]):
        total += gn * np.cos(2.0 * np.pi * (phi ** (m - n)))
    return phi0 * total

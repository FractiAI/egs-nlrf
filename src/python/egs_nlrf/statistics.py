"""Appendix D: statistical validation pipeline."""

from __future__ import annotations

import numpy as np
from scipy import stats


def chi2_statistic(obs: np.ndarray, theory: np.ndarray, error: np.ndarray) -> float:
    err = np.maximum(error, 1e-30)
    return float(np.sum(((obs - theory) / err) ** 2))


def log_phi_coordinates(nu_theory: np.ndarray, phi: float) -> np.ndarray:
    """x_i = ln(nu_theory,i) / ln(Phi_EGS)."""
    nu = np.maximum(np.abs(nu_theory), 1e-30)
    return np.log(nu) / np.log(phi)


def lattice_fourier_score(residuals: np.ndarray, coordinates: np.ndarray) -> float:
    """Non-uniform Fourier clustering score on log-Phi coordinates."""
    if len(residuals) == 0:
        return 0.0
    return float(np.abs(np.sum(residuals * np.cos(coordinates))))


def permutation_test(
    residuals: np.ndarray,
    coordinates: np.ndarray,
    iterations: int = 1000,
    seed: int = 42,
) -> dict:
    rng = np.random.default_rng(seed)
    observed = lattice_fourier_score(residuals, coordinates)
    null = np.zeros(iterations)
    for i in range(iterations):
        shuffled = rng.permutation(residuals)
        null[i] = lattice_fourier_score(shuffled, coordinates)
    p_value = float((np.sum(null >= observed) + 1) / (iterations + 1))
    return {
        "observed_score": observed,
        "null_mean": float(null.mean()),
        "null_std": float(null.std()),
        "p_value": p_value,
        "significant_at_0_05": p_value < 0.05,
    }


def aic(n_params: int, n_points: int, chi2: float) -> float:
    return chi2 + 2 * n_params


def bic(n_params: int, n_points: int, chi2: float) -> float:
    return chi2 + n_params * np.log(max(n_points, 1))


def bootstrap_ci(
    values: np.ndarray, n_boot: int = 500, seed: int = 42
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    boots = [float(np.mean(rng.choice(values, size=len(values), replace=True))) for _ in range(n_boot)]
    return float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))

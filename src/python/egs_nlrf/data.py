"""Hydrogen reference data loading and synthetic NIST-style generation."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from egs_nlrf.hamiltonian import corrected_transition_cm, rydberg_energy_cm


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def synthesize_hydrogen_transitions(
    n_lower: int = 2,
    n_max: int = 15,
    alpha_phi: float = 1e-5,
    phi: float = 1.618033988749895,
    noise_ppm: float = 0.5,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Demo dataset: theory = QED baseline (alpha_phi=0), obs = baseline + optional EGS residual + noise.
    Returns (observed_cm, theory_cm, error_cm).
    """
    rng = np.random.default_rng(seed)
    theory = []
    obs = []
    for n in range(n_lower + 1, n_max + 1):
        t0 = corrected_transition_cm(n, n_lower, alpha_phi=0.0, phi=phi)
        t1 = corrected_transition_cm(n, n_lower, alpha_phi=alpha_phi, phi=phi)
        theory.append(t0)
        noise = rng.normal(0, t0 * noise_ppm * 1e-6)
        obs.append(t1 + noise)
    theory = np.array(theory)
    obs = np.array(obs)
    err = theory * noise_ppm * 1e-6
    return obs, theory, err


def save_spectra_csv(
    path: Path,
    obs: np.ndarray,
    theory: np.ndarray,
    error: np.ndarray,
    n_lower: int = 2,
) -> None:
    import pandas as pd

    n_upper = np.arange(n_lower + 1, n_lower + 1 + len(obs))
    df = pd.DataFrame({
        "n_upper": n_upper,
        "n_lower": n_lower,
        "observed_cm": obs,
        "theory_qed_cm": theory,
        "error_cm": error,
    })
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def load_spectra_csv(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    import pandas as pd

    df = pd.read_csv(path)
    return (
        df["observed_cm"].to_numpy(),
        df["theory_qed_cm"].to_numpy(),
        df["error_cm"].to_numpy(),
    )

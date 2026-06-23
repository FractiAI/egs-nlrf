"""Hydrogen reference data: NIST ASD public spectra and synthetic demo fallback."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from egs_nlrf.hamiltonian import corrected_transition_cm, qed_transition_cm
from egs_nlrf.nist import fetch_nist_balmer_series, load_bundled_reference, records_to_arrays

ROOT = Path(__file__).resolve().parents[3]
BUNDLED_REF = ROOT / "data" / "reference" / "nist_asd_balmer_principal.json"


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def synthesize_hydrogen_transitions(
    n_lower: int = 2,
    n_max: int = 15,
    alpha_phi: float = 1e-5,
    phi: float = 1.618033988749895,
    noise_ppm: float = 0.5,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Synthetic demo dataset for pipeline smoke tests only.
    Returns (observed_cm, theory_cm, error_cm, n_upper).
    """
    rng = np.random.default_rng(seed)
    n_upper_arr = np.arange(n_lower + 1, n_max + 1)
    theory = np.array([qed_transition_cm(int(n), n_lower) for n in n_upper_arr])
    corrected = np.array([
        corrected_transition_cm(int(n), n_lower, alpha_phi, phi) for n in n_upper_arr
    ])
    noise = rng.normal(0, theory * noise_ppm * 1e-6, size=len(theory))
    obs = corrected + noise
    err = theory * noise_ppm * 1e-6
    return obs, theory, err, n_upper_arr


def load_nist_balmer_data(
    n_min: int = 3,
    n_max: int = 15,
    offline: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, dict]:
    """Load recognized public NIST ASD Balmer transitions."""
    if offline:
        records, meta = load_bundled_reference(BUNDLED_REF)
        records = [r for r in records if n_min <= r["n_upper"] <= n_max]
    else:
        records, meta = fetch_nist_balmer_series(n_min=n_min, n_max=n_max)
    obs, theory, err, n_upper = records_to_arrays(records)
    return obs, theory, err, n_upper, meta


def save_spectra_csv(
    path: Path,
    obs: np.ndarray,
    theory: np.ndarray,
    error: np.ndarray,
    n_upper: np.ndarray,
    n_lower: int = 2,
    source: str = "NIST ASD",
) -> None:
    import pandas as pd

    df = pd.DataFrame({
        "n_upper": n_upper.astype(int),
        "n_lower": n_lower,
        "observed_cm": obs,
        "theory_qed_cm": theory,
        "error_cm": error,
        "source": source,
    })
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def load_spectra_csv(path: Path) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray | None]:
    import pandas as pd

    df = pd.read_csv(path)
    n_upper = df["n_upper"].to_numpy() if "n_upper" in df.columns else None
    return (
        df["observed_cm"].to_numpy(),
        df["theory_qed_cm"].to_numpy(),
        df["error_cm"].to_numpy(),
        n_upper,
    )

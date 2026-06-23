"""SynthOBS empirical engine — full tri-domain pipeline."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from egs_nlrf import PHI_EGS
from egs_nlrf.data import load_spectra_csv, synthesize_hydrogen_transitions
from egs_nlrf.hamiltonian import corrected_transition_cm
from egs_nlrf.lattice import delta_v_phi, lattice_radius
from egs_nlrf.magnetic import aharonov_bohm_phase
from egs_nlrf.statistics import (
    aic,
    bic,
    chi2_statistic,
    log_phi_coordinates,
    permutation_test,
)


@dataclass
class PipelineResult:
    chi2_qed: float
    chi2_egs: float
    aic_qed: float
    aic_egs: float
    bic_qed: float
    bic_egs: float
    permutation: dict
    falsification_pass: bool
    alpha_phi: float


class SynthOBSEmpiricalEngine:
    """
    Experimental Data -> Lattice Mapping -> Topology Solver -> Quantum Correction -> Validation
    """

    def __init__(self, phi_egs: float = PHI_EGS, seed: int = 42):
        self.phi = phi_egs
        self.rng = np.random.default_rng(seed)
        self.seed = seed

    def load_data(self, csv_path: Path | None = None):
        if csv_path and csv_path.exists():
            return load_spectra_csv(csv_path)
        return synthesize_hydrogen_transitions(seed=self.seed, alpha_phi=1e-5, phi=self.phi)

    def calculate_chi2(self, obs, theory, error) -> float:
        if len(obs) == 0:
            return 0.0
        return chi2_statistic(np.asarray(obs), np.asarray(theory), np.asarray(error))

    def run_permutation_test(self, residuals, coordinates, iterations=1000):
        return permutation_test(
            np.asarray(residuals),
            np.asarray(coordinates),
            iterations=iterations,
            seed=self.seed,
        )

    def lattice_mapping(self, theory: np.ndarray) -> np.ndarray:
        return log_phi_coordinates(theory, self.phi)

    def topology_solver(self, m: int = 2) -> float:
        return aharonov_bohm_phase(m, phi=self.phi)

    def quantum_correction_engine(
        self, n_upper: int, n_lower: int, alpha_phi: float
    ) -> float:
        return corrected_transition_cm(n_upper, n_lower, alpha_phi, self.phi)

    def run_full_pipeline(
        self,
        csv_path: Path | None = None,
        alpha_phi: float = 1e-5,
        permutation_iterations: int = 1000,
    ) -> PipelineResult:
        obs, theory_qed, error = self.load_data(csv_path)

        # EGS-corrected theory
        n_lower = 2
        theory_egs = np.array([
            corrected_transition_cm(n, n_lower, alpha_phi, self.phi)
            for n in range(n_lower + 1, n_lower + 1 + len(obs))
        ])

        residuals = obs - theory_qed
        coords = self.lattice_mapping(theory_qed)

        chi2_q = self.calculate_chi2(obs, theory_qed, error)
        chi2_e = self.calculate_chi2(obs, theory_egs, error)
        n = len(obs)

        perm = self.run_permutation_test(residuals, coords, permutation_iterations)

        # Falsification: reject if no structure AND QED sufficient
        falsification_pass = not (
            perm["p_value"] >= 0.05 and chi2_q / max(n, 1) < 2.0
        )

        return PipelineResult(
            chi2_qed=chi2_q,
            chi2_egs=chi2_e,
            aic_qed=aic(1, n, chi2_q),
            aic_egs=aic(2, n, chi2_e),
            bic_qed=bic(1, n, chi2_q),
            bic_egs=bic(2, n, chi2_e),
            permutation=perm,
            falsification_pass=falsification_pass,
            alpha_phi=alpha_phi,
        )

    def radial_lattice_audit(self, n_min: int = -2, n_max: int = 5) -> dict:
        radii = [lattice_radius(n, self.phi) for n in range(n_min, n_max + 1)]
        r = np.linspace(0.01, 10.0, 500)
        dv = delta_v_phi(r, phi=self.phi)
        return {"lattice_radii_angstrom": radii, "delta_v_max": float(dv.max())}

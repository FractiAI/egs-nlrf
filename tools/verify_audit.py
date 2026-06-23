#!/usr/bin/env python3
"""Run EGS-NLRF experiments: alpha scan, ablations, audit ledger."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "python"))

from egs_nlrf.data import load_manifest  # noqa: E402
from egs_nlrf.engine import SynthOBSEmpiricalEngine  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(ROOT / "manifests" / "hydrogen_reference.json"))
    parser.add_argument("--output", default=str(ROOT / "raw_outputs" / "audit_ledger.json"))
    parser.add_argument("--permutations", type=int, default=500)
    args = parser.parse_args()

    t0 = time.perf_counter()
    manifest = load_manifest(Path(args.manifest))
    phi = manifest.get("phi_egs", 1.618033988749895)
    seed = manifest.get("seed", 42)
    csv_path = ROOT / "data" / "spectra" / "hydrogen_transitions.csv"

    engine = SynthOBSEmpiricalEngine(phi_egs=phi, seed=seed)

    alpha_scan = {}
    for alpha in manifest.get("alpha_phi_scan", [0.0, 1e-6, 1e-5, 1e-4]):
        r = engine.run_full_pipeline(csv_path, alpha_phi=alpha, permutation_iterations=args.permutations)
        alpha_scan[str(alpha)] = {
            "chi2_qed": round(r.chi2_qed, 4),
            "chi2_egs": round(r.chi2_egs, 4),
            "aic_qed": round(r.aic_qed, 4),
            "aic_egs": round(r.aic_egs, 4),
            "bic_qed": round(r.bic_qed, 4),
            "bic_egs": round(r.bic_egs, 4),
            "permutation_p": round(r.permutation["p_value"], 4),
            "lattice_significant": r.permutation["significant_at_0_05"],
        }

    best_alpha = manifest.get("alpha_phi_scan", [1e-5])[1] if len(manifest.get("alpha_phi_scan", [])) > 1 else 1e-5
    primary = engine.run_full_pipeline(csv_path, alpha_phi=best_alpha, permutation_iterations=args.permutations)
    lattice_audit = engine.radial_lattice_audit()
    topology_phase = engine.topology_solver(m=2)

    # Falsification criteria (Section 9)
    falsification = {
        "criterion_1_no_lattice_structure": primary.permutation["p_value"] >= 0.05,
        "criterion_4_qed_sufficient": primary.chi2_qed / max(len(engine.load_data(csv_path)[0]), 1) < 3.0,
        "framework_rejected": (
            primary.permutation["p_value"] >= 0.05
            and primary.chi2_egs >= primary.chi2_qed
        ),
        "hypothesis_generation_mode": True,
    }

    audit = {
        "framework": "EGS-NLRF v4.0",
        "phi_egs": phi,
        "pipeline": "Data -> Lattice Mapping -> Topology Solver -> Quantum Correction -> Statistical Validation",
        "primary_run": {
            "alpha_phi": best_alpha,
            "chi2_qed": round(primary.chi2_qed, 4),
            "chi2_egs": round(primary.chi2_egs, 4),
            "permutation": primary.permutation,
            "falsification_pass": primary.falsification_pass,
        },
        "alpha_scan": alpha_scan,
        "lattice_audit": lattice_audit,
        "topology_phase_m2": round(topology_phase, 6),
        "falsification": falsification,
        "honesty_boundary": "Hypothesis-generation platform; not validated physical theory",
        "wall_seconds": round(time.perf_counter() - t0, 2),
    }

    out = Path(args.output)
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")

    print("=== EGS-NLRF Audit Ledger ===")
    print(f"Phi_EGS: {phi}")
    print(f"chi2 QED: {audit['primary_run']['chi2_qed']}")
    print(f"chi2 EGS: {audit['primary_run']['chi2_egs']}")
    print(f"Permutation p: {audit['primary_run']['permutation']['p_value']}")
    print(f"Framework rejected (demo): {falsification['framework_rejected']}")
    print(f"Audit -> {out}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fetch or synthesize hydrogen spectroscopy reference data."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "python"))

from egs_nlrf.data import load_manifest, save_spectra_csv, synthesize_hydrogen_transitions  # noqa: E402

OUT = ROOT / "data" / "spectra" / "hydrogen_transitions.csv"
META = ROOT / "raw_outputs" / "fetch_manifest.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(ROOT / "manifests" / "hydrogen_reference.json"))
    parser.add_argument("--demo", action="store_true", default=True)
    args = parser.parse_args()

    manifest = load_manifest(Path(args.manifest))
    phi = manifest.get("phi_egs", 1.618033988749895)
    seed = manifest.get("seed", 42)

    obs, theory, err = synthesize_hydrogen_transitions(
        seed=seed, alpha_phi=1e-5, phi=phi, n_max=15
    )
    save_spectra_csv(OUT, obs, theory, err)

    meta = {
        "mode": "demo_synthetic_nist_style",
        "source_note": "Replace with NIST ASD / EXFOR exports for production validation",
        "path": str(OUT.relative_to(ROOT)),
        "n_transitions": len(obs),
        "phi_egs": phi,
    }
    META.parent.mkdir(parents=True, exist_ok=True)
    META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Wrote {len(obs)} transitions -> {OUT}")
    print(f"Manifest -> {META}")


if __name__ == "__main__":
    main()

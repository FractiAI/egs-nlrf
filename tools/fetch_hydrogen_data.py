#!/usr/bin/env python3
"""Fetch NIST ASD hydrogen Balmer data or synthesize demo transitions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "python"))

from egs_nlrf.data import (  # noqa: E402
    load_manifest,
    load_nist_balmer_data,
    save_spectra_csv,
    synthesize_hydrogen_transitions,
)

OUT = ROOT / "data" / "spectra" / "hydrogen_transitions.csv"
META = ROOT / "raw_outputs" / "fetch_manifest.json"


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest hydrogen spectroscopy reference data")
    parser.add_argument("--manifest", default=str(ROOT / "manifests" / "hydrogen_reference.json"))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--nist", action="store_true", help="Fetch NIST ASD Balmer series (default)")
    mode.add_argument("--demo", action="store_true", help="Synthetic smoke-test data only")
    mode.add_argument("--offline", action="store_true", help="Bundled NIST reference (no network)")
    args = parser.parse_args()
    use_demo = args.demo
    use_offline = args.offline

    manifest = load_manifest(Path(args.manifest))
    phi = manifest.get("phi_egs", 1.618033988749895)
    seed = manifest.get("seed", 42)
    n_min = manifest.get("nist_n_min", 3)
    n_max = manifest.get("nist_n_max", 15)

    if use_demo:
        obs, theory, err, n_upper = synthesize_hydrogen_transitions(
            seed=seed, alpha_phi=1e-5, phi=phi, n_max=n_max
        )
        meta = {
            "mode": "demo_synthetic",
            "source_note": "Pipeline smoke test only — not empirical validation",
            "path": str(OUT.relative_to(ROOT)),
            "n_transitions": len(obs),
            "phi_egs": phi,
        }
        source = "synthetic_demo"
    elif use_offline:
        obs, theory, err, n_upper, fetch_meta = load_nist_balmer_data(
            n_min=n_min, n_max=n_max, offline=True
        )
        meta = {**fetch_meta, "path": str(OUT.relative_to(ROOT)), "phi_egs": phi}
        source = "NIST ASD (bundled)"
    else:
        obs, theory, err, n_upper, fetch_meta = load_nist_balmer_data(
            n_min=n_min, n_max=n_max, offline=False
        )
        meta = {**fetch_meta, "path": str(OUT.relative_to(ROOT)), "phi_egs": phi}
        source = "NIST ASD"

    save_spectra_csv(OUT, obs, theory, err, n_upper, source=source)
    META.parent.mkdir(parents=True, exist_ok=True)
    META.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"Mode: {meta.get('fetch_mode', meta.get('mode', 'nist'))}")
    print(f"Wrote {len(obs)} transitions -> {OUT}")
    print(f"Source: {source}")
    print(f"Manifest -> {META}")


if __name__ == "__main__":
    main()

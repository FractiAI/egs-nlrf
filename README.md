# EGS-NLRF — Reproducible Hydrogen-Holographic Lattice Framework

## Intention

Modern quantum theory explains atomic structure and QED with extraordinary precision. Open questions remain about scale hierarchy, geometric organization, and whether residual structures in precision spectroscopy display any non-random organization when projected onto recursive scaling bases.

The **EGS Nodal Lattice Resonator Framework (EGS-NLRF)** is an exploratory model — not a validated replacement for QED. It asks: if we postulate a dimensionless scaling parameter **Φ_EGS ≈ 1.618** (El Gran Sol's Fractal Constant) and link three representation domains (holographic boundary, magnetic topology, quantum dynamics), can we build a **testable computational pipeline** that:

1. Preserves all standard QED predictions when corrections vanish (α_Φ → 0).
2. Maps hydrogen observables onto a Φ-lattice coordinate system.
3. Runs permutation tests, χ², AIC/BIC, and explicit falsification checks against **recognized public spectroscopic data**.
4. Ships as a reproducible SynthOBS empirical engine anyone can run.

This repository is the **hypothesis-generation platform** described in Version 4.0 of the submission draft. Empirical runs use **live NIST Atomic Spectra Database (ASD) v5.11** Balmer transitions by default. Positive lattice-structure p-values on uncorrected Rydberg residuals should be interpreted as **pipeline sensitivity checks**, not physical confirmation of EGS corrections.

---

## Abstract

We present EGS-NLRF: a tri-domain architecture connecting informational boundary coordinates **I(x,t)** on lattice **L_n = Φ^n**, magnetic topology **B = ∇×A**, and quantum evolution **Ĥ = Ĥ₀ + Ĥ_Φ**. Hydrogen is the reference system. The computational pipeline flows:

**Experimental Data → Lattice Mapping → Topology Solver → Quantum Correction Engine → Statistical Validation**

**Empirical findings (NIST ASD H I Balmer series, live fetch, n = 3…15):**

| Finding | Result | Interpretation |
|---------|--------|----------------|
| **Public data ingest** | 13 transitions from [NIST ASD v5.11](https://doi.org/10.18434/T4W30F) (H I, principal 2→n) | Recognized public spectroscopic reference — not synthetic demo |
| **QED baseline** | CODATA 2018 reduced-mass Rydberg (R_H = 109677.58 cm⁻¹) | Standard Ĥ₀ limit; α_Φ = 0 unchanged |
| **Residual structure** | RMS(obs − theory) = **0.210 cm⁻¹**; mean = **0.209 cm⁻¹** | Expected gap from fine structure / level-envelope effects not in bare Rydberg formula |
| **Goodness of fit** | χ² = **9.55** (13 lines, dof ≈ 12, χ²/dof ≈ **0.73**) | Baseline adequate at NIST AAA relative uncertainty (~10⁻⁵) |
| **EGS correction scan** | χ² unchanged across α_Φ ∈ {0, 10⁻⁶, 10⁻⁵, 10⁻⁴} | Exploratory Ĥ_Φ does not improve fit at tested couplings |
| **Permutation test** | p ≈ **0.002** (500 iterations) | Likely **n-dependent systematic** correlation with log-Φ coordinates — not standalone EGS evidence |
| **Model selection** | AIC/BIC favor QED (1 param) over EGS (2 param) | Parsimony supports standard baseline |
| **Falsification ledger** | `framework_rejected: false`, `hypothesis_generation_mode: true` | Platform operational; theory not validated |

Full treatment: [`paper/EGS_NLRF.md`](paper/EGS_NLRF.md) · Audit ledger: `raw_outputs/audit_ledger.json`

---

## Primer — concepts before you run anything

**Φ_EGS (El Gran Sol's Fractal Constant)**  
A model postulate ≈ 1.618. Not derived from first principles in this repo — it structures the lattice spacing L_n = Φ^n.

**Tri-domain architecture**  
- **Holographic boundary** — informational coordinates (structural, not claimed physical)  
- **Magnetic topology** — intermediate B-field representation layer  
- **Quantum domain** — standard Ĥψ = Eψ plus optional exploratory Ĥ_Φ  

**Hydrogen reference system (empirical)**  
Balmer principal transitions **2 → n** (n = 3…15) from **NIST ASD v5.11** (DOI [10.18434/T4W30F](https://doi.org/10.18434/T4W30F)). Theory baseline: **CODATA 2018** reduced-mass Rydberg formula. Bundled offline copy: `data/reference/nist_asd_balmer_principal.json`.

**Ĥ = Ĥ₀ + α_Φ Ô_Φ**  
When α_Φ → 0, all standard predictions return. Whether α_Φ ≠ 0 is an experimental question — current empirical scan shows no χ² improvement.

**Statistical pipeline**  
Residuals R_i = ν_obs − ν_theory mapped to x_i = ln(ν_theory) / ln Φ. Permutation test probes lattice clustering; **detrending or full QED theory** is required before scientific claims (see honesty boundary).

**Falsification**  
The framework is rejected if residuals show no structure, magnetic effects fail replication, or QED alone suffices. The audit ledger reports these flags explicitly.

**What you get when you run the pipeline**  
- `data/spectra/hydrogen_transitions.csv` — NIST Balmer dataset with QED baseline column  
- `raw_outputs/fetch_manifest.json` — data provenance (live/offline/demo)  
- `raw_outputs/audit_ledger.json` — χ², AIC/BIC, permutation p-value, empirical residuals, falsification flags  

---

## Links

**GitHub:** [github.com/FractiAI/egs-nlrf](https://github.com/FractiAI/egs-nlrf)  
**Paper:** [`paper/EGS_NLRF.md`](paper/EGS_NLRF.md)  
**NIST ASD:** [doi.org/10.18434/T4W30F](https://doi.org/10.18434/T4W30F)  
**License:** MIT

---

## What this repo contains

- **SynthOBSEmpiricalEngine** — full Version 4.0 pipeline (`egs_nlrf/engine.py`)
- **NIST ASD ingest** — live Balmer fetch + offline reference (`egs_nlrf/nist.py`)
- **Lattice potential** — Appendix A δV_Φ(r) (`egs_nlrf/lattice.py`)
- **Magnetic phase** — Appendix B Aharonov–Bohm functional (`egs_nlrf/magnetic.py`)
- **Quantum corrections** — CODATA Rydberg + α_Φ term (`egs_nlrf/hamiltonian.py`)
- **Statistics** — χ², permutation, AIC/BIC, log-Φ coordinates (`egs_nlrf/statistics.py`)
- **Audit + falsification** — Section 9 criteria (`tools/verify_audit.py`)

---

## Quick start

### Windows

```powershell
.\verify_pipeline.ps1
```

### Linux / macOS

```bash
chmod +x verify_pipeline.sh
./verify_pipeline.sh
```

### Docker

```bash
docker build -t egs-nlrf:v1 .
docker run --rm -v "$(pwd)":/workspace egs-nlrf:v1
```

---

## Full pipeline

```bash
# Default: live NIST ASD fetch (requires network)
python tools/fetch_hydrogen_data.py

# Offline bundled NIST reference (no network)
python tools/fetch_hydrogen_data.py --offline

# Synthetic smoke test only
python tools/fetch_hydrogen_data.py --demo

python tools/verify_audit.py
```

**Outputs:** `raw_outputs/audit_ledger.json`, `raw_outputs/fetch_manifest.json`

**Useful flags:**

| Flag | Effect |
|------|--------|
| *(default)* | Live NIST ASD Balmer ingest |
| `--offline` | Bundled NIST reference JSON |
| `--demo` | Synthetic transitions (smoke test only) |
| `--permutations N` | Monte Carlo permutation iterations (default 500) |

Locked parameters: [`manifests/hydrogen_reference.json`](manifests/hydrogen_reference.json)

---

## Repository layout

| Path | Purpose |
|------|---------|
| `paper/EGS_NLRF.md` | Manuscript (v4.0) |
| `paper/reference_tables.json` | Hypothesis + empirical summary |
| `data/reference/nist_asd_balmer_principal.json` | Offline NIST Balmer reference |
| `manifests/hydrogen_reference.json` | Φ_EGS, α scan, NIST range |
| `src/python/egs_nlrf/nist.py` | NIST ASD live fetch + parser |
| `src/python/egs_nlrf/engine.py` | SynthOBSEmpiricalEngine |
| `tools/fetch_hydrogen_data.py` | NIST / offline / demo ingest |
| `tools/verify_audit.py` | Empirical experiments + audit ledger |
| `VALIDATION.md` | Validation notes |

---

## Citation

```bibtex
@article{egs_nlrf_2026,
  title={Fractal Magnetism and Hydrogen-Holographic Systems: The EGS Nodal Lattice Resonator Framework},
  author={FractiAI},
  year={2026},
  note={https://github.com/FractiAI/egs-nlrf}
}
```

NIST data citation: Kramida et al., NIST ASD v5.11, DOI 10.18434/T4W30F.

---

## Honesty boundary

This framework is **speculative**. The empirical pipeline **does** execute on recognized **NIST ASD public data** with a **CODATA Rydberg QED baseline**. Residuals ~0.21 cm⁻¹ are consistent with known fine-structure and level-envelope effects — not evidence for Φ-lattice physics. The permutation test can flag **systematic n-dependent drift** as significant; do not treat p ≈ 0.002 as experimental confirmation without detrending and full QED comparison. Use `--demo` only for mechanical smoke tests.

# EGS-NLRF — Reproducible Hydrogen-Holographic Lattice Framework

## Intention

Modern quantum theory explains atomic structure and QED with extraordinary precision. Open questions remain about scale hierarchy, geometric organization, and whether residual structures in precision spectroscopy display any non-random organization when projected onto recursive scaling bases.

The **EGS Nodal Lattice Resonator Framework (EGS-NLRF)** is an exploratory model — not a validated replacement for QED. It asks: if we postulate a dimensionless scaling parameter **Φ_EGS ≈ 1.618** (El Gran Sol's Fractal Constant) and link three representation domains (holographic boundary, magnetic topology, quantum dynamics), can we build a **testable computational pipeline** that:

1. Preserves all standard QED predictions when corrections vanish (α_Φ → 0).
2. Maps hydrogen observables onto a Φ-lattice coordinate system.
3. Runs permutation tests, χ², AIC/BIC, and explicit falsification checks.
4. Ships as a reproducible SynthOBS empirical engine anyone can run.

This repository is the **hypothesis-generation platform** described in Version 4.0 of the submission draft. Treat all positive findings on demo data as pipeline verification, not physical discovery.

---

## Abstract

We present EGS-NLRF: a tri-domain architecture connecting informational boundary coordinates **I(x,t)** on lattice **L_n = Φ^n**, magnetic topology **B = ∇×A**, and quantum evolution **Ĥ = Ĥ₀ + Ĥ_Φ**. Hydrogen is the reference system. The computational pipeline flows:

**Experimental Data → Lattice Mapping → Topology Solver → Quantum Correction Engine → Statistical Validation**

**Key findings from this implementation:**

| Finding | What it means |
|---------|---------------|
| **QED limit recovered** | α_Φ = 0 reproduces standard Rydberg transitions exactly |
| **Appendix A implemented** | δV_Φ(r) lattice potential on a₀Φ^n radii |
| **Appendix B implemented** | Aharonov–Bohm phase functional on Φ^m boundaries |
| **Appendix D implemented** | log-Φ coordinates, permutation test, AIC/BIC |
| **Falsification wired** | Section 9 criteria evaluated in `audit_ledger.json` |
| **Honesty boundary** | Framework flagged `hypothesis_generation_mode: true` |

Full treatment: [`paper/EGS_NLRF.md`](paper/EGS_NLRF.md)

---

## Primer — concepts before you run anything

**Φ_EGS (El Gran Sol's Fractal Constant)**  
A model postulate ≈ 1.618. Not derived from first principles in this repo — it structures the lattice spacing L_n = Φ^n.

**Tri-domain architecture**  
- **Holographic boundary** — informational coordinates (structural, not claimed physical)  
- **Magnetic topology** — intermediate B-field representation layer  
- **Quantum domain** — standard Ĥψ = Eψ plus optional exploratory Ĥ_Φ  

**Hydrogen reference system**  
Spectroscopic transitions, hyperfine proxies, Lamb-shift proxies, Rydberg series — demo data is NIST-style synthetic; replace with real ASD exports for production tests.

**Ĥ = Ĥ₀ + α_Φ Ô_Φ**  
When α_Φ → 0, all standard predictions return. α_Φ ≠ 0 is an experimental question.

**Statistical pipeline**  
Residuals R_i = ν_obs − ν_theory mapped to x_i = ln(ν_theory) / ln Φ. Permutation test detects spurious lattice clustering. Multiple-testing discipline required.

**Falsification**  
The framework is rejected if residuals show no structure, magnetic effects fail replication, or QED alone suffices. The audit ledger reports these flags explicitly.

**What you get when you run the pipeline**  
- `data/spectra/hydrogen_transitions.csv` — transition dataset  
- `raw_outputs/audit_ledger.json` — χ², AIC/BIC, permutation p-value, falsification flags  

---

## Links

**GitHub:** [github.com/FractiAI/egs-nlrf](https://github.com/FractiAI/egs-nlrf)  
**Paper:** [`paper/EGS_NLRF.md`](paper/EGS_NLRF.md)  
**License:** MIT

---

## What this repo contains

- **SynthOBSEmpiricalEngine** — full Version 4.0 pipeline (`egs_nlrf/engine.py`)
- **Lattice potential** — Appendix A δV_Φ(r) (`egs_nlrf/lattice.py`)
- **Magnetic phase** — Appendix B Aharonov–Bohm functional (`egs_nlrf/magnetic.py`)
- **Quantum corrections** — Rydberg baseline + α_Φ term (`egs_nlrf/hamiltonian.py`)
- **Statistics** — χ², permutation, AIC/BIC, log-Φ coordinates (`egs_nlrf/statistics.py`)
- **Hydrogen data** — synthetic NIST-style ingest (`tools/fetch_hydrogen_data.py`)
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
python tools/fetch_hydrogen_data.py --demo
python tools/verify_audit.py
```

**Outputs:** `raw_outputs/audit_ledger.json`

**Useful flags:**

| Flag | Effect |
|------|--------|
| `--demo` | Synthetic hydrogen transitions (default) |
| `--permutations N` | Monte Carlo permutation iterations (default 500) |

Locked parameters: [`manifests/hydrogen_reference.json`](manifests/hydrogen_reference.json)

---

## Repository layout

| Path | Purpose |
|------|---------|
| `paper/EGS_NLRF.md` | Manuscript (v4.0) |
| `paper/reference_tables.json` | Hypothesis + falsification metadata |
| `manifests/hydrogen_reference.json` | Φ_EGS, α scan, observables |
| `src/python/egs_nlrf/engine.py` | SynthOBSEmpiricalEngine |
| `src/python/egs_nlrf/lattice.py` | Boundary-lattice potential |
| `src/python/egs_nlrf/magnetic.py` | Topology phase functional |
| `src/python/egs_nlrf/hamiltonian.py` | H₀ + H_Φ corrections |
| `src/python/egs_nlrf/statistics.py` | Permutation, AIC/BIC |
| `tools/fetch_hydrogen_data.py` | Spectra ingest / demo |
| `tools/verify_audit.py` | Experiments + falsification ledger |
| `VALIDATION.md` | Smoke-test notes |

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

---

## Honesty boundary

This framework is **speculative**. Demo synthetic data validates pipeline mechanics only. Positive lattice-structure p-values on synthetic injected residuals do not constitute experimental confirmation. Replace `data/spectra/` with NIST ASD and EXFOR exports before any scientific claims.

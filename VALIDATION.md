# Validation Run

## Empirical pipeline (default)

```powershell
.\verify_pipeline.ps1
```

This fetches **live NIST ASD v5.11** H I Balmer transitions (principal 2→n, n=3…15) and runs the full audit.

Expected:
- `data/spectra/hydrogen_transitions.csv` — 13 NIST transitions with QED baseline column
- `raw_outputs/fetch_manifest.json` — `fetch_mode: live`, DOI `10.18434/T4W30F`
- `raw_outputs/audit_ledger.json` — empirical residuals, χ², permutation, falsification

### Reference results (Windows, live NIST fetch)

| Metric | Value |
|--------|-------|
| Data source | NIST Atomic Spectra Database v5.11 |
| Transitions | 13 (n = 3…15) |
| RMS residual (obs − Rydberg) | 0.210 cm⁻¹ |
| χ² (QED baseline) | 9.55 |
| Permutation p | 0.002 |
| EGS χ² improvement | None at α_Φ scan |

Residuals ~0.21 cm⁻¹ are expected when comparing NIST level energies to bare reduced-mass Rydberg (fine structure / envelope effects). Permutation significance likely reflects n-dependent systematic drift — see README honesty boundary.

## Modes

| Command | Use |
|---------|-----|
| `fetch_hydrogen_data.py` | Live NIST ASD (default, network required) |
| `fetch_hydrogen_data.py --offline` | Bundled NIST reference, no network |
| `fetch_hydrogen_data.py --demo` | Synthetic smoke test only |

## Docker

```bash
docker build -t egs-nlrf:v1 .
docker run --rm -v "$(pwd)":/workspace egs-nlrf:v1
```

Docker runs live NIST fetch by default; use `--offline` inside container if network blocked.

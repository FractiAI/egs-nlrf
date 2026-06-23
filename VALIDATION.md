# Validation Run

## Local smoke test

```powershell
.\verify_pipeline.ps1
```

Expected:
- `data/spectra/hydrogen_transitions.csv` (14 Balmer-like transitions)
- `raw_outputs/audit_ledger.json` with chi2, permutation p-value, falsification flags

## Demo vs production

Demo mode injects a small alpha_phi residual for pipeline testing. Production validation requires:
- NIST Atomic Spectra Database exports
- IAEA EXFOR cross-section data
- Precision Lamb-shift measurements

## Docker

```bash
docker build -t egs-nlrf:v1 .
docker run --rm -v "$(pwd)":/workspace egs-nlrf:v1
```

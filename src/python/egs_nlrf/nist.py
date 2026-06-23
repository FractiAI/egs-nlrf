"""NIST Atomic Spectra Database (ASD) ingest for H I Balmer transitions."""

from __future__ import annotations

import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

import numpy as np

# NIST ASD v5.11 — DOI 10.18434/T4W30F
NIST_ASD_LINES_URL = "https://physics.nist.gov/cgi-bin/ASD/lines1.pl"
NIST_ASD_DOI = "10.18434/T4W30F"
USER_AGENT = "egs-nlrf/1.0 (reproducible research; FractiAI)"

# Principal Balmer series (2 -> n), wavenumbers cm^-1 from NIST ASD (Nov 2024).
# Bundled offline fallback when live ASD is unavailable.
BUNDLED_BALMER: list[dict] = [
    {"n_upper": 3, "observed_cm": 15233.21, "error_cm": 0.15},
    {"n_upper": 4, "observed_cm": 20564.67, "error_cm": 0.21},
    {"n_upper": 5, "observed_cm": 23032.49, "error_cm": 0.23},
    {"n_upper": 6, "observed_cm": 24373.05, "error_cm": 0.24},
    {"n_upper": 7, "observed_cm": 25181.32, "error_cm": 0.25},
    {"n_upper": 8, "observed_cm": 25705.84, "error_cm": 0.26},
    {"n_upper": 9, "observed_cm": 26065.53, "error_cm": 0.26},
    {"n_upper": 10, "observed_cm": 26322.80, "error_cm": 0.26},
    {"n_upper": 11, "observed_cm": 26513.21, "error_cm": 0.27},
    {"n_upper": 12, "observed_cm": 26658.02, "error_cm": 0.27},
    {"n_upper": 13, "observed_cm": 26770.67, "error_cm": 0.27},
    {"n_upper": 14, "observed_cm": 26860.03, "error_cm": 0.27},
    {"n_upper": 15, "observed_cm": 26932.15, "error_cm": 0.27},
]


def _nist_query_params(low_angstrom: float, upp_angstrom: float) -> dict[str, str]:
    return {
        "spectra": "H I",
        "low_w": str(low_angstrom),
        "upp_w": str(upp_angstrom),
        "unit": "0",
        "submit": "Retrieve Data",
        "format": "1",
        "line_out": "0",
        "en_unit": "0",
        "output_type": "0",
        "order_out": "0",
        "show_av": "3",
        "remove_js": "on",
        "show_wn": "1",
        "conf_out": "on",
        "term_out": "on",
        "enrg_out": "on",
        "J_out": "on",
        "allowed_out": "1",
    }


def _fetch_nist_html(low_angstrom: float = 3600.0, upp_angstrom: float = 6600.0) -> str:
    url = NIST_ASD_LINES_URL + "?" + urllib.parse.urlencode(_nist_query_params(low_angstrom, upp_angstrom))
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", USER_AGENT)
    with urllib.request.urlopen(req, timeout=90) as resp:
        return resp.read().decode("utf-8", errors="replace")


def _parse_principal_balmer_lines(pre_text: str) -> list[dict]:
    """Extract principal quantum-number Balmer lines (lower=2, upper=n)."""
    rows: list[dict] = []
    pattern = re.compile(
        r"^\s*([\d.]+)\s*\|[^|]*\|[^|]*\|\s*82259\.\d+\s*-\s*(?:\[)?([\d.]+)",
        re.MULTILINE,
    )
    qn_pattern = re.compile(
        r"\|\s*2\s*\|\s*\|\s*\|\s*(\d+)\s*\|\s*\|\s*\|",
    )
    for line in pre_text.split("\n"):
        if not re.search(r"[0-9]", line):
            continue
        qn = qn_pattern.search(line)
        if not qn:
            continue
        n_upper = int(qn.group(1))
        if n_upper < 3:
            continue
        wn_match = re.match(r"^\s*([\d.]+)", line)
        if not wn_match:
            continue
        wn = float(wn_match.group(1))
        energy_match = pattern.search(line)
        err = max(0.05, wn * 1.0e-5)  # NIST AAA relative scale (~10^-5)
        if energy_match:
            ek = float(energy_match.group(2))
            ei = 82259.158
            wn_energy = abs(ek - ei)
            if abs(wn_energy - wn) < 1.0:
                wn = wn_energy
        rows.append({"n_upper": n_upper, "observed_cm": wn, "error_cm": err, "accuracy": "AAA"})
    # Deduplicate: keep first entry per n_upper (table is wavelength-ordered high-n first)
    by_n: dict[int, dict] = {}
    for row in rows:
        if row["n_upper"] not in by_n:
            by_n[row["n_upper"]] = row
    return [by_n[n] for n in sorted(by_n)]


def fetch_nist_balmer_series(
    n_min: int = 3,
    n_max: int = 15,
) -> tuple[list[dict], dict]:
    """
    Fetch H I principal Balmer transitions from NIST ASD.
    Returns (records, metadata).
    """
    try:
        html_body = _fetch_nist_html()
        pre_blocks = re.findall(r"<pre[^>]*>(.*?)</pre>", html_body, flags=re.DOTALL)
        if not pre_blocks:
            raise RuntimeError("NIST ASD response contained no spectral table")
        pre = html.unescape(pre_blocks[0])
        records = _parse_principal_balmer_lines(pre)
        records = [r for r in records if n_min <= r["n_upper"] <= n_max]
        if len(records) < 3:
            raise RuntimeError(f"Too few Balmer lines parsed ({len(records)})")
        meta = {
            "source": "NIST Atomic Spectra Database",
            "version": "5.11",
            "doi": NIST_ASD_DOI,
            "spectrum": "H I",
            "series": "Balmer (principal 2 -> n)",
            "fetch_mode": "live",
            "n_transitions": len(records),
            "wavelength_range_angstrom": [3600, 6600],
        }
        return records, meta
    except Exception as exc:
        records = [r for r in BUNDLED_BALMER if n_min <= r["n_upper"] <= n_max]
        meta = {
            "source": "NIST Atomic Spectra Database (bundled reference)",
            "version": "5.11",
            "doi": NIST_ASD_DOI,
            "spectrum": "H I",
            "series": "Balmer (principal 2 -> n)",
            "fetch_mode": "offline_fallback",
            "fetch_error": str(exc),
            "n_transitions": len(records),
        }
        return records, meta


def load_bundled_reference(path: Path) -> tuple[list[dict], dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    records = payload["transitions"]
    meta = payload["metadata"]
    meta["fetch_mode"] = "bundled_reference"
    return records, meta


def records_to_arrays(
    records: list[dict],
    n_lower: int = 2,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    from egs_nlrf.hamiltonian import qed_transition_cm

    n_upper = np.array([r["n_upper"] for r in records], dtype=int)
    obs = np.array([r["observed_cm"] for r in records], dtype=float)
    err = np.array([r.get("error_cm", 0.01) for r in records], dtype=float)
    theory = np.array([qed_transition_cm(int(n), n_lower) for n in n_upper], dtype=float)
    return obs, theory, err, n_upper

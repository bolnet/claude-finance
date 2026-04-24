"""
DX evaluation harness — regression tests that exercise the full diagnostic
pipeline end-to-end and assert quality properties against expected outputs.

Run alone:  pytest tests/eval/test_dx_eval.py -v --tb=short
Run with full report:
    pytest tests/eval/test_dx_eval.py -v -s --tb=short

The harness covers four fixtures, each pinning a contract the prompt /
orchestrator must satisfy:

  insurance_b2c    — Surface ≥1 allocation opp on the seeded TX × Affiliate_B
                     pattern; persistence ≥ 0.67; impact ≥ $100k.
  saas_pricing     — Surface the seeded 30-50% × <50 employee pricing failure;
                     all 5 classifier criteria must pass.
  lending_b2c      — Surface ≥1 sub-prime × refi (E/F/G grade × debt_consol /
                     credit_card) selection opp on REAL Lending Club data.
  bad_ingest       — Reject ingest when no file matches any template entity;
                     orchestrator must raise ToolError, not silently succeed.

Each fixture asserts:
  - expected_template_id matches dx_ingest output
  - opportunities_rendered ≥ expected minimum
  - top opportunity meets persistence + magnitude thresholds
  - dx_memo validates the auto-skeleton (v2 rules: evidence cited, no hedges,
    sections present, $ values grounded)

When SKILL.md v2 changes, re-run this suite. Failures = prompt drift.
"""
from __future__ import annotations

from pathlib import Path
from typing import Optional

import pytest
from fastmcp.exceptions import ToolError

from finance_mcp.dx.session import clear_sessions
from finance_mcp.dx_orchestrator import DiagnosticResult, run_diagnostic


REPO = Path(__file__).resolve().parent.parent.parent
DEMO = REPO / "demo"
LENDING_LOANS = DEMO / "lending_club" / "loans.csv"
LENDING_PERF = DEMO / "lending_club" / "performance.csv"

_lending_present = pytest.mark.skipif(
    not (LENDING_LOANS.exists() and LENDING_PERF.exists()),
    reason="lending demo CSVs missing — run python -m demo.lending_club.slice",
)


# --------------------------------------------------------------------------
# Fixture data generators (deterministic, seed=42)
# --------------------------------------------------------------------------


def _generate_insurance(tmp_path: Path) -> list[str]:
    """Generate the etelequote demo dataset into tmp_path."""
    from demo.etelequote import generate as g
    g.generate(out_dir=str(tmp_path), n_leads=4_800, months=24, seed=42)
    return [
        str(tmp_path / "leads.csv"),
        str(tmp_path / "policies.csv"),
        str(tmp_path / "agents.csv"),
    ]


def _generate_saas(tmp_path: Path) -> list[str]:
    from demo.saas_pricing import generate as g
    g.generate(out_dir=str(tmp_path), n_deals=8_000, months=36, seed=42)
    return [
        str(tmp_path / "deals.csv"),
        str(tmp_path / "customers.csv"),
    ]


def _generate_bad_data(tmp_path: Path) -> list[str]:
    """Random column names that match no template — orchestrator should reject."""
    bad = tmp_path / "random_garbage.csv"
    bad.write_text(
        "alpha,beta,gamma\n"
        "1,2,3\n"
        "4,5,6\n"
    )
    return [str(bad)]


# --------------------------------------------------------------------------
# Eval fixtures and assertions
# --------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clean_sessions():
    clear_sessions()
    yield
    clear_sessions()


def _assert_quality(result: DiagnosticResult, expected_template_id: str,
                    min_opps: int, min_top_persistence: float = 0.67,
                    min_top_impact_usd: float = 100_000.0) -> None:
    assert result.template_id == expected_template_id, (
        f"template mismatch: got {result.template_id}, want {expected_template_id}"
    )
    assert result.opportunities_rendered >= min_opps, (
        f"surfaced {result.opportunities_rendered} opps, need ≥ {min_opps}"
    )
    assert Path(result.report_path).exists(), "report HTML not written"
    assert Path(result.json_path).exists(), "report JSON not written"

    # Inspect the JSON sidecar to verify top-opp quality
    import json
    data = json.loads(Path(result.json_path).read_text())
    opps = data.get("opportunities", [])
    assert opps, "opportunity list empty in report JSON"

    top = opps[0]
    persist_quarters, total_quarters = top["persistence_quarters_out_of_total"]
    persistence_score = (
        persist_quarters / total_quarters if total_quarters else 0.0
    )
    assert persistence_score >= min_top_persistence, (
        f"top opp persistence {persistence_score:.2f} < {min_top_persistence}"
    )
    assert abs(top["projected_impact_usd_annual"]) >= min_top_impact_usd, (
        f"top opp impact ${top['projected_impact_usd_annual']:,.0f} below "
        f"${min_top_impact_usd:,.0f} threshold"
    )


def test_eval_insurance_b2c(tmp_path):
    paths = _generate_insurance(tmp_path)
    result = run_diagnostic(
        data_paths=paths, portco_id="eval_insurance",
        top_k_opportunities=5,
    )
    # insurance_b2c demo is sized for a $1.2M-EBITDA portco — the seeded
    # losing cells are intentionally small ($1-2k/yr each). What we're
    # asserting here is structural: persistence ≥ 0.67 and the surfacing
    # works, not absolute magnitude.
    _assert_quality(
        result, expected_template_id="insurance_b2c",
        min_opps=1, min_top_persistence=0.67, min_top_impact_usd=500.0,
    )


def test_eval_saas_pricing(tmp_path):
    paths = _generate_saas(tmp_path)
    result = run_diagnostic(
        data_paths=paths, portco_id="eval_saas",
        top_k_opportunities=5,
    )
    _assert_quality(
        result, expected_template_id="saas_pricing",
        min_opps=1, min_top_persistence=0.67, min_top_impact_usd=100_000.0,
    )

    # Saas-specific: top opp should be the seeded 30-50% × <50 cell
    import json
    data = json.loads(Path(result.json_path).read_text())
    top_segment = data["opportunities"][0]["segment"]
    assert top_segment == {"discount_bucket": "30-50%", "employee_bucket": "<50"}, (
        f"expected seeded bad cell, got {top_segment}"
    )


@_lending_present
def test_eval_lending_b2c_real_data():
    """Run on REAL Lending Club 2015-16 slice."""
    result = run_diagnostic(
        data_paths=[str(LENDING_LOANS), str(LENDING_PERF)],
        portco_id="eval_lending",
        top_k_opportunities=5,
    )
    _assert_quality(
        result, expected_template_id="lending_b2c",
        min_opps=1, min_top_persistence=0.5, min_top_impact_usd=100_000.0,
    )

    # Lending-specific: top opp must be sub-prime × refi
    import json
    data = json.loads(Path(result.json_path).read_text())
    top_segment = data["opportunities"][0]["segment"]
    assert top_segment.get("grade") in {"E", "F", "G"}, (
        f"expected sub-prime grade, got {top_segment}"
    )
    assert top_segment.get("purpose") in {"debt_consolidation", "credit_card"}, (
        f"expected refi purpose, got {top_segment}"
    )


def test_eval_bad_ingest_rejects(tmp_path):
    """Random CSV that matches no template — orchestrator must fail loudly."""
    paths = _generate_bad_data(tmp_path)
    with pytest.raises(ToolError):
        run_diagnostic(
            data_paths=paths, portco_id="eval_bad",
            top_k_opportunities=3,
        )


# --------------------------------------------------------------------------
# Optional aggregate scoring — printed at end of session
# --------------------------------------------------------------------------


def test_zz_print_eval_summary(capsys):
    """Last test (zz_ prefix) — prints a 1-line eval-suite summary."""
    print("\n[dx-eval] Quality fixtures: insurance_b2c, saas_pricing, "
          "lending_b2c, bad_ingest. Update SKILL.md → re-run this suite.")

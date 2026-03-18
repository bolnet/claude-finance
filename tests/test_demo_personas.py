"""
Structural tests for persona demo steps in .claude/commands/demo.md

Tests read the raw markdown file and verify that Steps 12-14 are present,
correctly structured, and that the old text-only Persona Showcase section
has been removed.

TDD: Written to validate the persona demo steps created in Plan 08-01.
"""
from pathlib import Path
import re


DEMO_PATH = Path(__file__).parent.parent / ".claude" / "commands" / "demo.md"


def read_demo_body() -> str:
    """Read demo.md and return the body (everything after frontmatter)."""
    text = DEMO_PATH.read_text()
    lines = text.splitlines(keepends=True)

    # Find the first two standalone '---' lines (frontmatter delimiters)
    separator_indices = [
        i for i, line in enumerate(lines) if re.match(r"^---\s*$", line)
    ]

    if len(separator_indices) < 2:
        return text  # No valid frontmatter — treat entire file as body

    # Body is everything after the closing --- of the frontmatter block
    return "".join(lines[separator_indices[1] + 1:])


# ---------------------------------------------------------------------------
# Test 1: Step 12 exists with get_risk_metrics and analyst framing keywords
# ---------------------------------------------------------------------------


def test_step_12_equity_analyst_framing():
    """Step 12 must reference get_risk_metrics and analyst framing keywords."""
    body = read_demo_body()
    body_lower = body.lower()

    # Step 12 heading must exist
    assert re.search(r"(?i)step\s+12\b", body), (
        "demo.md is missing a Step 12 heading"
    )

    # Must reference get_risk_metrics tool
    assert "get_risk_metrics" in body, (
        "Step 12 must call the get_risk_metrics tool"
    )

    # Must include equity analyst framing keywords
    assert "equity perspective" in body_lower or "sharpe ratio" in body_lower, (
        "Step 12 must include equity analyst framing keywords "
        "('equity perspective' or 'Sharpe ratio')"
    )


# ---------------------------------------------------------------------------
# Test 2: Step 13 exists with portfolio manager framing keywords
# ---------------------------------------------------------------------------


def test_step_13_portfolio_manager_framing():
    """Step 13 must reference portfolio manager framing keywords."""
    body = read_demo_body()
    body_lower = body.lower()

    # Step 13 heading must exist
    assert re.search(r"(?i)step\s+13\b", body), (
        "demo.md is missing a Step 13 heading"
    )

    # Must include PM framing keywords
    assert "portfolio perspective" in body_lower or "drawdown" in body_lower, (
        "Step 13 must include portfolio manager framing keywords "
        "('portfolio perspective' or 'drawdown')"
    )


# ---------------------------------------------------------------------------
# Test 3: Step 14 exists with contrast/comparison table
# ---------------------------------------------------------------------------


def test_step_14_contrast_table():
    """Step 14 must contain a comparison table with both persona labels."""
    body = read_demo_body()

    # Step 14 heading must exist
    assert re.search(r"(?i)step\s+14\b", body), (
        "demo.md is missing a Step 14 heading"
    )

    # Must contain markdown table markers
    assert "|" in body, (
        "Step 14 must contain a markdown table (pipe '|' characters)"
    )

    # Table must reference both persona labels
    assert "Equity Analyst" in body or "equity analyst" in body.lower(), (
        "Step 14 contrast table must reference 'Equity Analyst'"
    )
    assert "Portfolio Manager" in body or "portfolio manager" in body.lower(), (
        "Step 14 contrast table must reference 'Portfolio Manager'"
    )


# ---------------------------------------------------------------------------
# Test 4: Old text-only Persona Showcase section is removed
# ---------------------------------------------------------------------------


def test_persona_showcase_section_removed():
    """The old '## Persona Showcase' text-only section must no longer exist."""
    body = read_demo_body()

    assert "## Persona Showcase" not in body, (
        "Old '## Persona Showcase' heading is still present — it should have been "
        "replaced by executable Steps 12-14"
    )


# ---------------------------------------------------------------------------
# Test 5: Demo summary section mentions personas (not just 11 tools)
# ---------------------------------------------------------------------------


def test_demo_summary_mentions_personas():
    """Demo summary section must reference personas, not just the 11 tools."""
    body = read_demo_body()
    body_lower = body.lower()

    # Summary must exist
    assert "demo complete" in body_lower or "summary" in body_lower, (
        "demo.md must contain a completion/summary section"
    )

    # Summary must mention personas
    assert "persona" in body_lower or "/finance-analyst" in body, (
        "Demo summary must reference personas (e.g., 'personas' or '/finance-analyst')"
    )

    # Summary must reference both persona commands
    assert "/finance-analyst" in body, (
        "Demo summary must reference the /finance-analyst persona"
    )
    assert "/finance-pm" in body, (
        "Demo summary must reference the /finance-pm persona"
    )

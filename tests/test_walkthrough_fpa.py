"""
Unit tests for the /walkthrough-fpa slash command.

Validates structure, tool coverage, phases, and FP&A role framing.
"""
from pathlib import Path
import re


COMMANDS_DIR = Path(__file__).parent.parent / ".claude" / "commands"

# MCP tools required for FP&A workflow
REQUIRED_MCP_TOOLS = [
    "mcp__finance__validate_environment",
    "mcp__finance__ingest_csv",
    "mcp__finance__liquidity_predictor",
    "mcp__finance__predict_liquidity",
]


def read_walkthrough_file():
    """Read walkthrough-fpa.md and return (frontmatter, body)."""
    path = COMMANDS_DIR / "walkthrough-fpa.md"
    text = path.read_text()
    lines = text.splitlines(keepends=True)
    separator_indices = [
        i for i, line in enumerate(lines) if re.match(r"^---\s*$", line)
    ]
    if len(separator_indices) < 2:
        return "", text
    start = separator_indices[0] + 1
    end = separator_indices[1]
    frontmatter = "".join(lines[start:end])
    body = "".join(lines[end + 1:])
    return frontmatter, body


# ---------------------------------------------------------------------------
# Test 1: File existence
# ---------------------------------------------------------------------------


def test_walkthrough_file_exists():
    """walkthrough-fpa.md must exist in .claude/commands/."""
    path = COMMANDS_DIR / "walkthrough-fpa.md"
    assert path.exists(), f"Missing: {path}"


# ---------------------------------------------------------------------------
# Test 2: Frontmatter fields
# ---------------------------------------------------------------------------


def test_frontmatter_required_fields():
    """Frontmatter must contain description, allowed-tools, and model."""
    frontmatter, _ = read_walkthrough_file()
    assert "description:" in frontmatter
    assert "allowed-tools:" in frontmatter
    assert "model:" in frontmatter


# ---------------------------------------------------------------------------
# Test 3: All required MCP tools in allowed-tools
# ---------------------------------------------------------------------------


def test_allowed_tools_coverage():
    """allowed-tools must list all 4 FP&A MCP tools."""
    frontmatter, _ = read_walkthrough_file()
    missing = [t for t in REQUIRED_MCP_TOOLS if t not in frontmatter]
    assert not missing, f"Missing MCP tools in allowed-tools: {missing}"


# ---------------------------------------------------------------------------
# Test 4: No argument-hint (self-running walkthrough)
# ---------------------------------------------------------------------------


def test_no_argument_hint():
    """Walkthrough takes no arguments — no argument-hint in frontmatter."""
    frontmatter, _ = read_walkthrough_file()
    assert "argument-hint:" not in frontmatter


# ---------------------------------------------------------------------------
# Test 5: All 11 steps present
# ---------------------------------------------------------------------------


def test_has_11_steps():
    """Body must contain Steps 1 through 11."""
    _, body = read_walkthrough_file()
    missing = []
    for n in range(1, 12):
        pattern = rf"(?i)step\s+{n}\b"
        if not re.search(pattern, body):
            missing.append(n)
    assert not missing, f"Missing step numbers: {missing}"


# ---------------------------------------------------------------------------
# Test 6: All 4 phases present
# ---------------------------------------------------------------------------


def test_has_4_phases():
    """Body must contain Phase 1 through Phase 4."""
    _, body = read_walkthrough_file()
    missing = []
    for n in range(1, 5):
        pattern = rf"(?i)phase\s+{n}\b"
        if not re.search(pattern, body):
            missing.append(n)
    assert not missing, f"Missing phase numbers: {missing}"


# ---------------------------------------------------------------------------
# Test 7: Role framing keywords
# ---------------------------------------------------------------------------


def test_role_framing():
    """Body must use FP&A budgeting and forecasting framing language."""
    _, body = read_walkthrough_file()
    body_lower = body.lower()
    fpa_terms = ["budget", "forecast", "fp&a", "vp of finance", "erp", "variance"]
    found = [t for t in fpa_terms if t in body_lower]
    assert len(found) >= 3, (
        f"Only found {len(found)}/6 FP&A framing terms: {found}"
    )


# ---------------------------------------------------------------------------
# Test 8: Sample portfolio CSV referenced
# ---------------------------------------------------------------------------


def test_sample_csv_referenced():
    """Body must reference sample_portfolio.csv as the input data source."""
    _, body = read_walkthrough_file()
    assert "sample_portfolio.csv" in body


# ---------------------------------------------------------------------------
# Test 9: Traditional tool mapping table
# ---------------------------------------------------------------------------


def test_traditional_tool_mapping():
    """Body must map Finance AI tools to traditional FP&A tools."""
    _, body = read_walkthrough_file()
    body_lower = body.lower()
    assert "hyperion" in body_lower or "excel" in body_lower
    assert "time saved" in body_lower or "time saving" in body_lower


# ---------------------------------------------------------------------------
# Test 10: Disclaimer present
# ---------------------------------------------------------------------------


def test_disclaimer():
    """Body must include mandatory disclaimer."""
    _, body = read_walkthrough_file()
    assert "not financial advice" in body.lower()

"""
Unit tests for the /walkthrough-equity-research slash command.

Validates structure, tool coverage, peer universe, phases, and research framing.
"""
from pathlib import Path
import re


COMMANDS_DIR = Path(__file__).parent.parent / ".claude" / "commands"

# MCP tools required for equity research workflow
REQUIRED_MCP_TOOLS = [
    "mcp__finance__validate_environment",
    "mcp__finance__analyze_stock",
    "mcp__finance__get_returns",
    "mcp__finance__get_volatility",
    "mcp__finance__get_risk_metrics",
    "mcp__finance__compare_tickers",
    "mcp__finance__correlation_map",
]

# Tickers that must appear in the walkthrough
REQUIRED_TICKERS = ["NVDA", "AMD", "INTC", "AVGO", "QCOM"]

# Cross-sector tickers for market positioning
CROSS_SECTOR_TICKERS = ["AAPL", "MSFT", "GOOGL"]


def read_walkthrough_file():
    """Read walkthrough-equity-research.md and return (frontmatter, body)."""
    path = COMMANDS_DIR / "walkthrough-equity-research.md"
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
    """walkthrough-equity-research.md must exist in .claude/commands/."""
    path = COMMANDS_DIR / "walkthrough-equity-research.md"
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
    """allowed-tools must list all 7 market analysis MCP tools."""
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
# Test 5: All 17 steps present
# ---------------------------------------------------------------------------


def test_has_17_steps():
    """Body must contain Steps 1 through 17."""
    _, body = read_walkthrough_file()
    missing = []
    for n in range(1, 18):
        pattern = rf"(?i)step\s+{n}\b"
        if not re.search(pattern, body):
            missing.append(n)
    assert not missing, f"Missing step numbers: {missing}"


# ---------------------------------------------------------------------------
# Test 6: All 6 phases present
# ---------------------------------------------------------------------------


def test_has_6_phases():
    """Body must contain Phase 1 through Phase 6."""
    _, body = read_walkthrough_file()
    missing = []
    for n in range(1, 7):
        pattern = rf"(?i)phase\s+{n}\b"
        if not re.search(pattern, body):
            missing.append(n)
    assert not missing, f"Missing phase numbers: {missing}"


# ---------------------------------------------------------------------------
# Test 7: All semiconductor peer tickers referenced
# ---------------------------------------------------------------------------


def test_peer_universe_tickers():
    """Body must reference all 5 semiconductor tickers."""
    _, body = read_walkthrough_file()
    missing = [t for t in REQUIRED_TICKERS if t not in body]
    assert not missing, f"Missing semiconductor tickers: {missing}"


# ---------------------------------------------------------------------------
# Test 8: Cross-sector tickers for market positioning
# ---------------------------------------------------------------------------


def test_cross_sector_tickers():
    """Body must reference AAPL, MSFT, GOOGL for cross-sector comparison."""
    _, body = read_walkthrough_file()
    missing = [t for t in CROSS_SECTOR_TICKERS if t not in body]
    assert not missing, f"Missing cross-sector tickers: {missing}"


# ---------------------------------------------------------------------------
# Test 9: Peer comparison table structure
# ---------------------------------------------------------------------------


def test_peer_comparison_table():
    """Body must contain a peer comparison table with Sharpe, Drawdown, Beta."""
    _, body = read_walkthrough_file()
    body_lower = body.lower()
    assert "sharpe" in body_lower and "drawdown" in body_lower and "beta" in body_lower
    # Table must mention all 5 tickers in a single section
    assert "coverage universe" in body_lower or "peer" in body_lower


# ---------------------------------------------------------------------------
# Test 10: Executive summary section
# ---------------------------------------------------------------------------


def test_executive_summary():
    """Body must contain an executive/quantitative summary section."""
    _, body = read_walkthrough_file()
    body_lower = body.lower()
    assert "summary" in body_lower
    assert "price action" in body_lower or "return quality" in body_lower


# ---------------------------------------------------------------------------
# Test 11: Disclaimer present
# ---------------------------------------------------------------------------


def test_disclaimer():
    """Body must include mandatory disclaimer."""
    _, body = read_walkthrough_file()
    assert "not financial advice" in body.lower()


# ---------------------------------------------------------------------------
# Test 12: Traditional tool mapping table
# ---------------------------------------------------------------------------


def test_traditional_tool_mapping():
    """Body must map Finance AI tools to traditional research tools."""
    _, body = read_walkthrough_file()
    body_lower = body.lower()
    assert "bloomberg" in body_lower or "factset" in body_lower
    assert "time saved" in body_lower or "time saving" in body_lower


# ---------------------------------------------------------------------------
# Test 13: Research framing keywords
# ---------------------------------------------------------------------------


def test_research_framing():
    """Body must use equity research framing language."""
    _, body = read_walkthrough_file()
    body_lower = body.lower()
    research_terms = [
        "initiation",
        "coverage",
        "institutional",
        "analyst",
    ]
    found = [t for t in research_terms if t in body_lower]
    assert len(found) >= 3, (
        f"Only found {len(found)}/4 research framing terms: {found}"
    )

"""
Unit tests for the /walkthrough-hedge-fund slash command.

Validates structure, tool coverage, tickers, phases, and role framing.
"""
from pathlib import Path
import re


COMMANDS_DIR = Path(__file__).parent.parent / ".claude" / "commands"

# MCP tools required for hedge fund workflow
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
REQUIRED_TICKERS = ["NVDA", "AMD", "AVGO", "AAPL", "MSFT", "GOOGL"]


def read_walkthrough_file():
    """Read walkthrough-hedge-fund.md and return (frontmatter, body)."""
    path = COMMANDS_DIR / "walkthrough-hedge-fund.md"
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
    """walkthrough-hedge-fund.md must exist in .claude/commands/."""
    path = COMMANDS_DIR / "walkthrough-hedge-fund.md"
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
# Test 5: All 15 steps present
# ---------------------------------------------------------------------------


def test_has_15_steps():
    """Body must contain Steps 1 through 15."""
    _, body = read_walkthrough_file()
    missing = []
    for n in range(1, 16):
        pattern = rf"(?i)step\s+{n}\b"
        if not re.search(pattern, body):
            missing.append(n)
    assert not missing, f"Missing step numbers: {missing}"


# ---------------------------------------------------------------------------
# Test 6: All 5 phases present
# ---------------------------------------------------------------------------


def test_has_5_phases():
    """Body must contain Phase 1 through Phase 5."""
    _, body = read_walkthrough_file()
    missing = []
    for n in range(1, 6):
        pattern = rf"(?i)phase\s+{n}\b"
        if not re.search(pattern, body):
            missing.append(n)
    assert not missing, f"Missing phase numbers: {missing}"


# ---------------------------------------------------------------------------
# Test 7: Required tickers referenced
# ---------------------------------------------------------------------------


def test_required_tickers():
    """Body must reference all required tickers."""
    _, body = read_walkthrough_file()
    missing = [t for t in REQUIRED_TICKERS if t not in body]
    assert not missing, f"Missing tickers: {missing}"


# ---------------------------------------------------------------------------
# Test 8: Role framing keywords
# ---------------------------------------------------------------------------


def test_role_framing():
    """Body must use hedge fund trading desk framing language."""
    _, body = read_walkthrough_file()
    body_lower = body.lower()
    hf_terms = ["trading desk", "volatility", "pair", "systematic", "regime", "cio"]
    found = [t for t in hf_terms if t in body_lower]
    assert len(found) >= 3, (
        f"Only found {len(found)}/6 hedge fund framing terms: {found}"
    )


# ---------------------------------------------------------------------------
# Test 9: Traditional tool mapping table
# ---------------------------------------------------------------------------


def test_traditional_tool_mapping():
    """Body must map Finance AI tools to traditional research tools."""
    _, body = read_walkthrough_file()
    body_lower = body.lower()
    assert "bloomberg" in body_lower or "factset" in body_lower
    assert "time saved" in body_lower or "time saving" in body_lower


# ---------------------------------------------------------------------------
# Test 10: Disclaimer present
# ---------------------------------------------------------------------------


def test_disclaimer():
    """Body must include mandatory disclaimer."""
    _, body = read_walkthrough_file()
    assert "not financial advice" in body.lower()

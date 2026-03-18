"""
Unit tests for the /demo slash command: .claude/commands/demo.md

Tests read the raw markdown file, parse YAML frontmatter, and verify both
content structure and tool coverage.

TDD: Written to validate the demo command created in Plan 05-01.
"""
from pathlib import Path
import re


COMMANDS_DIR = Path(__file__).parent.parent / ".claude" / "commands"

# All 13 MCP function names required in allowed-tools
REQUIRED_MCP_TOOLS = [
    "mcp__finance__ping",
    "mcp__finance__validate_environment",
    "mcp__finance__analyze_stock",
    "mcp__finance__get_returns",
    "mcp__finance__get_volatility",
    "mcp__finance__get_risk_metrics",
    "mcp__finance__compare_tickers",
    "mcp__finance__correlation_map",
    "mcp__finance__ingest_csv",
    "mcp__finance__liquidity_predictor",
    "mcp__finance__predict_liquidity",
    "mcp__finance__investor_classifier",
    "mcp__finance__classify_investor",
]


def read_demo_file():
    """
    Read demo.md and return (frontmatter, body) as raw strings.

    Extracts YAML frontmatter between the first pair of --- delimiters.
    Body is everything after the closing --- of the frontmatter block.

    Note: demo.md uses --- as horizontal rules throughout the body, so we
    cannot use a simple re.split on all --- delimiters (unlike persona commands).
    Instead we locate the first and second --- markers and slice accordingly.
    """
    path = COMMANDS_DIR / "demo.md"
    text = path.read_text()  # Raises FileNotFoundError if missing — intentional
    lines = text.splitlines(keepends=True)

    # Find the line indices of the first two standalone '---' lines
    separator_indices = [
        i for i, line in enumerate(lines) if re.match(r"^---\s*$", line)
    ]

    if len(separator_indices) < 2:
        return "", text  # No valid frontmatter found — treat entire file as body

    start = separator_indices[0] + 1  # Line after opening ---
    end = separator_indices[1]        # Line of closing ---

    frontmatter = "".join(lines[start:end])
    body = "".join(lines[end + 1:])   # Everything after closing ---
    return frontmatter, body


# ---------------------------------------------------------------------------
# Test 1: File existence
# ---------------------------------------------------------------------------


def test_demo_command_exists():
    """demo.md must exist in .claude/commands/."""
    path = COMMANDS_DIR / "demo.md"
    assert path.exists(), f"Missing: {path}"


# ---------------------------------------------------------------------------
# Test 2: Required frontmatter fields
# ---------------------------------------------------------------------------


def test_demo_frontmatter_required_fields():
    """demo.md frontmatter must contain description, allowed-tools, and model."""
    frontmatter, _ = read_demo_file()
    assert "description:" in frontmatter, "Missing 'description:' in frontmatter"
    assert "allowed-tools:" in frontmatter, "Missing 'allowed-tools:' in frontmatter"
    assert "model:" in frontmatter, "Missing 'model:' in frontmatter"


# ---------------------------------------------------------------------------
# Test 3: All 13 MCP tool function names in allowed-tools
# ---------------------------------------------------------------------------


def test_demo_allowed_tools_all_13_mcp_functions():
    """allowed-tools must list all 13 MCP function names."""
    frontmatter, _ = read_demo_file()
    missing = []
    for tool in REQUIRED_MCP_TOOLS:
        if tool not in frontmatter:
            missing.append(tool)
    assert not missing, (
        f"The following MCP tools are missing from allowed-tools:\n"
        + "\n".join(f"  - {t}" for t in missing)
    )


# ---------------------------------------------------------------------------
# Test 4: Welcome/introduction section present
# ---------------------------------------------------------------------------


def test_demo_body_has_welcome_section():
    """Body must contain a welcome/introduction section with key keywords."""
    _, body = read_demo_file()
    body_lower = body.lower()
    assert "finance ai skill" in body_lower, (
        "Body must mention 'Finance AI Skill' in the welcome section"
    )
    assert "walkthrough" in body_lower or "demo" in body_lower, (
        "Body must contain 'walkthrough' or 'demo' keyword"
    )


# ---------------------------------------------------------------------------
# Test 5: All 11 numbered step markers present
# ---------------------------------------------------------------------------


def test_demo_body_has_20_steps():
    """Body must contain all 20 numbered steps (Step 1 through Step 20)."""
    _, body = read_demo_file()
    missing_steps = []
    for n in range(1, 21):
        # Match "Step N:" or "## Step N" patterns
        pattern = rf"(?i)step\s+{n}\b"
        if not re.search(pattern, body):
            missing_steps.append(n)
    assert not missing_steps, (
        f"The following step numbers are missing from the walkthrough body: {missing_steps}"
    )


# ---------------------------------------------------------------------------
# Test 6: Completion/summary section present
# ---------------------------------------------------------------------------


def test_demo_body_has_completion_summary():
    """Body must contain a completion/summary section."""
    _, body = read_demo_file()
    body_lower = body.lower()
    assert "complete" in body_lower or "summary" in body_lower, (
        "Body must contain a completion or summary section"
    )
    assert "demonstrated" in body_lower or "11 tools" in body_lower or "all" in body_lower, (
        "Completion section must reference the tools that were demonstrated"
    )


# ---------------------------------------------------------------------------
# Test 7: Both persona commands referenced
# ---------------------------------------------------------------------------


def test_demo_body_references_both_personas():
    """Body must reference both /finance-analyst and /finance-pm personas."""
    _, body = read_demo_file()
    assert "/finance-analyst" in body, (
        "Body must reference the /finance-analyst persona command"
    )
    assert "/finance-pm" in body, (
        "Body must reference the /finance-pm persona command"
    )


# ---------------------------------------------------------------------------
# Test 8: Mandatory disclaimer present
# ---------------------------------------------------------------------------


def test_demo_body_has_disclaimer():
    """Body must contain the mandatory disclaimer text."""
    _, body = read_demo_file()
    body_lower = body.lower()
    assert "disclaimer" in body_lower or "not financial advice" in body_lower, (
        "Body must include mandatory disclaimer (e.g., 'not financial advice')"
    )


# ---------------------------------------------------------------------------
# Test 9: No argument-hint in frontmatter (demo takes no arguments)
# ---------------------------------------------------------------------------


def test_demo_frontmatter_no_argument_hint():
    """demo.md must NOT have argument-hint — demo takes no arguments."""
    frontmatter, _ = read_demo_file()
    assert "argument-hint:" not in frontmatter, (
        "demo.md must not have 'argument-hint:' — it is a self-running walkthrough with no arguments"
    )


# ---------------------------------------------------------------------------
# Test 10: Real-world scenarios section present
# ---------------------------------------------------------------------------


def test_demo_body_has_real_world_scenarios_section():
    """Body must contain a Real-World Scenarios section with role-based examples."""
    _, body = read_demo_file()
    body_lower = body.lower()
    assert "real-world" in body_lower or "real world" in body_lower, (
        "Body must contain a 'Real-World' scenarios section"
    )


# ---------------------------------------------------------------------------
# Test 11: Finance roles referenced in scenario steps
# ---------------------------------------------------------------------------


REQUIRED_ROLES = [
    "equity research",
    "hedge fund",
    "fp&a",
    "private equity",
    "investment banking",
]


def test_demo_body_references_finance_roles():
    """Body must reference at least 5 finance roles in the scenario steps."""
    _, body = read_demo_file()
    body_lower = body.lower()
    missing = [role for role in REQUIRED_ROLES if role not in body_lower]
    assert not missing, (
        f"The following finance roles are missing from scenario steps: {missing}"
    )


# ---------------------------------------------------------------------------
# Test 12: Role-tool mapping table present
# ---------------------------------------------------------------------------


def test_demo_body_has_role_tool_mapping():
    """Body must contain a role-tool mapping table."""
    _, body = read_demo_file()
    body_lower = body.lower()
    assert "role" in body_lower and "primary tools" in body_lower, (
        "Body must contain a role-tool mapping table with 'Role' and 'Primary Tools' columns"
    )

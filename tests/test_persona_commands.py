"""
Unit tests for persona command files: finance-analyst.md and finance-pm.md.

Tests read the raw markdown files, parse YAML frontmatter, and verify
both content structure and role-framing text.

TDD: These tests were written before the command files exist (RED phase).
"""
from pathlib import Path
import re


COMMANDS_DIR = Path(__file__).parent.parent / ".claude" / "commands"


def read_command_file(name: str):
    """
    Read a Claude command file and return (frontmatter, body) as raw strings.

    Splits on --- delimiter (YAML front-matter convention).
    Returns empty strings if parsing fails.
    """
    path = COMMANDS_DIR / name
    text = path.read_text()  # Raises FileNotFoundError if missing — intentional
    parts = re.split(r"^---\s*$", text, flags=re.MULTILINE)
    # parts[0] is text before first ---, parts[1] is frontmatter, parts[2] is body
    frontmatter = parts[1] if len(parts) > 1 else ""
    body = parts[2] if len(parts) > 2 else ""
    return frontmatter, body


# ---------------------------------------------------------------------------
# finance-analyst.md tests
# ---------------------------------------------------------------------------


def test_analyst_command_exists():
    """finance-analyst.md must exist in .claude/commands/."""
    path = COMMANDS_DIR / "finance-analyst.md"
    assert path.exists(), f"Missing: {path}"


def test_analyst_frontmatter_fields():
    """finance-analyst.md frontmatter must contain required fields."""
    frontmatter, _ = read_command_file("finance-analyst.md")
    assert "description:" in frontmatter, "Missing 'description:' in frontmatter"
    assert "argument-hint:" in frontmatter, "Missing 'argument-hint:' in frontmatter"
    assert "allowed-tools:" in frontmatter, "Missing 'allowed-tools:' in frontmatter"
    assert "model:" in frontmatter, "Missing 'model:' in frontmatter"


def test_analyst_role_framing():
    """finance-analyst.md body must contain equity analyst role framing."""
    _, body = read_command_file("finance-analyst.md")
    assert "sell-side equity analyst" in body, (
        "Body must contain 'sell-side equity analyst' role framing"
    )
    assert "equity perspective" in body.lower(), (
        "Body must contain 'equity perspective' output framing"
    )


def test_analyst_disclaimer_required():
    """finance-analyst.md must include mandatory disclaimer requirement."""
    _, body = read_command_file("finance-analyst.md")
    assert "disclaimer" in body.lower(), (
        "Body must reference mandatory disclaimer"
    )


# ---------------------------------------------------------------------------
# finance-pm.md tests
# ---------------------------------------------------------------------------


def test_pm_command_exists():
    """finance-pm.md must exist in .claude/commands/."""
    path = COMMANDS_DIR / "finance-pm.md"
    assert path.exists(), f"Missing: {path}"


def test_pm_frontmatter_fields():
    """finance-pm.md frontmatter must contain required fields."""
    frontmatter, _ = read_command_file("finance-pm.md")
    assert "description:" in frontmatter, "Missing 'description:' in frontmatter"
    assert "argument-hint:" in frontmatter, "Missing 'argument-hint:' in frontmatter"
    assert "allowed-tools:" in frontmatter, "Missing 'allowed-tools:' in frontmatter"
    assert "model:" in frontmatter, "Missing 'model:' in frontmatter"


def test_pm_role_framing():
    """finance-pm.md body must contain portfolio manager role framing."""
    _, body = read_command_file("finance-pm.md")
    assert "portfolio manager" in body.lower(), (
        "Body must contain 'portfolio manager' role framing"
    )
    assert "portfolio perspective" in body.lower(), (
        "Body must contain 'portfolio perspective' output framing"
    )


def test_pm_disclaimer_required():
    """finance-pm.md must include mandatory disclaimer requirement."""
    _, body = read_command_file("finance-pm.md")
    assert "disclaimer" in body.lower(), (
        "Body must reference mandatory disclaimer"
    )


# ---------------------------------------------------------------------------
# Cross-file tests
# ---------------------------------------------------------------------------


def test_both_commands_include_mcp_tools():
    """Both command files must reference mcp__finance__ tools in allowed-tools."""
    for filename in ("finance-analyst.md", "finance-pm.md"):
        frontmatter, _ = read_command_file(filename)
        assert "mcp__finance__" in frontmatter, (
            f"{filename}: allowed-tools must include mcp__finance__ tools"
        )

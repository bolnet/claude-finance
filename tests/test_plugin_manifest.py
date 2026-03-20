"""
Plugin manifest validation tests.

These tests verify that the finance-mcp-plugin directory is correctly structured
for Claude marketplace submission.
"""
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PLUGIN_DIR = PROJECT_ROOT / "finance-mcp-plugin"


def test_plugin_json_exists():
    """plugin.json must exist in .claude-plugin/."""
    assert (PLUGIN_DIR / ".claude-plugin" / "plugin.json").exists()


def test_plugin_json_valid_json():
    """plugin.json must parse as valid JSON and be a dict."""
    text = (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text()
    data = json.loads(text)  # raises JSONDecodeError if invalid
    assert isinstance(data, dict)


def test_plugin_json_required_fields():
    """plugin.json must have: name, version, description, author (with name key), keywords (list)."""
    text = (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text()
    data = json.loads(text)
    assert "name" in data, "Missing field: name"
    assert "version" in data, "Missing field: version"
    assert "description" in data, "Missing field: description"
    assert "author" in data, "Missing field: author"
    assert isinstance(data["author"], dict), "author must be an object"
    assert "name" in data["author"], "author must have a 'name' key"
    assert "keywords" in data, "Missing field: keywords"
    assert isinstance(data["keywords"], list), "keywords must be a list"
    assert len(data["keywords"]) > 0, "keywords must not be empty"


def test_plugin_commands_directory():
    """commands/ directory must contain finance.md, finance-analyst.md, finance-pm.md."""
    commands_dir = PLUGIN_DIR / "commands"
    assert (commands_dir / "finance.md").exists(), "Missing: commands/finance.md"
    assert (commands_dir / "finance-analyst.md").exists(), "Missing: commands/finance-analyst.md"
    assert (commands_dir / "finance-pm.md").exists(), "Missing: commands/finance-pm.md"


def test_plugin_skills_directory():
    """skills/finance/SKILL.md must exist."""
    assert (PLUGIN_DIR / "skills" / "finance" / "SKILL.md").exists()


def test_plugin_mcp_json_exists():
    """.mcp.json must exist in the plugin root."""
    assert (PLUGIN_DIR / ".mcp.json").exists()


def test_plugin_json_no_placeholders():
    """plugin.json must not contain any [owner] placeholder strings."""
    text = (PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text()
    assert "[owner]" not in text, "plugin.json still contains [owner] placeholder"


def test_plugin_json_correct_urls():
    """plugin.json homepage and repository must point to bolnet/Claude-Finance."""
    data = json.loads((PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text())
    assert "bolnet/Claude-Finance" in data["homepage"], (
        f"homepage does not contain bolnet/Claude-Finance: {data['homepage']}"
    )
    assert "bolnet/Claude-Finance" in data["repository"], (
        f"repository does not contain bolnet/Claude-Finance: {data['repository']}"
    )


def test_plugin_json_version_format():
    """plugin.json version must match semver format X.Y.Z."""
    import re
    data = json.loads((PLUGIN_DIR / ".claude-plugin" / "plugin.json").read_text())
    assert re.match(r"^\d+\.\d+\.\d+$", data["version"]), (
        f"version does not match X.Y.Z semver: {data['version']}"
    )


def test_hooks_json_exists():
    """hooks/hooks.json must exist in the plugin directory."""
    assert (PLUGIN_DIR / "hooks" / "hooks.json").exists()


def test_hooks_json_empty_array():
    """hooks/hooks.json must parse as JSON and equal an empty array."""
    data = json.loads((PLUGIN_DIR / "hooks" / "hooks.json").read_text())
    assert data == [], f"hooks.json should be empty array [], got: {data}"


def test_plugin_directory_structure():
    """Plugin directory must have all 4 required subdirectories."""
    for subdir in [".claude-plugin", "commands", "skills", "hooks"]:
        assert (PLUGIN_DIR / subdir).is_dir(), (
            f"Missing required subdirectory: finance-mcp-plugin/{subdir}/"
        )


def test_mcp_json_has_finance_server():
    """.mcp.json must have mcpServers.finance with command and args keys."""
    data = json.loads((PLUGIN_DIR / ".mcp.json").read_text())
    assert "mcpServers" in data, "Missing mcpServers key in .mcp.json"
    assert "finance" in data["mcpServers"], "Missing finance server in mcpServers"
    server = data["mcpServers"]["finance"]
    assert "command" in server, "finance server missing 'command' key"
    assert "args" in server, "finance server missing 'args' key"

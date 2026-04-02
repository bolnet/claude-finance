"""
Tests for MCP server scaffold.
Requirements: MCP-01, MCP-02, MCP-03

Wave 0: stubs only. Implementations land in plan 01-01 (server.py).
Full test commands:
  python3 -m pytest tests/test_mcp_server.py -v
"""
import sys
import os

import pytest

# Ensure src/ is on path if package not installed editably
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_server_module_importable():
    """MCP-01: finance_mcp.server is importable."""
    from finance_mcp import server  # noqa: F401
    assert server is not None


def test_fastmcp_instance_exists():
    """MCP-01: FastMCP instance named `mcp` exists on the server module."""
    from finance_mcp.server import mcp
    from fastmcp import FastMCP
    assert isinstance(mcp, FastMCP)


def test_ping_tool_registered():
    """MCP-02: `ping` tool is registered and callable."""
    from finance_mcp.server import ping
    result = ping()
    assert isinstance(result, str)
    assert len(result) > 0


def test_validate_environment_tool_registered():
    """MCP-02: `validate_environment` tool is registered and returns a dict."""
    from finance_mcp.server import validate_environment
    result = validate_environment()
    assert isinstance(result, dict)
    assert "_status" in result


def test_validate_environment_checks_required_packages():
    """MCP-02: validate_environment reports on all required finance packages."""
    from finance_mcp.server import validate_environment
    result = validate_environment()
    expected_keys = {"yfinance", "pandas", "numpy", "matplotlib", "seaborn", "sklearn"}
    assert expected_keys.issubset(result.keys())


def test_server_has_provider_instance():
    """MCP-03: server module exposes an active DataProvider instance."""
    from finance_mcp import server
    from finance_mcp.providers.base import DataProvider

    assert hasattr(server, "provider")
    assert isinstance(server.provider, DataProvider)

"""
Tests for Finance MCP HTTP server entry point (server_http.py).

Verifies that:
- server_http module can be imported
- server_http exposes the same mcp instance from server.py
- start() calls mcp.run with transport="streamable-http", host="0.0.0.0", port=8000
- start(port=N) passes the custom port to mcp.run
"""
import sys
import importlib
from unittest.mock import patch, call


def test_server_http_module_exists():
    """Importing finance_mcp.server_http does not raise ImportError."""
    import finance_mcp.server_http  # noqa: F401  — just importing is the assertion


def test_server_http_imports_mcp_instance():
    """finance_mcp.server_http.mcp is the same FastMCP instance from finance_mcp.server."""
    import finance_mcp.server_http as http_module
    import finance_mcp.server as server_module

    assert hasattr(http_module, "mcp"), "server_http must expose the mcp attribute"
    assert http_module.mcp is server_module.mcp, (
        "server_http.mcp must be the exact same object as server.mcp (not a copy)"
    )


def test_http_transport_called_with_correct_params(mocker):
    """start() calls mcp.run with transport='streamable-http', host='0.0.0.0', port=8000."""
    mock_run = mocker.patch("finance_mcp.server.mcp.run")

    import finance_mcp.server_http as http_module
    importlib.reload(http_module)  # ensure fresh import after patching

    http_module.start()

    mock_run.assert_called_once_with(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
    )


def test_custom_port_via_argv(mocker):
    """start(port=9000) passes port=9000 to mcp.run."""
    mock_run = mocker.patch("finance_mcp.server.mcp.run")

    import finance_mcp.server_http as http_module
    importlib.reload(http_module)

    http_module.start(port=9000)

    mock_run.assert_called_once_with(
        transport="streamable-http",
        host="0.0.0.0",
        port=9000,
    )

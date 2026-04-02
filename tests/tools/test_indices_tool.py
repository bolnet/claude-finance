"""Tests for indices_snapshot MCP tool."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from finance_mcp.output import DISCLAIMER


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_provider(snapshot_data: list[dict]) -> MagicMock:
    """Return a mock provider with INDICES capability and indices_snapshot."""
    from finance_mcp.providers.base import Capability

    provider = MagicMock()
    provider.capabilities = frozenset({Capability.INDICES})
    provider.indices_snapshot.return_value = snapshot_data
    return provider


_SNAPSHOT_DATA = [
    {"ticker": "I:SPX", "name": "S&P 500", "session": {"close": 4500.12}},
    {"ticker": "I:NDX", "name": "Nasdaq 100", "session": {"close": 15200.50}},
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_indices_snapshot_returns_string():
    """indices_snapshot returns a str."""
    with patch("finance_mcp.tools.indices_tool.get_provider", return_value=_make_provider(_SNAPSHOT_DATA)):
        from finance_mcp.tools.indices_tool import indices_snapshot

        result = indices_snapshot("I:SPX,I:NDX")

    assert isinstance(result, str)


def test_indices_snapshot_contains_tickers():
    """Output contains each requested ticker."""
    with patch("finance_mcp.tools.indices_tool.get_provider", return_value=_make_provider(_SNAPSHOT_DATA)):
        from finance_mcp.tools.indices_tool import indices_snapshot

        result = indices_snapshot("I:SPX,I:NDX")

    assert "I:SPX" in result
    assert "I:NDX" in result


def test_indices_snapshot_contains_names():
    """Output contains index names from the provider response."""
    with patch("finance_mcp.tools.indices_tool.get_provider", return_value=_make_provider(_SNAPSHOT_DATA)):
        from finance_mcp.tools.indices_tool import indices_snapshot

        result = indices_snapshot("I:SPX,I:NDX")

    assert "S&P 500" in result
    assert "Nasdaq 100" in result


def test_indices_snapshot_contains_values():
    """Output contains the close values."""
    with patch("finance_mcp.tools.indices_tool.get_provider", return_value=_make_provider(_SNAPSHOT_DATA)):
        from finance_mcp.tools.indices_tool import indices_snapshot

        result = indices_snapshot("I:SPX,I:NDX")

    assert "4500" in result or "4500.12" in result
    assert "15200" in result or "15200.50" in result


def test_indices_snapshot_ends_with_disclaimer():
    """Output always ends with the standard disclaimer."""
    with patch("finance_mcp.tools.indices_tool.get_provider", return_value=_make_provider(_SNAPSHOT_DATA)):
        from finance_mcp.tools.indices_tool import indices_snapshot

        result = indices_snapshot("I:SPX")

    assert result.strip().endswith(DISCLAIMER)


def test_indices_snapshot_calls_provider_with_list():
    """Provider.indices_snapshot is called with a list of tickers (not a string)."""
    provider = _make_provider(_SNAPSHOT_DATA)
    with patch("finance_mcp.tools.indices_tool.get_provider", return_value=provider):
        from finance_mcp.tools.indices_tool import indices_snapshot

        indices_snapshot("I:SPX,I:NDX")

    provider.indices_snapshot.assert_called_once_with(["I:SPX", "I:NDX"])


def test_indices_snapshot_missing_capability_raises():
    """ToolError is raised when provider lacks INDICES capability."""
    from fastmcp.exceptions import ToolError
    from finance_mcp.providers.base import Capability

    provider = MagicMock()
    provider.capabilities = frozenset()  # no capabilities

    with patch("finance_mcp.tools.indices_tool.get_provider", return_value=provider):
        from finance_mcp.tools.indices_tool import indices_snapshot

        with pytest.raises(ToolError):
            indices_snapshot("I:SPX")


def test_indices_snapshot_empty_result():
    """Returns graceful output when provider returns no results."""
    with patch("finance_mcp.tools.indices_tool.get_provider", return_value=_make_provider([])):
        from finance_mcp.tools.indices_tool import indices_snapshot

        result = indices_snapshot("I:SPX")

    assert isinstance(result, str)
    assert result.strip().endswith(DISCLAIMER)

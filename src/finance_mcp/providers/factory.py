"""Provider factory — selects the active DataProvider from environment config."""
from __future__ import annotations

import os


def get_provider() -> object:
    """Return the configured DataProvider instance.

    Reads the ``DATA_PROVIDER`` environment variable to decide which provider
    to instantiate:

    - ``"polygon"`` → :class:`~finance_mcp.providers.polygon_provider.PolygonProvider`
      Requires the ``POLYGON_API_KEY`` environment variable to be set.
    - anything else (including unset) → :class:`~finance_mcp.providers.yfinance_provider.YFinanceProvider`

    Returns:
        An instance satisfying the :class:`~finance_mcp.providers.base.DataProvider`
        Protocol.

    Raises:
        RuntimeError: When ``DATA_PROVIDER=polygon`` but ``POLYGON_API_KEY`` is
            not set.
    """
    provider_name = os.environ.get("DATA_PROVIDER", "yfinance").lower().strip()

    if provider_name == "polygon":
        api_key = os.environ.get("POLYGON_API_KEY")
        if not api_key:
            raise RuntimeError(
                "DATA_PROVIDER=polygon requires POLYGON_API_KEY to be set. "
                "Export POLYGON_API_KEY=<your-key> and try again."
            )
        from finance_mcp.providers.polygon.provider import PolygonProvider

        return PolygonProvider(api_key=api_key)

    from finance_mcp.providers.yfinance_provider import YFinanceProvider

    return YFinanceProvider()

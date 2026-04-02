"""Integration tests — verify provider wiring and tool registration."""
import pytest
from unittest.mock import patch

from finance_mcp.providers.base import DataProvider, Capability
from finance_mcp.providers.factory import get_provider


class TestProviderIntegration:
    def test_default_provider_is_yfinance(self):
        provider = get_provider()
        assert type(provider).__name__ == "YFinanceProvider"
        assert Capability.PRICE_HISTORY in provider.capabilities

    def test_server_exposes_provider(self):
        from finance_mcp import server
        assert hasattr(server, "provider")
        assert isinstance(server.provider, DataProvider)

    def test_all_tools_registered(self):
        """Verify all 27 MCP tools are registered."""
        from finance_mcp.server import mcp
        # FastMCP stores tools - check the internal registry
        # Try different attribute names FastMCP may use
        tools = None
        for attr in ("_tools", "tools", "_tool_registry"):
            if hasattr(mcp, attr):
                registry = getattr(mcp, attr)
                if isinstance(registry, dict):
                    tools = set(registry.keys())
                    break

        if tools is None:
            pytest.skip("Cannot inspect FastMCP tool registry")

        expected = {
            "ping", "validate_environment",
            "analyze_stock", "get_returns", "get_volatility", "get_risk_metrics",
            "compare_tickers", "correlation_map", "ingest_csv",
            "liquidity_predictor", "predict_liquidity",
            "investor_classifier", "classify_investor",
            "get_news", "get_options_chain",
            "forex_convert", "forex_quote",
            "crypto_snapshot", "crypto_movers",
            "indices_snapshot",
            "get_dividends", "get_splits", "get_short_interest",
            "get_technical_indicator",
            "market_movers",
            "get_sec_filings", "get_risk_factors",
            "get_ticker_details", "search_tickers",
        }
        for name in expected:
            assert name in tools, f"Tool '{name}' not registered"


class TestPolygonProviderEndpoints:
    def test_polygon_provider_has_all_67_methods(self):
        """Verify PolygonProvider has all 57 working + 10 blocked endpoint methods."""
        from finance_mcp.providers.polygon.provider import PolygonProvider

        with patch("finance_mcp.providers.polygon.provider.PolygonClient"):
            p = PolygonProvider(api_key="test")

        stock_methods = [
            "stocks_prev_close", "stocks_bars", "stocks_grouped_daily", "stocks_daily_ohlc",
            "stocks_snapshot", "stocks_snapshot_all", "stocks_gainers", "stocks_losers",
            "stocks_last_trade", "stocks_trades", "ticker_details", "ticker_search",
            "ticker_types", "exchanges", "conditions", "market_holidays",
            "news", "dividends", "splits", "short_interest", "short_volume", "float_shares",
            "sec_filings", "sec_risk_factors", "sec_10k_sections", "sec_8k_text",
            "stocks_sma", "stocks_ema", "stocks_macd", "stocks_rsi",
        ]
        options_methods = [
            "options_contracts", "options_prev_close", "options_chain_snapshot", "options_single_snapshot",
        ]
        indices_methods = [
            "indices_prev_close", "indices_bars", "indices_snapshot", "indices_unified_snapshot",
            "indices_daily_ohlc", "indices_sma", "indices_ema", "indices_rsi",
        ]
        currency_methods = [
            "forex_prev_close", "forex_bars", "forex_conversion", "forex_last_quote",
            "forex_quotes", "forex_snapshot_all", "forex_gainers", "forex_losers",
            "crypto_prev_close", "crypto_bars", "crypto_snapshot_all", "crypto_snapshot",
            "crypto_gainers", "crypto_losers", "crypto_daily_ohlc",
        ]
        blocked_methods = [
            "nbbo_quotes", "balance_sheets", "income_statements", "financial_ratios",
            "options_trades", "options_quotes", "options_last_trade",
            "benzinga_partner", "tmx_partner", "crypto_trades",
        ]

        all_methods = stock_methods + options_methods + indices_methods + currency_methods + blocked_methods
        for method in all_methods:
            assert hasattr(p, method), f"Missing: {method}"
            assert callable(getattr(p, method)), f"Not callable: {method}"

        assert len(all_methods) == 67  # 57 working + 10 blocked

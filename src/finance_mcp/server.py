"""
Finance MCP Server — FastMCP stdio transport.

This module is the entry point for the MCP server registered in .mcp.json.
All finance tools are registered here via @mcp.tool decorator.
FastMCP generates MCP JSON schemas automatically from type hints and docstrings.

Run:  python -m finance_mcp.server   (stdio transport, launched by Claude Code)
Log:  all debug output goes to stderr (stdout is the MCP protocol channel)
"""
import sys
import importlib

from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from finance_mcp.providers import get_provider
from finance_mcp.tools.price_chart import analyze_stock
from finance_mcp.tools.returns import get_returns
from finance_mcp.tools.volatility import get_volatility
from finance_mcp.tools.risk_metrics import get_risk_metrics
from finance_mcp.tools.comparison import compare_tickers
from finance_mcp.tools.correlation import correlation_map
from finance_mcp.tools.csv_ingest import ingest_csv
from finance_mcp.tools.liquidity_model import liquidity_predictor, predict_liquidity
from finance_mcp.tools.investor_model import investor_classifier, classify_investor
from finance_mcp.tools.market_movers import market_movers
from finance_mcp.tools.sec_filings import get_sec_filings, get_risk_factors
from finance_mcp.tools.ticker_info import get_ticker_details, search_tickers
from finance_mcp.tools.indices_tool import indices_snapshot
from finance_mcp.tools.fundamentals import get_dividends, get_splits, get_short_interest
from finance_mcp.tools.technicals import get_technical_indicator

mcp = FastMCP("Finance MCP Server")

# Initialize the active data provider (reads DATA_PROVIDER env var)
provider = get_provider()

mcp.add_tool(analyze_stock)
mcp.add_tool(get_returns)
mcp.add_tool(get_volatility)
mcp.add_tool(get_risk_metrics)
mcp.add_tool(compare_tickers)
mcp.add_tool(correlation_map)
mcp.add_tool(ingest_csv)
mcp.add_tool(liquidity_predictor)
mcp.add_tool(predict_liquidity)
mcp.add_tool(investor_classifier)
mcp.add_tool(classify_investor)
mcp.add_tool(market_movers)
mcp.add_tool(get_sec_filings)
mcp.add_tool(get_risk_factors)
mcp.add_tool(get_ticker_details)
mcp.add_tool(search_tickers)
mcp.add_tool(indices_snapshot)
mcp.add_tool(get_dividends)
mcp.add_tool(get_splits)
mcp.add_tool(get_short_interest)
mcp.add_tool(get_technical_indicator)


@mcp.tool
def ping() -> str:
    """Health check — confirms the finance MCP server is running and reachable by Claude Code."""
    return "Finance MCP Server is running. Ready to execute finance analysis."


@mcp.tool
def validate_environment() -> dict:
    """
    Detect Python environment and validate required finance packages are installed.

    Returns a dict mapping package name → version string (or 'MISSING' if not installed).
    Claude Code should call this tool first to confirm the environment is ready before
    generating analysis code.
    """
    packages = {
        "yfinance": "yfinance",
        "pandas": "pandas",
        "numpy": "numpy",
        "matplotlib": "matplotlib",
        "seaborn": "seaborn",
        "sklearn": "sklearn",
        "tabulate": "tabulate",
    }
    results = {}
    missing = []
    for display_name, import_name in packages.items():
        try:
            mod = importlib.import_module(import_name)
            results[display_name] = getattr(mod, "__version__", "installed")
        except ImportError:
            results[display_name] = "MISSING"
            missing.append(display_name)

    if missing:
        results["_status"] = "INCOMPLETE"
        results["_install_hint"] = (
            f"Missing packages: {', '.join(missing)}. "
            f"Run: pip install {' '.join(missing)}"
        )
    else:
        results["_status"] = "OK"

    print(f"[finance-mcp] Environment check: {results['_status']}", file=sys.stderr)
    return results


if __name__ == "__main__":
    # stdio transport is the default — Claude Code connects via stdin/stdout
    # All debug output must go to stderr to avoid polluting the MCP protocol channel
    print("[finance-mcp] Starting Finance MCP Server (stdio)", file=sys.stderr)
    mcp.run()

"""Phase 2 live smoke test — calls each tool with real data."""
import sys
sys.path.insert(0, "src")
from finance_mcp.tools.price_chart import analyze_stock
from finance_mcp.tools.returns import get_returns
from finance_mcp.tools.volatility import get_volatility
from finance_mcp.tools.risk_metrics import get_risk_metrics
from finance_mcp.tools.comparison import compare_tickers
from finance_mcp.tools.correlation import correlation_map

ticker = "AAPL"
start = "2024-01-01"
end = "2024-12-31"

print("=== analyze_stock ===")
print(analyze_stock(ticker, start, end))
print()

print("=== get_returns ===")
print(get_returns(ticker, start, end))
print()

print("=== get_volatility ===")
print(get_volatility(ticker, start, end))
print()

print("=== get_risk_metrics ===")
print(get_risk_metrics(ticker, start, end))
print()

print("=== compare_tickers ===")
print(compare_tickers("AAPL,MSFT,GOOGL", start, end))
print()

print("=== correlation_map ===")
print(correlation_map("AAPL,MSFT,GOOGL,AMZN", start, end))
print()

print("SMOKE TEST COMPLETE — check finance_output/charts/ for PNG files")

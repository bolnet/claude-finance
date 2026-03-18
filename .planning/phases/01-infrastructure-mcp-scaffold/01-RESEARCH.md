# Phase 1: Infrastructure & MCP Scaffold - Research

**Researched:** 2026-03-17
**Domain:** FastMCP Python server, Claude Code command/skill format, yfinance adapter layer, Python project structure
**Confidence:** HIGH (MCP registration, command format, FastMCP API from official sources); MEDIUM (yfinance column name behavior in 0.2.54+, needs live verification)

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|-----------------|
| INFRA-01 | Skill detects Python environment and validates required packages on first run | Dynamic context injection with `!` syntax in command file; `python3 -c "import ..."` pattern |
| INFRA-02 | Skill installs missing packages or prints clear install instructions | `Bash(pip:*)` in allowed-tools; Bash pip install fallback pattern |
| INFRA-03 | yfinance data adapter layer isolates all Yahoo Finance API calls behind a single module | `src/finance_mcp/adapter.py` — single module, all yf calls centralized there |
| INFRA-04 | All chart outputs saved as PNG to `finance_output/` (no plt.show(); uses Agg backend) | `matplotlib.use('Agg')` before any import of pyplot; `plt.savefig()` + `plt.close()` pattern |
| INFRA-05 | All outputs include hardcoded investment advice disclaimer | Disclaimer constant in output conventions module; command file template enforces it |
| INFRA-06 | Data validation wrapper catches empty DataFrames, invalid tickers, bad date ranges | Post-fetch validation: `df.empty` check, row-count sanity check, column presence check |
| INFRA-07 | All output leads with plain-English interpretation before DataFrame/chart/metric | Output ordering convention in SKILL.md: interpretation → data → disclaimer |
| MCP-01 | Python MCP server at `src/finance_mcp/server.py` using FastMCP, registered in `.mcp.json` | FastMCP `@mcp.tool` decorator + `.mcp.json` with `"command": "python", "args": ["-m", "finance_mcp.server"]` |
| MCP-02 | MCP server exposes tools with clear descriptions Claude can discover and invoke | FastMCP generates tool schemas from docstrings + type hints automatically |
| MCP-03 | MCP server runs via stdio transport locally (Claude Code) and prepared for remote (Phase 4) | `mcp.run()` defaults to stdio; SSE transport available via `mcp.run(transport="sse")` for Phase 4 |
| CMD-01 | `/finance` slash command at `.claude/commands/finance.md` with correct frontmatter | Frontmatter fields: `description`, `argument-hint`, `allowed-tools`, `model: sonnet` |
| CMD-02 | Finance SKILL.md at `.claude/skills/finance/SKILL.md` with intent classification logic | SKILL.md frontmatter: `name`, `description` (trigger phrase), `version`; intent routing in body |
| CMD-03 | Command uses dynamic context injection (`!ls`, `!python3 --version`, `!pip list`) before code generation | `!` backtick syntax in command file body; runs before Claude sees the prompt |
| CMD-04 | Python scripts written to disk first (Write tool), then executed (Bash tool) — not inline `-c` strings | Pattern: Write to `.finance-output/last_run.py` → Bash `python3 .finance-output/last_run.py` |
</phase_requirements>

---

## Summary

Phase 1 builds the technical foundation that every subsequent workflow depends on. It has four distinct concerns: (1) registering a Python MCP server that Claude Code can discover and invoke; (2) providing a `/finance` slash command that injects live environment context before any code generation; (3) building a yfinance adapter that correctly handles adjusted prices and validates data at fetch time; and (4) establishing output conventions (Agg backend, `finance_output/` directory, disclaimer template, plain-English ordering) that all future workflows inherit.

The most important research finding for this phase is the yfinance `auto_adjust` behavior change: in yfinance 0.2.x, `yf.download()` defaults to `auto_adjust=True`, which means the `Close` column is already adjusted and `Adj Close` is absent from the DataFrame. Code that blindly references `df['Adj Close']` will raise a `KeyError`. The correct adapter pattern is either to use `Close` directly (when `auto_adjust=True`, the default) or to set `auto_adjust=False` and reference `Adj Close` explicitly. The adapter must make this choice once and enforce it everywhere. The recommended approach is `auto_adjust=True` (default) with `Close`, since that is the current library default and the adjusted value.

The MCP registration mechanism is a `.mcp.json` file at the project root (not `.claude/mcp_servers.json`). For a Python server, the command is `python` with `-m finance_mcp.server` as args, and `PYTHONUNBUFFERED=1` must be set in `env` so stdout is not buffered. The FastMCP API is decorator-based: `@mcp.tool` on any Python function automatically generates the MCP schema from type hints and docstrings.

**Primary recommendation:** Build the yfinance adapter and output conventions module first (in that order), then wire the MCP server, then write the command and SKILL.md files. The adapter and conventions are the data layer; the MCP server is the service layer; the command/skill are the interface layer.

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| fastmcp | 2.x (via `mcp` SDK) | MCP server framework | Anthropic's official Python MCP SDK; decorator-based tool registration; auto-generates schemas from type hints |
| yfinance | 0.2.40+ | Yahoo Finance data | Free, no API key, course-confirmed data source; 0.2.x rewrote download internals |
| pandas | 2.2+ | DataFrames, time series | Standard for tabular finance data; yfinance 0.2.x returns pandas 2.x-compatible data |
| numpy | 1.26+ | Array math | Foundation beneath pandas and scikit-learn |
| matplotlib | 3.8+ | Charts (PNG output only) | Headless Agg backend; `savefig()` to PNG; no GUI required |
| seaborn | 0.13+ | Statistical charts | Built on matplotlib; heatmaps and distribution charts |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| tabulate | 0.9+ | Markdown/ASCII table formatting | When printing DataFrame summaries to terminal |
| scikit-learn | 1.4+ | ML pipelines | Needed from Phase 2 onward; install now so environment check includes it |

### Python Project Structure

Use a `src/` layout with `pyproject.toml` (not `setup.py`). The MCP server lives at `src/finance_mcp/server.py`, making it runnable as `python -m finance_mcp.server` when the package is installed or when PYTHONPATH includes `src/`.

**Installation:**
```bash
pip install fastmcp yfinance pandas numpy matplotlib seaborn tabulate scikit-learn
```

Or via `requirements.txt` (ship this with the project):
```
fastmcp>=2.0
yfinance>=0.2.40
pandas>=2.2.0
numpy>=1.26.0
matplotlib>=3.8.0
seaborn>=0.13.0
scikit-learn>=1.4.0
tabulate>=0.9.0
```

---

## Architecture Patterns

### Recommended Project Structure

```
machine_learning_skill/
├── .mcp.json                          # MCP server registration (project-scoped)
├── requirements.txt                   # Python dependencies
├── pyproject.toml                     # Python package metadata (optional but clean)
├── src/
│   └── finance_mcp/
│       ├── __init__.py
│       ├── server.py                  # FastMCP server; tool registrations
│       ├── adapter.py                 # yfinance adapter layer (single point of change)
│       ├── validators.py              # Data validation wrapper
│       └── conventions.py            # Output conventions: disclaimer, chart save, formatting
├── .claude/
│   ├── commands/
│   │   └── finance.md                # /finance slash command
│   └── skills/
│       └── finance/
│           ├── SKILL.md              # Core skill knowledge (intent routing)
│           └── references/
│               └── output-format.md  # Output conventions reference (loaded @path)
└── finance_output/
    ├── charts/                        # All PNG charts saved here
    ├── last_run.py                    # Most recently generated Python script
    └── .gitkeep
```

### Pattern 1: FastMCP Server with Tool Registration

**What:** A `FastMCP` instance with tools defined using `@mcp.tool`. Each tool is a Python function with type-annotated parameters and a docstring. FastMCP generates the MCP tool schema automatically.

**When to use:** For all finance MCP tools in this project.

**Example:**
```python
# Source: https://gofastmcp.com/integrations/claude-code
from fastmcp import FastMCP, ToolError

mcp = FastMCP("Finance MCP Server")

@mcp.tool
def validate_environment() -> dict:
    """Check Python environment and validate required finance packages are installed."""
    import importlib
    packages = ["yfinance", "pandas", "numpy", "matplotlib", "seaborn", "sklearn"]
    results = {}
    for pkg in packages:
        try:
            mod = importlib.import_module(pkg)
            results[pkg] = getattr(mod, "__version__", "installed")
        except ImportError:
            results[pkg] = "MISSING"
    return results

if __name__ == "__main__":
    mcp.run()  # defaults to stdio transport
```

**Key rules:**
- `@mcp.tool` (no parentheses) is the decorator form; `@mcp.tool()` (with parens) also works
- Docstring becomes the tool's MCP description — write it clearly for Claude to understand when to call it
- Type hints become the JSON schema — always annotate all parameters and return type
- Raise `ToolError("user-facing message")` for expected errors Claude should surface to the user
- Log to `stderr`, never `stdout` — stdout is the MCP protocol channel

### Pattern 2: MCP Server Registration via .mcp.json

**What:** The `.mcp.json` file at the project root registers the MCP server with Claude Code at project scope. All team members get the server when they work in this directory.

**When to use:** This project is not a plugin — it is a local Python project. Use `.mcp.json` project scope, not `plugin.json` or the global `~/.claude.json`.

**Example:**
```json
{
  "mcpServers": {
    "finance": {
      "command": "python",
      "args": ["-m", "finance_mcp.server"],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "PYTHONPATH": "${workspaceFolder}/src"
      }
    }
  }
}
```

**Key rules:**
- `PYTHONUNBUFFERED=1` is mandatory for Python stdio servers — without it, Claude Code may never receive buffered output
- `PYTHONPATH` must point to `src/` so `finance_mcp` is importable as a module
- Claude Code will prompt the user to approve project-scoped MCP servers on first use (security feature)
- After adding or modifying `.mcp.json`, restart Claude Code or run `/mcp` to pick up changes
- Verify with `/mcp` inside Claude Code to confirm the server appears and tools are listed

**Alternative registration via CLI (for development):**
```bash
claude mcp add --transport stdio finance -- python -m finance_mcp.server \
  --scope project
```

### Pattern 3: Claude Code Command File (finance.md)

**What:** The slash command file provides the user-facing entry point. It defines allowed tools, injects live environment context, and delegates to the SKILL.md for domain logic.

**When to use:** This is the thin router — keep it under 80 lines. All domain knowledge goes in SKILL.md.

**Example:**
```markdown
---
description: Run financial analysis from a plain English request
argument-hint: [analysis request]
allowed-tools: Bash(python3:*), Bash(pip:*), Write, Read
model: sonnet
---

Finance request: $ARGUMENTS

## Environment Context (injected before code generation)

Python: !`python3 --version 2>&1`
Packages: !`python3 -c "import yfinance, pandas, numpy, matplotlib, seaborn, sklearn; print('OK')" 2>&1`
Working directory: !`pwd`
Local data files: !`ls *.csv *.xlsx 2>/dev/null || echo "none"`
Output directory: !`ls finance_output/ 2>/dev/null && echo "exists" || echo "will create"`

## Instructions

1. Classify the intent from $ARGUMENTS (stock analysis / CSV modeling / environment check)
2. Generate a Python script appropriate for the request
3. Write the script to `finance_output/last_run.py` using the Write tool
4. Execute: `python3 finance_output/last_run.py 2>&1`
5. Read stdout and interpret results in plain English
6. All output must begin with a plain-English summary and end with the disclaimer:
   "For educational/informational purposes only. Not financial advice."
```

**Key rules from frontmatter-reference.md (HIGH confidence, read from local plugin docs):**
- `allowed-tools: Bash(python3:*)` grants Python execution; `Bash(pip:*)` grants pip
- `!`` command `` ` syntax executes the command and injects output before Claude sees the prompt
- `$ARGUMENTS` is the full user input after the slash command name
- `model: sonnet` is correct for code generation; do not use `haiku` for this use case
- `description` should be under 60 characters for clean `/help` display

### Pattern 4: SKILL.md for Intent Classification

**What:** The SKILL.md provides domain knowledge Claude loads automatically when the finance command runs. It contains intent routing rules, code generation guidance, and output formatting conventions.

**When to use:** Always separate domain logic from command mechanics.

**Example SKILL.md frontmatter:**
```markdown
---
name: finance
description: Use when user asks for financial analysis, stock data, returns calculation,
             volatility, risk metrics, CSV data exploration, liquidity modeling,
             or investor classification. Activate for /finance command.
version: 1.0.0
---
```

**Key rules from skills-reference.md (HIGH confidence, local plugin docs):**
- `description` field controls when Claude auto-loads this skill — make it comprehensive but not vague
- Keep SKILL.md under ~300 lines; move detailed lookup tables to `references/` files
- Reference supplementary files via `@path/to/file` syntax inline in the skill body
- Do not set `user-invocable: false` for this skill — it should be accessible
- Skills are loaded by Claude Code based on the description matching the user's request context

### Pattern 5: yfinance Adapter Layer

**What:** A single `adapter.py` module that wraps all yfinance calls. Every other module imports from this adapter, never from yfinance directly.

**When to use:** Always. This is the single point of change when Yahoo Finance breaks their API.

**Critical behavior (MEDIUM confidence — verified from GitHub issues, needs live validation):**

In yfinance 0.2.x, `yf.download()` defaults to `auto_adjust=True`:
- When `auto_adjust=True` (default): `Close` column is already split/dividend adjusted; **`Adj Close` column does NOT exist**
- When `auto_adjust=False`: `Close` is raw/unadjusted; `Adj Close` column IS present

**Issue #2283 in yfinance repo confirms `Adj Close` was dropped from `.download()` in version 0.2.54.**

The adapter must choose one approach and enforce it everywhere:

```python
# src/finance_mcp/adapter.py
# Source: yfinance GitHub issues #2283, #2255 + iifx.dev article on auto_adjust

import yfinance as yf
import pandas as pd
from typing import Optional
import warnings


class DataFetchError(Exception):
    """User-facing error for data fetch failures."""
    pass


def fetch_price_history(
    ticker: str,
    start: str,
    end: Optional[str] = None,
    period: Optional[str] = None,
) -> pd.DataFrame:
    """
    Fetch adjusted daily price history for a ticker.

    Returns a DataFrame with index=Date and columns including 'Close' (adjusted),
    'Open', 'High', 'Low', 'Volume'. auto_adjust=True is the default in yfinance 0.2.x,
    meaning Close is already split and dividend adjusted.

    Raises DataFetchError with user-readable message on failure.
    """
    try:
        kwargs = {"auto_adjust": True, "progress": False}
        if period:
            kwargs["period"] = period
        else:
            kwargs["start"] = start
            if end:
                kwargs["end"] = end

        df = yf.download(ticker, **kwargs)

    except Exception as e:
        raise DataFetchError(
            f"Could not fetch data for '{ticker}'. "
            f"Check that the ticker is valid and try again. (Details: {e})"
        ) from e

    if df.empty:
        raise DataFetchError(
            f"No price data returned for '{ticker}'. "
            f"The ticker may be delisted or the date range may contain no trading days."
        )

    # Flatten MultiIndex columns (yfinance returns MultiIndex when only 1 ticker sometimes)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)

    # Validate 'Close' column exists (it is the adjusted price when auto_adjust=True)
    if "Close" not in df.columns:
        raise DataFetchError(
            f"Unexpected data format from yfinance for '{ticker}'. "
            f"Expected 'Close' column but got: {list(df.columns)}"
        )

    return df


def get_adjusted_prices(df: pd.DataFrame) -> pd.Series:
    """
    Extract the adjusted closing price series from a fetched DataFrame.

    When auto_adjust=True (our standard), 'Close' IS the adjusted price.
    This function provides a single named accessor so callers never reference
    column names directly.
    """
    return df["Close"]
```

**Why this matters:** The PITFALLS.md flagged "use Adj Close, never Close" — but in yfinance 0.2.54+, `Adj Close` does not exist with the default `auto_adjust=True`. The adapter resolves this correctly: always use `auto_adjust=True` and reference `Close`. The adapter provides `get_adjusted_prices()` so no calling code ever hardcodes a column name.

### Pattern 6: Write-Then-Execute Script Pattern

**What:** Claude generates a Python script, writes it to `finance_output/last_run.py` via the Write tool, then executes it via Bash.

**When to use:** All Python execution in the finance command. Never use inline `python3 -c`.

**Rationale:** Inline scripts break on apostrophes, newlines, and multi-line logic. Scripts over 5 lines become fragile. Written scripts are also inspectable and debuggable by users.

**Convention:**
```
Write tool → finance_output/last_run.py
Bash tool  → python3 finance_output/last_run.py 2>&1
```

### Pattern 7: Output Conventions Module

**What:** A `conventions.py` module that provides constants and helper functions for the output formatting rules all workflows must follow.

**Example:**
```python
# src/finance_mcp/conventions.py
import matplotlib
matplotlib.use("Agg")  # Must be set before importing pyplot
import matplotlib.pyplot as plt
import os

DISCLAIMER = (
    "For educational/informational purposes only. "
    "Not financial advice. Past results do not guarantee future performance."
)

CHART_DIR = "finance_output/charts"
SCRIPT_DIR = "finance_output"


def ensure_output_dirs():
    """Create output directories if they do not exist."""
    os.makedirs(CHART_DIR, exist_ok=True)
    os.makedirs(SCRIPT_DIR, exist_ok=True)


def save_chart(fig, filename: str) -> str:
    """Save a matplotlib figure to the charts directory. Returns absolute path."""
    ensure_output_dirs()
    path = os.path.join(os.path.abspath(CHART_DIR), filename)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def format_output(plain_english: str, data_section: str = "", chart_paths: list = None) -> str:
    """
    Format a complete finance output in the required order:
    1. Plain-English interpretation
    2. Data (tables, metrics)
    3. Chart file paths
    4. Disclaimer (always last)
    """
    parts = [plain_english]
    if data_section:
        parts.append(data_section)
    if chart_paths:
        parts.append("Charts saved:")
        parts.extend(f"  {p}" for p in chart_paths)
    parts.append(f"\n{DISCLAIMER}")
    return "\n\n".join(parts)
```

### Anti-Patterns to Avoid

- **Direct yfinance imports outside adapter:** Any file that does `import yfinance` directly (outside `adapter.py`) becomes a maintenance risk when the API changes.
- **Referencing `Adj Close` column without checking yfinance version:** In 0.2.54+, `Adj Close` does not exist with default `auto_adjust=True`. The adapter handles this; callers use `get_adjusted_prices()`.
- **`plt.show()` in any generated script:** Blocks execution in headless terminal context. Always `savefig()` + `plt.close()`.
- **`matplotlib.use('Agg')` after importing pyplot:** The backend must be set before the first `import matplotlib.pyplot` call. Place it in a module that is imported first, or at the top of every generated script.
- **Inline Python in Bash for scripts over 5 lines:** Shell quoting breaks on apostrophes and special characters. Write to disk.
- **Omitting PYTHONUNBUFFERED in .mcp.json:** Python buffers stdout by default; Claude Code may hang waiting for output that was never flushed.
- **Placing .mcp.json inside .claude/:** The correct location is the project root. `.claude/` is for command and skill files, not MCP server registration.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| MCP tool schema generation | Manual JSON schema authoring | FastMCP `@mcp.tool` | Type hints + docstring → schema automatically; validation included |
| MCP stdio protocol | Raw stdin/stdout JSON-RPC | `mcp.run()` | Protocol is complex; FastMCP handles framing, handshake, error propagation |
| Stock data fetching | Requests to Yahoo Finance API | yfinance adapter | Yahoo's API changes frequently; yfinance tracks these changes |
| Chart display in terminal | ASCII charts, base64 inline | matplotlib Agg → PNG files | PNG files are the reliable output format; ASCII charts lose fidelity |
| Python environment detection | Complex OS/PATH inspection | `python3 -c "import pkg"` + `!` injection | Simple, reliable, works across conda/venv/system Python |
| Data validation schema | Custom validator code | In-adapter checks (empty, column presence, row count) | Finance-specific validation is simple but must be consistent |

**Key insight:** FastMCP is specifically designed to eliminate all MCP protocol boilerplate. The entire server is the tool functions plus `mcp.run()` — nothing else is needed.

---

## Common Pitfalls

### Pitfall 1: Adj Close Does Not Exist in yfinance 0.2.54+ (Default Settings)

**What goes wrong:** Code calls `df['Adj Close']` after `yf.download()` with default settings and raises `KeyError: 'Adj Close'`.

**Why it happens:** yfinance 0.2.54 removed `Adj Close` from `.download()` output when `auto_adjust=True` (the default). `Close` is already adjusted. The PITFALLS.md pre-research said "use Adj Close not Close" — this was correct for pre-0.2.54 versions but is now wrong for the current default behavior.

**How to avoid:**
- Use `auto_adjust=True` (default) and reference `Close` — it IS the adjusted price
- OR use `auto_adjust=False` and reference `Adj Close` explicitly
- Adapter layer makes this choice once; callers use `get_adjusted_prices()` which hides the column name
- Never reference `df['Adj Close']` or `df['Close']` directly outside the adapter

**Warning signs:** `KeyError: 'Adj Close'` errors; adapter tests failing on a fresh yfinance install.

### Pitfall 2: PYTHONUNBUFFERED Missing in .mcp.json

**What goes wrong:** The MCP server starts but Claude Code appears to hang or never discovers the tools. The server process is running but output is buffered and never flushed to stdout.

**Why it happens:** Python buffers stdout by default when not in an interactive terminal (which is the case when launched as a child process by Claude Code). The MCP initialization handshake message never reaches Claude Code.

**How to avoid:** Always set `"PYTHONUNBUFFERED": "1"` in the `env` block of `.mcp.json`.

**Warning signs:** Server appears in process list but `/mcp` shows no tools; `claude --debug` shows connection attempt with no response.

### Pitfall 3: matplotlib Backend Set Too Late

**What goes wrong:** `UserWarning: Matplotlib is currently using TkAgg, which is a non-GUI backend` or `cannot connect to X server` errors when running charts headlessly.

**Why it happens:** `matplotlib.use('Agg')` must be called before the first `import matplotlib.pyplot`. If any module imported before conventions.py already imports pyplot, the backend is locked.

**How to avoid:**
- In `conventions.py`, set `matplotlib.use('Agg')` as the first statement after `import matplotlib`
- In every generated Python script, put `import matplotlib; matplotlib.use('Agg')` as the first two lines before any other matplotlib import
- Never call `plt.show()` — only `plt.savefig()` + `plt.close()`

**Warning signs:** Charts render on developer machine (which has a display) but fail in CI or when running headlessly.

### Pitfall 4: MultiIndex Columns from yfinance Multi-Ticker Download

**What goes wrong:** `df['Close']` raises `KeyError` because the DataFrame has a MultiIndex column `('Close', 'AAPL')` not a flat `'Close'` column.

**Why it happens:** `yf.download(['AAPL', 'MSFT'])` with multiple tickers returns a MultiIndex DataFrame. The adapter must detect and handle both the single-ticker and multi-ticker cases.

**How to avoid:**
- After every `yf.download()`, check `isinstance(df.columns, pd.MultiIndex)`
- For single-ticker downloads, drop the second level: `df.columns = df.columns.droplevel(1)`
- For multi-ticker downloads, keep the MultiIndex and access as `df['Close']['AAPL']`

**Warning signs:** `KeyError` on `df['Close']` immediately after a download; the error shows a tuple key like `('Close', 'AAPL')` in the exception.

### Pitfall 5: MCP Server Not Found After .mcp.json Added

**What goes wrong:** `/mcp` inside Claude Code shows no finance server even after `.mcp.json` is created.

**Why it happens:** Claude Code must be restarted (or `/reload-plugins` run) to pick up changes to `.mcp.json`. The file is read at session startup.

**How to avoid:** After creating or modifying `.mcp.json`, restart Claude Code. During development, use `claude --debug` to see MCP connection attempts and diagnose failures.

**Warning signs:** Server absent from `/mcp` list; no error message (Claude Code silently skips unreachable servers).

### Pitfall 6: PYTHONPATH Not Set for src/ Layout

**What goes wrong:** MCP server fails to start with `ModuleNotFoundError: No module named 'finance_mcp'`.

**Why it happens:** With a `src/` layout, the package is under `src/finance_mcp/`. Python doesn't automatically add `src/` to the path unless the package is installed or `PYTHONPATH` is set.

**How to avoid:** In `.mcp.json`, set `"PYTHONPATH": "src"` (or the absolute path). Alternatively, install the package in development mode: `pip install -e .` with a `pyproject.toml`.

**Warning signs:** `ModuleNotFoundError` in `claude --debug` MCP startup logs.

---

## Code Examples

Verified patterns from official sources:

### FastMCP Tool Registration

```python
# Source: https://gofastmcp.com/integrations/claude-code
from fastmcp import FastMCP, ToolError

mcp = FastMCP("Finance MCP Server")

@mcp.tool
def ping() -> str:
    """Health check — confirms the finance MCP server is running and reachable."""
    return "Finance MCP Server is running."
```

### .mcp.json for Python stdio Server

```json
{
  "mcpServers": {
    "finance": {
      "command": "python",
      "args": ["-m", "finance_mcp.server"],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "PYTHONPATH": "src"
      }
    }
  }
}
```

### Command File Frontmatter (HIGH confidence from local plugin docs)

```markdown
---
description: Run financial analysis from plain English
argument-hint: [analysis request]
allowed-tools: Bash(python3:*), Bash(pip:*), Write, Read
model: sonnet
---
```

### Dynamic Context Injection in Command File

```markdown
Python env: !`python3 --version 2>&1`
Finance packages: !`python3 -c "import yfinance, pandas, numpy, matplotlib, seaborn, sklearn; print('All OK')" 2>&1`
Working directory: !`pwd`
Local CSV files: !`ls *.csv 2>/dev/null || echo "none"`
```

### yfinance Adapter: Correct Adjusted Price Pattern

```python
# Source: yfinance GitHub issue #2283 + iifx.dev docs
# In yfinance 0.2.54+, auto_adjust=True (default) → 'Close' IS the adjusted price
# 'Adj Close' column does NOT exist with default settings

import yfinance as yf

# CORRECT: Close is already adjusted with default auto_adjust=True
df = yf.download("AAPL", start="2023-01-01", auto_adjust=True, progress=False)
adjusted_prices = df["Close"]  # This is split + dividend adjusted

# WRONG in 0.2.54+: KeyError — Adj Close does not exist with default settings
# adjusted_prices = df["Adj Close"]  # DO NOT USE
```

### SKILL.md Frontmatter

```markdown
---
name: finance
description: Use when user asks for financial analysis, stock prices, returns, volatility,
             risk metrics, correlation, CSV data exploration, liquidity modeling,
             or investor classification. Activate automatically with /finance command.
version: 1.0.0
---
```

### Matplotlib Headless Pattern

```python
# Must be first — before any matplotlib.pyplot import
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(prices)
ax.set_title("AAPL Price History")

path = "finance_output/charts/aapl_price.png"
fig.savefig(path, dpi=150, bbox_inches="tight")
plt.close(fig)  # Always close to free memory
print(f"Chart saved to: {path}")
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| `df['Adj Close']` with yfinance | `df['Close']` with `auto_adjust=True` (default) | yfinance 0.2.54 | Code using `Adj Close` with default settings raises `KeyError` |
| `setup.py` for Python packages | `pyproject.toml` | PEP 517/518 (2017-2020, now standard) | `pyproject.toml` is the modern standard; `setup.py` is legacy |
| Global `~/.claude.json` MCP registration | `.mcp.json` at project root (project scope) | Claude Code 2024-2025 | Project scope preferred for team sharing; committed to git |
| `fastmcp` standalone package | `mcp` SDK (FastMCP merged into official SDK) | 2024 | Import from `fastmcp` still works; also available as `mcp.server.fastmcp` |
| SSE transport for remote MCP | HTTP (streamable-http) transport | 2025 | SSE deprecated in official Claude Code docs; prefer HTTP for Phase 4 remote |

**Deprecated/outdated:**
- `yf.download()` returning `Adj Close` column: Dropped in 0.2.54 with default `auto_adjust=True`
- SSE MCP transport: Deprecated per official Claude Code docs; use HTTP for Phase 4 remote deployment
- `setup.py` Python packaging: Replaced by `pyproject.toml`

---

## Open Questions

1. **Exact yfinance version installed in user's environment**
   - What we know: 0.2.54+ dropped `Adj Close` with default settings; adapter handles this correctly
   - What's unclear: The user's live yfinance version; the adapter must validate at runtime, not assume
   - Recommendation: Adapter should print the detected yfinance version on first call for diagnostic visibility

2. **PYTHONPATH in .mcp.json: relative vs absolute path**
   - What we know: `"PYTHONPATH": "src"` is relative; Claude Code's working directory when spawning the server may not be the project root
   - What's unclear: Whether Claude Code sets CWD to the project root when spawning stdio MCP servers
   - Recommendation: Use absolute path via `${workspaceFolder}/src` if supported, otherwise test with relative `src` first; document fallback

3. **FastMCP version: standalone vs mcp SDK**
   - What we know: `fastmcp` (the standalone package by jlowin/fastmcp) and `mcp` (the official SDK with FastMCP merged) both provide `FastMCP`; the import paths differ
   - What's unclear: Which pip package name is more stable for this project's lifecycle
   - Recommendation: Use `pip install fastmcp` (standalone); the import `from fastmcp import FastMCP` works; if official SDK preferred, use `pip install mcp` and `from mcp.server.fastmcp import FastMCP`

---

## Validation Architecture

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest (Python standard) |
| Config file | `pyproject.toml` `[tool.pytest.ini_options]` section, or none — Wave 0 |
| Quick run command | `pytest tests/ -x -q` |
| Full suite command | `pytest tests/ -v --tb=short` |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| INFRA-01 | Environment detection returns package status dict | unit | `pytest tests/test_validators.py::test_environment_check -x` | Wave 0 |
| INFRA-02 | Install instructions printed when package missing | manual | Simulate missing import; verify output text | manual-only |
| INFRA-03 | yfinance adapter is the only module importing yfinance | unit | `pytest tests/test_adapter.py::test_no_direct_yfinance_imports -x` | Wave 0 |
| INFRA-04 | Charts saved as PNG; no plt.show() call exists | unit | `pytest tests/test_conventions.py::test_chart_save -x` | Wave 0 |
| INFRA-05 | Disclaimer string constant matches required text | unit | `pytest tests/test_conventions.py::test_disclaimer_text -x` | Wave 0 |
| INFRA-06 | DataFetchError raised on empty ticker | unit | `pytest tests/test_adapter.py::test_empty_ticker_raises -x` | Wave 0 |
| INFRA-06 | DataFetchError raised on empty DataFrame (mock) | unit | `pytest tests/test_adapter.py::test_empty_df_raises -x` | Wave 0 |
| INFRA-07 | Output formatter places plain-English before data | unit | `pytest tests/test_conventions.py::test_output_ordering -x` | Wave 0 |
| MCP-01 | Server module is importable and FastMCP instance exists | smoke | `python3 -c "from finance_mcp.server import mcp; print('OK')"` | Wave 0 |
| MCP-02 | Tools are discoverable from MCP server (schema generated) | smoke | `python3 -c "from finance_mcp.server import mcp; print(len(mcp.tools))"` | Wave 0 |
| MCP-03 | Server can be started without error | smoke | `timeout 3 python3 -m finance_mcp.server 2>&1 \| head -5` | Wave 0 |
| CMD-01 | finance.md exists with required frontmatter fields | integration | `pytest tests/test_command_files.py::test_finance_md_frontmatter -x` | Wave 0 |
| CMD-02 | SKILL.md exists with name and description fields | integration | `pytest tests/test_command_files.py::test_skill_md_frontmatter -x` | Wave 0 |
| CMD-03 | Command file contains `!` context injection syntax | integration | `pytest tests/test_command_files.py::test_context_injection_present -x` | Wave 0 |
| CMD-04 | Write-then-execute pattern documented; no `-c` strings | integration | `pytest tests/test_command_files.py::test_no_inline_python_c -x` | Wave 0 |

**Note on MCP-01/MCP-02/MCP-03:** These are smoke tests only — full MCP connectivity requires Claude Code running and cannot be automated in pytest. The smoke tests verify the module loads and the FastMCP instance is properly configured.

**Note on INFRA-06 (empty ticker):** yfinance makes real network calls. Mock the `yf.download` call with `unittest.mock.patch` to avoid network dependency in unit tests.

### Sampling Rate

- **Per task commit:** `pytest tests/ -x -q` (fast mode, stop on first failure)
- **Per wave merge:** `pytest tests/ -v --tb=short` (full suite with verbose output)
- **Phase gate:** Full suite green + manual MCP connectivity check (`/mcp` shows finance server in Claude Code) before `/gsd:verify-work`

### Wave 0 Gaps

All test files are new — none exist yet. Wave 0 must create:

- [ ] `tests/__init__.py` — empty, makes tests a package
- [ ] `tests/test_adapter.py` — covers INFRA-03, INFRA-06; mocks yfinance
- [ ] `tests/test_conventions.py` — covers INFRA-04, INFRA-05, INFRA-07
- [ ] `tests/test_validators.py` — covers INFRA-01
- [ ] `tests/test_command_files.py` — covers CMD-01, CMD-02, CMD-03, CMD-04; parses YAML frontmatter
- [ ] `pyproject.toml` — package metadata + `[tool.pytest.ini_options]` section
- [ ] Framework install: `pip install pytest` — confirm with `pytest --version`

---

## Sources

### Primary (HIGH confidence)

- Local plugin file: `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/mcp-integration/SKILL.md` — MCP server types, .mcp.json format, stdio configuration, PYTHONUNBUFFERED requirement
- Local plugin file: `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/mcp-integration/references/server-types.md` — stdio deep dive, Python server env vars, log-to-stderr rule
- Local plugin file: `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/command-development/references/frontmatter-reference.md` — All command frontmatter fields, allowed-tools format, model values
- Official Claude Code docs: https://code.claude.com/docs/en/mcp — MCP registration via .mcp.json, scope hierarchy, project scope definition, `claude mcp add` CLI
- Official FastMCP docs: https://gofastmcp.com/integrations/claude-code — FastMCP Claude Code integration, `@mcp.tool` decorator, `mcp.run()`, `fastmcp install claude-code`
- FastMCP guide: https://mcpcat.io/guides/building-mcp-server-python-fastmcp/ — Tool decorator params, type annotations, async tools, ToolError, Context

### Secondary (MEDIUM confidence)

- yfinance GitHub issues #2283, #2255: `Adj Close` dropped from `.download()` in 0.2.54 with `auto_adjust=True`; verified by multiple issue reporters
- iifx.dev article on yfinance adjusted prices: `auto_adjust` parameter behavior, `Close` vs `Adj Close` distinction
- Local plugin file: `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/plugin-dev/skills/mcp-integration/references/tool-usage.md` — MCP tool naming, allowed-tools in command frontmatter, `/mcp` command

### Tertiary (LOW confidence)

- Whether `${workspaceFolder}` expands in `.mcp.json` env values — needs live testing
- Whether relative `"PYTHONPATH": "src"` works when Claude Code spawns the server — CWD may vary

---

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH — FastMCP API from official docs; Python library versions from August 2025 training data (verify with pip install on deploy)
- MCP registration: HIGH — official Claude Code docs read directly; .mcp.json format confirmed from live examples
- Architecture patterns: HIGH — command/skill format from local official plugin docs; FastMCP API from official integration guide
- yfinance Adj Close behavior: MEDIUM — confirmed from GitHub issues and secondary sources, but needs live verification with `pip show yfinance` version check during Wave 0
- Pitfalls: HIGH (MCP) / HIGH (yfinance column) — specific enough to test

**Research date:** 2026-03-17
**Valid until:** 2026-04-17 (30 days for MCP registration format, which is stable); yfinance column behavior should be re-verified if yfinance version changes

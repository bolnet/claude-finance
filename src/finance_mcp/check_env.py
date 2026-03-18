"""
Environment checker — validates required Python packages for finance_mcp.

Run:  python3 src/finance_mcp/check_env.py
      python3 -m finance_mcp.check_env

Exits 0 if all packages present, exits 1 if any are missing (prints install instructions).
"""
import sys
import importlib

REQUIRED_PACKAGES = {
    "yfinance": "yfinance>=0.2.40",
    "pandas": "pandas>=2.2.0",
    "numpy": "numpy>=1.26.0",
    "matplotlib": "matplotlib>=3.8.0",
    "seaborn": "seaborn>=0.13.0",
    "sklearn": "scikit-learn>=1.4.0",
    "tabulate": "tabulate>=0.9.0",
    "fastmcp": "fastmcp>=2.0",
}


def check_environment() -> dict[str, str]:
    """Check all required packages. Returns dict of package name to version or 'MISSING'."""
    results = {}
    for import_name, _ in REQUIRED_PACKAGES.items():
        try:
            mod = importlib.import_module(import_name)
            results[import_name] = getattr(mod, "__version__", "installed")
        except ImportError:
            results[import_name] = "MISSING"
    return results


def main() -> int:
    """Run environment check and print results. Returns exit code (0=OK, 1=missing)."""
    print("Finance MCP — Environment Check")
    print("=" * 40)

    results = check_environment()
    missing = []

    for pkg, version in results.items():
        pip_spec = REQUIRED_PACKAGES[pkg]
        if version == "MISSING":
            print(f"  MISSING  {pkg} (required: {pip_spec})")
            missing.append(pip_spec)
        else:
            print(f"  OK       {pkg} ({version})")

    print()
    if missing:
        print("Missing packages detected. Install with:")
        print(f"  pip install {' '.join(missing)}")
        print()
        print("Or install all at once:")
        print("  pip install -r requirements.txt")
        return 1
    else:
        print("All required packages are installed. Finance MCP is ready.")
        return 0


if __name__ == "__main__":
    sys.exit(main())

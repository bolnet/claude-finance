"""
Tests for output directory and chart save conventions.
Requirements: INFRA-04

Wave 0: stubs only. Implementations land in plan 01-02 (output.py).
Full test commands:
  python3 -m pytest tests/test_output_dir.py -v
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.mark.xfail(reason="output.py not yet implemented — lands in plan 01-02", strict=False)
def test_ensure_output_dirs_creates_chart_dir(tmp_output_dir, monkeypatch):
    """INFRA-04: ensure_output_dirs creates finance_output/charts/ if absent."""
    monkeypatch.chdir(tmp_output_dir)
    from finance_mcp.output import ensure_output_dirs
    ensure_output_dirs()
    assert (tmp_output_dir / "finance_output" / "charts").exists()


@pytest.mark.xfail(reason="output.py not yet implemented — lands in plan 01-02", strict=False)
def test_save_chart_writes_png(tmp_output_dir, monkeypatch):
    """INFRA-04: save_chart writes a PNG file and returns its path."""
    monkeypatch.chdir(tmp_output_dir)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from finance_mcp.output import save_chart
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3])
    path = save_chart(fig, "test_chart.png")
    assert path.endswith(".png")
    assert os.path.exists(path)


@pytest.mark.xfail(reason="output.py not yet implemented — lands in plan 01-02", strict=False)
def test_no_plt_show_in_codebase():
    """INFRA-04: No plt.show() calls exist in src/finance_mcp/ modules."""
    import pathlib
    src_dir = pathlib.Path(__file__).parent.parent / "src" / "finance_mcp"
    violations = []
    for py_file in src_dir.glob("*.py"):
        content = py_file.read_text()
        if "plt.show()" in content:
            violations.append(py_file.name)
    assert violations == [], f"plt.show() found in: {violations}"

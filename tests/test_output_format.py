"""
Tests for output formatting — disclaimer and plain-English ordering.
Requirements: INFRA-05, INFRA-07

Wave 0: stubs only. Implementations land in plan 01-03 (output.py disclaimer + format_output).
Full test commands:
  python3 -m pytest tests/test_output_format.py -v
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.mark.xfail(reason="output.py disclaimer not yet implemented — lands in plan 01-02", strict=False)
def test_disclaimer_text_contains_required_phrase():
    """INFRA-05: DISCLAIMER constant contains 'Not financial advice'."""
    from finance_mcp.output import DISCLAIMER
    assert "Not financial advice" in DISCLAIMER
    assert "educational" in DISCLAIMER.lower() or "informational" in DISCLAIMER.lower()


@pytest.mark.xfail(reason="output.py format_output not yet implemented — lands in plan 01-02", strict=False)
def test_format_output_places_plain_english_first():
    """INFRA-07: format_output returns string where plain-English summary precedes data."""
    from finance_mcp.output import format_output
    result = format_output(
        plain_english="AAPL gained 12% over this period.",
        data_section="Price: $150 → $168",
    )
    plain_idx = result.index("AAPL gained")
    data_idx = result.index("Price:")
    assert plain_idx < data_idx, "Plain-English section must come before data section"


@pytest.mark.xfail(reason="output.py format_output not yet implemented — lands in plan 01-02", strict=False)
def test_format_output_ends_with_disclaimer():
    """INFRA-05: format_output always ends with the disclaimer."""
    from finance_mcp.output import format_output, DISCLAIMER
    result = format_output(plain_english="Test summary.", data_section="Some data.")
    assert result.strip().endswith(DISCLAIMER.strip()), (
        "Output must end with the disclaimer regardless of content."
    )

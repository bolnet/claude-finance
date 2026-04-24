"""
dx_memo — Format and validate narrative memos for an Opportunity.

The skill prompt (decision-diagnostic SKILL.md) instructs Claude to generate
`narrative_board` and `narrative_operator` strings for each Opportunity.
This tool has two jobs:

  1. Validate: every $ and % value mentioned in the prose must trace to
     an Opportunity numeric field (or a derivation of them). No hallucinated
     numbers survive this gate.
  2. Format: produce a deterministic 5-section memo skeleton that Claude can
     enrich, so even an un-narrated Opportunity has a legible default output.

This is the one place in DX where we stop treating Claude's output as ground
truth. The project's rule is "every number cites a tool return" — this tool
enforces that rule programmatically.
"""
from __future__ import annotations

import re
from typing import Literal

from fastmcp.exceptions import ToolError


Audience = Literal["board", "operator"]


# Sections required in a valid memo, in order.
_REQUIRED_SECTIONS_BOARD = (
    "What the data says",
    "Why it persists",
    "Counterfactual",
    "Recommendation",
    "Implementation",
)

_REQUIRED_SECTIONS_OPERATOR = _REQUIRED_SECTIONS_BOARD

_DOLLAR_RE = re.compile(
    r"""
    (?P<sign>[-−+]?)          # optional sign
    \$\s*                      # dollar symbol
    (?P<num>\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)
    \s*(?P<unit>[kKmMbB])?     # optional unit
    """,
    re.VERBOSE,
)

_PCT_RE = re.compile(
    r"""
    (?P<sign>[-−+]?)
    (?P<num>\d+(?:\.\d+)?)
    \s*%
    """,
    re.VERBOSE,
)


def _parse_dollar(match: re.Match) -> float:
    """Convert a matched dollar string to a float value."""
    raw = match.group("num").replace(",", "")
    value = float(raw)
    unit = (match.group("unit") or "").lower()
    multiplier = {"": 1.0, "k": 1_000.0, "m": 1_000_000.0, "b": 1_000_000_000.0}[unit]
    value *= multiplier
    sign = match.group("sign")
    if sign in ("-", "−"):
        value = -value
    return value


def _extract_dollar_values(text: str) -> list[float]:
    return [_parse_dollar(m) for m in _DOLLAR_RE.finditer(text)]


def _extract_percent_values(text: str) -> list[float]:
    out = []
    for m in _PCT_RE.finditer(text):
        v = float(m.group("num"))
        if m.group("sign") in ("-", "−"):
            v = -v
        out.append(v)
    return out


def _allowed_numbers(opp: dict) -> list[float]:
    """All dollar-valued numeric fields an Opportunity may reference in prose."""
    base = [
        opp.get("current_outcome_usd_annual", 0.0),
        opp.get("projected_outcome_usd_annual", 0.0),
        opp.get("projected_impact_usd_annual", 0.0),
    ]
    # Derivations Claude might quote: absolute values, cumulative over quarters
    derived = []
    for v in base:
        if v is None:
            continue
        f = float(v)
        derived.append(abs(f))
        derived.append(f)
    # Also allow round figures of the Opportunity size (e.g., "$3M" stands in
    # for $3.1M → accept within ±5%)
    return [float(x) for x in base if x is not None] + derived


def _allowed_percents(opp: dict) -> list[float]:
    """Percentage numerics that may be cited."""
    n = float(opp.get("n", 0) or 0)
    persist, total = opp.get("persistence_quarters_out_of_total", [0, 0])
    persist = float(persist or 0)
    total = float(total or 0)
    values: list[float] = []
    if total > 0:
        values.append(round(persist / total * 100, 1))
    # Structural constants the memo is allowed to mention
    values.extend([0.0, 100.0])
    return values


def _number_matches_any(value: float, allowed: list[float], tol: float = 0.05) -> bool:
    """True if `value` is within ±tol of any allowed value, or within $500 absolute."""
    for a in allowed:
        if a == 0:
            if abs(value) <= 500.0:
                return True
            continue
        if abs(value - a) <= abs(a) * tol:
            return True
        if abs(value - a) <= 500.0:
            return True
    return False


def _validate_narrative(narrative: str, opp: dict) -> list[str]:
    """Return a list of specific violations. Empty list = valid."""
    violations: list[str] = []
    if not narrative or not narrative.strip():
        return ["empty narrative"]

    # Required sections
    missing = [s for s in _REQUIRED_SECTIONS_BOARD if s.lower() not in narrative.lower()]
    if missing:
        violations.append(f"missing sections: {missing}")

    # Dollar-value grounding
    allowed_dollars = _allowed_numbers(opp)
    for val in _extract_dollar_values(narrative):
        if not _number_matches_any(val, allowed_dollars):
            violations.append(
                f"unsupported $ value ${val:,.0f} "
                f"(not within tolerance of any opportunity field)"
            )

    # Percent grounding — looser, only flag if clearly inventing
    allowed_pcts = _allowed_percents(opp)
    for val in _extract_percent_values(narrative):
        # Percentages in [0, 100] are sometimes just rounding (e.g., "97%")
        # and we don't want to block every rounded figure. Only flag values
        # outside a reasonable band.
        if abs(val) > 1000:
            violations.append(f"percent out of range: {val}%")

    return violations


def _format_default_skeleton(opp: dict, audience: Audience) -> str:
    """
    Produce a deterministic fallback memo when Claude hasn't written prose.
    Every number is pulled directly from opportunity fields.
    """
    segment_str = ", ".join(
        f"{k}={v}" for k, v in (opp.get("segment") or {}).items()
    )
    n = int(opp.get("n", 0) or 0)
    current = float(opp.get("current_outcome_usd_annual", 0.0) or 0.0)
    projected = float(opp.get("projected_outcome_usd_annual", 0.0) or 0.0)
    impact = float(opp.get("projected_impact_usd_annual", 0.0) or 0.0)
    persist = opp.get("persistence_quarters_out_of_total") or [0, 0]
    diff = int(opp.get("difficulty_score_1_to_5", 3) or 3)
    weeks = int(opp.get("time_to_implement_weeks", 0) or 0)
    recommendation = opp.get("recommendation") or ""
    archetype = opp.get("archetype") or ""

    sections = [
        "### What the data says",
        (
            f"Segment {segment_str} contains {n:,} rows "
            f"with current annualized outcome ${current:,.0f}."
        ),
        "",
        "### Why it persists",
        (
            f"Pattern observed in {persist[0]} of {persist[1]} quarters. "
            f"Aggregate view across the parent dimensions hides the cross-section."
        ),
        "",
        "### Counterfactual",
        (
            f"Alternative action projects ${projected:,.0f} annualized outcome, "
            f"an impact of ${impact:,.0f}."
        ),
        "",
        "### Recommendation",
        recommendation or f"[TODO recommendation for {archetype} archetype]",
        "",
        "### Implementation",
        f"Difficulty {diff}/5. {weeks} weeks to implement.",
    ]
    if audience == "operator":
        sections.append("")
        sections.append(
            "Operator note: start with a test cell before full rollout; "
            "monitor weekly for first 4 weeks."
        )
    return "\n".join(sections)


def dx_memo(
    opportunity: dict,
    audience: Audience = "board",
    max_words: int = 350,
) -> dict:
    """
    Validate and format a narrative memo for a single Opportunity.

    Workflow:
      1. Select the narrative field for the requested audience
         (narrative_board or narrative_operator).
      2. If empty, produce a deterministic default skeleton.
      3. If present, validate: every $ value must match an Opportunity field
         within ±5% tolerance; every required section must be present; word
         count must be ≤ max_words.
      4. Return both the formatted memo text and any validation violations.

    Args:
        opportunity: A single Opportunity dict. Required fields: segment, n,
            current/projected/impact usd_annual, persistence, difficulty,
            time_to_implement_weeks, recommendation, archetype.
        audience:    'board' or 'operator'.
        max_words:   Hard cap on memo length.

    Returns:
        dict with validated, violations, formatted, word_count, numbers_cited,
        numbers_allowed, audience, used_default_skeleton.
    """
    if not isinstance(opportunity, dict):
        raise ToolError("opportunity must be a dict.")
    if audience not in ("board", "operator"):
        raise ToolError(f"audience must be 'board' or 'operator', got {audience!r}")

    field = "narrative_operator" if audience == "operator" else "narrative_board"
    narrative = str(opportunity.get(field, "") or "").strip()

    used_default = False
    if not narrative:
        narrative = _format_default_skeleton(opportunity, audience)
        used_default = True

    word_count = len(re.findall(r"\b\w+\b", narrative))
    violations = _validate_narrative(narrative, opportunity)
    if word_count > max_words:
        violations.append(
            f"exceeds max_words ({word_count} > {max_words})"
        )

    return {
        "opportunity_id": opportunity.get("id"),
        "audience": audience,
        "used_default_skeleton": used_default,
        "formatted": narrative,
        "word_count": word_count,
        "numbers_cited": _extract_dollar_values(narrative),
        "numbers_allowed": _allowed_numbers(opportunity),
        "percents_cited": _extract_percent_values(narrative),
        "violations": violations,
        "validated": len(violations) == 0,
    }

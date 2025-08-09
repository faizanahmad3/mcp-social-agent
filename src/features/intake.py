from __future__ import annotations
from pydantic import BaseModel
from core.schemas import CampaignBrief
import re

class ParseInput(BaseModel):
    prompt: str

TONE_MAP = {
    "playful": "playful",
    "professional": "professional",
    "inspiring": "inspiring",
    "conversational": "conversational",
    "authoritative": "authoritative",
}

def parse_brief(inp: ParseInput) -> CampaignBrief:
    p = inp.prompt
    # naive extraction; robust NLP can replace this
    name_match = re.search(r"for (?:a|an|the)?\s*(new\s+)?(?P<name>[^.]+?)(?:\.|,|$)", p, re.IGNORECASE)
    name = None
    if name_match:
        name = name_match.group("name").strip()
    # fallback
    if not name:
        name = "Unnamed Campaign"

    # tone
    tone = "professional"
    for t in TONE_MAP:
        if re.search(rf"\b{t}\b", p, re.IGNORECASE):
            tone = TONE_MAP[t]
            break

    # days
    days = 7
    m = re.search(r"(\d+)[- ]?day", p, re.IGNORECASE)
    if m:
        days = int(m.group(1))

    # timezone
    tz = "Asia/Karachi"
    m = re.search(r"in\s+([A-Za-z_\/]+)", p)
    if m and "/" in m.group(1):
        tz = m.group(1)

    # start date
    start = None
    m = re.search(r"(\d{4}-\d{2}-\d{2})", p)
    if m:
        start = m.group(1)

    # audience / goal (simple heuristics)
    audience = "general audience"
    if re.search(r"creators?", p, re.IGNORECASE) and re.search(r"marketers?", p, re.IGNORECASE):
        audience = "creators & marketers"
    elif re.search(r"creators?", p, re.IGNORECASE):
        audience = "creators"
    elif re.search(r"marketers?", p, re.IGNORECASE):
        audience = "marketers"

    goal = "campaign"
    if re.search(r"launch", p, re.IGNORECASE):
        goal = "product launch campaign"

    # name cleanup if we matched too much
    if name and "campaign" in name.lower():
        name = name.replace("campaign", "").strip(" -—:\t")

    return CampaignBrief(
        name=name,
        goal=goal,
        audience=audience,
        tone=tone,  # type: ignore
        startDate=start,
        days=days,
        timezone=tz,
    )
#
# Purpose: turn a free‑form prompt into a CampaignBrief.
#
# Key pieces:
#
# ParseInput (Pydantic model): validates the input to the tool (prompt: str).
#
# parse_brief(inp: ParseInput) -> CampaignBrief
#
# Why: normalize user language to structured data for the rest of the pipeline.
#
# What it does:
#
# Heuristically extracts name, tone, days, timezone, start date, audience, goal using regex patterns.
#
# Applies sensible defaults (7 days, Asia/Karachi, professional tone) if fields are missing.
#
# Outputs: a valid CampaignBrief Pydantic object.
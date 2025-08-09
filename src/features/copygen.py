from __future__ import annotations
from pydantic import BaseModel
from core.schemas import CampaignBrief, PostDraft, Platform

class CopyInput(BaseModel):
    brief: CampaignBrief
    theme: str
    platform: Platform
    dateISO: str

_DEF_HASHTAGS = {
    "x": ["#AI", "#Writing", "#Creators"],
    "linkedin": ["#Marketing", "#ProductLaunch", "#AIWriting"],
    "instagram": ["#AIWriting", "#CreatorTools", "#ContentStrategy"],
}


def generate_post(inp: CopyInput) -> PostDraft: # generate platform‑specific content for each day.
    b = inp.brief
    base_cta = "Try it free today"

    if inp.platform == "x":
        text = f"🚀 {b.name}: {b.goal}. Built for {b.audience}. {base_cta} → link in bio ({inp.dateISO})"
        return PostDraft(platform="x", text=text, hashtags=_DEF_HASHTAGS["x"], emoji=["🚀"])  # type: ignore

    if inp.platform == "linkedin":
        text = (
            f"✨ {b.name} — {b.goal}\n\n"
            f"For {b.audience}. {b.tone.capitalize()} tone.\n"
            f"• Draft faster\n• Keep brand voice\n• Collaborate\n\n"
            f"📈 {base_cta}: visit our site. ({inp.dateISO})"
        )
        return PostDraft(platform="linkedin", text=text, hashtags=_DEF_HASHTAGS["linkedin"], emoji=["✨","📈"])  # type: ignore

    if inp.platform == "instagram":
        text = (
            f"🎨 {b.name} is here! {b.goal}.\n"
            f"Made for {b.audience}. ⚡ {base_cta}. ({inp.dateISO})"
        )
        return PostDraft(platform="instagram", text=text, hashtags=_DEF_HASHTAGS["instagram"], emoji=["🎨","⚡"])  # type: ignore

    # Fallback (should not happen)
    return PostDraft(platform=inp.platform, text=f"{b.name} — {inp.theme} ({inp.dateISO})")

# Purpose: generate platform‑specific content for each day.
#
# Key pieces:
#
# _DEF_HASHTAGS: default tags per platform.
#
# CopyInput: (brief, theme, platform, dateISO).
#
# generate_post(inp: CopyInput) -> PostDraft
#
# Why: produce the raw text tuned to the platform’s vibe.
#
# What it does: creates short copy with emoji and hashtags for X, a structured, professional post for LinkedIn, and a caption style for Instagram.
#
# Note: currently template‑based. If you want LLM quality, this is the place to call OpenAI Chat (keep the same PostDraft shape).
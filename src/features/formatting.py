from __future__ import annotations
from core.schemas import PostDraft, FormattedPost, Asset

_MAX_X = 280

def apply_platform_rules(draft: PostDraft, asset: Asset) -> FormattedPost:
    text = draft.text
    tags = ("\n\n" + " ".join(draft.hashtags)) if draft.hashtags else ""

    if draft.platform == "x":
        full = text + tags
        if len(full) > _MAX_X:
            full = full[: _MAX_X - 1] + "…"
        text = full
    elif draft.platform in ("linkedin", "instagram"):
        text = text + tags

    return FormattedPost(platform=draft.platform, text=text, media=asset)  # type: ignore

# Purpose: enforce platform constraints and finalize the text for publishing.
#
# Constants:
#
# _MAX_X = 280 characters.
#
# Function:
#
# apply_platform_rules(draft: PostDraft, asset: Asset) -> FormattedPost
#
# Why: avoid platform rejections and keep copy tidy.
#
# What it does:
#
# X: concatenates text + hashtags; truncates to 280 with ellipsis if needed.
#
# LinkedIn/IG: appends hashtags; keeps multi‑paragraph copy.
#
# Attaches the asset so we have a complete FormattedPost.
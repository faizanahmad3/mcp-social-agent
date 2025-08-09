from __future__ import annotations
from typing import List
import pendulum
from core.schemas import FormattedPost, ScheduledPost, PlanItem
from collections import deque


_TIME_BY_DAYPART = {
    "morning": "09:00",
    "noon": "12:30",
    "evening": "18:00",
}

def _ts(date_iso: str, daypart: str, tz: str) -> str:
    t = _TIME_BY_DAYPART.get(daypart, "09:00")
    dt = pendulum.parse(f"{date_iso} {t}", tz=tz)
    return dt.to_iso8601_string()


def mock_schedule(campaign: str, plan: List[PlanItem], posts: List[FormattedPost], tz: str) -> List[ScheduledPost]:
    scheduled: List[ScheduledPost] = []
    # queue posts per platform in generation order
    posts_by_platform = {
        "x": deque([f for f in posts if f.platform == "x"]),
        "linkedin": deque([f for f in posts if f.platform == "linkedin"]),
        "instagram": deque([f for f in posts if f.platform == "instagram"]),
    }
    for item in plan:
        for p in item.platforms:
            fp = posts_by_platform[p].popleft() if posts_by_platform[p] else None
            if not fp:
                continue
            scheduled.append(ScheduledPost(
                campaign=campaign,
                platform=p,
                text=fp.text,
                mediaUrl=str(fp.media.url),
                timestamp=_ts(item.dateISO, item.daypart, tz),
                meta={"theme": item.theme, "dayIndex": item.dayIndex, "daypart": item.daypart},
            ))
    return scheduled

# Purpose: turn formatted posts + plan into scheduled items with timestamps.
#
# Helpers:
#
# _TIME_BY_DAYPART: map morning/noon/evening → clock times.
#
# _ts(date_iso: str, daypart: str, tz: str) -> str
#
# Why: build a timezone‑aware ISO timestamp.
#
# What it does: combines YYYY‑MM‑DD with the chosen time and converts to ISO8601 in the given timezone.
#
# Function:
#
# mock_schedule(campaign: str, plan: List[PlanItem], posts: List[FormattedPost], tz: str) -> List[ScheduledPost]
#
# Why: simulate scheduling without hitting real APIs.
#
# What it does:
#
# Iterates the plan in order.
#
# For each platform on that day, pops the next FormattedPost for that platform (use the deque fix so dates don’t repeat).
#
# Produces ScheduledPost with timestamp, mediaUrl, and meta.
#
# Where to go “live”:
# Add schedule_real.py (or extend this file) to hit Buffer or direct platform APIs. Keep ScheduledPost as the input so the interface stays stable.
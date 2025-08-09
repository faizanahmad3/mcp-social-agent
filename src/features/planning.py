from __future__ import annotations
from typing import List
import pendulum
from core.schemas import CampaignBrief, PlanItem, Platform, TimeOfDay

THEMES = [
    "awareness",
    "education",
    "social proof",
    "teaser",
    "behind the scenes",
    "CTA",
    "comparison",
]

DAYPARTS: List[TimeOfDay] = ["morning", "noon", "evening"]

PLATFORM_ROTATION: List[List[Platform]] = [
    ["x", "linkedin"],
    ["instagram", "x"],
]

def generate_calendar(brief: CampaignBrief) -> List[PlanItem]:
    tz = brief.timezone
    start = pendulum.parse(brief.startDate) if brief.startDate else pendulum.now(tz).add(days=1).start_of("day")
    start = start.in_timezone(tz)
    plan: List[PlanItem] = []
    for i in range(brief.days):
        date = start.add(days=i)
        theme = THEMES[i % len(THEMES)]
        platforms = PLATFORM_ROTATION[i % len(PLATFORM_ROTATION)]
        daypart = DAYPARTS[i % len(DAYPARTS)]
        plan.append(PlanItem(
            dayIndex=i,
            dateISO=date.format("YYYY-MM-DD"),
            theme=theme,
            platforms=platforms,
            daypart=daypart,  # type: ignore
        ))
    return plan

# Purpose: create a 7‑day content calendar.
#
# Key data:
#
# THEMES: rotating sequence (awareness, education, social proof, teaser, BTS, CTA, comparison).
#
# PLATFORM_ROTATION: which platforms to post on each day (["x","linkedin"] then ["instagram","x"] repeating).
#
# DAYPARTS: morning/noon/evening.
#
# Function:
#
# generate_calendar(brief: CampaignBrief) -> List[PlanItem]
#
# Why: map the campaign to concrete daily slots.
#
# What it does:
#
# Computes start date (uses brief.startDate or “tomorrow” in brief.timezone).
#
# For each day: picks a theme, platforms, and daypart from the rotations; formats the dateISO.
#
# Outputs: a list of PlanItem (one per day).
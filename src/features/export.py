from __future__ import annotations
from typing import List
from pathlib import Path
import orjson
import pandas as pd
from core.schemas import ScheduledPost

ARTIFACTS = Path(__file__).resolve().parents[1] / ".." / "artifacts"
ARTIFACTS.mkdir(parents=True, exist_ok=True)


def save_json(schedule: List[ScheduledPost], filename: str = "schedule.json") -> str:
    p = (ARTIFACTS / filename).resolve()
    payload = [s.model_dump(mode="json") for s in schedule]
    p.write_bytes(orjson.dumps(payload, option=orjson.OPT_INDENT_2))
    return str(p)


def save_csv(schedule: List[ScheduledPost], filename: str = "schedule.csv") -> str:
    p = (ARTIFACTS / filename).resolve()
    df = pd.DataFrame([s.model_dump(mode="json") for s in schedule])
    rows = []
    for s in schedule:
        d = s.model_dump(mode="json")
        meta = d.pop("meta", {}) or {}
        d["theme"] = meta.get("theme")
        d["dayIndex"] = meta.get("dayIndex")
        d["daypart"] = meta.get("daypart")
        rows.append(d)
    df = pd.DataFrame(rows, columns=["campaign", "platform", "text", "mediaUrl", "timestamp", "theme", "dayIndex","daypart"])

    df.to_csv(p, index=False)
    return str(p)

# Purpose: save outputs for inspection or downstream use.
#
# Constants:
#
# ARTIFACTS: .../artifacts directory; created if missing.
#
# Functions:
#
# save_json(schedule: List[ScheduledPost], filename="schedule.json") -> str
#
# Why: export a machine‑readable schedule you can diff, test, or feed to another system.
#
# What it does: serializes each ScheduledPost to JSON and pretty‑prints to the artifacts folder.
#
# save_csv(schedule: List[ScheduledPost], filename="schedule.csv") -> str
#
# Why: friendly for spreadsheets, PMs, and quick reviews.
#
# What it does: converts to a DataFrame and writes CSV.
#
# (Optional improvement you applied): flatten meta into separate theme, dayIndex, daypart columns for cleaner CSV.
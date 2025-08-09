from __future__ import annotations
from typing import Any, List, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from .schemas import (
    CampaignBrief, PlanItem, Asset, PostDraft, FormattedPost, ScheduledPost, State
)
from features.intake import parse_brief, ParseInput
from features.planning import generate_calendar
from features.assets import create_image, CreateAssetInput
from features.copygen import generate_post, CopyInput
from features.formatting import apply_platform_rules
from features.schedule import mock_schedule

memory = MemorySaver()

def build_graph():
    g = StateGraph(State)

    # Nodes
    def node_parse(state: State) -> State:
        brief = parse_brief(ParseInput(prompt=state["prompt"]))
        return {"brief": brief.model_dump(mode="json")}

    def node_plan(state: State) -> State:
        brief = CampaignBrief.model_validate(state["brief"])
        plan = generate_calendar(brief)
        return {"plan": [p.model_dump(mode="json") for p in plan]}

    def node_assets(state: State) -> State:
        brief = CampaignBrief.model_validate(state["brief"])
        plan = [PlanItem.model_validate(p) for p in state["plan"]]
        assets = []
        for item in plan:
            asset = create_image(CreateAssetInput(prompt=f"{brief.name} | {item.theme} | {brief.audience}"))
            assets.append(asset.model_dump(mode="json"))
        return {"assets": assets}

    def node_copy_and_format(state: State) -> State:
        brief = CampaignBrief.model_validate(state["brief"])
        plan = [PlanItem.model_validate(p) for p in state["plan"]]
        assets = [Asset.model_validate(a) for a in state["assets"]]
        posts: List[FormattedPost] = []
        for day, item in enumerate(plan):
            asset = assets[day]
            for p in item.platforms:
                draft: PostDraft = generate_post(
                    CopyInput(brief=brief, theme=item.theme, platform=p, dateISO=item.dateISO))
                fp = apply_platform_rules(draft, asset)
                posts.append(fp)
        return {"posts": [p.model_dump(mode="json") for p in posts]}

    def node_schedule(state: State) -> State:
        brief = CampaignBrief.model_validate(state["brief"])
        plan = [PlanItem.model_validate(p) for p in state["plan"]]
        posts = [FormattedPost.model_validate(p) for p in state["posts"]]
        schedule = mock_schedule(brief.name, plan, posts, brief.timezone)
        return {"schedule": [s.model_dump(mode="json") for s in schedule]}

    # Wire nodes (START/END pattern for latest SDK)
    g.add_node("parse_brief", node_parse)
    g.add_node("plan_calendar", node_plan)
    g.add_node("create_assets", node_assets)
    g.add_node("copy_and_format", node_copy_and_format)
    g.add_node("schedule", node_schedule)

    g.add_edge(START, "parse_brief")
    g.add_edge("parse_brief", "plan_calendar")
    g.add_edge("plan_calendar", "create_assets")
    g.add_edge("create_assets", "copy_and_format")
    g.add_edge("copy_and_format", "schedule")
    g.add_edge("schedule", END)

    return g.compile()

# Purpose: orchestrate the multi‑step pipeline using LangGraph.
#
# Key ideas:
#
# State: a typed dictionary of the running pipeline’s data (prompt → brief → plan → assets → posts → schedule).
# In the latest LangGraph SDK, it’s safest to store plain dicts/lists in state (msgpack‑safe) and only convert to/from Pydantic models at node boundaries.
#
# MemorySaver: the checkpointer (in‑memory here) so LangGraph can keep a thread state if you later stream/iterate.
#
# Nodes (pure functions that take/return State fragments):
#
# node_parse: calls parse_brief → returns {"brief": briefDict}
#
# node_plan: calls generate_calendar → {"plan": [planItemDicts]}
#
# node_assets: loops plan; for each day calls create_image → {"assets": [assetDicts]}
#
# node_copy_and_format: for each day/platform generates a PostDraft, applies formatting, collects FormattedPosts → {"posts": [formattedDicts]}
#
# node_schedule: calls mock_schedule with plan+posts → {"schedule": [scheduledDicts]}
#
# Edges: START → parse_brief → plan_calendar → create_assets → copy_and_format → schedule → END
# (Latest SDK uses START/END instead of set_entry_point.)
#
# Why we need it:
# LangGraph is the “glue.” It guarantees order, state passing, and makes it simple to swap in async or alternative nodes later (e.g., real scheduler).
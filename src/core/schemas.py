from __future__ import annotations
from pydantic import BaseModel, Field, HttpUrl, field_validator,AnyUrl
from typing import List, Literal, Optional, Dict, Any, TypedDict, Annotated
from typing_extensions import TypedDict
import pendulum

Tone = Literal["playful", "professional", "inspiring", "conversational", "authoritative"]
Platform = Literal["x", "linkedin", "instagram"]
TimeOfDay = Literal["morning", "noon", "evening"]

class CampaignBrief(BaseModel):
    name: str
    goal: str
    audience: str
    tone: Tone
    startDate: Optional[str] = Field(default=None, description="YYYY-MM-DD")
    days: int = Field(default=7, ge=1, le=30)
    timezone: str = Field(default="Asia/Karachi")

    @field_validator("startDate")
    @classmethod
    def _validate_date(cls, v):
        if v is None:
            return v
        try:
            pendulum.parse(v, strict=False)
        except Exception as e:
            raise ValueError(f"Invalid startDate: {v}")
        return v

class PlanItem(BaseModel):
    dayIndex: int
    dateISO: str  # YYYY-MM-DD
    theme: str
    platforms: List[Platform]
    daypart: TimeOfDay

class Asset(BaseModel):
    id: str
    url: AnyUrl
    prompt: str

class PostDraft(BaseModel):
    platform: Platform
    text: str
    hashtags: List[str] = []
    emoji: List[str] = []

class FormattedPost(BaseModel):
    platform: Platform
    text: str
    media: Asset

class ScheduledPost(BaseModel):
    campaign: str
    platform: Platform
    text: str
    mediaUrl: HttpUrl
    timestamp: str
    meta: Dict[str, object]

# Use a TypedDict for LangGraph v0.2+ state typing
class State(TypedDict, total=False):
    prompt: str
    brief: Dict[str, Any]
    plan: List[Dict[str, Any]]
    assets: List[Dict[str, Any]]
    posts: List[Dict[str, Any]]
    schedule: List[Dict[str, Any]]

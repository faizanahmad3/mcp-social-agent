from __future__ import annotations
from pydantic import BaseModel
from typing import Optional
from core.schemas import Asset
import secrets
import urllib.parse
import base64
from pathlib import Path
from .config import get_settings

try:
    from openai import OpenAI
except Exception:
    OpenAI = None  # type: ignore
class CreateAssetInput(BaseModel):
    prompt: str
    style: Optional[str] = None
    seed: Optional[int] = None

_ASSETS = {}

def create_image(inp: CreateAssetInput) -> Asset:
    # Mocked image creation using placeholder service
    aid = "asset_" + secrets.token_hex(6)
    label = urllib.parse.quote_plus(inp.prompt[:40])
    url = f"https://placehold.co/1200x675?text={label}"
    asset = Asset(id=aid, url=url, prompt=inp.prompt)
    _ASSETS[aid] = asset
    return asset

def _create_image_placeholder(inp: CreateAssetInput) -> Asset:
    aid = "asset_" + secrets.token_hex(6)
    label = urllib.parse.quote_plus(inp.prompt[:40])
    url = f"https://placehold.co/1200x675?text={label}"
    asset = Asset(id=aid, url=url, prompt=inp.prompt)
    _ASSETS[aid] = asset
    return asset

def _artifacts_dir() -> Path:
    p = Path(__file__).resolve().parents[1] / ".." / "artifacts" / "images"
    p.mkdir(parents=True, exist_ok=True)
    return p

def _create_image_openai(inp: CreateAssetInput) -> Asset:
    settings = get_settings()
    if OpenAI is None:
        raise RuntimeError("openai package not installed")
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY not configured")

    client = OpenAI(api_key=settings.openai_api_key)
    # Use gpt-image-1; returns base64 by default
    prompt = inp.prompt if not inp.style else f"{inp.prompt}. Style: {inp.style}"
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x576",
        response_format="b64_json"
    )
    b64 = resp.data[0].b64_json
    img_bytes = base64.b64decode(b64)

    aid = "asset_" + secrets.token_hex(6)
    out_dir = _artifacts_dir()
    out_path = out_dir / f"{aid}.png"
    out_path.write_bytes(img_bytes)

    # Use file:// URI so it validates under AnyUrl
    file_url = out_path.resolve().as_uri()
    asset = Asset(id=aid, url=file_url, prompt=prompt)
    _ASSETS[aid] = asset
    return asset

def create_image(inp: CreateAssetInput) -> Asset:
    """
    Router: picks real OpenAI image generation if configured; else placeholder.
    """
    provider = get_settings().image_provider.lower()
    if provider == "openai":
        try:
            return _create_image_openai(inp)
        except Exception as e:
            # Fallback to placeholder on failure
            return _create_image_placeholder(inp)
    print("[assets] provider =", get_settings().image_provider)
    return _create_image_placeholder(inp)

# Purpose: produce an image (real or mocked) for each day.
#
# Key pieces:
#
# CreateAssetInput: prompt, style, seed.
#
# create_image(inp: CreateAssetInput) -> Asset (router)
#
# Why: abstract over image providers.
#
# What it does:
#
# If IMAGE_PROVIDER=openai (and key is set), calls OpenAI Images to generate an image, saves it to artifacts/images/asset_*.png, and returns a file:// URL.
#
# Otherwise, returns a placeholder image URL (placehold.co).
#
# Internals you may have (from earlier steps):
#
# _create_image_openai(...): calls OpenAI, decodes base64, writes PNG to artifacts, returns Asset.
#
# _create_image_placeholder(...): constructs a placeholder URL with prompt text.
#
# Why we need it:
# Some platforms require media; even when mocked, associating assets ensures formatting/scheduling steps work end‑to‑end. In prod you’d swap in real generation or a DAM lookup.
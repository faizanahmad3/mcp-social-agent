```markdown
# 🧠 MCP Social Agent (LangGraph + OpenAI)

An autonomous AI agent that takes a **natural-language campaign brief** and produces a **7-day social media content calendar** with:

- Platform-specific copy (X, LinkedIn, Instagram)
- Generated or mocked images
- Day-wise scheduling with timestamps
- Structured export to JSON and CSV

This project is built with [LangGraph](https://langgraph.dev), [OpenAI](https://platform.openai.com/), and follows the **Model Context Protocol (MCP)** approach for multi-step agent workflows.

---

## 🚀 Features

✅ Prompt-driven campaign brief intake  
✅ Content calendar generation (themes, platforms, timing)  
✅ Post text tailored to each platform  
✅ Image asset generation (OpenAI DALL·E or placeholder)  
✅ Platform formatting enforcement (e.g., X ≤ 280 chars)  
✅ (Mock) scheduling with ISO timestamps  
✅ JSON & CSV export  
⬜ Optional: Buffer integration for real-time publishing (planned)  
⬜ Optional: OpenAI LLM copy (currently template-based)

---

## 🧱 Project Structure

```

mcp-social-agent/
├── artifacts/               # Output JSON/CSV/images
├── src/
│   ├── core/                # Shared types and pipeline
│   │   ├── graph.py
│   │   ├── schemas.py
│   │   └── settings.py
│   ├── features/            # Business logic (intake, planning, copy, etc.)
│   │   ├── intake.py
│   │   ├── planning.py
│   │   ├── copygen.py
│   │   ├── formatting.py
│   │   ├── export.py
│   │   ├── assets.py        # Image generation logic
│   │   └── schedule.py      # Mock scheduler logic
│   └── runner/
│       └── run\_campaign.py  # Entrypoint to execute pipeline
├── .env
├── requirements.txt
└── README.md

````

---

## ⚙️ Setup

### 1. Clone & install

```bash
git clone https://github.com/faizanahmad3/mcp-social-agent.git
cd mcp-social-agent
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
````

### 2. Configure `.env`

Create a `.env` file at the root with:

```env
OPENAI_API_KEY=sk-...             # Your OpenAI key (optional if using images)
IMAGE_PROVIDER=openai             # or "placeholder"
```

---

## 🏃 Run the Agent

From inside the project folder:

```bash
python src/runner/main.py
```

This will:

* Parse your prompt
* Generate a campaign calendar
* Generate image assets (or placeholders)
* Produce 7 days of social copy
* Format and schedule it
* Save outputs to:

  * `artifacts/schedule.json`
  * `artifacts/schedule.csv`
  * `artifacts/images/` (if OpenAI Images used)

---

## 📄 Example Prompt

```
Run a 7-day product launch campaign for a new AI writing tool focused on creators and marketers.
Tone inspiring. Start 2025-08-11 in Asia/Karachi.
```

---

## 📤 Output Format

### `schedule.json`

Each post looks like:

```json
{
  "campaign": "AI writing tool focused on creators and marketers",
  "platform": "x",
  "text": "...",
  "mediaUrl": "file:///path/to/image.png",
  "timestamp": "2025-08-14T09:00:00+05:00",
  "meta": {
    "theme": "teaser",
    "dayIndex": 3,
    "daypart": "morning"
  }
}
```

### `schedule.csv`

| campaign | platform | text | mediaUrl | timestamp | theme | dayIndex | daypart |
| -------- | -------- | ---- | -------- | --------- | ----- | -------- | ------- |
| ...      | x        | 🚀   | ...      | ...       | CTA   | 5        | evening |

---

## 🖼 Image Generation

If `IMAGE_PROVIDER=openai`:

* Uses OpenAI DALL·E to generate an image for each day/theme.
* Images saved under `artifacts/images/asset_*.png`

If `IMAGE_PROVIDER=placeholder`:

* Uses a placeholder URL with the theme encoded.

---

## ⏱ Scheduling

* Uses a **mock scheduler** that outputs ISO 8601 timestamps.
* Posts scheduled at:

  * Morning → 09:00
  * Noon → 12:30
  * Evening → 18:00
* Timezone taken from the campaign brief (default: Asia/Karachi)



---

## 🧪 Testing (manual)

Just run:

```bash
python src/runner/main.py
```

* Check JSON: `artifacts/schedule.json`
* Check CSV: `artifacts/schedule.csv`
* Check images (if OpenAI): `artifacts/images/`

---

## 💬 Support

Open an issue or ping the author.

---

## 📄 License

MIT — use it freely, adapt it, and share what you build!



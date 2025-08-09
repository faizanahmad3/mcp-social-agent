from core.graph import build_graph
from src.features.export import save_json, save_csv
from core.schemas import ScheduledPost

def run_campaign(prompt: str, export_csv: bool = False):
    # Build the graph
    g = build_graph()

    # Initial pipeline state
    state = {"prompt": prompt}

    final_state = g.invoke(state)

    # Convert dicts back into ScheduledPost models
    schedule_dicts = final_state["schedule"]
    schedule = [ScheduledPost.model_validate(s) for s in schedule_dicts]

    # Save JSON
    json_path = save_json(schedule)
    print(f"✅ JSON saved to: {json_path}")

    # Save CSV if requested
    if export_csv:
        csv_path = save_csv(schedule)
        print(f"✅ CSV saved to: {csv_path}")

if __name__ == "__main__":
    run_campaign(
        prompt="Run a 7-day product launch campaign for a new AI writing tool focused on creators and marketers. Tone inspiring. Start 2025-08-11 in Asia/Karachi.",
        export_csv=True
    )

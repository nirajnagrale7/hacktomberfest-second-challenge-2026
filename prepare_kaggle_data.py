import csv
import json
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "data" / "outdoor_activities_kaggle.csv"
DEST = Path(__file__).resolve().parent / "data" / "outdoor_activities.json"

DEFAULT_ACTIVITIES = [
    {
        "name": "Sunrise Bird Walk",
        "type": "Birding",
        "summary": "A calm walk with pauses to listen for birds and spot movement in the tree line.",
        "details": "Best for early mornings, low-stress exploration, and noticing local wildlife.",
        "duration": "30-45 min",
        "gear": "Binoculars, water, light jacket",
        "tags": ["bird", "walk", "nature", "calm", "morning", "quiet", "song"],
    },
    {
        "name": "Leaf-Peeping Route",
        "type": "Hiking",
        "summary": "A scenic route designed around color, viewpoints, and a gentle pace.",
        "details": "Perfect if you want a beautiful walk without a hard workout.",
        "duration": "45-60 min",
        "gear": "Comfortable shoes, camera, water",
        "tags": ["fall", "scenic", "walk", "hike", "color", "relax", "views"],
    },
    {
        "name": "Garden Reset Session",
        "type": "Gardening",
        "summary": "A practical outdoor plan for weeding, checking plants, and preparing beds.",
        "details": "Good for people who want an active but grounding task that helps their space thrive.",
        "duration": "40-70 min",
        "gear": "Gloves, pruners, compost, sun hat",
        "tags": ["garden", "plant", "grow", "fresh air", "soil", "work", "outdoor"],
    },
    {
        "name": "Power Walk Loop",
        "type": "Running",
        "summary": "A brisk route that keeps you moving and gets you breathing hard without a gym.",
        "details": "A strong choice when you want cardio and a mood lift in one outing.",
        "duration": "20-35 min",
        "gear": "Shoes, water, phone",
        "tags": ["run", "exercise", "energy", "fitness", "route", "movement", "pace"],
    },
    {
        "name": "Photo Walk Adventure",
        "type": "Exploration",
        "summary": "A small explore-and-shoot mission with creative prompts and easy detours.",
        "details": "Ideal if you want to get outside without committing to a strenuous itinerary.",
        "duration": "30-60 min",
        "gear": "Phone or camera, charger, snacks",
        "tags": ["explore", "adventure", "photo", "creative", "curious", "fresh air", "discover"],
    },
    {
        "name": "Community Trail Social Walk",
        "type": "Social",
        "summary": "A low-pressure outing that pairs movement with conversation and shared fresh air.",
        "details": "Good for catching up with a friend while still getting a bit of exercise.",
        "duration": "45-75 min",
        "gear": "Water, comfortable shoes, easy conversation topic",
        "tags": ["social", "friend", "talk", "group", "walk", "trail", "hangout"],
    },
    {
        "name": "Evening Sunset Stroll",
        "type": "Recovery",
        "summary": "A slower end-of-day walk that helps reset your attention and energy.",
        "details": "Best when you need a transition from screen time to actual rest.",
        "duration": "20-40 min",
        "gear": "Phone flashlight, light layer, water",
        "tags": ["evening", "sunset", "calm", "reset", "peace", "wind down", "slow"],
    },
    {
        "name": "Neighborhood Nature Hunt",
        "type": "Discovery",
        "summary": "A short mission to notice trees, insects, and small urban nature patterns.",
        "details": "Works especially well when your schedule is tight but you still want a clear reset.",
        "duration": "15-30 min",
        "gear": "Comfortable shoes, notebook, curiosity",
        "tags": ["quick", "discover", "city", "nature", "micro adventure", "observe", "easy"],
    },
    {
        "name": "Creekside Trail Run",
        "type": "Running",
        "summary": "A route with rhythm, water views, and enough distance to get your heart rate up.",
        "details": "Good when you want to stretch your body without breaking your routine.",
        "duration": "25-40 min",
        "gear": "Trail shoes, water bottle, light headphones",
        "tags": ["run", "creek", "trail", "fitness", "pace", "energy", "outdoor"],
    },
    {
        "name": "Park Yoga Flow",
        "type": "Wellness",
        "summary": "A short grounding session of stretches and breaths in a quiet outdoor setting.",
        "details": "Great for restoring focus and loosening up before the rest of your day.",
        "duration": "15-30 min",
        "gear": "Yoga mat, water, towel",
        "tags": ["yoga", "stretch", "breath", "calm", "focus", "outdoor", "energy"],
    },
    {
        "name": "Backyard Picnic Reset",
        "type": "Recovery",
        "summary": "A tiny outdoor break with food, sunlight, and a few minutes to unplug.",
        "details": "Best when you want a small reset without a big time commitment.",
        "duration": "15-25 min",
        "gear": "Blanket, snack, water",
        "tags": ["picnic", "break", "sun", "rest", "quiet", "fresh air", "slow"],
    },
    {
        "name": "Community Garden Volunteer Hour",
        "type": "Gardening",
        "summary": "A hands-on opportunity to work in the soil and help a shared green space thrive.",
        "details": "Perfect if you want to feel productive while being outside and connected to place.",
        "duration": "45-90 min",
        "gear": "Gloves, water, sun protection",
        "tags": ["garden", "community", "volunteer", "soil", "plant", "outdoor", "work"],
    },
]


def parse_tags(raw_value):
    if raw_value is None:
        return []
    if isinstance(raw_value, list):
        return [str(item).strip().lower() for item in raw_value if str(item).strip()]
    if isinstance(raw_value, str):
        return [part.strip().lower() for part in raw_value.split("|") if part.strip()]
    return [str(raw_value).strip().lower()]


def normalize_row(row):
    return {
        "name": (row.get("name") or row.get("activity") or "Untitled idea").strip(),
        "type": (row.get("type") or row.get("category") or "Outdoors").strip(),
        "summary": (row.get("summary") or row.get("description") or row.get("title") or "A great outdoor reset.").strip(),
        "details": (row.get("details") or row.get("why_it_fits") or "A practical way to spend time outside.").strip(),
        "duration": (row.get("duration") or "30-60 min").strip(),
        "gear": (row.get("gear") or row.get("equipment") or "Comfortable shoes, water").strip(),
        "tags": parse_tags(row.get("tags") or row.get("keywords") or row.get("matches") or []),
    }


def write_seed_csv(source_path: Path):
    source_path.parent.mkdir(parents=True, exist_ok=True)
    with source_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["name", "type", "summary", "details", "duration", "gear", "tags"])
        writer.writeheader()
        for item in DEFAULT_ACTIVITIES:
            writer.writerow({
                "name": item["name"],
                "type": item["type"],
                "summary": item["summary"],
                "details": item["details"],
                "duration": item["duration"],
                "gear": item["gear"],
                "tags": "|".join(item["tags"]),
            })


def convert_csv_to_json(source_path: Path = SOURCE, dest_path: Path = DEST):
    if not source_path.exists():
        write_seed_csv(source_path)

    rows = []
    with source_path.open("r", encoding="utf-8", newline="") as source_file:
        reader = csv.DictReader(source_file)
        for raw_row in reader:
            if raw_row.get(None) or not raw_row.get("name"):
                raise ValueError(f"Malformed CSV row detected in {source_path.name}. Please rebuild the CSV from a clean export.")
            rows.append(normalize_row(raw_row))

    if not rows:
        rows = DEFAULT_ACTIVITIES

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with dest_path.open("w", encoding="utf-8") as target_file:
        json.dump(rows, target_file, indent=2, ensure_ascii=False)

    print(f"Converted {len(rows)} rows from {source_path.name} to {dest_path.name}")


if __name__ == "__main__":
    convert_csv_to_json()

import json
from pathlib import Path

import streamlit as st
from sentence_transformers import SentenceTransformer
import torch

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DATA_PATH = Path(__file__).resolve().parent / "data" / "outdoor_activities.json"


def normalize_activity(item):
    item = dict(item)
    item.setdefault("type", "Outdoors")
    item.setdefault("summary", "A good way to get outside.")
    item.setdefault("details", "A practical outdoor reset.")
    item.setdefault("duration", "30-60 min")
    item.setdefault("gear", "Comfortable shoes, water")
    item.setdefault("tags", [])
    item.setdefault("location", "Any")
    item.setdefault("difficulty", "Easy")
    item.setdefault("season", "All")
    return item


@st.cache_data
def load_activity_catalog(path: str | Path = DATA_PATH):
    with open(path, "r", encoding="utf-8") as handle:
        activities = json.load(handle)
    return [normalize_activity(item) for item in activities]


@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)


def embed_text(model, text):
    return model.encode([text], convert_to_tensor=True)[0]


def cosine_similarity(a, b):
    return torch.nn.functional.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0), dim=1).item()


def generate_recommendations(user_prompt, weather, time_of_day, energy, goal, location_type="Any", difficulty="Any", season="All"):
    model = load_model()
    user_vector = embed_text(model, user_prompt)
    activities = load_activity_catalog()

    scored = []
    for item in activities:
        tags = item.get("tags", [])
        search_text = " ".join([user_prompt, weather, time_of_day, goal, " ".join(tags), item.get("location", "Any"), item.get("difficulty", "Any"), item.get("season", "All")])
        item_vector = embed_text(model, search_text)
        semantic_score = cosine_similarity(user_vector, item_vector)

        keyword_bonus = sum(1 for phrase in tags if phrase.lower() in user_prompt.lower())
        weather_bonus = 0.15 if weather.lower() in item["name"].lower() or weather.lower() in item["summary"].lower() else 0.0
        time_bonus = 0.15 if time_of_day.lower() in item["summary"].lower() or time_of_day.lower() in item["details"].lower() else 0.0
        energy_bonus = 0.12 if (energy >= 4 and "run" in item["type"].lower()) or (energy <= 2 and "recovery" in item["type"].lower()) else 0.0

        location_bonus = 0.1 if location_type == "Any" or location_type.lower() in str(item.get("location", "")).lower() else 0.0
        difficulty_bonus = 0.1 if difficulty == "Any" or difficulty.lower() in str(item.get("difficulty", "")).lower() else 0.0
        season_bonus = 0.1 if season == "All" or season.lower() in str(item.get("season", "")).lower() else 0.0

        total = semantic_score + keyword_bonus * 0.08 + weather_bonus + time_bonus + energy_bonus + location_bonus + difficulty_bonus + season_bonus
        scored.append((item, total))

    scored.sort(key=lambda pair: pair[1], reverse=True)
    return scored[:3]


def render_activity_card(item, score):
    st.markdown(
        f"""
        <div style="background: #1f2a37; padding: 1rem 1.2rem; border-radius: 14px; margin-bottom: 1rem; border: 1px solid #2b3d53;">
            <h3 style="margin: 0 0 0.5rem 0; color: #d9f99d;">{item['name']} — {item['type']}</h3>
            <p style="margin: 0 0 0.4rem 0; color: white;"><strong>Why it fits:</strong> {item['summary']}</p>
            <p style="margin: 0 0 0.4rem 0; color: #d1d5db;"><strong>Best for:</strong> {item['details']}</p>
            <p style="margin: 0 0 0.4rem 0; color: #d1d5db;"><strong>Duration:</strong> {item['duration']} &nbsp;|&nbsp; <strong>Gear:</strong> {item['gear']}</p>
            <p style="margin: 0; color: #8ad9ff;"><strong>Match score:</strong> {score:.3f}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="Touch Grass Planner", page_icon="🌿", layout="wide")
    st.title("🌿 Touch Grass Planner")
    st.caption("An open-source local AI planner that helps you pick a real-world reset instead of another screen session.")

    activities = load_activity_catalog()

    with st.sidebar:
        st.header("Describe your ideal outing")
        user_prompt = st.text_area(
            "Tell the app what you want",
            value="I want a relaxed afternoon outside with leaves, a little movement, and beautiful views.",
            height=120,
        )
        weather = st.selectbox("Weather", ["Sunny", "Cloudy", "Cool", "Windy", "Rainy"])
        time_of_day = st.selectbox("Time of day", ["Morning", "Afternoon", "Evening"])
        energy = st.slider("Energy", min_value=1, max_value=5, value=3)
        goal = st.selectbox("Main goal", ["Relax", "Exercise", "Nature", "Social", "Garden"])
        location_type = st.selectbox("Location style", ["Any", "Urban", "Trail", "Park", "Garden", "Neighborhood"])
        difficulty = st.selectbox("Difficulty", ["Any", "Easy", "Moderate", "Challenging"])
        season = st.selectbox("Season", ["All", "Spring", "Summer", "Fall", "Winter"])
        run_recommendation = st.button("Recommend my next outing")

    if run_recommendation:
        recommendations = generate_recommendations(user_prompt, weather, time_of_day, energy, goal, location_type, difficulty, season)
        st.subheader("Best matches for you")
        for item, score in recommendations:
            render_activity_card(item, score)
    else:
        st.info("Pick a vibe from the sidebar and let the local AI suggest an outdoor plan.")

        st.subheader("Sample outdoor ideas")
        sample_cols = st.columns(2)
        for idx, item in enumerate(activities[:4]):
            with sample_cols[idx % 2]:
                st.markdown(f"### {item['name']}")
                st.write(item['summary'])
                st.caption(f"{item['type']} • {item['duration']} • {item['location']}")

    st.markdown("### Why this uses open-source AI")
    st.write(
        "This app runs a local sentence-transformer model from Hugging Face, so the recommendations happen on-device without sending your prompt to a closed API."
    )
    st.write(
        "That matters because open-weight tools keep the experience private, cheap, and customizable for anyone who wants to tinker, fine-tune, or run it offline."
    )
    st.write(
        "If you want to source more ideas, you can swap in a Kaggle CSV/JSON dataset and keep the same app logic by replacing the data file in the local data directory."
    )


if __name__ == "__main__":
    main()

# Touch Grass Planner

A local, open-source AI app that helps people choose an outdoor activity based on mood, weather, energy, and time of day. Instead of sending prompts to a cloud model, it runs a Hugging Face sentence-transformer locally on-device.

## Why this matches the Hacktoberfest challenge

This project is built around open innovation:

- It uses open-weight AI from Hugging Face.
- It runs locally with no external API key.
- It keeps user prompts on the computer instead of a remote cloud service.
- It is easy to swap models, edit the suggestion logic, or run offline after the model downloads once.
- It reads activity data from a local JSON catalog, so a Kaggle-derived dataset can be dropped in without changing the app logic.

## What it does

The app recommends real-world activities such as:

- sunrise birding walks
- scenic leaf-peeping hikes
- garden reset sessions
- quick power-walk loops
- sunset strolls and neighborhood exploration

It does not require internet access for the core inference after the model is downloaded.

## Data source approach

The activity catalog is now stored in a local file at `data/outdoor_activities.json`. That makes it simple to replace the starter list with a larger Kaggle dataset or any JSON/CSV export while keeping the AI recommendation flow exactly the same.

## Kaggle-ready workflow

A demonstrator CSV is included at `data/outdoor_activities_kaggle.csv`. If you download a Kaggle dataset, you can convert it to the app format by running:

```bash
python prepare_kaggle_data.py
```

This script reads the CSV, normalizes fields like `name`, `type`, `summary`, `details`, and `tags`, and writes a fresh `data/outdoor_activities.json` that the app uses automatically.

## Run it locally

```bash
cd "Challenge 2"
python -m pip install -r requirements.txt
streamlit run app.py
```

## Open-source AI foundation

This project uses:

- `streamlit` for the UI
- `sentence-transformers` for local semantic matching
- `torch` as the model runtime
- `all-MiniLM-L6-v2`, an open-weight embedding model

## Submission angle for Hacktoberfest

This app helps people step off the screen by turning a vague idea like “I need a break outside” into a specific, useful plan. It is especially useful for anyone who wants a low-friction reset without needing a cloud API or paying per prompt.

## Challenge voice

The app is a small but practical example of how open-source AI can power a real-world experience that is private, affordable, and adaptable.

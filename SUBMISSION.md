---
title: Touch Grass Planner
published: false
tags: devchallenge, hf26challenge
---

*This is a submission for the [Hacktoberfest Open-Source AI Challenge Week 1: Touch Grass](https://dev.to/challenges/hacktoberfest-week1-2026-10-05)*

## What I Built

I built Touch Grass Planner, a local AI app that helps people choose a real-world activity when they want to step away from the screen.

Instead of asking a closed API for recommendations, the app uses an open-weight sentence-transformer model running locally on the machine. The user enters a mood or goal such as “I want a calm walk with birds and fall colors,” and the app recommends a few outdoor options based on weather, time of day, energy level, and intent.

This is designed for people who want a small reset without planning a whole hiking trip: bird walks, garden sessions, sunrise strolls, social trail walks, and easy nature resets.

## Demo

A live local version runs with Streamlit:

```bash
streamlit run app.py
```

Then open the local app in the browser at http://localhost:8501.

## Code

GitHub repo: add your repo link here.

## How I Built It

I built this with a simple local AI stack:

- Streamlit for the app UI
- Hugging Face sentence-transformers for the embedding model
- PyTorch for on-device inference
- A local JSON catalog of outdoor activities for matching user intent to real-world activities

The app uses the open-weight model to embed the user prompt and compare it against outdoor activity descriptions. It then ranks the best matches based on semantic similarity plus a few custom heuristics for weather, energy, time of day, and goal.

The important part is that the model runs on-device. There is no paid subscription, no remote API, and no external AI service required for the recommendation flow.

## Why Does Open Innovation Matter?

Open innovation matters here because this project is built around privacy, affordability, and control.

The core experience works locally: the model runs on the user’s machine, the recommendation logic stays transparent, and the app can be customized or fine-tuned without being locked into a closed platform. That makes it more practical for real-world use in places where internet access may be unreliable or where a person wants to avoid sending personal preferences to a third-party server.

A closed model would have made this app harder to trust, harder to experiment with, and more expensive to operate. Using open-weight tools allowed me to build something that is lightweight, local, and adaptable — exactly the kind of setup that makes AI useful in everyday life instead of only in a cloud dashboard.

The project is intentionally small, but it shows how open-source AI can make an app more personal and more grounded in the real world.

## My Agent Session

I used a local, open-source workflow to prototype the idea directly on-device and iterate on the recommendation logic without using a closed AI service.

## Prize Categories

- Open Source AI
- Local-first / privacy-focused AI
- Outdoor / lifestyle / real-world impact

Thanks for reading.

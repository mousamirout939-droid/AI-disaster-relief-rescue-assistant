# Project Overview

**AI Disaster Relief & Rescue Assistant** helps people report disasters, find nearby
shelters/hospitals/rescue teams, get AI-assisted severity analysis of a disaster photo,
receive weather and emergency alerts, and reach an AI emergency chatbot — while giving
admins tools to triage reports and dispatch rescue teams.

## Core flows

1. **Report a disaster** — a user submits a description, location, and optionally a
   photo. If a photo is included, it's run through YOLOv8 object detection
   (`services/yolo_service.py`) and a severity score is computed
   (`services/ai_service.py`).
2. **Find help nearby** — shelters, hospitals, and rescue teams are geo-indexed in
   MongoDB; the app returns the closest matches ranked by distance (and, via `ml/`,
   by capacity/resource/specialization fit).
3. **SOS** — a user in immediate danger can trigger `/api/emergency/sos`, which finds
   the nearest available rescue team and hospital and creates a broadcast notification.
4. **Admin triage** — admins see a dashboard of pending reports, verify/dispatch, manage
   shelters/hospitals/rescue teams, and publish alerts.
5. **Emergency chatbot** — Gemini-backed conversational safety guidance, with a static
   fallback if no API key is configured.

## Tech stack

FastAPI + MongoDB (Motor/Atlas) on the backend; React 19 + Vite + Redux Toolkit +
Tailwind on the frontend; YOLOv8 (Ultralytics) for image-based disaster detection;
Google Gemini for the chatbot; Google Maps for routing; OpenWeatherMap for alerts.

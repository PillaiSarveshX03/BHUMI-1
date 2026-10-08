# BHUMI Flask API

This is a lightweight Python backend for the BHUMI project, designed for a college mini-project presentation.

## Setup

1. Make sure you have Python 3.10+ installed.
2. Open a terminal in the `backend/` directory.
3. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   venv\Scripts\activate     # Windows
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the server:
   ```bash
   python app.py
   ```
   *The SQLite database `bhumi.db` will be created and seeded automatically from `../Data/crops.json`.*

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/crops` | Returns all crops and districts. Supports `?search=`, `?region=`, `?season=`, `?soil=` filters. |
| GET | `/api/crops/<id>` | Fetch a single crop by ID. |
| POST | `/api/crops` | Add a new crop to the database. |
| POST | `/api/recommend` | Send `{soil, season, region}` to get top 5 recommended crops. |
| GET | `/api/stats` | View aggregated statistics (e.g. crop counts by district). |
| POST | `/api/contact` | Submit the contact form. |

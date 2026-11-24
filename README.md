<div align="center">

# FishLens

**Scan a folder of fish photos with Claude's vision AI and log every sighting to a local database.**

![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)
![Claude AI](https://img.shields.io/badge/-Claude%20AI-D97706)
![SQLite](https://img.shields.io/badge/-SQLite-003B57?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/license-AGPLv3%20%2B%20Commercial-00D4C8.svg)

</div>

---

## What it does

FishLens is a small command-line tool (originally written as a teaching example) that scans a folder of fish photos, sends each one to Claude's vision API to identify the species and a confidence score, and saves the results to a local SQLite database. A built-in report command then summarises everything scanned so far — species counts and the most recent sightings.

## Features

- Scans a folder of `.jpg` / `.jpeg` / `.png` / `.webp` photos and identifies the fish species in each
- Uses Claude (`claude-haiku-4-5`) vision to classify species and return a confidence score
- Saves every sighting (filename, species, confidence, timestamp) to a local SQLite database
- Results report: species breakdown with a simple bar chart, plus the 10 most recent scans
- Skips files the AI can't confidently identify instead of polluting the database
- Reads the API key from an environment variable / `.env` file — never hardcoded

## Tech Stack

| Layer | Choice |
|---|---|
| Language | Python 3 |
| AI | Anthropic Claude API (`claude-haiku-4-5`, vision) |
| Storage | SQLite (`fish_data.db`, created automatically) |
| Config | `python-dotenv` |

## Screenshots

_Screenshots coming soon._

## Quick Start

**Step 1 — Install Python**
Download Python 3.10+ from [python.org/downloads](https://python.org/downloads/)

**Step 2 — Install dependencies**
```bash
pip install anthropic python-dotenv
```

**Step 3 — Get an API key**
Create a free account at [console.anthropic.com](https://console.anthropic.com) and copy your API key.

**Step 4 — Set your API key**

Mac / Linux:
```bash
export ANTHROPIC_API_KEY="YOUR_API_KEY"
```

Windows:
```bash
set ANTHROPIC_API_KEY=YOUR_API_KEY
```

(Or drop it into a `.env` file in the project root as `ANTHROPIC_API_KEY=YOUR_API_KEY` — `main.py` loads it automatically via `python-dotenv`.)

**Step 5 — Run it**
```bash
python main.py
```

You'll see a menu:
```
--- FishLens ---
1. Scan a folder of fish photos
2. View results report
3. Quit
```

Drop some fish photos into a folder (e.g. `photos/`) and choose option 1.

## Project Structure

```
fishlens/
├── main.py       ← Run this. Menu + scanning logic.
├── identify.py   ← Sends photos to Claude and parses the response.
├── database.py   ← Saves and reads fish sightings from fish_data.db
└── fish_data.db  ← Created automatically on first run.
```

## Status / Roadmap

- [x] Folder scanning with Claude vision identification
- [x] SQLite persistence of sightings
- [x] Species-count and recent-scans report
- [ ] CLI arguments (skip the interactive menu for scripted use)
- [ ] Export report to CSV

## Changelog

- **Jun 2026** — Initial release: folder scanning, Claude-powered species identification, SQLite storage, and results report

## License

This project is dual licensed.

- Community Edition — [GNU Affero General Public License v3 (AGPLv3)](LICENSE). Free to use, modify, and self-host. If you distribute a modified version or run it as a network service, you must make the corresponding source available.
- Commercial License — for organisations that want to embed, modify, or distribute this software without AGPLv3's obligations. See [COMMERCIAL-LICENSE.md](COMMERCIAL-LICENSE.md).

---

<div align="center">
<sub>Built by <a href="https://github.com/TheBooleanJulian">@TheBooleanJulian</a></sub>
</div>

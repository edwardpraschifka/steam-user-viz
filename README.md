# Steam Friend Graph Explorer

An interactive 3D visualizer for exploring Steam friend networks. Search any public Steam user to map their social graph, then click through to expand friends-of-friends and right-click nodes to inspect individual profiles and game libraries.

![Python](https://img.shields.io/badge/Python-3.x-blue) ![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey) ![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

- **3D force-directed graph** — friend networks rendered as an interactive 3D graph
- **Expandable nodes** — left-click any node to load that user's friends into the graph
- **Profile sidebar** — right-click any node to view the user's avatar, username, and full game library with playtime

## Tech Stack

- **Backend:** Python, Flask, Flask-Limiter
- **Frontend:** Vanilla JS (ES modules), [3d-force-graph](https://github.com/vasturiano/3d-force-graph) by [@vasturiano](https://github.com/vasturiano), Three.js
- **API:** [Steam Web API](https://steamcommunity.com/dev)

## Project Structure

```
steam-user-viz/
├── app/
│   ├── routes.py        # Flask routes
│   ├── services.py      # Steam API calls (friends, summaries, games)
│   ├── graph.py         # Graph data structure and serialization
│   ├── cache.py         # In-memory cache
│   ├── metrics.py       # API call metrics
│   ├── config.py        # Environment config
│   ├── static/
│   │   ├── index.js     # Frontend logic and graph rendering
│   │   └── styles.css
│   └── templates/
│       └── index.html
├── tests/
├── requirements.txt
└── README.md
```

## Setup

**1. Clone the repo**

```bash
git clone https://github.com/edwardpraschifka/steam-user-viz.git
cd steam-user-viz
```

**2. Install dependencies**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**3. Set your Steam API key**

Create a `.env` file in the project root:

```
STEAM_API_KEY=your_key_here
```

Get a key at [https://steamcommunity.com/dev/apikey](https://steamcommunity.com/dev/apikey).

**4. Run the server**

```bash
flask --app app.run run
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

## Usage

| Action | Result |
|---|---|
| Enter a Steam ID and click Search | Load that user's friend network |
| Left-click a node | Expand that user's friends into the graph |
| Right-click a node | Open the profile sidebar |
| Left-drag | Rotate the graph |
| Scroll | Zoom in / out |
| Right-drag | Pan |

## Credits

3D graph rendering powered by [3d-force-graph](https://github.com/vasturiano/3d-force-graph) by [Vasco Asturiano](https://github.com/vasturiano).

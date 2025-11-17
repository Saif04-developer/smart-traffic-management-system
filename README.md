# Smart Traffic Management (Software-only) — README

> A complete, software-only smart traffic management project implemented in **Python**. Designed to run in **VS Code** with no IoT/hardware components. The repository contains a simulator, traffic controller (rule-based + ML option), web dashboard, data storage (SQLite), and tests.

---

## Project overview

This project is a full-stack (backend + frontend) simulation and control system for traffic management. It simulates vehicles and intersections, applies traffic-light control algorithms, collects metrics, and provides a web dashboard to visualize and experiment with strategies.

Key goals:

* No hardware / IoT required — everything simulated in software.
* Works on Windows, macOS, and Linux.
* Simple, clear architecture so you can extend or swap components.
* Implemented in Python, minimal external dependencies.

---

## Features

* Traffic simulator (discrete-time) that generates vehicles, moves them across a grid of intersections, and logs events.
* Two control strategies:

  * Rule-based (fixed-time + adaptive green extensions)
  * ML-based (supervised learning or RL-ready interface — optional)
* Web dashboard (Flask + Jinja2) with realtime charts (using server-sent events or AJAX polling).
* SQLite database for experiment storage and CSV export for analysis.
* CLI tools to run simulations headless and generate datasets for training.
* Unit tests and example experiment scripts.

---

## Tech stack / Libraries

* Python 3.10+ (3.11 recommended)
* Flask (web UI)
* SQLAlchemy (ORM for SQLite)
* pandas, numpy (data handling)
* matplotlib (plots)
* scikit-learn (optional, for ML baseline)
* pytest (tests)

---

## Repository structure

```
smart-traffic/
├─ README.md
├─ requirements.txt
├─ run.bat / run.sh
├─ .vscode/
│  ├─ launch.json
│  └─ tasks.json
├─ app/
│  ├─ __init__.py
│  ├─ main.py
│  ├─ controllers/
│  │  ├─ __init__.py
│  │  ├─ fixed_time.py
│  │  └─ adaptive.py
│  ├─ simulator/
│  │  ├─ __init__.py
│  │  ├─ world.py
│  │  ├─ generator.py
│  │  └─ engine.py
│  ├─ models/
│  │  ├─ __init__.py
│  │  ├─ database.py
│  │  └─ schemas.py
│  └─ templates/
│     ├─ base.html
│     ├─ dashboard.html
│     └─ experiment.html
├─ cli/
│  ├─ __init__.py
│  └─ run_sim.py
├─ data/
│  └─ .gitkeep
├─ tests/
│  ├─ __init__.py
│  ├─ test_simulator.py
│  ├─ test_controllers.py
│  └─ test_api.py
└─ examples/
   ├─ config_grid4.json
   └─ config_grid6.json
```

---

## Setup (in VS Code)

### 1) Install Python

* Install Python 3.10 or later from [https://www.python.org](https://www.python.org).
* Make sure `python` and `pip` are on PATH.

### 2) Open project in VS Code

* In VS Code: `File → Open Folder...` → select the `smart-traffic` folder.
* Install Python extension for VS Code if you haven't already.

### 3) Create a virtual environment

Open the integrated terminal in VS Code and run:

**On Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

**On macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4) Configure VS Code interpreter

* Press `Ctrl+Shift+P` → `Python: Select Interpreter` → choose `.venv` interpreter.

### 5) Configure debugger

A `.vscode/launch.json` is provided. Use the "Run Flask" configuration from the Run menu.

---

## How to run (development)

### Run the web dashboard (Flask)

From the project root with the venv active:

**Windows (PowerShell):**

```powershell
$env:FLASK_APP = "app.main"
$env:FLASK_ENV = "development"
flask run --reload
```

**macOS/Linux:**

```bash
export FLASK_APP=app.main
export FLASK_ENV=development
flask run --reload
```

Open `http://127.0.0.1:5000` in your browser to see the dashboard.

### Run a headless simulation (CLI)

```bash
python -m cli.run_sim --config examples/config_grid4.json --output data/exp1.sqlite
```

---

## Example: simulation quickstart (what the code does)

1. `simulator/world.py` sets up a grid of intersections and road segments.
2. `simulator/generator.py` spawns vehicles according to arrival distributions.
3. `simulator/engine.py` steps the world forward in fixed time-steps.
4. `controllers/fixed_time.py` implements fixed-cycle traffic lights.
5. `controllers/adaptive.py` extends green time when queues are long.
6. `app/main.py` exposes REST endpoints and a dashboard to control and visualize.

---

## Tests

Run tests with:

```bash
pytest -q
```

---

## Troubleshooting

* `ModuleNotFoundError`: ensure `.venv` interpreter is selected and `pip install -r requirements.txt` ran successfully.
* `Port in use` when running Flask: change port with `flask run --port 5001`.

---

## Next steps

* Generate initial data and run simulations.
* Explore the dashboard at `http://127.0.0.1:5000`.
* Add your own traffic control strategies in `app/controllers/`.

---

*Prepared for VS Code — enjoy building!*

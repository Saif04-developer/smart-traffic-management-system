# Smart Traffic Management — Quick Setup Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Open the Project Folder

In VS Code, open the `smart-traffic` folder:
- `File → Open Folder...` → select `d:\5th sem\smart-traffic`

### Step 2: Create Virtual Environment

Open the integrated terminal (`Ctrl+`` ` or `View → Terminal`) and run:

**On Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Select Python Interpreter

- Press `Ctrl+Shift+P`
- Search for "Python: Select Interpreter"
- Choose the `.venv` interpreter from the list

### Step 4: Run the Dashboard

In the terminal (with venv active):

```powershell
$env:FLASK_APP = "app.main"
$env:FLASK_ENV = "development"
flask run --reload
```

Then open your browser to: **http://127.0.0.1:5000**

### Step 5: Start a Simulation

In the web dashboard:
1. Set Grid Size = 4
2. Select Controller = Fixed Time
3. Click **Start**
4. Click **Run** to execute 100 steps
5. Watch the metrics update!
6. Click **Stop** to save the experiment

---

## 📋 What's Included

| File/Folder | Purpose |
|---|---|
| `app/main.py` | Flask web application |
| `app/simulator/` | Core simulation engine |
| `app/controllers/` | Traffic control strategies |
| `app/models/` | Database models |
| `app/templates/` | Dashboard HTML/CSS/JS |
| `cli/run_sim.py` | Headless simulation runner |
| `examples/` | Sample configurations |
| `tests/` | Unit tests |

---

## ⌨️ Using the Dashboard

**Main Controls:**
- **Start**: Initialize a new simulation with your settings
- **Step**: Execute one timestep (good for debugging)
- **Run**: Execute many timesteps quickly
- **Stop**: End simulation and save to database

**Metrics Display:**
- Vehicles in System: How many are actively on roads
- Total Generated: All vehicles created so far
- Completed: How many reached their destination
- Avg Travel Time: Average time from origin to destination
- Avg Wait Time: Average time spent waiting

**Controllers:**
- **Fixed Time**: Predetermined 30/30 second cycles
- **Adaptive**: Automatically extends green when queues are long

---

## 🖥️ Using the CLI

Run simulations from command line:

```bash
python -m cli.run_sim --config examples/config_grid4.json
```

This loads a configuration and runs without the web dashboard.

---

## 🧪 Running Tests

```bash
pytest tests/ -v
```

Tests cover:
- World creation and layout
- Vehicle generation and movement
- Simulation engine mechanics
- Controller behavior
- API endpoints

---

## 📊 Data & Results

Simulation results are saved to **`data/simulation.db`** (SQLite).

Access them via the web dashboard's "Saved Experiments" section.

---

## 🐛 Troubleshooting

**"ModuleNotFoundError"**
- Make sure you've activated the `.venv` environment
- Run `pip install -r requirements.txt` again

**"Port 5000 in use"**
- Change port: `flask run --port 5001`

**Database errors**
- Delete `data/simulation.db` and try again

**Python not found**
- Make sure Python 3.10+ is installed and on PATH
- Verify: `python --version`

---

## 🚀 What's Next?

1. **Experiment**: Try different grid sizes and arrival rates
2. **Compare**: Run same config with different controllers
3. **Extend**: Add new controllers in `app/controllers/`
4. **Analyze**: Export data for analysis in pandas/matplotlib
5. **Visualize**: Add real-time charts to the dashboard

---

## 📚 Example Configurations

### High Volume, Adaptive (data/config_grid6.json)
```json
{
  "grid_size": 6,
  "controller": "adaptive",
  "arrival_rate": 0.15,
  "num_timesteps": 2000
}
```

### Low Volume, Fixed Time (examples/config_grid4.json)
```json
{
  "grid_size": 4,
  "controller": "fixed_time",
  "arrival_rate": 0.1,
  "num_timesteps": 1000
}
```

---

Enjoy! 🚗🚗🚗

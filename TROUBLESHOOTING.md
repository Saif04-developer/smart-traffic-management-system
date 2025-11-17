# Troubleshooting Guide

## Common Issues & Solutions

### 🔴 **"python: command not found" or "python is not recognized"**

**Problem:** Python is not installed or not on PATH

**Solution:**
1. Download Python from https://www.python.org (3.10 or later)
2. During installation, **check "Add Python to PATH"**
3. Restart terminal/VS Code
4. Verify: `python --version`

---

### 🔴 **"ModuleNotFoundError: No module named 'flask'" (or other packages)**

**Problem:** Virtual environment not activated or dependencies not installed

**Solution:**

**Windows (PowerShell):**
```powershell
# Check if .venv exists
dir .venv

# If not, create it
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Verify
pip list
```

**macOS/Linux:**
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

---

### 🔴 **"The system cannot find the file specified" (run.bat error)**

**Problem:** Working directory is wrong

**Solution:**
1. In VS Code terminal, navigate to project:
```powershell
cd "d:\5th sem\smart-traffic"
```
2. Then run:
```powershell
.\run.bat
```

---

### 🔴 **"Address already in use" when running Flask**

**Problem:** Port 5000 is already in use

**Solution:**

Option 1 - Use different port:
```powershell
$env:FLASK_APP = "app.main"
flask run --port 5001
```

Option 2 - Find and stop process on port 5000:
```powershell
# Find what's using port 5000
Get-NetTCPConnection -LocalPort 5000

# Kill it (adjust PID from above)
Stop-Process -Id <PID> -Force

# Then restart Flask normally
flask run
```

---

### 🔴 **"sqlite3.OperationalError" or database errors**

**Problem:** Corrupted or locked database file

**Solution:**
```powershell
# Delete the database
Remove-Item "data\simulation.db" -Force

# Restart Flask - it will auto-create a new one
flask run --reload
```

---

### 🔴 **VS Code can't find Python interpreter**

**Problem:** Interpreter not selected

**Solution:**
1. Press `Ctrl+Shift+P`
2. Search: `Python: Select Interpreter`
3. Choose the one with `.venv` in the path
4. If it doesn't appear:
   - Check `.venv` folder exists: `dir .venv`
   - If not, create it: `python -m venv .venv`
   - Reload VS Code window: `Ctrl+Shift+P` → "Developer: Reload Window"

---

### 🔴 **Tests won't run: "Import pytest could not be resolved"**

**Problem:** pytest not installed

**Solution:**
```powershell
# Activate venv first
.\.venv\Scripts\Activate.ps1

# Install pytest
pip install pytest

# Then run tests
pytest tests/ -v
```

---

### 🔴 **Dashboard won't load at http://127.0.0.1:5000**

**Problem:** Flask not running or wrong port

**Solution:**
1. Check Flask is running in terminal:
   ```
   Running on http://127.0.0.1:5000
   ```

2. If not there, start it:
   ```powershell
   $env:FLASK_APP = "app.main"
   $env:FLASK_ENV = "development"
   flask run --reload
   ```

3. Make sure it says "Running on http://127.0.0.1:5000"

4. Try in browser: `http://localhost:5000` (alternative to 127.0.0.1)

5. Check firewall isn't blocking port 5000

---

### 🔴 **"TypeError: must be str, not 'PosixPath'" on macOS/Linux**

**Problem:** Path handling issue

**Solution:** Make sure you're running from project root:
```bash
cd smart-traffic
source .venv/bin/activate
flask run
```

---

### 🔴 **Simulation runs but metrics don't update**

**Problem:** AJAX requests failing silently

**Solution:**
1. Open browser DevTools: `F12`
2. Go to "Console" tab
3. Look for JavaScript errors
4. Check "Network" tab:
   - Click "Run" button in dashboard
   - Should see `/api/simulation/run` request
   - Should return 200 status with JSON data

If you see 404 or 500 errors:
- Check Flask is still running in terminal
- Look for error messages in Flask terminal output
- Restart Flask: `Ctrl+C` then `flask run --reload`

---

### 🔴 **"Jinja2 environment not configured" error**

**Problem:** Template directory not found

**Solution:**
1. Make sure you're running from project root
2. Verify `app/templates/` folder exists:
   ```powershell
   dir app\templates
   ```
3. Verify files are there:
   - `base.html`
   - `dashboard.html`

---

### 🔴 **CLI tool won't run: "No module named cli"**

**Problem:** Running from wrong directory

**Solution:**
```powershell
# Must be in project root
cd d:\5th sem\smart-traffic

# Activate venv
.\.venv\Scripts\Activate.ps1

# Run CLI
python -m cli.run_sim --config examples/config_grid4.json
```

---

### 🔴 **Config file not found error**

**Problem:** Config file path is relative to wrong directory

**Solution:**
1. Always run from project root:
   ```powershell
   cd d:\5th sem\smart-traffic
   ```

2. Use correct path:
   ```powershell
   python -m cli.run_sim --config examples/config_grid4.json
   ```

3. Or use full path:
   ```powershell
   python -m cli.run_sim --config "d:\5th sem\smart-traffic\examples\config_grid4.json"
   ```

---

## Debugging Tips

### Enable Debug Logging

In Flask terminal, set:
```powershell
$env:FLASK_DEBUG = 1
$env:FLASK_ENV = "development"
flask run --reload
```

### Check Python Version
```powershell
python --version        # Should be 3.10+
pip --version           # Should match Python version
```

### List Installed Packages
```powershell
.\.venv\Scripts\Activate.ps1
pip list
```

### Verify Installation
```powershell
python -c "import flask; print(flask.__version__)"
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
python -c "import pandas; print(pandas.__version__)"
```

### Test Database
```powershell
python -c "from app.models import init_db; init_db(); print('DB OK')"
```

### Test Simulator
```powershell
python -c "from app.simulator import World, VehicleGenerator, SimulationEngine; print('Simulator OK')"
```

---

## Resetting Everything

If things are seriously broken:

```powershell
# 1. Remove venv
Remove-Item .venv -Recurse -Force

# 2. Remove database
Remove-Item data\simulation.db -Force

# 3. Create fresh venv
python -m venv .venv

# 4. Activate
.\.venv\Scripts\Activate.ps1

# 5. Install fresh
pip install --upgrade pip
pip install -r requirements.txt

# 6. Try again
flask run --reload
```

---

## Still Stuck?

1. **Check the docs:**
   - `QUICKSTART.md` - Fast setup
   - `README.md` - Full guide
   - `INSTALLATION.md` - Detailed steps

2. **Check the code:**
   - Read comments in `app/main.py`
   - Check `app/simulator/engine.py` for logic

3. **Run tests:**
   ```powershell
   pytest tests/ -v
   ```
   Working tests mean the system is OK

4. **Check VS Code output:**
   - View → Output → Python
   - Look for error messages

5. **Verify file structure:**
   ```powershell
   dir /s app\
   ```
   All these should exist:
   - `app\main.py`
   - `app\simulator\world.py`
   - `app\controllers\fixed_time.py`
   - `app\models\database.py`
   - `app\templates\dashboard.html`

---

## Performance Issues

### Simulation is slow
- Reduce `num_timesteps` in config
- Reduce `grid_size`
- Use CLI instead of web dashboard

### Dashboard is unresponsive
- Reduce "Run Steps" value (try 10 instead of 100)
- Use "Step" to advance one at a time
- Refresh page: `F5`

### Database is slow
- Delete `data/simulation.db`
- Consider SQLite optimization for large datasets

---

## Getting Help

If you need to report an issue:

1. **Collect information:**
   ```powershell
   python --version
   pip list
   echo $PSVersionTable.PSVersion
   ```

2. **Capture error:**
   - Copy exact error message
   - Include last 5 lines of terminal output

3. **Simplify reproduction:**
   - Use smallest config (grid 2×2)
   - Run for just 10 timesteps
   - Use fixed-time controller

4. **Check if it's environmental:**
   - Try on different Windows user account
   - Try on different machine if possible

---

**Last resort:** Start fresh with a new virtual environment from scratch. Usually fixes mysterious import issues.

Good luck! 🚗

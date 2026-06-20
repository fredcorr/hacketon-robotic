# SO101 Robotic Arm — Hackathon Starter

This project lets you control a SO101 robotic arm through the Cyberwave Digital Twin Platform. We start in **simulation mode** (no physical hardware needed) and switch to the real arm later in the day by changing one line of code.

The code is intentionally simple: one file, clear comments, and a structure that makes it easy to drop in an AI decision loop without restructuring anything.

---

## Setup (do this once, in order)

### Step 1 — Clone the repo

```bash
git clone <your-repo-url>
cd hacketon-robotic
```

### Step 2 — Create a virtual environment

A virtual environment keeps this project's dependencies separate from everything else on your machine. Think of it as a clean sandbox.

**Mac / Linux:**
```bash
python3 -m venv venv
```

**Windows (Command Prompt):**
```bat
python -m venv venv
```

### Step 3 — Activate the virtual environment

You must do this every time you open a new terminal window for this project.

**Mac / Linux:**
```bash
source venv/bin/activate
```

**Windows (Command Prompt):**
```bat
venv\Scripts\activate.bat
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

When it's active you'll see `(venv)` at the start of your terminal prompt.

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

This reads `requirements.txt` and installs every library the project needs, at the exact versions that are pinned there.

### Step 5 — Set up your API key

```bash
# Mac / Linux
cp .env.example .env

# Windows
copy .env.example .env
```

Open the new `.env` file in any text editor and replace `your-key-here` with your real Cyberwave API key. Get it at **https://cyberwave.com/profile**.

> **Never commit `.env` to git.** It contains a secret. The `.gitignore` file already excludes it.

### Step 6 — Run the script

```bash
python main.py
```

You should see output like:
```
Connecting to SO101 arm twin in simulation mode...
Connected: <JointTwin ...>

Running test motion...
  Joint 'Rotation' moved to 0.5 rad — test motion complete.

All good! The simulation is responding to commands.
```

---

## Switching to the real robot

Find this line in `main.py`:

```python
cw.affect("simulation")
```

Change it to:

```python
cw.affect("real-world")
```

That's it. Everything else stays the same.

---

## Adding your AI loop

The code is already structured for a **Perception → Decision → Action** loop. In `main.py`, look for this comment:

```python
# --- Perception → Decision → Action loop (add your AI here) ---
```

Replace `run_test_motion(arm)` with calls to your own functions:

```python
observation = perceive(arm)   # read sensors / camera
action      = decide(observation)  # your AI / LLM call
act(arm, action)              # send the command to the arm
```

You can import `setup_arm` and `run_test_motion` from other files without any refactoring because the setup and action logic are already separated.

---

## Troubleshooting

### `pip: command not found`

Python 3 ships `pip` as a module, not always as a standalone command. Use:

```bash
python3 -m pip install -r requirements.txt
```

### `cyberwave: command not found` in the terminal

The `cyberwave` CLI tool (used for `cyberwave pair`) is a separate entry point. If it's not on your PATH, you don't need it to write or run Python code — it's only needed for the pairing workflow. You can also run it directly through the venv:

```bash
venv/bin/cyberwave pair        # Mac / Linux
venv\Scripts\cyberwave pair    # Windows
```

### macOS: permission error running scripts from Documents or Desktop

macOS restricts scripts run from `~/Documents` and `~/Desktop` when Terminal doesn't have full disk access. Fix either way:

- **Move the project** to your home folder (`~/hacketon-robotic`) where Terminal always has access.
- **Or grant Terminal access:** System Settings → Privacy & Security → Full Disk Access → enable Terminal.

### SSL error: `certificate verify failed: unable to get local issuer certificate`

Python 3.x installed from python.org on macOS doesn't link the system certificate store by default, so HTTPS requests fail. The project code already works around this automatically via `certifi`, but if you hit this error elsewhere, run the one-time fix that ships with Python:

```bash
open "/Applications/Python 3.14/Install Certificates.command"
```

A Terminal window opens, runs, and closes on its own. After that, all Python HTTPS requests on your machine work without any code changes.

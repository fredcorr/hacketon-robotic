"""
SO101 Robotic Arm — Hackathon starter script
============================================
This script connects to the SO101 arm digital twin in simulation mode
and runs one test motion to confirm everything is working.

Later in the day, swap cw.affect("simulation") → cw.affect("real-world")
to run on the real hardware without changing anything else.
"""

import os
import sys
import ssl
import certifi

# python-dotenv loads the variables from your .env file into os.environ
# so the rest of the code can read them with os.environ.get(...)
from dotenv import load_dotenv
load_dotenv()

# macOS Python 3.x doesn't link the system certificate store by default,
# so HTTPS requests fail with "certificate verify failed".
# certifi ships a trusted CA bundle; pointing these env vars at it
# fixes SSL for the Cyberwave SDK (and any other HTTPS library) without
# needing to touch system files.
os.environ.setdefault("SSL_CERT_FILE", certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())

from cyberwave import Cyberwave


# ── 1. Configuration ─────────────────────────────────────────────────────────

def get_api_key() -> str:
    """Read the API key from the environment and give a friendly error if missing."""
    key = os.environ.get("CYBERWAVE_API_KEY")
    if not key:
        print()
        print("ERROR: CYBERWAVE_API_KEY is not set.")
        print()
        print("  1. Copy .env.example to .env")
        print("     Mac/Linux:  cp .env.example .env")
        print("     Windows:    copy .env.example .env")
        print()
        print("  2. Open .env and paste your API key after the = sign.")
        print("     Get your key at: https://cyberwave.com/profile")
        print()
        sys.exit(1)   # exit cleanly — no ugly traceback
    return key


# ── 2. Setup — connect to the arm twin ───────────────────────────────────────

def setup_arm():
    """
    Create the Cyberwave client, point it at the simulation, and return the arm twin.
    Call this once at startup; pass `arm` into any function that needs to move the robot.
    """
    api_key = get_api_key()

    # Create the client — it handles authentication and communication
    cw = Cyberwave(api_key=api_key)

    # Tell the SDK to send all commands to the simulation, not the real robot.
    # Later: change "simulation" to "real-world" to drive the physical arm.
    cw.affect("simulation")

    print("Connecting to SO101 arm twin in simulation mode...")

    # Connect to the SO101 digital twin on the Cyberwave platform.
    # twin() returns a JointTwin object because SO101 is a joint-controlled arm.
    arm = cw.twin("the-robot-studio/so101")

    print(f"Connected: {arm}")
    return arm


# ── 3. Actions — everything that moves the arm goes here ─────────────────────

def run_test_motion(arm) -> None:
    """
    Move one joint to confirm the connection is working.
    This is the function you will replace / extend with your AI decision loop.
    """
    print("\nRunning test motion...")

    # set_joints() sends a position command to one or more joints.
    # - The key is the joint name (a string matching what the SDK expects).
    # - The value is the target angle in radians (0.5 rad ≈ 29°).
    # - degrees=False is the default; pass degrees=True to use degrees instead.
    arm.set_joints({"_1": 0.5})

    print("  Joint '_1' moved to 0.5 rad — test motion complete.")
    print("\nAll good! The simulation is responding to commands.")


# ── 4. Main entry point ───────────────────────────────────────────────────────
# This block only runs when you execute `python main.py` directly.
# It does NOT run when another file imports this module, which means
# you can later do `from main import setup_arm, run_test_motion` in other files.

if __name__ == "__main__":
    arm = setup_arm()

    # --- Perception → Decision → Action loop (add your AI here) ---
    # Later: replace run_test_motion with something like:
    #   observation = perceive(arm)
    #   action      = decide(observation)
    #   act(arm, action)

    run_test_motion(arm)

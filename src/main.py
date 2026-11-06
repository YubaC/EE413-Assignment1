"""
Main file for the robot connection script.

This script connects to the robot using the IP address specified in the
`ROBOT_HOST` environment variable.

Usage:
    `uv run poe robot`

Raises:
    ValueError: If the `ROBOT_HOST` environment variable is not set.
"""

import os
import subprocess

ROBOT_HOST = os.getenv("ROBOT_HOST")

if __name__ == "__main__":
    if ROBOT_HOST is None:
        raise ValueError("ROBOT_HOST environment variable is not set.")

    # Try to connect to the robot using the specified IP address
    try:
        subprocess.run(["uv", "run", "scripts/test-connection.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to connect to the robot at {ROBOT_HOST}. Error: {e}")
        raise SystemExit(1)
    else:
        print(f"Successfully connected to the robot at {ROBOT_HOST}.")

    print(f"Configured robot host: {ROBOT_HOST}")

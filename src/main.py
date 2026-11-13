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

ROBOT_HOST = os.getenv("ROBOT_HOST")

if __name__ == "__main__":
    if not ROBOT_HOST:
        raise ValueError("ROBOT_HOST environment variable is not set.")

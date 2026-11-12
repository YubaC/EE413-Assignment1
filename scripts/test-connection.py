"""
This file is used to test the connection to the UR5e robot using RTDE.
If the connection is successful, it will print the actual joint angles of the robot.

Address of the robot is specified in the `ROBOT_HOST` environment variable.
Default value is set to `192.168.77.2`.

Usage:
    `uv run scripts/test-connection.py`
"""

import os

import rtde_receive

ROBOT_IP_ADDRESS = os.getenv("ROBOT_HOST") or "192.168.77.2"

# Establish a connection to the UR5e robot
print("Connecting to UR5e...")
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP_ADDRESS)
print("Connected successfully!")

# Get the actual joint angles of the robot
joints = rtde_r.getActualQ()
print("Joint angles [rad]:")
print(joints)

rtde_r.disconnect()

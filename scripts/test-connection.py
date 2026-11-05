"""
This file is used to test the connection to the UR5e robot using RTDE.

Usage:
    `uv run scripts/test-connection.py`
"""

import rtde_receive

ROBOT_IP_ADDRESS = "192.168.77.2"

# Establish a connection to the UR5e robot
print("Connecting to UR5e...")
rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP_ADDRESS)
print("Connected successfully!")

# Get the actual joint angles of the robot
joints = rtde_r.getActualQ()
print("Joint angles [rad]:")
print(joints)

rtde_r.disconnect()

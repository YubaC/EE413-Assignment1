import os
from typing import Optional

import rtde_control
import rtde_io
import rtde_receive
from dashboard_client import DashboardClient

from .gripper import Gripper

ROBOT_HOST = os.getenv("ROBOT_HOST")


class _Robot:
    """
    A robot controller class that manages the connection to the UR5e robot.

    This class provides methods to connect and disconnect from the robot, as well as
    access to the robot's control, receive, IO, and dashboard interfaces. It also
    provides a gripper controller for opening and closing the gripper.

    Raises:
        ValueError: If the `ROBOT_HOST` environment variable is not set.
        RuntimeError: If the robot connection fails or if any of the robot
            interfaces fail to connect or if the robot is not connected when
            attempting to use the gripper or other interfaces.
    """

    _instance: Optional["_Robot"] = None
    connected: bool = False
    control: rtde_control.RTDEControlInterface
    receive: rtde_receive.RTDEReceiveInterface
    dashboard: DashboardClient
    io: rtde_io.RTDEIOInterface
    gripper: Gripper

    def __init__(self):
        if not ROBOT_HOST:
            raise ValueError("ROBOT_HOST environment variable is not set.")

        self.connect()

    def connect(self):
        """
        Connect to the UR5e robot and initialize the control, receive, IO,
        and dashboard interfaces.

        Raises:
            RuntimeError: If failed to connect to robot or any of the robot
                interfaces fail to connect.
        """
        try:
            self.control = rtde_control.RTDEControlInterface(ROBOT_HOST)
            self.receive = rtde_receive.RTDEReceiveInterface(ROBOT_HOST)
            self.io = rtde_io.RTDEIOInterface(ROBOT_HOST)
            self.dashboard = DashboardClient(ROBOT_HOST)
            self.dashboard.connect(5000)

            # Check if all interfaces are connected
            all_connected = (
                self.control.isConnected()
                and self.receive.isConnected()
                and self.io.isConnected()
                and self.dashboard.isConnected()
            )

            if not all_connected:
                raise RuntimeError("Failed to connect to one or more robot interfaces.")

        except Exception as e:
            self.disconnect()
            raise RuntimeError("Failed to connect to robot") from e

        self.gripper = Gripper(self)
        self.connected = True

    def disconnect(self):
        """
        Disconnect from the UR5e robot and clean up the control, receive, IO,
        and dashboard interfaces.
        """
        for name in ("control", "receive", "io", "dashboard"):
            interface = getattr(self, name, None)
            if interface is not None:
                interface.disconnect()

        self.connected = False


ROBOT = _Robot()

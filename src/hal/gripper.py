"""
Gripper HAL module.

This file is part of the HAL (Hardware Abstraction Layer) module for
controlling the gripper on the robot. It provides a simple interface
to open and close the gripper using URP programs on the robot dashboard.

Classes:
    Gripper: A gripper controller class.

The robot instance is injected into the gripper so it can use the existing
dashboard connection.
"""

from __future__ import annotations

import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .robot import _Robot


GRIPPER_ACTUATION_TIME = 1.0
GRIPPER_PROGRAM_TIMEOUT = 15.0


class Gripper:
    """
    A gripper controller class.

    The Gripper class provides methods to open and close the gripper using
    URP programs on the robot dashboard. It requires an existing robot
    connection to function properly.

    Raises:
        RuntimeError: If the robot is not connected or if the gripper program fails to run.
        TimeoutError: If the gripper program does not finish within the expected time.
    """

    def __init__(self, robot: _Robot):
        """Create a gripper controller using an existing robot connection."""
        self._robot = robot

    def _run(self, program_name: str) -> None:
        """
        Run a gripper program on the robot.

        Args:
            program_name (str): The name of the URP program to run (e.g., "OpenRG2.urp" or "CloseRG2.urp").

        Raises:
            RuntimeError: If the robot is not connected or if the program fails to run.
            TimeoutError: If the program does not finish within the expected time.
        """

        if not self._robot.connected:
            raise RuntimeError("Robot is not connected. Cannot run gripper program.")

        # The caller must finish all arm motion before switching programs.
        self._robot.control.stopScript()
        self._wait_until_stopped()
        self._robot.dashboard.loadURP(program_name)
        self._robot.dashboard.play()

        time.sleep(GRIPPER_ACTUATION_TIME)

        self._wait_until_stopped()
        self._restore_control()

    def _wait_until_stopped(self) -> None:
        """
        Waits until the current program is stopped.

        Raises:
            RuntimeError: If the program state is unexpected.
            TimeoutError: If the program does not stop within the expected time.
        """

        deadline = time.monotonic() + GRIPPER_PROGRAM_TIMEOUT

        # Wait for the program to stop
        while True:
            state = self._robot.dashboard.programState().strip()
            if state.startswith("STOPPED"):
                break
            if not state.startswith("PLAYING"):
                raise RuntimeError(f"Unexpected gripper program state: {state}")
            if time.monotonic() >= deadline:
                raise TimeoutError("Gripper program still running; RTDE not restored.")
            time.sleep(0.01)

    def _restore_control(self) -> None:
        """
        Restore the RTDE control script after the gripper program finishes.

        Raises:
            RuntimeError: If the dashboard program is not stopped or the RTDE
                control script cannot be uploaded.
            TimeoutError: If the RTDE control script does not start within
                five seconds.
        """

        control = self._robot.control
        dashboard = self._robot.dashboard

        state = dashboard.programState().strip()
        if not state.startswith("STOPPED"):
            raise RuntimeError(f"Cannot restore RTDE while program state is: {state}")

        if not control.reuploadScript():
            raise RuntimeError("Failed to upload RTDE control script.")

        deadline = time.monotonic() + 5.0
        while not control.isProgramRunning():
            if time.monotonic() >= deadline:
                raise TimeoutError("RTDE control script did not start.")
            time.sleep(0.1)

    def open(self) -> None:
        """
        Open the gripper.
        """

        self._run("OpenRG2.urp")

    def close(self) -> None:
        """
        Close the gripper.
        """

        self._run("CloseRG2.urp")

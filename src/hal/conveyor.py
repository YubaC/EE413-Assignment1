"""
Conveyor HAL module.

This file is part of the HAL (Hardware Abstraction Layer) module for
controlling the conveyors in the system. It provides a simple interface
to start and stop the conveyors using the robot's digital outputs.

Classes:
    _Conveyor: A conveyor controller class.

The robot instance is injected into the conveyor so it can use the existing
dashboard connection.
"""

from .robot import ROBOT


class _Conveyor:
    """
    A conveyor controller class.

    The _Conveyor class provides methods to start and stop a conveyor using
    the robot's digital outputs. Each conveyor is identified by an ID (0 or 1).

    Raises:
        ValueError: If the conveyor ID is not 0 or 1.
        RuntimeError: If the robot is not connected when attempting to start or
            stop the conveyor.
    """

    id: int

    def __init__(self, id: int) -> None:
        if id not in (0, 1):
            raise ValueError(f"Invalid conveyor id: {id}. Must be 0 or 1.")

        self.id = id

    def start(self) -> None:
        """
        Start the conveyor.

        Raises:
            RuntimeError: If the robot is not connected.
        """

        if not ROBOT.connected:
            raise RuntimeError("Robot is not connected. Cannot start conveyor.")

        assert ROBOT.io is not None
        ROBOT.io.setStandardDigitalOut(self.id, True)

    def stop(self) -> None:
        """
        Stops the conveyor.

        Raises:
            RuntimeError:  If the robot is not connected.
        """

        if not ROBOT.connected:
            raise RuntimeError("Robot is not connected. Cannot stop conveyor.")

        assert ROBOT.io is not None
        ROBOT.io.setStandardDigitalOut(self.id, False)


CONVEYOR_X = _Conveyor(0)  # Conveyor in X direction
CONVEYOR_Y = _Conveyor(1)  # Conveyor in Y direction

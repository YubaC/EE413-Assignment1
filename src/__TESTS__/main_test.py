"""
This file contains unit tests for the `main.py` module.
"""

import runpy
from pathlib import Path

import pytest


def test_main_requires_robot_host(monkeypatch):
    """
    main() should throw a ValueError if the `ROBOT_HOST` environment variable
    is not set.

    Args:
        monkeypatch (pytest.MonkeyPatch): A pytest fixture that allows to
        modify environment variables.
    """

    monkeypatch.delenv("ROBOT_HOST", raising=False)
    main_path = Path(__file__).resolve().parents[1] / "main.py"

    with pytest.raises(
        ValueError, match=r"^ROBOT_HOST environment variable is not set\.$"
    ):
        runpy.run_path(str(main_path), run_name="__main__")

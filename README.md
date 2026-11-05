# EE413 Assignment 1

## Requirements

- uv

## Environment Setup

run the following command to install dependencies:

```sh
uv sync --locked --managed-python
uv run --locked python --version
```

To connect to the robot, after connecting the computer to the robot via Ethernet, configure the network card with the following settings:

- IP address: `192.168.77.1`
- Subnet mask: `255.255.255.0`

To have a quick test of the connection, run the following command:

```sh
uv run scripts/test-connection.py
```

## Commands

- `uv run poe format` - Format the code using `ruff`.
- `uv run poe lint` - Lint the code using `ruff`.

**Note: Please make sure to run the above commands before committing the code to ensure that the code is properly formatted and linted.**

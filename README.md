# EE413 Assignment 1

## Requirements

- `uv`
- Docker Desktop with Docker Compose (required for simulation only)

Run all commands from the repository root.

## Environment Setup

### Python environment

Install the project dependencies and check the Python version.

```sh
uv sync --locked --managed-python
uv run --locked python --version
```

### Physical robot network

1. Connect your computer to the UR5e controller via Ethernet.

2. Configure your computer’s **wired network adapter** with IP address `192.168.77.1` and subnet mask `255.255.255.0`.

The robot controller’s address is `192.168.77.2`.

### Simulation environment

Open Docker Desktop and wait for the Docker engine to start. The repository includes the Compose configuration for URSim.

## Usage

Both commands below run the same main program.

### Run against the physical robot

Power on the UR5e, confirm the Ethernet connection, and select **Remote Control** on the teach pendant. Then run the program.

```sh
uv run poe robot
```

For a standalone connection check, run `uv run scripts/test-connection.py`. It uses `192.168.77.2` by default.

### Run against URSim (simulation)

1. Start URSim in the background. This will take a few minutes to download the image and start the container for the first time.

   ```sh
   uv run poe sim-up
   ```

2. Open the [simulated teach pendant](http://127.0.0.1:6080/vnc.html) and follow the prompts to initialize and start the simulated robot.

3. Run the program against the local simulator.

   ```sh
   uv run poe sim
   ```

4. When finished, stop URSim.

   ```sh
   uv run poe sim-down
   ```

## Contributing

Before committing, format and lint the Python code with Ruff.

```sh
uv run poe format
uv run poe lint
uv run poe test
```

### Tests

Place each test file in a `__TESTS__/` subdirectory of the directory containing the code it tests. For example, tests for `src/main.py` go in `src/__TESTS__/main_test.py`.

Name test files `*_test.py` so pytest can discover them. Run the test suite from the repository root.

## Command Reference

- `uv run poe format` - Format the Python code with Ruff.
- `uv run poe lint` - Lint the Python code with Ruff.
- `uv run poe test` - Run the unit tests with pytest.
- `uv run poe robot` - Run the main program against the physical robot.
- `uv run poe sim` - Run the main program against URSim.
- `uv run poe sim-up` - Start URSim in the background.
- `uv run poe sim-down` - Stop URSim.

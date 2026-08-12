pulse -- Experiment 001 probe harness
=======================================

What this is: a minimal runner for the two confirmed probes
(probe_storage_write, probe_settings_persist) against one adb-connected
Android device, with run-over-run comparison (NEW/UNCHANGED/CHANGED/
NO_COMPARISON) persisted to a local JSON history file.

See ../README.txt and ../RESEARCH.txt for the research question,
hypothesis, and per-probe justification. This file only covers running
the code.

DEPENDENCIES
------------
Runtime: none beyond the Python standard library.
Dev/test: pytest (see pyproject.toml).
Transport: the system `adb` binary must be on PATH, and a device must
already be connected (`adb devices` shows it) -- this package does not
manage pairing/connecting itself.

SETUP
-----
    cd pulse
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"

RUN THE PROBES
---------------
    pulse-run --serial <serial-as-shown-by-adb-devices>

    # example:
    pulse-run --serial 10.161.62.188:40139

Each run prints one JSON line per probe result and appends to
pulse_history.json (in the current directory by default; override with
--history <path>) so the next run can report NEW/UNCHANGED/CHANGED for
the same assumption.

RUN THE TESTS
--------------
    pytest

Tests in test_store.py are pure logic and need no device. Tests in
test_probes_live.py run the actual probes against a connected device
(including one deliberately-triggered FAIL case) and are skipped
automatically if `adb devices` shows nothing connected.

"""Shared test fixtures.

`adb devices` (device listing only, no shell command against the device)
is used here purely to let live-device tests skip cleanly when nothing is
connected, rather than fail with a confusing transport error. It reads no
device state and is not one of the two confirmed probes' own commands, but
it's the minimum plumbing needed to run them conditionally, not a probe of
its own.
"""

from __future__ import annotations

import subprocess

import pytest


def _connected_serials() -> list[str]:
    try:
        proc = subprocess.run(
            ["adb", "devices"], capture_output=True, text=True, timeout=10
        )
    except (subprocess.TimeoutExpired, OSError):
        return []
    lines = proc.stdout.strip().splitlines()[1:]  # skip "List of devices attached"
    return [line.split()[0] for line in lines if line.strip().endswith("device")]


@pytest.fixture(scope="session")
def device_serial() -> str:
    serials = _connected_serials()
    if not serials:
        pytest.skip("no adb device connected -- skipping live-device tests")
    return serials[0]

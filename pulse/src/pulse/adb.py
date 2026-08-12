"""Minimal adb transport wrapper. The only transport this project uses
(entropy budget: transport = 1, adb). Shells out to the system `adb`
binary rather than reimplementing the protocol.
"""

from __future__ import annotations

import shlex
import subprocess
from dataclasses import dataclass


class AdbTransportError(Exception):
    """adb itself failed to run or respond -- not a probe-level FAIL.

    Callers must map this to Observation.UNKNOWN, never Observation.FAIL:
    a transport error tells you nothing about whether the assumption under
    test holds.
    """


@dataclass(frozen=True)
class ShellResult:
    returncode: int
    stdout: str
    stderr: str


class AdbShell:
    """One adb-connected device, addressed by its serial (as shown by
    `adb devices`). Every probe interacts with the device only through
    this wrapper's `run` method -- there is no other adb entrypoint in
    this package, so every device-touching command a probe issues is
    visible here.
    """

    def __init__(self, serial: str, timeout_seconds: float = 10.0) -> None:
        self.serial = serial
        self.timeout_seconds = timeout_seconds

    def run(self, shell_command: str) -> ShellResult:
        """Run `shell_command` inside `adb shell` on this device and
        return its result. Never raises for a non-zero exit from the
        command itself -- that is data for the probe to interpret. Raises
        AdbTransportError only when adb/the transport itself fails.
        """
        argv = ["adb", "-s", self.serial, "shell", shell_command]
        try:
            proc = subprocess.run(
                argv,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
            )
        except (subprocess.TimeoutExpired, OSError) as exc:
            raise AdbTransportError(f"{argv!r} failed: {exc}") from exc
        return ShellResult(proc.returncode, proc.stdout, proc.stderr)


def quote(value: str) -> str:
    """Shell-quote a value being interpolated into an adb shell command
    string, so probe-authored content can't be reinterpreted as extra
    shell syntax."""
    return shlex.quote(value)

"""The two probes confirmed in RESEARCH.txt. Each probe touches only its
own throwaway marker file or its own inert settings key -- never any
pre-existing data on the device -- and cleans up after itself regardless
of outcome, per this project's device access scope.
"""

from __future__ import annotations

from .adb import AdbShell, AdbTransportError, quote
from .model import Observation, ProbeResult, now_iso

DEFAULT_STORAGE_PATH = "/sdcard/pulse_probe_test"
STORAGE_MARKER_CONTENT = "pulse-probe"

DEFAULT_SETTINGS_NAMESPACE = "global"
DEFAULT_SETTINGS_KEY = "pulse_probe_test_key"
SETTINGS_MARKER_VALUE = "pulse-probe"


def probe_storage_write(
    shell: AdbShell, path: str = DEFAULT_STORAGE_PATH
) -> ProbeResult:
    """Assumption: a file can be written to and read back from `path` via
    adb shell, right now, on this device.

    `path` is parameterizable so tests can point it at a deliberately
    unwritable location (e.g. under /system) to confirm this probe can
    actually detect FAIL, not just always report PASS.
    """
    assumption = "storage_write"
    quoted_path = quote(path)
    try:
        # Best-effort pre-clean of our own marker path only; ignore its
        # result (it legitimately fails if the path never existed).
        shell.run(f"rm -f {quoted_path}")

        write = shell.run(f"echo {quote(STORAGE_MARKER_CONTENT)} > {quoted_path}")
        if write.returncode != 0:
            return ProbeResult(
                assumption,
                Observation.FAIL,
                f"write failed (exit {write.returncode}): {write.stderr.strip()}",
                now_iso(),
            )

        read = shell.run(f"cat {quoted_path}")
        shell.run(f"rm -f {quoted_path}")  # cleanup regardless of read outcome

        if read.returncode != 0:
            return ProbeResult(
                assumption,
                Observation.FAIL,
                f"read-back failed (exit {read.returncode}): {read.stderr.strip()}",
                now_iso(),
            )

        observed = read.stdout.strip()
        if observed == STORAGE_MARKER_CONTENT:
            return ProbeResult(
                assumption, Observation.PASS, "write+read-back matched", now_iso()
            )
        return ProbeResult(
            assumption,
            Observation.FAIL,
            f"content mismatch: wrote {STORAGE_MARKER_CONTENT!r}, read back {observed!r}",
            now_iso(),
        )
    except AdbTransportError as exc:
        return ProbeResult(
            assumption, Observation.UNKNOWN, f"adb transport error: {exc}", now_iso()
        )


def probe_settings_persist(
    shell: AdbShell,
    namespace: str = DEFAULT_SETTINGS_NAMESPACE,
    key: str = DEFAULT_SETTINGS_KEY,
    skip_write: bool = False,
) -> ProbeResult:
    """Assumption: a value written to the Settings provider via adb shell
    persists unchanged when read back immediately after.

    `namespace`/`key` are parameterizable, and `skip_write` lets a test
    deliberately read a key that was never written (expected: FAIL, since
    the read-back can't match a value that was never set) to confirm this
    probe can actually detect FAIL.
    """
    assumption = "settings_persist"
    try:
        if not skip_write:
            put = shell.run(
                f"settings put {namespace} {key} {quote(SETTINGS_MARKER_VALUE)}"
            )
            if put.returncode != 0:
                return ProbeResult(
                    assumption,
                    Observation.FAIL,
                    f"settings put failed (exit {put.returncode}): {put.stderr.strip()}",
                    now_iso(),
                )

        get = shell.run(f"settings get {namespace} {key}")
        shell.run(f"settings delete {namespace} {key}")  # cleanup regardless

        if get.returncode != 0:
            return ProbeResult(
                assumption,
                Observation.FAIL,
                f"settings get failed (exit {get.returncode}): {get.stderr.strip()}",
                now_iso(),
            )

        observed = get.stdout.strip()
        if observed == SETTINGS_MARKER_VALUE:
            return ProbeResult(
                assumption, Observation.PASS, "put+get matched", now_iso()
            )
        return ProbeResult(
            assumption,
            Observation.FAIL,
            f"value mismatch: wrote {SETTINGS_MARKER_VALUE!r}, read back {observed!r}",
            now_iso(),
        )
    except AdbTransportError as exc:
        return ProbeResult(
            assumption, Observation.UNKNOWN, f"adb transport error: {exc}", now_iso()
        )


ALL_PROBES = (probe_storage_write, probe_settings_persist)

"""Live-device tests: the two confirmed probes run for real, plus
deliberately-triggered FAIL cases (brief's TESTS requirement) to confirm
each probe can actually detect a failure and doesn't just always report
PASS by construction.

Every adb command used here is one of the two probes' own commands
(write/read/delete a throwaway marker file; put/get/delete an inert
settings key), the FAIL-case variant of the storage probe pointed at a
path expected to be unwritable, or the FAIL-case variant of the settings
probe reading a key that was deliberately never written -- nothing else
on the device is touched, per this project's device access scope.
"""

from pulse.adb import AdbShell
from pulse.model import Observation
from pulse.probes import probe_settings_persist, probe_storage_write


def test_storage_write_probe_passes_on_normal_path(device_serial):
    shell = AdbShell(device_serial)
    result = probe_storage_write(shell)
    assert result.observation is Observation.PASS, result.detail


def test_settings_persist_probe_passes_on_normal_key(device_serial):
    shell = AdbShell(device_serial)
    result = probe_settings_persist(shell)
    assert result.observation is Observation.PASS, result.detail


def test_storage_write_probe_detects_deliberate_failure(device_serial):
    """Deliberately-triggered FAIL case: /system is not writable by the
    adb shell user on a normal, non-rooted build, so this must FAIL --
    proving the probe can distinguish FAIL from PASS rather than always
    reporting PASS regardless of what actually happened.
    """
    shell = AdbShell(device_serial)
    result = probe_storage_write(shell, path="/system/pulse_probe_test_should_fail")
    assert result.observation is Observation.FAIL, (
        "expected FAIL for a deliberately unwritable path -- if this is "
        f"PASS instead, the probe isn't actually detecting failure: {result.detail}"
    )


def test_settings_persist_probe_detects_deliberate_failure(device_serial):
    """Deliberately-triggered FAIL case: read a key that was never
    written (skip_write=True). The read-back cannot match the expected
    marker value, so this must FAIL -- closes the gap noted in
    RESEARCH.txt Section 8 (R1 report), where this case existed in code
    but had not actually been exercised against a live device.
    """
    shell = AdbShell(device_serial)
    result = probe_settings_persist(
        shell, key="pulse_probe_test_key_never_written", skip_write=True
    )
    assert result.observation is Observation.FAIL, (
        "expected FAIL when reading a key that was never written -- if "
        f"this is PASS instead, the probe isn't actually detecting failure: {result.detail}"
    )

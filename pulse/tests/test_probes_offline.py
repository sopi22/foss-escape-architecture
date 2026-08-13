"""Offline regression test for the detail-string bug found by Autopsy
Experiment #001 (see ../../autopsy_experiment_001_findings.txt): the
settings_persist probe's mismatch message must not claim a write
happened when skip_write=True skipped it. Uses a fake shell so this
runs without a live device -- the live-device suite covers real
behavior, this covers the probe's own reporting logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pulse.model import Observation
from pulse.probes import probe_settings_persist


@dataclass
class _FakeShellResult:
    returncode: int
    stdout: str
    stderr: str


@dataclass
class _FakeShell:
    commands: list[str] = field(default_factory=list)

    def run(self, shell_command: str) -> _FakeShellResult:
        self.commands.append(shell_command)
        if shell_command.startswith("settings get"):
            return _FakeShellResult(0, "null\n", "")
        return _FakeShellResult(0, "", "")


def test_settings_persist_skip_write_detail_string_is_accurate():
    shell = _FakeShell()
    result = probe_settings_persist(
        shell, key="pulse_probe_test_key_never_written", skip_write=True
    )

    assert result.observation is Observation.FAIL
    assert "no write attempted" in result.detail
    assert "wrote 'pulse-probe'" not in result.detail
    assert not any(cmd.startswith("settings put") for cmd in shell.commands)


def test_settings_persist_normal_mismatch_still_says_wrote():
    shell = _FakeShell()
    result = probe_settings_persist(shell, key="pulse_probe_test_key")

    assert result.observation is Observation.FAIL
    assert "wrote 'pulse-probe'" in result.detail

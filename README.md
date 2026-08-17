# PULSE — Experiment 001

## RESEARCH QUESTION
Can a meaningful subset of software/environment compatibility failures be
represented as explicit, falsifiable operating assumptions whose state is
observable through safe behavioral probes and compared over time — in a
way that tells you something conventional environment metadata (getprop,
dumpsys, pm) does not already tell you?

## HYPOTHESIS
H1 (research hypothesis): yes — a meaningful subset can be represented and
  observed this way.
H0 (null hypothesis): no — behavioral probing adds nothing materially
  useful beyond conventional metadata for the failures tested.

A result supporting H0 is a complete, successful experiment, not a failed
one. See RESEARCH.md for the full falsification criteria, baseline
methodology, and what would change my mind (stated in advance).

## NON-GOALS
This is explicitly NOT: a signing/PKI system, a reproducible-build
verifier, a dependency-risk scorer, a source archival tool, a
permission manager, an app store, a capability/provider abstraction, a
cost model, a daemon, a network service, or a background process. If any
of these appears to be needed, that is a stop-and-flag condition, not
something to build.

## CURRENT PHASE
Phase 1 CLOSED — both confirmed probes are implemented and have been
reproduced across four sessions (R4) and three device identities: a real
Samsung Galaxy A53 (Android 16/API 36, R1/R2), a Google emulator (AVD,
Android 14/API 34, R3), and a real Samsung Galaxy A54 (Android 16/API 36,
R4), including both probes' deliberate FAIL-detection cases on all three.
See RESEARCH.md Section 8 for the falsification report; conclusion is
SUPPORTED, with a named residual limitation — no run has yet used a
second vendor's shipped OEM skin on physical hardware (the emulator is a
reference "google_apis" image, and R4's A54 is a second Samsung model,
same OEM as R1/R2 — it added evidence but did not close this gap).

That limitation is logged as an OPEN, NOT-SCHEDULED item — a second
Android device that is both a different OEM *and* a physical device
(not a reference-image emulator, and not another Samsung model) would
close it, but none is available right now, it is not being actively
sourced, and it is not required for Experiment 001 to be considered
complete. See RESEARCH.md Section 8's recommended next experiment for
the exact status. No other items are
pending on this phase.

## SETUP / RUN
See pulse/README.md for exact, copy-pasteable setup and run commands.
Short version:
    cd pulse
    python3 -m venv .venv && source .venv/bin/activate
    pip install -e ".[dev]"
    pytest                                    # run the test suite
    pulse-run --serial <serial-from-adb-devices>   # run the probes

## AUTHOR
Jhoana Sophia Munar (jhosophie@proton.me)

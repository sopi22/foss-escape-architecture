PULSE — Experiment 001
=======================

RESEARCH QUESTION
------------------
Can a meaningful subset of software/environment compatibility failures be
represented as explicit, falsifiable operating assumptions whose state is
observable through safe behavioral probes and compared over time — in a
way that tells you something conventional environment metadata (getprop,
dumpsys, pm) does not already tell you?

HYPOTHESIS
----------
H1 (research hypothesis): yes — a meaningful subset can be represented and
  observed this way.
H0 (null hypothesis): no — behavioral probing adds nothing materially
  useful beyond conventional metadata for the failures tested.

A result supporting H0 is a complete, successful experiment, not a failed
one. See RESEARCH.txt for the full falsification criteria, baseline
methodology, and what would change our mind (stated in advance).

NON-GOALS
---------
This is explicitly NOT: a signing/PKI system, a reproducible-build
verifier, a dependency-risk scorer, a source archival tool, a
permission manager, an app store, a capability/provider abstraction, a
cost model, a daemon, a network service, or a background process. If any
of these appears to be needed, that is a stop-and-flag condition, not
something to build.

CURRENT PHASE
--------------
Phase 1 complete — both confirmed probes are implemented and have now
been reproduced across three sessions (R3) and two device identities: a
real Samsung Galaxy A53 (Android 16/API 36, R1/R2) and a Google emulator
(AVD, Android 14/API 34, R3), including both probes' deliberate
FAIL-detection cases on both devices. See RESEARCH.txt Section 8 for the
falsification report; conclusion is SUPPORTED, with a named residual
limitation — the emulator is a reference "google_apis" image, not a
second vendor's shipped OEM skin, so that specific gap is not yet closed.

What would close the remaining gap: a second Android device that is both
a different OEM *and* a physical device (not a reference-image emulator).
None is available in this environment yet; see RESEARCH.txt Section 8's
recommended next experiment.

SETUP / RUN
------------
See pulse/README.txt for exact, copy-pasteable setup and run commands.
Short version:
    cd pulse
    python3 -m venv .venv && source .venv/bin/activate
    pip install -e ".[dev]"
    pytest                                    # run the test suite
    pulse-run --serial <serial-from-adb-devices>   # run the probes

AUTHOR
------
Jhoana Sophia Munar (jhosophie@proton.me)

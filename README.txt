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
Phase 1 complete — both confirmed probes are implemented and have been
run against a real device (Samsung Galaxy A53, Android 16/API 36), with
a falsification report recorded from those actual runs. See RESEARCH.txt
Section 8 for the report; conclusion so far is WEAKLY SUPPORTED at R1
reproducibility (one device, one session) — see Section 7 for what R2/R3
would require and Section 8's recommended next experiment.

What unlocks the next phase: a second, genuinely separate-session run
(R2), and ideally a second device of a different make (R3) — neither has
happened yet, so no claim beyond R1 is made anywhere in this project.

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

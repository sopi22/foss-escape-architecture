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
Phase 0 — clarification gate and probe proposal only. No implementation
code exists yet. See RESEARCH.txt for the full novelty-firewall analysis,
hypothesis framing, and the two proposed probes (probe_storage_write,
probe_settings_persist) with their justification.

What unlocks Phase 1 (implementation): explicit operator confirmation of
the probe selection in RESEARCH.txt, per this experiment's brief
("wait for my confirmation before proceeding to implementation").

Phase 1 also needs an actual Android target to run probes against — this
is now resolved: a physical device (Samsung Galaxy A53, Android 16) is
reachable over adb via Wireless debugging. See RESEARCH.txt, Section 6,
for connection details and the one caveat (the WiFi adb session may need
reconnecting in a future terminal session).

SETUP / RUN
------------
Not applicable yet — no implementation exists. This section will be
replaced with exact, copy-pasteable setup and run commands once Phase 1
begins.

AUTHOR
------
Jhoana Sophia Munar (jhosophie@proton.me)

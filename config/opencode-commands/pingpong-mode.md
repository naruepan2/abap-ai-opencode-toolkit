---
description: Pingpong mode — short alias that starts an unattended SAP ABAP delivery run
agent: abap-auto-delivery-by-pongg
---
Invoke the `auto-abap-delivery` skill with: start-unattended $ARGUMENTS

This is a pure forwarder to the existing `start-unattended` token — not a second mode.
Spec, plan, qualification, interaction policy and Autonomy Envelope still require approval
before any SAP write; the workflow still stops at `READY_FOR_UAT`. Never duplicate delivery
rules here; keep them in `auto-abap-delivery/SKILL.md` and its references.

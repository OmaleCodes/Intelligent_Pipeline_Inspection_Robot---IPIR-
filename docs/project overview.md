# IPIR — Project Overview

## The problem

Pipeline infrastructure inspection is traditionally manual — someone has to
physically walk, crawl, or scope a pipeline section to spot cracks, rust,
and structural defects before they become failures. It's slow, it doesn't
scale, and small early-stage defects are easy for a human to miss,
especially in low-visibility or hard-to-reach sections. This became clear
firsthand during my internship, seeing how much of pipeline maintenance
still depends on manual visual checks.

## The solution

IPIR (Intelligent Pipeline Inspection Robot) is a computer-vision-based
system that inspects pipe sections, automatically flags visual defects
(cracks and rust) using classical image processing, logs every detection
with its location and timestamp, and displays everything on a live
operator dashboard. The long-term goal is a physical robot that drives
through pipe sections autonomously; the current build proves out the full
detection-to-dashboard pipeline in software first.

## Current status

This is an active, in-progress build — not a finished product, and this
README won't pretend otherwise:

- **Working today:** camera capture, image preprocessing, defect detection
  (edge-based crack detection, color-based rust detection), SQLite logging,
  and a live Streamlit dashboard showing defect counts and trends across
  inspection runs.
- **In progress:** a small hardware prototype (budget-constrained, sourced
  via AliExpress) to move from webcam-on-a-desk to an actual mobile camera
  platform.
- **Designed but paused:** an AI classifier (Roboflow-hosted model) to give
  a second opinion on detected defects; a diameter-measurement module that's
  intentionally stubbed out until depth/IR sensor hardware is available.

See `docs/Architecture.md` for the full technical breakdown of what's built
versus what's still aspirational, and `project_roadmap.md` for the
day-to-day build log.

## Who this is for

Built with pipeline maintenance operators and inspection teams in mind —
anyone who currently relies on slow, manual visual inspection and could
benefit from an automated first pass that flags likely defects for human
review. It's also my main capstone/internship project and the subject of a
30-day public build series, documenting the process of learning computer
vision, embedded systems, and full-stack Python development from the ground
up.
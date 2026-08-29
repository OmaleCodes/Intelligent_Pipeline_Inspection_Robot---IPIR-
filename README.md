# IPIR — Intelligent Pipeline Inspection Robot

A computer-vision-based system that inspects pipe sections, automatically
flags visual defects (cracks, rust, and more), logs every detection, and
displays everything on a live operator dashboard.

Built as part of an internship capstone at NGIC (Nigeria Gas
Infrastructure Company), and documented daily as part of a **30 Days of
Code** build-in-public challenge.

> **Status: active, in-progress build.** This is not a finished product —
> see [`docs/Architecture.md`](docs/Architecture.md) for exactly what's
> working today versus what's still aspirational.

---

## What it does

- Captures live video from a camera (webcam today; ESP32-CAM planned for
  the mini hardware prototype)
- Detects likely defects using classical computer vision — Canny edge
  detection for cracks, HSV color thresholding for rust
- Sends each detected region to a custom-trained AI model (RF-DETR,
  trained on Roboflow) as a **second opinion**, never a hard filter —
  the original detection is always logged regardless of what the model
  says
- Logs every detection (type, location, timestamp, and the AI's second
  opinion when available) to a SQLite database
- Displays defect counts, trends across inspection runs, and a live
  table on a Streamlit dashboard

## Current pipeline

```
Camera → Preprocessing (CLAHE + HSV) → Defect Detection (Canny + rust mask)
       → AI second opinion (Roboflow RF-DETR, throttled)
       → SQLite logging → Live dashboard
```

## Tech stack

- **Vision:** Python, OpenCV
- **AI:** Roboflow-hosted RF-DETR model, custom-trained on a public pipe
  defects dataset
- **Database:** SQLite
- **Dashboard:** Streamlit, Pandas
- **Testing:** Pytest

## Getting started

Requires Python 3.12 (not 3.13+ — `inference-sdk` doesn't yet support
newer Python versions).

```bash
git clone https://github.com/OmaleCodes/Intelligent_Pipeline_Inspection_Robot---IPIR-.git
cd Intelligent_Pipeline_Inspection_Robot---IPIR-
pip install -r requirements.txt
```

Create a `.env` file in the project root with your own Roboflow API key:
```
ROBOFLOW_API_KEY=your_key_here
```

Run the live pipeline:
```bash
python3 kratos.py
```

Run the dashboard:
```bash
streamlit run dashboard/pages.py
```

Populate the dashboard with fake data (useful for testing without a
camera):
```bash
python3 seed_test_data.py
```

## Project structure

```
kratos.py              # main orchestrator — camera to detection to logging
vision/                 # camera capture, preprocessing, defect detection,
                        #   distance estimation, diameter placeholder
ai/                     # Roboflow classifier — second opinion on defects
database/               # SQLite models and queries
dashboard/              # Streamlit pages and charts
docs/                   # architecture, roadmap, research notes
tests/                  # pytest test suite
```

## Documentation

- [`docs/Architecture.md`](docs/Architecture.md) — full system
  architecture: long-term vision vs. current implementation vs.
  in-progress hardware decisions
- [`docs/project overview.md`](docs/project%20overview.md) — the problem,
  the solution, who it's for
- [`project_roadmap.md`](project_roadmap.md) — day-to-day build log
- [`docs/Ideas.md`](docs/Ideas.md) — backlog and future features
- [`docs/Research.md`](docs/Research.md) — notes and reasoning behind key
  technical decisions

## Known limitations (being upfront about these)

- `vision/diameter.py` is an intentional placeholder — no IR/depth
  sensor hardware exists yet, so it honestly returns `is_estimated:
  False` rather than faking a number
- The AI classifier's accuracy varies by defect class (measured at
  training time: crack 51%, hole 65%, rupture 87%) — treated as a
  second opinion precisely because of this, never as ground truth
- No physical robot yet — a mini ESP32-CAM-based prototype is in
  progress, budget-constrained

## Author

PHILIP MOSES OMALE  — Electrical & Electronics Engineering student,
Air Force Institute of Technology, Kaduna, Nigeria.
# Intelligent Pipeline Inspection Robot (IPIR)

A real-time computer vision system for detecting pipe defects — cracks and rust — built for autonomous gas pipeline inspection. Live camera feed → preprocessing → defect detection → SQLite logging → Streamlit operator dashboard.

Built in public as part of a **30 Days of Code** challenge, documenting daily progress from a first working prototype toward a deployable inspection system.

---

## Why this project

During an internship at a gas infrastructure company, I saw first-hand how pipeline inspection, maintenance, and commissioning are done on the ground — and how much of it still depends on manual visual checks. IPIR is my attempt to combine that industry exposure with what I'm learning in embedded systems and computer vision: a robot that can traverse a pipeline and flag defects automatically, logging every inspection for review.

## How it works

```
CameraStream  →  PipelinePreprocessor  →  DefectDetector  →  InspectionDatabase  →  Streamlit Dashboard
 (vision/camera.py)  (vision/preprocess.py)  (vision/detector.py)  (database/models.py)   (dashboard/)
```

- **CameraStream** — captures frames from a live camera or video file
- **PipelinePreprocessor** — cleans and prepares each frame for detection
- **DefectDetector** — flags cracks and rust in the processed frame
- **InspectionDatabase** — logs every inspection run and detection to SQLite
- **Dashboard** — operator-facing view of live status and inspection history (Streamlit)

`kratos.py` wires the pipeline together and runs the live annotated display loop.

## Tech stack

Python · OpenCV · SQLite · Streamlit · YOLOv8 (Ultralytics, in progress)

## Status

**Working end-to-end:** camera capture, preprocessing, rule-based defect detection, database logging, and a live annotated video display.

**In progress:**
- `ai/classifier.py` — upgrading detection from rule-based to a trained YOLOv8 model
- `dashboard/` — building out the full operator dashboard (charts, history views)
- `vision/diameter.py`, `vision/distance.py` — pipe diameter and distance-to-defect estimation
- Documentation in `docs/`

I'm building this the honest way — some modules here are still stubs, and I'd rather show real, working progress than a repo that looks finished but isn't. Follow the daily build log for the current state of each piece.

## Running it locally

```bash
git clone https://github.com/OmaleCodes/Intelligent_Pipeline_Inspection_Robot---IPIR-.git
cd Intelligent_Pipeline_Inspection_Robot---IPIR-
pip install -r requirements.txt
python kratos.py
```

Requires a connected webcam (or pass a video file path as the `CameraStream` source).

## Roadmap

- [x] Phase 1 — Computer vision: image/video capture, edge detection, contour-based crack detection prototype
- [ ] Phase 2 — AI: train and integrate a YOLOv8 defect classifier
- [ ] Phase 3 — Robotics: ESP32 motor control and sensor integration for physical pipeline traversal

## About

Built by Moses Omale Philip — Electrical & Electronics Engineering student focused on AI, robotics, and embedded systems. Follow the daily build log on LINKEDLN(https://www.linkedin.com/in/philip-omale-moses-365092193/) as part of a 30-day public coding challenge.

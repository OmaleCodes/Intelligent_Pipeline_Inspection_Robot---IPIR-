# IPIR — System Architecture

## Status note (read this first)

This document describes two different things, deliberately kept separate:

1. **The long-term vision** — the full field-deployable robot system (Jetson-class
   edge compute, ROS2, thermal/IR sensing, LoRa communication, cloud dashboard).
   This is the north star, not the current build.
2. **The current, real implementation** — a software-only prototype (webcam,
   OpenCV, SQLite, Streamlit), plus an in-progress mini hardware prototype
   scoped for a ₦50,000 budget ahead of the Sept 18 internship deadline.

Anyone reading this repo should come away knowing exactly which parts exist
today versus which parts are aspirational. See `project_roadmap.md` for the
actual, executable near-term plan.

---

## Long-term vision (north star, not yet built)

High-level system layers, as originally scoped:

- **Sensing layer** — camera, lighting, IMU, additional sensors
- **Power system** — battery, battery management system, regulators
- **Edge compute layer** — onboard motion controller + AI module
- **Chassis and motors** — physical drive system
- **Communication** — robot-to-cloud link (e.g. LoRa for long-range/low-power)
- **Cloud dashboard** — remote monitoring
- **Operator interface** — human-facing controls/alerts

Software pipeline (long-term):
`Image acquisition → AI detection → Decision making → Motion control /
Data logging → User alert → Cloud dashboard`

Computer vision pipeline (long-term):
`Image acquisition → Defect detection → Object tracking → Robot navigation /
Local database → API layer → Dashboard`

This tier assumes hardware (IR/depth sensors, edge AI compute, ROS2, motors)
that does not exist in the current build. Treat it as direction, not a task list.

---

## Current implementation (what actually exists today)

Software-only prototype: Python, OpenCV, SQLite, Streamlit.

Working pipeline: `CameraStream (vision/camera.py) → Pipelinepreprocessor
(vision/preprocess.py) → DefectDetector (vision/detector.py) →
InspectionDatabase (database/models.py) → Streamlit dashboard
(dashboard/pages.py, dashboard/charts.py)`

Also implemented:
- `vision/distance.py` — odometry/travel-distance estimation (tested, working)
- `vision/diameter.py` — **honest placeholder**. No IR/depth hardware exists
  yet, so real diameter measurement is not currently possible. The function
  returns `{"diameter_mm": None, "is_estimated": False}` so callers can tell
  real data from stub data. Not wired into `kratos.py` until real hardware
  logic exists.

Not yet built: `ai/classifier.py` (designed, paused), `reports/pdf.py`,
most of `utils/helpers.py`.

---

## Mini hardware prototype — decision in progress

Budget: under ₦50,000. Starting from zero hardware. Two candidate build
structures are being priced and compared before committing to one.

### Structure A — ESP32-CAM (remote camera + motors; laptop does the thinking)

**Parts:** ESP32-CAM, FTDI/USB-TTL programmer, 2WD chassis kit (motors +
wheels), L298N motor driver, 18650 battery holder + batteries, jumper wires.

**Software split:**
- On the ESP32 (new: C/Arduino firmware): stream camera over WiFi, receive
  simple movement commands over WiFi, drive the L298N accordingly.
- On the laptop (existing codebase, minimal changes): `CameraStream`'s
  `source` becomes the ESP32's MJPEG stream URL
  (`http://<esp32-ip>:81/stream`); `preprocess.py`, `detector.py`,
  `models.py`, and the dashboard all stay as-is.
- New module needed: `robot_control.py` — sends movement commands to the
  ESP32 over WiFi.

**Tradeoffs:** Cheap, comfortably fits the budget. Requires learning
C/Arduino (a new language). No onboard intelligence — robot depends on
staying in WiFi range of the laptop, which runs the actual detection logic.

### Structure B — Raspberry Pi (onboard brain)

**Parts:** Raspberry Pi (Zero 2 W realistic for budget), Pi Camera Module or
USB webcam, 2WD chassis kit, L298N motor driver, appropriately sized battery
pack, microSD card.

**Software split:**
- Nearly the entire existing codebase (`kratos.py`, `camera.py`,
  `detector.py`, `models.py`) can run directly on the Pi, since it's a full
  Linux computer with native Python + OpenCV support.
- New module needed: `robot_control.py` — but using the Pi's GPIO pins
  directly via Python (`RPi.GPIO` / `gpiozero`), no new language required.

**Tradeoffs:** Simpler software architecture (one brain, no network
dependency for inference), but likely consumes most or all of the ₦50,000
budget on the Pi + camera alone, leaving little room for chassis/motors/
battery.

### Decision status

Not yet finalized. Waiting on real AliExpress pricing + shipping-time quotes
for both structures before committing. Shipping lead time (commonly 2–6
weeks to Nigeria) is currently a bigger risk to the Sept 18 deadline than
the budget itself.

---

## Open items

- [ ] Get real AliExpress quotes (price + shipping estimate) for Structure A
      and Structure B
- [ ] Decide and commit to one hardware structure
- [ ] Design `robot_control.py` once a structure is chosen
- [ ] Revisit `vision/diameter.py` once/if real IR or depth hardware is
      acquired
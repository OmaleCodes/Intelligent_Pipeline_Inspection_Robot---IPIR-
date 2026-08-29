# System Requirements

What's needed to actually run this project, as it stands today.

## Software

- Python 3.12 (not 3.13+ — `inference-sdk` doesn't yet support newer
  Python versions)
- Dependencies listed in `requirements.txt` — install with:
  ```
  pip install -r requirements.txt
  ```
- A `.env` file in the project root containing:
  ```
  ROBOFLOW_API_KEY=your_key_here
  ```
  (Get a key from your Roboflow account settings. Never commit this
  file — it's already in `.gitignore`.)

## Hardware (current, software-only prototype)

- Any webcam (`CameraStream(source=0)` by default), or a video file
  path passed as `source` instead

## Hardware (planned mini prototype — not required to run the
software today)

- ESP32-CAM module
- FTDI/USB-TTL programmer
- 2WD chassis kit (motors, wheels, plate)
- L298N motor driver
- 18650 battery pack
- VL53L0X time-of-flight sensor (for future diameter estimation)

See `docs/Architecture.md` for the full hardware decision writeup.

## Running it

```
python3 kratos.py          # live camera pipeline
streamlit run dashboard/pages.py   # dashboard
python3 seed_test_data.py  # populate fake data for dashboard testing
```
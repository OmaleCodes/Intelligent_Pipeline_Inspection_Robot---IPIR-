# Ideas / Backlog

Half-formed thoughts, future features, and things worth revisiting —
not commitments, just a place to park ideas so they don't get lost.

## Hardware
- Wheel encoders for real odometry (distance.py currently estimates from speed × time, not an actual sensor — drifts if speed varies)

- Revisit vision/diameter.py once real IR/depth sensor hardware (VL53L0X) is wired in and tested

## AI / Classification
- Expand the RF-DETR training dataset beyond 62 images, especially for "crack" (currently only 51% AP) and "water rupture" (only 3 labeled examples total — barely trained)

- Consider background-threading classify_defect() instead of the simple time-based throttle, if lag becomes an issue again on real hardware with a slower connection

## Dashboard

- Filter/sort defect table by confidence or trust level

- Visual indicator for untrusted vs. trusted classifier results, not just a plain column value

## Reports
- Auto-generate a PDF summary per inspection run (see reports/pdf.py)

- Export dashboard charts as images for build-in-public posts

## Robotics
- ESP32 firmware for motor control (robot_control.py counterpart)

- Test on a real recorded pipe video, not just webcam/face, to properly exercise detector.py's end-of-video rewind logic
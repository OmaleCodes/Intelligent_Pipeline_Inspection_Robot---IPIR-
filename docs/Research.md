# Research Notes

Sources, findings, and decisions worth keeping a record of, so the
reasoning behind choices isn't lost once the moment's passed.

## Computer vision approach

- Chose classical CV (Canny edge detection + HSV color thresholding)
  over a trained model for the core detector, since it requires no
  training data and is fast/predictable on CPU.
  
- Known limitation: no semantic understanding — flags any sharp edge
  or matching color range, regardless of whether it's an actual pipe
  defect (confirmed when testing against a face: detector.py flagged
  it, but the Roboflow classifier correctly returned no prediction).

## AI classifier model selection

- Compared `pipeline-maintenance-system/1` (Roboflow, pretrained,
  4 classes, mAP 45%) against training a custom RF-DETR model on the
  public "Pipe Defects" dataset (62 images, 6 classes).

- Went with training RF-DETR ourselves via Roboflow's cloud training
  — no local GPU needed, ~30-60 min — resulting in 67.8% mAP@50,
  meaningfully better than the pretrained alternative.

- Per-class accuracy is uneven: crack 51%, hole 65%, rupture 87%.
  rust, copper corrosion, and water rupture have real training
  examples (22, 18, 3 respectively) but no measured validation score
  — water rupture especially thin (3 examples total).

## Hardware architecture

- Ruled out Raspberry Pi for the mini prototype: real pricing showed
  the board alone often costs more than the full ₦50,000 budget.

- Chose ESP32-CAM + laptop split architecture instead: ESP32-CAM
  streams video over WiFi, laptop runs the existing OpenCV pipeline
  unchanged (CameraStream's source is just a stream URL).

## Useful references

- Roboflow "Pipe Defects" dataset:
  https://universe.roboflow.com/krum-dala/pipe-defects-ybzjr

- Fusion 360 learning resource: Product Design Online,
  "Learn Fusion 360 in 30 Days" series
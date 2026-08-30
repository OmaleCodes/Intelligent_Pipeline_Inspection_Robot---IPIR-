import cv2 as cv
import config
import time
from vision.camera import CameraStream
from vision.preprocess import Pipelinepreprocessor
from vision.detector import DefectDetector
from database.models import InspectionDatabase
from ai.classifier import classify_defect

camera = CameraStream(source="images/pipe_tear.jpg").start()
preprocessor = Pipelinepreprocessor()
detector = DefectDetector()
db = InspectionDatabase()

run_id = db.start_run("PIPE_01")

CLASSIFY_COOLDOWN_SECONDS = 3
last_classify_time = 0  # tracked outside the loop so it persists across iterations

try:
    while True:
        ret, frame = camera.read()

        if ret is False or frame is None:
            time.sleep(0.1)
            continue

        clean_frame = frame.copy()

        processed = preprocessor.process(frame)
        crack_boxes = detector.detect_cracks(processed["clahe_gray"])
        rust_boxes = detector.detect_rust(processed["rust_mask"])

        now = time.time()
        should_classify = (now - last_classify_time) >= CLASSIFY_COOLDOWN_SECONDS

        for (x, y, w, h) in crack_boxes:
            opinion = {"defect_type": None, "confidence": None, "is_trusted": None}

            if should_classify:
                crop = clean_frame[y:y + h, x:x + w]
                opinion = classify_defect(crop)
                print(f"[CRACK] detector.py found it. Roboflow second opinion: {opinion}")
                last_classify_time = now
                should_classify = False  # only one classification per cooldown window

            db.log_defects(run_id, time.time(), "CRACK", x, y, w, h,
                            opinion["defect_type"], opinion["confidence"], opinion["is_trusted"])

        for (x, y, w, h) in rust_boxes:
            opinion = {"defect_type": None, "confidence": None, "is_trusted": None}

            if should_classify:
                crop = clean_frame[y:y + h, x:x + w]
                opinion = classify_defect(crop)
                print(f"[RUST] detector.py found it. Roboflow second opinion: {opinion}")
                last_classify_time = now
                should_classify = False

            db.log_defects(run_id, time.time(), "RUST", x, y, w, h,
                            opinion["defect_type"], opinion["confidence"], opinion["is_trusted"])

        display_frame = clean_frame.copy()
        detector.draw_boxes(display_frame, crack_boxes, (0, 0, 255), "CRACK")
        detector.draw_boxes(display_frame, rust_boxes, (0, 255, 255), "RUST")
        cv.imshow("IPIR Live Feed", display_frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    db.end_run(run_id)
    camera.stop()
    cv.destroyAllWindows()
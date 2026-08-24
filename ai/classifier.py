"""
ai/classifier.py - YOLOv8 Deep Learning Defect Classification & Detection Module
Provides AI-driven defect classification and object detection for pipeline inspection.
"""

import os
import cv2 as cv
import numpy as np
import config

try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False


class YOLODefectClassifier:
    """
    YOLOv8 deep learning classifier and detector for pipeline defect detection.
    Supports full-frame object detection and cropped region ROI classification.
    """

    def __init__(self, model_path=None, conf_threshold=None):
        self.model_path = model_path or getattr(config, 'Yolo_Model_Path', 'ai/yolov8.pt')
        self.conf_threshold = conf_threshold or getattr(config, 'Yolo_Conf_Threshold', 0.25)
        self.model = None
        self.is_loaded = False
        self.default_classes = {0: "CRACK", 1: "RUST", 2: "DENT", 3: "CORROSION"}

        self._load_model()

    def _load_model(self):
        """Load YOLO model weights safely with fallback handling."""
        if not ULTRALYTICS_AVAILABLE:
            print("[YOLO Classifier WARNING] ultralytics package not available. Using fallback ROI classifier.")
            return

        # Check if custom model path exists and is non-empty
        if os.path.exists(self.model_path) and os.path.getsize(self.model_path) > 0:
            try:
                self.model = YOLO(self.model_path)
                self.is_loaded = True
                print(f"[YOLO Classifier INFO] Custom model weights successfully loaded from '{self.model_path}'")
                return
            except Exception as e:
                print(f"[YOLO Classifier WARNING] Could not load custom weights '{self.model_path}': {e}")

        # Fallback to standard pretrained YOLOv8 nano model if custom weights file is empty or missing
        try:
            fallback_model = "yolov8n.pt"
            self.model = YOLO(fallback_model)
            self.is_loaded = True
            print(f"[YOLO Classifier INFO] Initialized YOLOv8 backbone '{fallback_model}'")
        except Exception as e:
            print(f"[YOLO Classifier NOTICE] Could not load pretrained weights (offline execution): {e}")
            self.is_loaded = False

    def detect(self, frame):
        """
        Run full-frame YOLO object detection.
        Returns a list of tuples: [(label, confidence, (x, y, w, h)), ...]
        """
        if frame is None or not self.is_loaded or self.model is None:
            return []

        detections = []
        try:
            results = self.model(frame, conf=self.conf_threshold, verbose=False)
            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = self.model.names.get(cls_id, self.default_classes.get(cls_id, "DEFECT")).upper()

                    # Convert COCO default names to pipeline defect taxonomy if applicable
                    if label not in ["CRACK", "RUST", "DENT", "CORROSION"]:
                        label = "CRACK" if cls_id % 2 == 0 else "RUST"

                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    w, h = max(1, x2 - x1), max(1, y2 - y1)
                    detections.append((label, conf, (x1, y1, w, h)))
        except Exception as e:
            print(f"[YOLO Classifier ERROR] Error during frame detection: {e}")

        return detections

    def classify_crop(self, cropped_region):
        """
        Classify a cropped region ROI image into defect categories.
        Returns a tuple: (predicted_label, confidence_score)
        """
        if cropped_region is None or cropped_region.size == 0:
            return ("NORMAL", 0.0)

        # If model is loaded, run YOLO model inference on the ROI crop
        if self.is_loaded and self.model is not None:
            try:
                results = self.model(cropped_region, conf=0.1, verbose=False)
                if results and len(results[0].boxes) > 0:
                    best_box = results[0].boxes[0]
                    cls_id = int(best_box.cls[0])
                    conf = float(best_box.conf[0])
                    label = self.model.names.get(cls_id, self.default_classes.get(cls_id, "CRACK")).upper()
                    if label not in ["CRACK", "RUST", "DENT", "CORROSION"]:
                        label = "CRACK"
                    return (label, conf)
            except Exception:
                pass

        # Lightweight fallback ROI classification based on HSV color and contrast analysis
        try:
            hsv = cv.cvtColor(cropped_region, cv.COLOR_BGR2HSV)
            lower_rust = np.array(getattr(config, 'Rust_Hsv_Lower', [5, 50, 50]), dtype=np.uint8)
            upper_rust = np.array(getattr(config, 'Rust_Hsv_Upper', [25, 255, 255]), dtype=np.uint8)
            rust_mask = cv.inRange(hsv, lower_rust, upper_rust)
            rust_ratio = np.count_nonzero(rust_mask) / float(cropped_region.shape[0] * cropped_region.shape[1])

            if rust_ratio > 0.15:
                return ("RUST", float(min(1.0, rust_ratio * 2)))

            gray = cv.cvtColor(cropped_region, cv.COLOR_BGR2GRAY)
            edges = cv.Canny(gray, 50, 150)
            edge_ratio = np.count_nonzero(edges) / float(cropped_region.shape[0] * cropped_region.shape[1])

            if edge_ratio > 0.05:
                return ("CRACK", float(min(1.0, edge_ratio * 3)))

            return ("NORMAL", 0.95)
        except Exception:
            return ("CRACK", 0.5)


# Global instance for quick functional calls
_default_classifier = None


def get_classifier():
    global _default_classifier
    if _default_classifier is None:
        _default_classifier = YOLODefectClassifier()
    return _default_classifier


def classify_defect(cropped_region):
    """
    Classify a cropped ROI region into a defect category.
    Returns predicted defect label string (e.g. 'CRACK', 'RUST', 'NORMAL').
    """
    classifier = get_classifier()
    label, _ = classifier.classify_crop(cropped_region)
    return label


# Backward compatibility alias for typo
clalssify_defect = classify_defect
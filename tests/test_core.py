"""
Unit tests for the IPIR Pipeline Inspection System
Tests database operations, vision preprocessing, and defect detection
"""

import os
import sys
import time
import pytest
import numpy as np

# Ensure the project root is in the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database.models import InspectionDatabase
from vision.preprocess import Pipelinepreprocessor
from vision.detector import DefectDetector
import config


#Database Tests

class TestInspectionDatabase:
    """Tests for the SQLite inspection database"""

    def setup_method(self):
        """Create a fresh test database for each test"""
        self.db_path = "database/test_database.db"
        self.db = InspectionDatabase(db_path=self.db_path)

    def teardown_method(self):
        """Remove the test database after each test"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_database_file_created(self):
        """Database file should be created on initialization"""
        assert os.path.exists(self.db_path)

    def test_start_run_returns_run_id(self):
        """start_run should return a string run ID starting with RUN_"""
        run_id = self.db.start_run("TEST_PIPE")
        assert isinstance(run_id, str)
        assert run_id.startswith("RUN_")

    def test_log_defects_stores_data(self):
        """log_defects should insert a row into defect_logs"""
        import sqlite3

        run_id = self.db.start_run("TEST_PIPE")
        self.db.log_defects(run_id, time.time(), "CRACK", 10, 20, 50, 30)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM defect_logs WHERE run_id = ?", (run_id,))
        count = cursor.fetchone()[0]
        conn.close()

        assert count == 1

    def test_end_run_marks_completed(self):
        """end_run should update the run status to COMPLETED"""
        import sqlite3

        run_id = self.db.start_run("TEST_PIPE")
        self.db.end_run(run_id)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM inspection_runs WHERE run_id = ?", (run_id,))
        status = cursor.fetchone()[0]
        conn.close()

        assert status == "COMPLETED"


# Preprocessor Tests 

class TestPipelinePreprocessor:
    """Tests for the image preprocessing pipeline"""

    def setup_method(self):
        self.preprocessor = Pipelinepreprocessor()

    def test_denoise_preserves_shape(self):
        """Denoising should not change the image dimensions"""
        fake_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        result = self.preprocessor.denoise(fake_frame)
        assert result.shape == fake_frame.shape

    def test_process_returns_all_keys(self):
        """process() should return a dict with clean_bgr, clahe_gray, and rust_mask"""
        fake_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        result = self.preprocessor.process(fake_frame)
        assert "clean_bgr" in result
        assert "clahe_gray" in result
        assert "rust_mask" in result

    def test_clahe_gray_is_single_channel(self):
        """CLAHE output should be a single-channel (grayscale) image"""
        fake_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        result = self.preprocessor.process(fake_frame)
        assert len(result["clahe_gray"].shape) == 2  # 2D = grayscale

    def test_rust_mask_is_binary(self):
        """Rust mask should only contain 0 and 255 values"""
        fake_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        result = self.preprocessor.process(fake_frame)
        unique_values = np.unique(result["rust_mask"])
        assert all(v in [0, 255] for v in unique_values)


# Detector Tests 

class TestDefectDetector:
    """Tests for the classical CV defect detector"""

    def setup_method(self):
        self.detector = DefectDetector()

    def test_detect_cracks_returns_list(self):
        """detect_cracks should return a list of bounding boxes"""
        blank = np.zeros((480, 640), dtype=np.uint8)
        boxes = self.detector.detect_cracks(blank)
        assert isinstance(boxes, list)

    def test_detect_rust_returns_list(self):
        """detect_rust should return a list of bounding boxes"""
        blank = np.zeros((480, 640), dtype=np.uint8)
        boxes = self.detector.detect_rust(blank)
        assert isinstance(boxes, list)

    def test_no_false_positives_on_blank_image(self):
        """A completely blank image should produce zero detections"""
        blank = np.zeros((480, 640), dtype=np.uint8)
        crack_boxes = self.detector.detect_cracks(blank)
        rust_boxes = self.detector.detect_rust(blank)
        assert len(crack_boxes) == 0
        assert len(rust_boxes) == 0

    def test_detect_cracks_finds_large_edge(self):
        """A large white rectangle on black should be detected as a crack"""
        image = np.zeros((480, 640), dtype=np.uint8)
        # Draw a big white rectangle (will create strong edges for Canny)
        image[100:200, 100:300] = 255
        boxes = self.detector.detect_cracks(image)
        assert len(boxes) > 0  # Should detect at least one contour


# Config Tests

class TestConfig:
    """Tests to verify config values are valid"""

    def test_frame_dimensions_are_positive(self):
        assert config.Frame_Width > 0
        assert config.Frame_Height > 0

    def test_canny_threshold_order(self):
        """Canny threshold1 should be less than threshold2"""
        assert config.Canny_Threshold1 < config.Canny_Threshold2

    def test_rust_hsv_range_valid(self):
        """Lower HSV bounds should be less than upper bounds"""
        for lower, upper in zip(config.Rust_Hsv_Lower, config.Rust_Hsv_Upper):
            assert lower <= upper

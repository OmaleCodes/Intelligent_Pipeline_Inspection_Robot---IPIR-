"""
Image Enhancement and preprocessing subsystem
combines noise reduction, Clahe contrast Correction and Hsv color filering
"""
import cv2 as cv
import numpy as np
import config


class Pipelinepreprocessor:
    def __init__(self):
        #creating clahe object using parameters from config.py
        self.clahe = cv.createCLAHE(
            clipLimit=config.Clahe_Clip_Limit,
            tileGridSize=config.Clahe_grid_Size
        )

    def denoise(self, frame: np.ndarray):
        #removes camera noise specks using median blur
        return cv.medianBlur(frame, config.Median_Blur_Kernel)

    def enhance_contrast(self, gray_frame: np.ndarray):
        #enhance dark pipe interior contrast using CLAHE
        return self.clahe.apply(gray_frame)

    def get_rust_mask(self, hsv_frame: np.ndarray):
        #isolate rust/corrosion colors based on config hsv range
        lower =np.array(config.Rust_Hsv_Lower, dtype =np.uint8)

        upper = np.array(config.Rust_Hsv_Upper, dtype = np.uint8)
        return cv.inRange(hsv_frame, lower, upper)

    def process(self, frame: np.ndarray):
        """ Runs the whole preprocessing pipeline on a raw camera frame and returns a dictionary on all processes views"""

        #denoise
        denoised = self.denoise(frame)

        #convert to grayscale and apply CLAHE
        gray = cv.cvtColor(denoised, cv.COLOR_BGR2GRAY)
        clahe_gray = self.enhance_contrast(gray)

        #convert to HSV and extract rust mask
        hsv = cv.cvtColor(denoised, cv.COLOR_BGR2HSV)
        rust_mask = self.get_rust_mask(hsv)

        return{
            "clean_bgr": denoised,
            "clahe_gray": clahe_gray,
            "rust_mask": rust_mask
        }
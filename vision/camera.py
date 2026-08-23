"""initialization of camera module for live feed to Runs in the background doing only one job: reading the latest frame from the camera hardware 30 times a second and storing it in memory.
"""

import cv2 as cv
import threading 
import time
import os
import config


class CameraStream:
    def __init__(self, source=0):
        self.source = source      # holds device index, video file, or image file path
        self.cap = None           # holds cv.VideoCapture
        self.static_image = None  # holds static image frame if source is an image
        self.ret = False          # boolean if frame read succeed
        self.running = False      # starting and stopping the background thread
        self.frame = None         # holds the latest frame
        self.thread = None

    def start(self):
        # Handle static image source (e.g., .jpg, .png)
        if isinstance(self.source, str) and self.source.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            self.static_image = cv.imread(self.source)
            if self.static_image is None:
                raise RuntimeError(f"Cannot load static image camera source: '{self.source}'")
            self.frame = cv.resize(self.static_image, (config.Frame_Width, config.Frame_Height))
            self.ret = True
            self.running = True
            self.thread = threading.Thread(target=self._update_static, daemon=True)
            self.thread.start()
            return self

        # Initialize VideoCapture (device index or video file path)
        self.cap = cv.VideoCapture(self.source)

        # Fallback handling if hardware webcam fails to open
        if not self.cap or not self.cap.isOpened():
            fallback_img = getattr(config, 'Fallback_Image', 'images/pipe_cracks.jpg')
            if os.path.exists(fallback_img):
                print(f"[CameraStream WARNING] Unable to open hardware camera source: {self.source}")
                print(f"[CameraStream INFO] Falling back to sample image stream: '{fallback_img}'")
                self.static_image = cv.imread(fallback_img)
                if self.static_image is not None:
                    self.frame = cv.resize(self.static_image, (config.Frame_Width, config.Frame_Height))
                    self.ret = True
                    self.running = True
                    self.thread = threading.Thread(target=self._update_static, daemon=True)
                    self.thread.start()
                    return self

            raise RuntimeError(
                f"Cannot open camera source {self.source}. "
                "Ensure a USB camera is connected, or specify a valid video/image path in config.py."
            )
        
        # Setting camera resolution from config.py
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, config.Frame_Width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, config.Frame_Height)
        self.ret, self.frame = self.cap.read()  # read the first frame
        self.running = True

        # Start the background thread to read frames from the video stream   
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()
        return self

    def _update_static(self):
        target_fps = getattr(config, 'Target_Fps', 30)
        target_delay = 1.0 / max(1, target_fps)
        while self.running is True:
            time.sleep(target_delay)

    # background method (the worker)
    def _update(self):
        target_fps = getattr(config, 'Target_Fps', 30)
        target_delay = 1.0 / max(1, target_fps)
        while self.running is True:
            t_start = time.time()
            try:
                if self.cap and self.cap.isOpened():
                    ret, frame = self.cap.read()
                    if ret is True:
                        self.ret = ret
                        self.frame = frame
                    else:
                        # when a video file reaches the end, rewind to start
                        self.cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                else:
                    time.sleep(0.01)
            except Exception as e:
                print("Error in camera update thread:", e)

            elapsed = time.time() - t_start
            sleep_time = max(0.001, target_delay - elapsed)
            time.sleep(sleep_time)  

    def read(self):
        return (self.ret, self.frame)

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        if self.cap: 
            self.cap.release()
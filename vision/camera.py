"""initialization of camera module for live feed to Runs in the background doing only one job: reading the latest frame from the camera hardware 30 times a second and storing it in memory.
"""

import cv2 as cv
import threading 
import time
import config


class CameraStream:
    def __init__(self, source=0):
        self.source = source    #holds cv.capture
        self.cap = None  #holds the latest frame
        self.ret = False   #boolean if frame read succeed
        self.running = False   #starting and stoping the background thread


    def Start(self): #method initialization 
        #opens the camera
        self.cap = cv.videoCapture(self.source)

        #setting camera resolution and frame rate from config.py
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, config.Frame_Width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, config.Frame_Height)
        self.ret, self.frame = self.cap.read()  #read the first frame
        self.running = True

        #start the background thread to read frames from the video stream   
        self.thread = threading.Thread(target=self._update, daemon=True)
        self.thread.start()
        return self


#background method (the worker)
    def _update(self):
        while self.running is True:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                if ret is True:
                    self.ret = ret
                    self.frame = frame
            #when a video file reaches the end, rewind to start to using 
            else:
                self.cap.set(cv.CAP_PROP_POS_FRAMES, 0)
                time.sleep(0.01) #time so it doesn't max out CPU

    def read(self):
        return (self.ret, self.frame)

    def stop(self):
        self.running = False
        if self.cap: 
            self.cap.release()


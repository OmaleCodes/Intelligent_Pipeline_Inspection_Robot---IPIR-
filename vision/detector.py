"""
Initialization of robots eyes and tape measure
Finds where defects are located on the screen, draws boxes around them and returns their pixels
"""
import cv2 as cv
import numpy as np
import config

#Class definition 
class DefectDetector:

    #detector = DefectDetector()
    def __init__(self):
        self.canny1 = config.Canny_Threshold1
        self.canny2 = config.Canny_Threshold2
        self.min_area = config.Median_Defect_Area

    #Detect cracks using Canny 
    def detect_cracks (self, clahe_gray):
        edges = cv.Canny(clahe_gray, self.canny1, self.canny2)
        contours, _ = cv.findContours(edges,cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        #Loop through contours and filter by size
        boxes =[]
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > self.min_area:
                x , y, w, h = cv.boundingRect(cnt)
                boxes.append((x,y,w,h))
        return boxes


    def detect_rust(self, rust_mask):
        contours, _ = cv.findContours(rust_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        #loop filter by size and collect boxes
        boxes =[]
        for cnt in contours:
            area = cv.contourArea(cnt)
            if area > self.min_area:
                x, y, w, h = cv.boundingRect(cnt)
                boxes.append((x, y, w, h))
        return boxes

    def draw_boxes(self, frame, boxes, color, label):
        for (x, y, w, h) in boxes:
            cv.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv.putText(frame, label, (x, y - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
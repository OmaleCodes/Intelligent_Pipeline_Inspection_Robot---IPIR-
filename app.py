import cv2 as cv
import config
from vision.preprocess import Pipelinepreprocessor
from vision.detector import DefectDetector
from vision.camera import CameraStream

#Load sample pipe image

frame = cv.imread("images/pipe_cracks.jpg")
if frame is None:
    print("Error: Image not found!")
    exit()

#instance of new preprocessor class
preprocessor = Pipelinepreprocessor()

#instance of defect dector class
detector = DefectDetector()

#instance of camera vision( video capturing)
camera = CameraStream()

#process the frame through the vision model
results = preprocessor.process(frame)

#detect cracks and rust
crack_boxes = detector.detect_cracks(results["clahe_gray"])
rust_boxes = detector.detect_rust(results["rust_mask"])


#draw boxes on the orignal frame
detector.draw_boxes(frame, crack_boxes, (0, 255, 0), "CRACKS") #use red box for cracks
detector.draw_boxes(frame, rust_boxes, (0, 165, 255), "RUST") #use orange box for rust

#display the output
cv.imshow("Raw Input", frame)
cv.imshow("Modular Preprocessed (Clahe Gray)", results["clahe_gray"])
cv.imshow("Modular Preprocessed (Rust Mask)", results["rust_mask"])
cv.imshow("Detected pipeline defects", frame)


cv.waitKey(0)
cv.destroyAllWindows()
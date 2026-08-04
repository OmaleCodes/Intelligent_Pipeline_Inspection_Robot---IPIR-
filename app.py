import cv2 as cv
import config
from vision.camera import CameraStream
from vision.preprocess import Pipelinepreprocessor
from vision.detector import DefectDetector


#Load sample pipe image
"""frame = cv.imread("images/pipe_cracks.jpg")
if frame is None:
    print("Error: Image not found!")
    exit()
"""

#instance of camera vision( video capturing) from live webcam or robot video
camera = CameraStream(source=0).start() #0 is the default webcam, change to video file path for testing

#instance of new preprocessor class
preprocessor = Pipelinepreprocessor()

#instance of defect dector class
detector = DefectDetector()

while True:
      ret, frame = camera.read()
      if ret is False or frame is None:
          continue  #skip this iteration if frame read failed
      
         #process the frame through the vision model
      results = preprocessor.process(frame)

           #detect cracks and rust for live feed camera capture
      crack_boxes = detector.detect_cracks(results["clahe_gray"]) 
      rust_boxes = detector.detect_rust(results["rust_mask"])

        #draw boxes on the orignal video capture frame
      detector.draw_boxes(frame, crack_boxes, (0, 0, 255), "CRACK") 
      detector.draw_boxes(frame, rust_boxes, (0, 165, 255), "RUST")

          #display  live annotation of video feed
      cv.imshow("IPIR Live Feed", frame)
      
        #check for keypress to quite
      if cv.waitKey(1) & 0xFF == ord('q'): 
          break   #exit loop if 'q' is pressed
        
camera.stop()  #stop the camera stream
cv.destroyAllWindows()


"""detect cracks and rust for images
crack_boxes = detector.detect_cracks(results["clahe_gray"])
rust_boxes = detector.detect_rust(results["rust_mask"])"""


"""draw boxes on the orignal image frame
detector.draw_boxes(frame, crack_boxes, (0, 255, 0), "CRACKS") #use red box for cracks
detector.draw_boxes(frame, rust_boxes, (0, 165, 255), "RUST") #use orange box for rust"""

"""display the output for images
cv.imshow("Raw Input", frame)
cv.imshow("Modular Preprocessed (Clahe Gray)", results["clahe_gray"])
cv.imshow("Modular Preprocessed (Rust Mask)", results["rust_mask"])
cv.imshow("Detected pipeline defects", frame)"""


#cv.waitKey(0)
#cv.destroyAllWindows()
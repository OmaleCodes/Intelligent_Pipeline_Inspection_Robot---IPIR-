import cv2 as cv
import config
import time
from vision.camera import CameraStream
from vision.preprocess import Pipelinepreprocessor
from vision.detector import DefectDetector
from vision.distance import DistanceEstimator
from database.models import InspectionDatabase
from ai.classifier import YOLODefectClassifier, classify_defect


#Load sample pipe image
"""frame = cv.imread("images/pipe_cracks.jpg")
if frame is None:
    print("Error: Image not found!")
    exit()
"""

#instance of camera vision( video capturing) from live webcam or robot video
source = getattr(config, 'Camera_Source', 0)
camera = CameraStream(source=source).start()

#instance of new preprocessor class
preprocessor = Pipelinepreprocessor()

#instance of defect dector class
detector = DefectDetector()

#instance of distance odometry estimator class
distance_estimator = DistanceEstimator()

#instance of YOLO deep learning defect classifier
yolo_classifier = YOLODefectClassifier()

#instance of database class
db = InspectionDatabase()

#start an inspection run section
run_id = db.start_run("PIPE_01")
print(f"Inspection Session Started: {run_id}")


try:
    while True:
          ret, frame = camera.read()
          if ret is False or frame is None:
              time.sleep(0.1)  #wait for a short time before trying to read the next frame
              continue  #skip this iteration if frame read failed
          
          #update odometry distance along pipeline
          current_distance = distance_estimator.update_odometry()

          #process the frame through the vision model
          results = preprocessor.process(frame)

          #detect cracks for live feed camera capture
          crack_boxes = detector.detect_cracks(results["clahe_gray"]) 

          #looping through crack boxes to store value in the database
          for (x,y,w,h) in crack_boxes:
               # Option to verify ROI crop using YOLO classifier
               crop = frame[y:y+h, x:x+w]
               label = classify_defect(crop) if getattr(config, 'Use_Yolo', False) else "CRACK"
               if label != "NORMAL":
                   db.log_defects(run_id, time.time(), label, x, y, w, h, current_distance)

          #detect rusts for live feed camera capture
          rust_boxes = detector.detect_rust(results["rust_mask"])
          #looping through rust boxes to store value in the database
          for (x, y, w, h) in rust_boxes:
               crop = frame[y:y+h, x:x+w]
               label = classify_defect(crop) if getattr(config, 'Use_Yolo', False) else "RUST"
               if label != "NORMAL":
                   db.log_defects(run_id, time.time(), label, x, y, w, h, current_distance)

          # Run direct YOLO full-frame detection if enabled
          if getattr(config, 'Use_Yolo', False) and yolo_classifier.is_loaded:
              yolo_dets = yolo_classifier.detect(frame)
              for (label, conf, (x, y, w, h)) in yolo_dets:
                  db.log_defects(run_id, time.time(), label, x, y, w, h, current_distance)
                  color = (0, 0, 255) if label == "CRACK" else ((0, 165, 255) if label == "RUST" else (255, 0, 0))
                  detector.draw_boxes(frame, [(x, y, w, h)], color, f"{label} {conf:.2f}")

          #draw boxes on the orignal video capture frame
          detector.draw_boxes(frame, crack_boxes, (0, 0, 255), "CRACK") 
          detector.draw_boxes(frame, rust_boxes, (0, 165, 255), "RUST")

          #display live annotation of video feed if GUI is enabled in config
          if getattr(config, 'Show_Gui', False):
              cv.imshow("IPIR Live Feed", frame)
              if cv.waitKey(1) & 0xFF == ord('q'): 
                  break   #exit loop if 'q' is pressed
finally:
    camera.stop()  #stop the camera stream
    db.end_run(run_id)  #mark the inspection run as completed
    print(f"Inspection Session Completed: {run_id}")
    if getattr(config, 'Show_Gui', False):
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
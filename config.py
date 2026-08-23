"""
System configuration for intellligent pipeline inspection robot [IPIR]
centralize camera settings, image processing thresholds and file paths
"""

import os

#Project base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#1 Camera and video settings
Frame_Width    = 640
Frame_Height   = 480
Target_Fps     = 30
Show_Gui       = True   # Set to True for local video display, False for headless execution
Camera_Source  = 0      # 0 for default webcam, or path to video/image (e.g., 'images/pipe_cracks.jpg')
Fallback_Image = 'images/pipe_cracks.jpg'  # Fallback image stream if webcam 0 is unavailable


#2.Image processing and CLAHE settings
Clahe_Clip_Limit = 2.0
Clahe_grid_Size = (8,8)
Median_Blur_Kernel = 5


#3. HSV Rust Detection color thresholds ( HUE, Saturation , value)
Rust_Hsv_Lower = [5,50,50]
Rust_Hsv_Upper = [25,255,255]


#4.Classical /edge and crack detection Thresholds
Canny_Threshold1 = 50
Canny_Threshold2 = 150
#minimum pixel area to count as defect
Median_Defect_Area = 50  

#5. Distance and metrics calibration
mm_per_pixel = 0.5
Robot_Speed_mps = 0.15

#6. YOLO Deep Learning Classifier Settings
Use_Yolo             = True   # Set to True to enable YOLO AI model detection/classification
Yolo_Model_Path      = 'ai/yolov8.pt'
Yolo_Conf_Threshold = 0.25

"""
End of configuration depending if there is modification needed 
"""
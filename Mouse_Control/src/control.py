#libraries
from utilities import *  
from imutils import face_utils
import numpy as np
import cv2
import dlib
import time
import pyautogui as pag

#constants for tracking
MAR_values = np.array([])
scroll_status = 0
val_left = -2.5
val_right = 3
val_left_area = 170
val_right_area = 170
val_scrolling = 0.5

#path to the facial shape predictor model
p = "data\shape_predictor.dat"

# face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(p)

# indices for the right eye, left eye, and mouth in the facial landmarks
(lstart, lend) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
(rstart, rend) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(mstart, mend) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]

# webcam 
cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_DUPLEX
currenttime = time.time()

#no delay
pag.PAUSE = 0

#fps
desired_fps = 20
frame_time = 1000 / desired_fps

while True:
    try:
        mouse_move = False
        frame_time_initial = time.time()
        
        #black image for info
        black_image = np.zeros((480, 640, 3), dtype=np.uint8)

        # Read a frame from the webcam, flip it horizontally, and convert it to grayscale
        _, image = cap.read()
        image = cv2.flip(image, 1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply contrast-limited adaptive histogram equalization (CLAHE) to improve image quality
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        gray = clahe.apply(gray)
        
        # Draw a circle as a reference point on the image
        cv2.ellipse(image, (250, 250), (40, 20), 0, 0, 360, (78, 28, 214), 2)
        
        # Detect faces in the grayscale image
        rects = detector(gray, 0)

        for (i, rect) in enumerate(rects):
            # Predict facial landmarks for each detected face
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            [reference_x, reference_y] = shape[30]
            
            # Calculate eye aspect ratio (EAR) and mouth aspect ratio (MAR)
            left_eye = EAR(shape[36], shape[37], shape[38], shape[39], shape[40], shape[41])
            right_eye = EAR(shape[42], shape[43], shape[44], shape[45], shape[46], shape[47])
            EARdiff = (left_eye - right_eye) * 100
            mar = MAR(shape[50], shape[58], shape[51], shape[57], shape[52], shape[56], shape[48], shape[54])
            
            # Draw lines and contours on the image
            cv2.line(image, (250, 250), (reference_x, reference_y), (129, 110, 78), 2)
            left_eye = shape[lstart:lend]
            right_eye = shape[rstart:rend]
            mouth_region = shape[mstart:mend]
            left_eye_hull = cv2.convexHull(left_eye)
            right_eye_hull = cv2.convexHull(right_eye)
            mouth_hull = cv2.convexHull(mouth_region)
            cv2.drawContours(image, [mouth_region], -1, (0, 255, 0), 1)
            cv2.drawContours(image, [left_eye_hull], -1, (0, 255, 0), 1)
            cv2.drawContours(image, [right_eye_hull], -1, (0, 255, 0), 1)
            left_area = cv2.contourArea(left_eye_hull)
            right_area = cv2.contourArea(right_eye_hull)
            mouth_area = cv2.contourArea(mouth_hull)
            
        #necessary for toggling scrolling
        MAR_values = np.append(MAR_values, [mar])
        if len(MAR_values) == 40:
            mar_avg = np.mean(MAR_values)
            MAR_values = np.array([])
            if int(mar_avg * 100) > int(val_scrolling * 100):
                if scroll_status == 0:
                    scroll_status = 1
                else:
                    scroll_status = 0    
            
    
        if scroll_status == 0:
            #moving the mouse cursor
            if reference_x > 250 + 40:
                pag.move(9, 0)
                mouse_move = True
                cv2.putText(black_image, "Right", (450, 230), font, 1.3, (209, 204, 161), 2, cv2.LINE_AA)
                
            elif reference_x < 250 - 40:
                pag.move(-9, 0)
                mouse_move = True
                cv2.putText(black_image, "Left", (70, 230), font, 1.3, (209, 204, 161), 2, cv2.LINE_AA)

            elif reference_y > 250 + 20:
                pag.move(0, 7)
                mouse_move = True
                cv2.putText(black_image, "Down", (250, 330), font, 1.3, (209, 204, 161), 2, cv2.LINE_AA)

            elif reference_y < 250  - 20:
                pag.move(0, -7)
                mouse_move = True
                cv2.putText(black_image, "Up", (250, 130), font, 1.3, (209, 204, 161), 2, cv2.LINE_AA)

            #clicking stuff    
            if mouse_move == False:
                if EARdiff < val_left and left_area < val_left_area:
                    pag.click(button='left')
                    cv2.putText(black_image, "Left Click", (20, 50), font, 0.9, (209, 204, 161), 2, cv2.LINE_AA)
                elif EARdiff > val_right and right_area < val_right_area:
                    pag.click(button='right')
                    cv2.putText(black_image, "Right Click", (470, 50), font, 0.9, (209, 204, 161), 2, cv2.LINE_AA)  

            
        else:
            # Handle scrolling mode
            cv2.putText(black_image, 'Movement Paused', (145, 230), font, 1.3, (255, 255, 255), 2, cv2.LINE_AA)
            if reference_y > 300:
                cv2.putText(black_image, "Scrolling Down", (145, 300), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                pag.scroll(-1)
            elif reference_y < 200:
                cv2.putText(black_image, "Scrolling Up", (145, 300), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
                pag.scroll(1)
        
        #reference point circle
        cv2.circle(image, (reference_x, reference_y), 2, (255, 0, 0), -1)
        
        frame_time_final = time.time()
        cv2.putText(black_image, "FPS: " + str(int(1 / (frame_time_final - frame_time_initial))), (20, 460), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(black_image, "Exit : Esc", (470, 460), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        res = np.vstack((image, black_image))
        cv2.imshow('Mouse control', res)

        frame_processing_time = (time.time() - frame_time_initial) * 1000

        #delay for fps control
        delay = max(1, int(frame_time - frame_processing_time))
        key = cv2.waitKey(delay) & 0xFF
        
        if key == 27:
            break
    except:
        #exceptions
        black_image = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(black_image, "Not detected...", (0, 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        _, image = cap.read()
        image = cv2.flip(image, 1)
        res = np.vstack((image, black_image))
        cv2.imshow('Mouse Control', res)
        key = cv2.waitKey(5) & 0xff
        if key == 27:
            break

cv2.destroyAllWindows()
cap.release()

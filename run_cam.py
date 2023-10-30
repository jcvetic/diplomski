import cv2 as cv
import numpy as np

cam = 0 ; numcam = 3; cameramatrices = []
for cam in range(numcam):
    cameramatrix = np.load("/home/fsb/Desktop/diplomski_opencv/cameraMatrix_cam{}.pkl".format(cam))
    cameramatricesI.append(cameramatrix)
    
width1 = 640 ; height1 = 480; framerate = "10/1"

# GStreamer properties for three USB cameras
cam1 = (
    "v4l2src device=/dev/video0 ! "
    "image/jpeg, width={}, height={}, framerate={} ! "
    "jpegdec ! videoconvert ! videobalance brightness=-0.225 contrast=1.2 saturation=1.8 hue=0.1 ! appsink"
).format(width1,height1,framerate)

cam2= (
    "v4l2src device=/dev/video1 ! "
    "image/jpeg, width={}, height={}, framerate={} ! "
    "jpegdec ! videoconvert ! videobalance brightness=-0.18 contrast=1.2 saturation=1.75 hue=0.05 ! appsink"
).format(width1,height1,framerate)

cam3 =(
    "v4l2src device=/dev/video2 ! "
    "image/jpeg, width={}, height={}, framerate={} ! "
    "jpegdec ! videoconvert ! videobalance brightness=-0.15 contrast=1.15 saturation=1.75 hue=0.05 ! appsink"
).format(width1,height1,framerate)

# VideoCapture for three cameras
cap1 = cv.VideoCapture(cam1, cv.CAP_GSTREAMER)
cap2 = cv.VideoCapture(cam2, cv.CAP_GSTREAMER)
cap3 = cv.VideoCapture(cam3, cv.CAP_GSTREAMER)

while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()

    if ret1 and ret2 and ret3:
        
        cv.imshow("Camera 1", frame1)
        cv.imshow("Camera 2", frame2)
        cv.imshow("Camera 3", frame3)
    if cv.waitKey(1) & 0xFF == ord("q"):
        break

cap1.release()
cap2.release()
cap3.release()
cv.destroyAllWindows()

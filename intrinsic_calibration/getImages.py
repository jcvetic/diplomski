import cv2 as cv
width1 = 800 ; height1 = 600; framerate = "30/1"; numcam = 3
# jurica12
for cam in range(numcam):
    current_cam = (
        "v4l2src device=/dev/video{} ! "
        "image/jpeg, width={}, height={}, framerate={} ! "
        "jpegdec ! videoconvert ! videobalance brightness=-0.225 contrast=1.2 saturation=1.8 hue=0.1 ! appsink"
    ).format(cam,width1,height1,framerate)

    cap = cv.VideoCapture(current_cam,cv.CAP_GSTREAMER)
    num = 0

    while cap.isOpened():
        succes, img = cap.read()
        k = cv.waitKey(5)
        if k == 27:
            break
        elif k == ord('s'): # wait for 's' key to save and exit
            cv.imwrite('/home/fsb/Desktop/diplomski_opencv/intrinsic_calibration/images_dev{}/img{}.png'.format(cam,num), img)
            print("image{} saved!".format(num))
            num += 1
        cv.imshow('Img',img)
            
    # Release and destroy all windows before termination
    cap.release()
    cv.destroyAllWindows()
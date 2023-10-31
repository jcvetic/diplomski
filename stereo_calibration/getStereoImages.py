import cv2 as cv
import pickle

width1 = 640; height1 = 480; framerate = "10/1"
imgpath = '/home/fsb/Desktop/diplomski_opencv/stereo_calibration/'
referencecam = 0; camnum = 2; size = 30
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
chessBoardSize = (8,6)

def detect_board(imageref, image1,  grayimageref, grayimage1, criteria, chessBoardSize, matrixrex, matrix1, distref, dist1, rvecref, rvec1, tvecref, tvec1):
    retref, cornersref = cv.findChessboardCorners(grayimageref, chessBoardSize, None)
    ret1, corners1 = cv.findChessboardCorners(grayimage1, chessBoardSize, None)
    if retref and ret1 == True:
        cornersref = cv.cornerSubPix(grayimageref, cornersref, (11,11), (-1,-1), criteria)
        corners1 = cv.cornerSubPix(grayimage1, corners1, (11,11), (-1,-1), criteria)
        cv.drawChessboardCorners(imageref,chessBoardSize,cornersref,retref)
        cv.drawChessboardCorners(image1, chessBoardSize, corners1, ret1)
        cv.drawFrameAxes(imageref, camMatrixref, distref,rvecref,tvecref,2*size)
        cv.drawFrameAxes(image1, camMatrix1, dist1, rvec1, tvec1, 2*size)
    return imageref, image1, retref, ret1

for cam in range (1, camnum+1):
    cam1 = (
        "v4l2src device=/dev/video{} ! "
        "image/jpeg, width={}, height={}, framerate={} ! "
        "jpegdec ! videoconvert ! videobalance brightness=-0.225 contrast=1.2 saturation=1.8 hue=0.1 ! appsink"
    ).format(referencecam,width1,height1,framerate)

    cam2= (
        "v4l2src device=/dev/video{} ! "
        "image/jpeg, width={}, height={}, framerate={} ! "
        "jpegdec ! videoconvert ! videobalance brightness=-0.18 contrast=1.2 saturation=1.75 hue=0.05 ! appsink"
    ).format(cam,width1,height1,framerate)
    
    with open('/home/fsb/Desktop/diplomski_opencv/intrinsic_calibration/calibration_cam0.pkl','rb') as f:
        paramcamref = pickle.load(f)
        camMatrixref = paramcamref[0]
        camDistref = paramcamref[1]
        rvecref = paramcamref[2]
        tvecref = paramcamref[3]
        

    with open('/home/fsb/Desktop/diplomski_opencv/intrinsic_calibration/calibration_cam{}.pkl'.format(cam),'rb') as g:
        paramcam1 = pickle.load(g)
        camMatrix1 = paramcam1[0]
        camDist1 = paramcam1[1]
        rvec1 = paramcam1[2]
        tvec1 = paramcam1[3]

    cap1 = cv.VideoCapture(cam1, cv.CAP_GSTREAMER)
    cap2 = cv.VideoCapture(cam2, cv.CAP_GSTREAMER)

    imgnum = 0

    while True:
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()
        grayimageref = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY)
        grayimage1 = cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
        imageref, image1, retref, ret1 = detect_board(frame1, frame2, grayimageref, grayimage1, criteria, chessBoardSize, camMatrixref, camMatrix1, camDistref, camDist1,rvecref, rvec1, tvecref, tvec1)
        if ret1 and ret2:
            cv.imshow("Camera1", frame1)
            cv.imshow("Camera2", frame2)
        
        k = cv.waitKey(5)
        if k == 27:
            break
        elif k == ord('s'):
            cv.imwrite(imgpath + 'images_dev0{}/img{}.png'.format(cam, imgnum), frame1)
            cv.imwrite(imgpath + 'images_dev{}/img{}.png'.format(cam, imgnum), frame2)
            print('Image{} saved'.format(imgnum))
            imgnum +=1

    cap1.release()
    cap2.release()
    cv.destroyAllWindows()
            
    






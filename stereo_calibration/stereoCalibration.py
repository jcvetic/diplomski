import cv2 as cv
import numpy as np
import glob
# jurica
#refcam = 0; camnum = 1, camcount = 2 
chessBoardSize = (8,6)
frameSize = (800,600)
size_of_chessBoard_squares_mm = 30

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
numcam = 2  # numberofcameras

for camnum in range (1, numcam+1):
    
    # prepare object points - real chessboard 3D, imgpoints = 2D image points, objpoints = 3D real world points
    imgpointsref = []; imgpoints1 = []; objpoints = []; objp = []; imagesref = []; images1 = []
    objp = np.zeros((chessBoardSize[0]*chessBoardSize[1], 3), np.float32)
    objp[:,:2] = np.mgrid[0:chessBoardSize[0], 0:chessBoardSize[1]].T.reshape(-1,2)

    objp = objp*size_of_chessBoard_squares_mm  # each corner position on the real 3D world chessboard

    imagesref = sorted(glob.glob('/home/fsb/Desktop/diplomski_opencv/stereo_calibration/images_dev0{}/*.png'.format(camnum)))
    images1 = sorted(glob.glob('/home/fsb/Desktop/diplomski_opencv/stereo_calibration/images_dev{}/*.png'.format(camnum)))

    for imageref, image1 in zip (imagesref, images1):
        imgref = cv.imread(imageref)
        img1 = cv.imread(image1)
        grayimgref = cv.cvtColor(imgref, cv.COLOR_BGR2GRAY)
        grayimg1 = cv.cvtColor(img1,cv.COLOR_BGR2GRAY)
      
        # find chessboard corners after image preparation
        retref, cornerref = cv.findChessboardCorners(grayimgref, chessBoardSize, None)
        ret1, corner1 = cv.findChessboardCorners(grayimg1, chessBoardSize, None)
      
        if retref and ret1 == True:
            objpoints.append(objp)
            cornersref = cv.cornerSubPix(grayimgref, cornerref,(11,11), (-1,-1), criteria)
            corners1 = cv.cornerSubPix(grayimg1, corner1, (11,11), (-1,-1), criteria)
          
            imgpointsref.append(cornersref)
            imgpoints1.append(corners1)
          
            cv.drawChessboardCorners(imgref, chessBoardSize, cornersref, retref)
            cv.drawChessboardCorners(img1, chessBoardSize, corners1, ret1)
            cv.imshow('imgref',imgref)
            cv.imshow('img1',img1)
            cv.waitKey(1000)
          
    cv.destroyAllWindows()

    ########################## CALIBRATION #################################################
    retref, cameraMatrixref, distref, rvecsref, tvecsref = cv.calibrateCamera(objpoints, imgpointsref, frameSize, None, None)
    print(retref)
    heightref, widthref, channelsref = imgref.shape
    newCameraMatrixref, roiref = cv.getOptimalNewCameraMatrix(cameraMatrixref, distref, (widthref,heightref), 1, (widthref,heightref))
    

    # getOptimalNewCameraMatrix is used since cv.undistort undistorts each pixel and puts it in a place where it should really be,
    # hence some pixels might go outside the image format (those spots are filled with black pixels). To fix that, 
    # getOptimalNewCameraMatrix is used to adjust those changes in the picture format we want to have undistorted.
    # This is especially important for pixel information at the edges of the picutres. This command prevents black borders
    # and retains the maximum useful information. cv.calibrateCamera does the same job, but it doesn't adjust to the 
    # image size, so there could be unwanted information loss, hence the usage of cv.getOptimalNewCameraMatrix

    ret1, cameraMatrix1, dist1, rvecs1, tvecs1 = cv.calibrateCamera(objpoints, imgpoints1, frameSize, None, None)
    print(ret1)
    height1, width1, channels1 = img1.shape
    newCameraMatrix1, roi1 = cv.getOptimalNewCameraMatrix(cameraMatrix1, dist1, (width1,height1), 1, (width1,height1))
    
    i = 0
    for imageref, image1 in zip (imagesref,images1):
        imgref = cv.imread(imageref)
        img1 = cv.imread(image1)
        grayimgref = cv.cvtColor(imgref, cv.COLOR_BGR2GRAY)
        grayimg1 = cv.cvtColor(img1,cv.COLOR_BGR2GRAY)
      
        # find chessboard corners after image preparation
        retref, cornerref = cv.findChessboardCorners(grayimgref, chessBoardSize, None)
        ret1, corner1 = cv.findChessboardCorners(grayimg1, chessBoardSize, None)

        rvecsref1 = rvecsref[i]
        rvecs11 = rvecs1[i]
        tvecsref1 = tvecsref[i]
        tvecs11 = tvecs1[i]
        if retref and ret1 == True:
            objpoints.append(objp)
            cornersref = cv.cornerSubPix(grayimgref, cornerref,(6,6), (-1,-1), criteria)
            corners1 = cv.cornerSubPix(grayimg1, corner1, (6,6), (-1,-1), criteria)
          
            imgpointsref.append(cornersref)
            imgpoints1.append(corners1)
          
            cv.drawChessboardCorners(imgref, chessBoardSize, cornersref, retref)
            cv.drawChessboardCorners(img1, chessBoardSize, corners1, ret1)
            cv.drawFrameAxes(imgref, newCameraMatrixref,distref,rvecsref1,tvecsref1, 2*size_of_chessBoard_squares_mm)
            cv.drawFrameAxes(img1,newCameraMatrix1, dist1, rvecs11, tvecs11, 2*size_of_chessBoard_squares_mm)
            cv.imshow('imgref',imgref)
            cv.imshow('img1',img1)
            cv.waitKey(1000)
            i +=1

    
    ############################## STEREO_CALIBRATION ####################################
    stereoflags = 0
    stereoflags = cv.CALIB_FIX_INTRINSIC 
    criteria_stereo = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # fixed intrinsic matrices so they are not calculated, since we can calculate the intrinsic matrices using
    # cv.calibrate for each camera seperately with better precision
    retStereo, newCameraMatrixref, distref, newCameraMatrix1, dist1, rot, trans, essentialMatrix, fundamentalMatrix = cv.stereoCalibrate(objpoints, imgpointsref, imgpoints1, newCameraMatrixref, distref, newCameraMatrix1, dist1, grayimgref.shape[::-1], criteria = criteria_stereo, flags = stereoflags)
    print(retStereo)
    print('')
    ############################## STEREO_RECTIFICATION ###################################
    rectifyscale = 1
    rectref, rect1, projMatrixref, projMatrix1, Q, roiref, roi1 = cv.stereoRectify(newCameraMatrixref, distref, newCameraMatrix1, dist1,  grayimgref.shape[::-1], rot, trans, rectifyscale, (0,0))

    stereoMapRef = cv.initUndistortRectifyMap(newCameraMatrixref, distref, rectref, projMatrixref, grayimgref.shape[::-1], cv.CV_16SC2)
    stereoMap1 = cv.initUndistortRectifyMap(newCameraMatrix1, dist1, rect1, projMatrix1, grayimg1.shape[::-1], cv.CV_16SC2)

    print('Saving data.')
    cvfile = cv.FileStorage('/home/fsb/Desktop/diplomski_opencv/stereo_calibration/stereoMap0{}.xml'.format(camnum), cv.FILE_STORAGE_WRITE)

    cvfile.write('stereoMapRef_x',stereoMapRef[0])
    cvfile.write('stereoMapRef_y',stereoMapRef[1])
    cvfile.write('stereoMap1_x',stereoMap1[0])
    cvfile.write('stereoMap1_y',stereoMap1[1])

    cvfile.release()
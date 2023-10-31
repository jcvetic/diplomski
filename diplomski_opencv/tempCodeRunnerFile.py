import numpy as np
import pickle
import pdb

a = 2; b =3
c = a + b 

objp = []
chessboardSize = (8,6) 
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32) # type: ignore
pdb.set_trace()
print(objp)

objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

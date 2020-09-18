# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 20:34:46 2019

@author: mfm160330

This file is used for calibrating the cameras (so far Back camera) every time a drive is performed
# check that the calibration label values make sense
"""

import csv
import numpy as np
import pickle
import rmsd
import argparse
import math
from scipy.spatial.transform import Rotation as R



def orient_square(loc, rotation_quat, aptag_square_length):
    sq_radius = aptag_square_length/2
    sqr = np.array([[sq_radius, sq_radius, 0], [-sq_radius, sq_radius, 0],
                    [-sq_radius, -sq_radius, 0], [sq_radius, -sq_radius, 0]])
    trans_sqr = np.zeros((4, 3))
    for i in range(0, sqr.shape[0]):
        center_offset = rotation_quat.apply(sqr[i, :])
        location = center_offset + loc
        trans_sqr[i] = location
    return trans_sqr

def make_positive(angle):
    return (angle + 2 * math.pi) % (2 * math.pi)

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("backCalib", help="BackCalibAprilTag csv file", type=str)
    parser.add_argument('RefTagsLoc', help='Saved reference tags locations pickle file', type=str)
    parser.add_argument('KabaschRotTrans', help='KabaschRotTrans.pickle Output file', type=str)

    return parser.parse_args()


args = get_args()
backCalibAprilFile = args.backCalib
refCalibFile = args.RefTagsLoc
KabaschRotTrans = args.KabaschRotTrans 

#backCalibAprilFile = "C:/Users/mfm160330/OneDrive - The University of Texas at Dallas/ADAS data/OutputFiles/D2019-7-23/FixedGaze/AprilTag_CalibBack1.csv"  #"../../output/D2019-10-30/ContGaze/AprilCalibContGaze.csv"
#refCalibFile = "C:/Users/mfm160330/OneDrive - The University of Texas at Dallas/ADAS/Spyder files/CornerPoints/MarkersAppended2019-6-20CornersAppendedStandardSorted.pickle"  # calibPickleFiles/MarkersAppended2019-6-20BackStandard.pickle#"../../config/MarkersAppended2019-6-20BackStandard.pickle"
#KabaschRotTrans = "C:/Users/mfm160330/OneDrive - The University of Texas at Dallas/ADAS data/OutputFiles/D2019-7-23/FixedGaze/KabaschRotTransTestNoCorners.pickle"   #"../../output/KabaschRotTransCont.pickle"

#====== read ID file, Shuffle it, create pathes for train and test data sets =========#
NULL_Marker = 2222
doorTags = [314, 316, 317, 318] # you should be careful about these tags (in case door or window was open)
TagConsider = 101 # Consider only all tags above this value (To ignore Cap Tags)
#### ===== Read detection IDs, hamming distance error, x,y,z of the tag  from CSV ==== ####
xCartesian, yCartesian, zCartesian = [], [], []
yawAngle, pitchAngle, rollAngle = [], [], []
hamDistErrs, detIDs = [], []
countTest = 0
with open(backCalibAprilFile, "r") as csvfile:
    next(csvfile) #skip heading
    readCSV = csv.reader(csvfile, delimiter='\t')
    for frameNum,detID,hamDistErr,dist,x,y,z,yaw,pitch,roll in readCSV:
        countTest = countTest + 1
        detIDs.append(int(detID))
        hamDistErrs.append(int(hamDistErr))
        xCartesian.append(float(x))
        yCartesian.append(float(y))
        zCartesian.append(float(z))
        yawAngle.append(make_positive(float(yaw)))
        pitchAngle.append(make_positive(float(pitch)))
        rollAngle.append(make_positive(float(roll)))
        # Need to make sure all angles are positive so that we can average them

#### ====== Put all uniques detected Tags in TagIDs ===== ####
TagIDs = np.unique(detIDs)  # get all detected tags in sorted manner
index = np.argwhere(TagIDs == NULL_Marker) 
TagIDs = np.delete(TagIDs, index) # remove the null marker from unique list of detected tags
index2 =  np.argwhere(TagIDs < TagConsider)
TagIDs = np.delete(TagIDs, index2) # remove helmet tags
#index2 = np.argwhere(TagIDs == 203)
#TagIDs = np.delete(TagIDs, index2) # remove the calibration tags in the car
index3 = np.argwhere(TagIDs == 300)
TagIDs = np.delete(TagIDs, index3) # remove tag number 300 because this is the moving outdoor AprilTag marker
print('========== Back Calibration ===================\n')
print("detctedTags are ", TagIDs, "/n")



### === Transform the columns to numpy arrays ==== ####
detIDs = np.array(detIDs) # All detected tags (column 1 in the AprilTag output)
xCartesian = np.array(xCartesian) 
yCartesian = np.array(yCartesian)
zCartesian = np.array(zCartesian)
yawAngle = np.array(yawAngle) 
pitchAngle = np.array(pitchAngle)
rollAngle = np.array(rollAngle)
hamDistErrs = np.array(hamDistErrs)

### === Remove Tags having high hamming distance error from LISTs === ###
index4 = np.argwhere(hamDistErrs > 2) 
hamDistErrs = np.delete(hamDistErrs, index4)
detIDs = np.delete(detIDs, index4) # All detected tags (column 1 in the AprilTag output)
xCartesian = np.delete(xCartesian, index4) 
yCartesian = np.delete(yCartesian, index4)
zCartesian = np.delete(zCartesian, index4)
yawAngle = np.delete(yawAngle, index4) 
pitchAngle = np.delete(pitchAngle, index4) 
rollAngle = np.delete(rollAngle, index4) 


### ==== Intialize all the variables in current video to all zeros ==== ####
xAvgCurrent = np.zeros(len(TagIDs)) 
yAvgCurrent = np.zeros(len(TagIDs)) 
zAvgCurrent = np.zeros(len(TagIDs)) 
yawAvgCurrent = np.zeros(len(TagIDs)) 
pitchAvgCurrent = np.zeros(len(TagIDs)) 
rollAvgCurrent = np.zeros(len(TagIDs)) 
numElem = np.zeros(len(TagIDs)) 


for i1 in range(len(TagIDs)):
 
    IDOneTag = np.array(np.where(detIDs == TagIDs[i1]))
    if IDOneTag.shape[1] == 0:
        # All detections of this tag do not meet the requirements (door was open or high hamming errors)
        continue
    else:
        xOneTag = xCartesian[IDOneTag]
        yOneTag = yCartesian[IDOneTag]
        zOneTag = zCartesian[IDOneTag]
        yawOneTag = yawAngle[IDOneTag]
        pitchOneTag = pitchAngle[IDOneTag]
        rollOneTag = rollAngle[IDOneTag]
        
        
        xAvgCurrent[i1] = np.average(xOneTag[0]).T #X value of the label in current video
        yAvgCurrent[i1] = np.average(yOneTag[0]).T
        zAvgCurrent[i1] = np.average(zOneTag[0]).T
        yawAvgCurrent[i1] = np.average(yawOneTag[0]).T
        pitchAvgCurrent[i1] = np.average(pitchOneTag[0]).T
        rollAvgCurrent[i1] = np.average(rollOneTag[0]).T



#======= Calculating the corner points location ====================#
TagIDs_c = TagIDs #with corners
for i1 in range(len(TagIDs)):
        
    points = (xAvgCurrent[i1], yAvgCurrent[i1], zAvgCurrent[i1])
    rot = (yawAvgCurrent[i1], pitchAvgCurrent[i1], rollAvgCurrent[i1]) # rotations
    rot_quat = R.from_euler('xyz', rot) #rotations in quertonians
        
    corners = orient_square(points, rot_quat, .02)
    
    for i2 in range(0, 4):
        corner = corners[i2]
        TagIDs_c = np.append(TagIDs_c,[TagIDs[i1]*10 + (i2 + 1)])
        xAvgCurrent = np.append(xAvgCurrent, [corner[0]])
        yAvgCurrent = np.append(yAvgCurrent, [corner[1]])
        zAvgCurrent = np.append(zAvgCurrent, [corner[2]])
    

        
numElem[i1] = xOneTag.shape[1]
assert (xAvgCurrent.shape[0] >= 3), "Error: Less than 3 calibration tags are detected in calibration video. Repeat calibration"
# Kabach Algorithm needs at least 3 reference tags to work
     

XYZcurrent = np.vstack((xAvgCurrent, yAvgCurrent, zAvgCurrent)).T
print("detected IDs = ",TagIDs)
print("x = ",xAvgCurrent)
print("y = ",yAvgCurrent)
print("z= ",zAvgCurrent)
print("number of detected tags for each ID is", numElem)

#======== load the saved labels locations ===========#
pickle_in = open(refCalibFile,"rb")
labelIDsUni = pickle.load(pickle_in)

index = np.argwhere(labelIDsUni < 300 )
index2 = np.argwhere(labelIDsUni > 400 )
index = np.append(index,index2)
labelIDsRef = labelIDsUni[index]   # detected labels in reference video
#print("IDs = ", labelIDsRef, '/n')

XlabelRef = pickle.load(pickle_in)[index] # X values of the labels in reference video
YlabelRef = pickle.load(pickle_in)[index] # Y values of the labels in ref video
ZlabelRef = pickle.load(pickle_in)[index]
#print("XlabelRef = ",XlabelRef, '/n')
#print("YlabelRef = ",YlabelRef, '/n')
#print("ZlabelRef = ",ZlabelRef, '/n')

XYZref = np.vstack((XlabelRef, YlabelRef, ZlabelRef)).T



#print('DoubleIndx =', DoubleIndx, '\n')

# Get indicies of Tags detected in ref video and in current video
# Since the labels are sorted in both arrays, this method works
#DoubleIndx = np.argwhere(labelIDsRef == TagIDs_c) # 
indxRef = np.nonzero(np.in1d(labelIDsRef, TagIDs_c))[0] 
indxCurr = np.nonzero(np.in1d(TagIDs_c, labelIDsRef))[0]

XYZref = XYZref[ indxRef,:] 
XYZcurrent = XYZcurrent[indxCurr,:] 
print('XYZref =', XYZref, '\n')
print('XYZcurrent =', XYZcurrent, '\n')
##=============== rmsd.kabsh requires the point sets to be of size m x D, ====================== ###
# where m is the number of points, D is the cartesian dimension "D=3 in our case"
C_curr = rmsd.centroid (XYZcurrent)
C_ref = rmsd.centroid (XYZref)
print('C_curr =', C_curr, '\n')
print('C_ref =', C_ref, '\n')



XYZcurr_centered = XYZcurrent - C_curr  #XYZ current after centering 
XYZref_centered = XYZref - C_ref
print('XYZcurr_centered =', XYZcurr_centered, '\n')
print('XYZref_centered =', XYZref_centered, '\n')

R = rmsd.kabsch(XYZcurr_centered, XYZref_centered) # the optimal rotation matrix to rotate XYZcurrent to XYZref
print('R =', R, '\n')

#CurrUpdate = np.dot(avg_mesh - C_curr, R) + C_ref
## ========================= ###

##### save R, C_curr, C_ref to use in labeling script 
pickle_out = open(KabaschRotTrans,"wb")
pickle.dump(R, pickle_out)
pickle.dump(C_curr, pickle_out)
pickle.dump(C_ref, pickle_out)
pickle.dump(XYZcurrent, pickle_out)
pickle.dump(numElem,pickle_out)
pickle_out.close()
print('=========End of back calibration =================')


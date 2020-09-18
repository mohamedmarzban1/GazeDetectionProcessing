import tensorflow as tf
import sys
sys.path.insert(0, '/home/marzban/calibrateCameras/naofal-lab/visualize_2')

import Visualize_2
import kabsch_move_road_to_back
import Calibration, standardize_visualizeT2, standardize_road, unify_road_and_head, move_to_reference

OutputFolderName = 'D2019-7-23Test/ContGaze'
OutputsDir = "../../../outputs/"
configDir = "../../config"
VisualizeDir = "../../visualize_2"

STD_ROAD = OutputsDir + OutputFolderName + "/road_normalized.csv"
STD_VIS = OutputsDir + OutputFolderName + "/visualize_framesT2.csv"

AP_ROAD = OutputsDir + OutputFolderName + "/AprilRoadOutdoor2.csv"
AP_HAT_Calib_BACK = OutputsDir + OutputFolderName + "/AprilHatContGaze.csv"
AP_Road_calib = OutputsDir + OutputFolderName + "/AprilRoadCalib.csv" ####### NOT Ready yet

# pickle files have the reference maerkers + corner points location
Ref_Calib_Back = configDir + "/MarkersAppended2019-6-20BackStandard.pickle"  #"config/BackCalibAll2019-6-20Rmv300.pickle"
Ref_Calib_Road = configDir + "/MarkersRoadRef2019-6-20StandardCornersAppended.pickle"

# Rotation and Translation matrices for Transformation between current coordinates and reference coordinates
KabaschRotTransBack = OutputsDir + "/KabaschRotTransBack.pickle"
KabaschRotTransBack = OutputsDir + "/KabaschRotTransRoad.pickle"

# Output files
OP_R2B = OutputsDir + "/road_proj_to_back.csv"
OP_FACE = OutputsDir + "/ContGazeIntialLabelsAllFrames.csv"
OP_VIS = VisualizeDir + "/meshsave_back_2.mat"
OutDoorTagID = 300
B_R_offset = 0 # sync Offset in frame number between the back and the road videos
F_offset = 0




print("Calculating center of mass Output to ", OP_VIS)

Visualize_2("../"+HAT_BACK)

#kabsch_move_road_to_back(AP_ROAD)


print("Calculating the rotation and translation matrices for the back camera")
# outputs the rotation and translation matrices required to calibrate the back camera
Calibration(AP_HAT_Calib_BACK, Ref_Calib_Back, KabaschRotTrans)


print("Calculating the rotation and translation matrices for the road camera")
# outputs the rotation and translation matrices required to calibrate the road camera
Calibration(AP_HAT_Calib_BACK, Ref_Calib_Back, KabaschRotTrans) 


standardize_visualizeT2(HAT_BACK, OP_VIS)

print("Standardizing $OP_R2B by considering only AprilTag marker frames and changing file schema")
standardize_road(OP_R2B, OutDoorTagID)

print("Move COM and outdoor tag to reference coordinates by appling Kabash algorithm on the obtained transformation matrices")
move_to_reference (A_com, B_com)

move_to_reference (A_road, B_road)

print("Extracting viable face frames by combining visualize_frames.csv & road_normalized.csv")
unify_road_and_head(STD_VIS, STD_ROAD, B_R_offset)

print("Projecting road distance vectors to the back camera using the sync frames defined in move_back_to_road.py. Output to $OP_R2B")
#kabsch_move_road_to_back(AP_ROAD)

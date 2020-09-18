from Calibration import Calibration
from standardize_visualizeT2 import standardize_visualizeT2
from standardize_roadT2 import standardize_roadT2
from move_to_reference import move_to_reference
from unify_road_and_head_T2 import unify_road_and_head_T2


OutputFolderName = '2019-11-14-001/contGaze'
OutputsDir = "/media/sf_UbuntuWinShare/"
configDir = "../../config"
VisualizeDir = "../../visualize_2"

# AprilTag files
AP_ROAD = OutputsDir + OutputFolderName + "/AprilRoadOutdoor2.csv"
AP_HAT_Calib_BACK = OutputsDir + OutputFolderName + "/AprilHatContGaze.csv"
AP_Road_calib = OutputsDir + OutputFolderName + "/AprilRoadCalib.csv" ####### NOT Ready yet

# pickle files have the reference maerkers + corner points location
Ref_Calib_Back = configDir + "/BackMarkers2019-6-20CornersSorted.pickle" #"/MarkersAppended2019-6-20BackStandard.pickle"  #"config/BackCalibAll2019-6-20Rmv300.pickle"
Ref_Calib_Road = configDir + "/MarkersRoadRef2019-6-20StandardCornersAppended.pickle"
# Rotation and Translation matrices for Transformation between current coordinates and reference coordinates
KabaschRotTransBack = OutputsDir + OutputFolderName + "/KabaschRotTransBack.pickle"
KabaschRotTransRoad = OutputsDir + OutputFolderName + "/KabaschRotTransRoad.pickle"
KabaschRotTransRefRoadToRefBack = configDir + "/KabaschRotTransRefRoadToRefBack.pickle" ### Not Ready yet

# standardized files
STD_VIS = OutputsDir + OutputFolderName + "/visualize_framesT2.csv"
STD_ROAD = OutputsDir + OutputFolderName + "/road_normalized.csv"
REF_VIS = OutputsDir + OutputFolderName + "/visualize_frames_ref.csv"
REF_ROAD = OutputsDir + OutputFolderName + "/road_normalized_ref.csv"

# Output files
OP_R2B = OutputsDir + OutputFolderName + "/road_proj_to_back.csv"
OP_intialLabeling = OutputsDir + OutputFolderName + "/ContGazeIntialLabelsAllFrames.csv"
OP_VIS = VisualizeDir + "/meshsave_back_2.mat"
OutDoorTagID = 300
B_R_offset = 0 # sync Offset in frame number between the back and the road videos
F_offset = 0
noRotationFlag = 1 

print("Calculating the rotation and translation matrices for the back camera")

Calibration(AP_HAT_Calib_BACK, Ref_Calib_Back, KabaschRotTransBack, OutDoorTagID, noRotationFlag)

print("Calculating the rotation and translation matrices for the road camera")
Calibration(AP_Road_calib, Ref_Calib_Road, KabaschRotTransRoad, OutDoorTagID, noRotationFlag) 

print("Standardizing visualize and converting coordinates back to AprilTag format")
standardize_visualizeT2(AP_HAT_Calib_BACK, OP_VIS, STD_VIS)

print("Standardizing AP_ROAD by considering only AprilTag marker frames and changing file schema")
standardize_roadT2(AP_ROAD, STD_ROAD, OutDoorTagID)

print("Move COM reference coordinates by appling Kabash algorithm on the obtained transformation matrices\n")
move_to_reference (STD_VIS, REF_VIS, KabaschRotTransBack)

print("Move outdoor tag to reference coordinates by appling Kabash algorithm on the obtained transformation matrices\n")
move_to_reference (STD_ROAD, REF_ROAD, KabaschRotTransRoad)

print("Extracting viable face frames by combining visualize_frames.csv & road_normalized.csv and transforms outdoorTag to back camera coordinates")
unify_road_and_head_T2(REF_VIS, REF_ROAD, B_R_offset, OP_intialLabeling, KabaschRotTransRefRoadToRefBack)

print("Finished labelling subject")

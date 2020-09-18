STD_ROAD="output/road_normalized.csv"
STD_VIS="output/visualize_frames.csv"

AP_BACK="output/D2019-10-31/ContGaze/AprilBackOutdoor.csv"
AP_ROAD="output/D2019-10-31/ContGaze/AprilRoadOutdoor.csv"
AP_HAT_Calib_BACK="output/D2019-10-31/ContGaze/AprilHatContGaze.csv"
AP_Road_calib="output/D2019-10-31/ContGaze/AprilRoadCalib.csv"

Ref_Calib_Back="config/MarkersAppended2019-6-20BackStandard.pickle"  #"config/BackCalibAll2019-6-20Rmv300.pickle"
KabaschRotTrans="output/KabaschRotTransCont.pickle"

OP_R2B="output/road_proj_to_back.csv"
OP_FACE="output/ContGazeIntialLabelsAllFrames.csv"
OP_VIS="visualize_2/meshsave_back_2.mat"
OutDoorTagID="300"
B_R_offset="0" # sync Offset in frame number between the back and the road videos
F_offset="0"



cd visualize_2/
echo "Calculating center of mass. Output to $OP_VIS"
python3 Visualize_2.py "../$HAT_BACK" &
cd ..

wait

#echo "Projecting road distance vectors to the back camera using the sync frames defined in move_back_to_road.py. Output to $OP_R2B"
#python3 apriltags/scripts/kabsch_move_road_to_back.py $AP_ROAD

#wait

echo "Calculating the rotation and translation matrices for the back camera"
# outputs the rotation and translation matrices required to calibrate the back camera
python3 apriltags/scripts/Calibration.py "$AP_HAT_Calib_BACK" "$Ref_Calib_Back" "$KabaschRotTrans"  & 


echo "Calculating the rotation and translation matrices for the road camera"
# outputs the rotation and translation matrices required to calibrate the road camera
python3 apriltags/scripts/Calibration.py "$AP_HAT_Calib_BACK" "$Ref_Calib_Back" "$KabaschRotTrans"  & 


echo "Standardizing visualize_2 output by writing pose_all matrix from meshsave to a csv file & adding a frame column"
python3 apriltags/scripts/standardize_visualizeT2.py    $AP_HAT_Calib_BACK $OP_VIS &

echo "Standardizing $OP_R2B by considering only AprilTag marker frames and changing file schema"
python3 apriltags/scripts/standardize_road.py $OP_R2B $OutDoorTagID &

wait

# Move COM and outdoor tag to reference coordinates by appling Kabash algorithm on the obtained transformation matrices
echo "Move COM and outdoor tag to reference coordinates by appling Kabash algorithm on the obtained transformation matrices"

python3 apriltags/scripts/move_to_reference.py $A_com $B_com  #modifyMe

python3 apriltags/scripts/move_to_reference.py $A_road $B_road #modifyMe


echo "Extracting viable face frames by combining visualize_frames.csv & road_normalized.csv"
# Extracting viable face frames by combining visualize_frames.csv & road_normalized.csv, also transforms visualize frames to AprilTag coordinates
python3 apriltags/scripts/unify_road_and_headT2.py      $STD_VIS     $STD_ROAD  $B_R_offset

wait






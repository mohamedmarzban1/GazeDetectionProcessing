#!/bin/bash
#if [ $# -lt 1 ]; then
#    echo "Usage: $0 <back video path>" >&2
#    exit 1
#fi

videosPath="/media/sf_UbuntuWinShare/2019-10-31"
BackVideo="$videosPath/GH030163.MP4" 
OutputsPath="$videosPath/FixedGaze"

HAT_BACK="$OutputsPath/AprilTag_Hat1.csv"
OP_VIS="meshsave_back_2.mat"
AprilTag_Calib_Back="$OutputsPath/AprilTag_CalibBack1.csv"
Ref_Calib_Back="config/BackReference0.032Corners_sorted.pickle" #"config/MarkersAppended2019-6-20BackStandard.pickle"
KabaschRotTrans="$OutputsPath/KabaschRotTrans.pickle"



APRIL_TAG=./apriltags/build/bin/apriltags_demo




#=============== Runs AprilTag with Back behind the scenes for cap
$APRIL_TAG -F 1000 -W 1920 -H 1080 -S 0.032 -I "$BackVideo" -O "$HAT_BACK" -f -d & 

wait

cd visualize_3/ #we have to enter visualize_2 directory because files are saved there
echo "Calculating center of mass. Output to $OP_VIS"
python3 Visualize_2.py "$HAT_BACK" &
wait
cp $OP_VIS $OutputsPath


wait
cd ..
echo "Standardizing visualize_2 output by writing pose_all matrix from meshsave to a csv file & adding a frame column"
python3 apriltags/scripts/standardize_visualize.py    $HAT_BACK "$OutputsPath/$OP_VIS"

#=========== Calibrate the back camera to obtain the transformation rotation and trasnlation mastrices 
echo "Calculating transformation matrices w.r.t the reference saved back coordinates and outputting to $KabaschRotTrans"
cd apriltags/scripts/
python3 Calibration.py "$HAT_BACK" "../../$Ref_Calib_Back" "$KabaschRotTrans"  & 




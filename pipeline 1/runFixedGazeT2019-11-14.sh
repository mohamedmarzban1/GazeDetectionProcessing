

####N.B.: Manually set the start and end frame of the calibration in this script
declare -i BackStart=151795
declare -i BackEnd=174014
declare -i noRotationFlag=0

videosPath="/media/sf_UbuntuWinShare/2019-11-22-001"
BackVideo="$videosPath/back.mp4" 
OutputsPath="$videosPath/FixedGaze"


AP_BackHatCalib="$OutputsPath/AprilHatFixedGaze.csv"
OP_VIS="meshsave_back_2.mat"
STD_VIS="$OutputsPath/visualize_framesT2.csv"
Ref_Calib_Back="/home/marzban/calibrateCameras/naofal-lab/config/BackMarkers2019-6-20CornersSorted.pickle"
#"config/MarkersAppended2019-6-20CornersAppendedStandardSorted.pickle" MarkersAppended2019-6-20BackStandard.pickle"
KabaschRotTrans="$OutputsPath/KabaschRotTrans.pickle"

APRIL_TAG=./build/bin/apriltags_demo



# checks if output folder exists

if [ ! -d "$OutputsPath" ]; then
    echo "Creating output folder."
    mkdir $OutputsPath
fi


#=============== Runs AprilTag with Back behind the scenes for cap and calibration
cd apriltags
$APRIL_TAG -F 1000 -W 1920 -H 1080 -S 0.032 -I $BackVideo -O "$AP_BackHatCalib" -b $BackStart -e $BackEnd -d -f & 

wait

cd ../visualize_3/ #we have to enter visualize_3 directory because files are saved there
echo "Calculating center of mass. Output to $OP_VIS"
python3 Visualize_2.py "$AP_BackHatCalib" &
cp $OP_VIS $OutputsPath


wait
cd ..
echo "Calculating transformation matrices w.r.t the reference saved back coordinates and outputting to $KabaschRotTrans" 
echo "Standardizing visualize_2 output by writing pose_all matrix from meshsave to a csv file & adding a frame column"
python3 apriltags/scriptsPythonWrapper/fixedGazeWrapper.py "$AP_BackHatCalib" $Ref_Calib_Back "$KabaschRotTrans" "visualize_3/$OP_VIS" $STD_VIS $BackStart


#python3 apriltags/scriptsPythonWrapperCalibration.py "$AP_BackHatCalib", "../../$Ref_Calib_Back", "$KabaschRotTransBack" & 
#python3 apriltags/scriptsPythonWrapper/standardize_visualizeT2.py    $AP_BackHatCalib "visualize_3/$OP_VIS" $STD_VIS $BackStart

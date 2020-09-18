


# Run AprilTags on back-outdoor, back-cap and road-outdoor cameras
#tags sizes
#a- calibration and Cap: 0.032
#b- Outdoor tag: 0.16

videosPath="/media/sf_UbuntuWinShare/2019-12-06-001" 
declare -i BackStart=20586
declare -i BackEnd=41364
declare -i RoadStart=20586
declare -i RoadEnd=41364

OutputsPath="$videosPath/contGaze"
BackVideo="$videosPath/back.mp4"
RoadVideo="$videosPath/road.mp4"

echo "$BackVideo"

AP_BackOutdoor="$OutputsPath/AprilBackOutdoorT2.csv"
AP_BackHatCalib="$OutputsPath/AprilHatContGaze.csv"
AP_RoadOutdoor="$OutputsPath/AprilRoadOutdoor2.csv"
AP_RoadCalib="$OutputsPath/AprilRoadCalib.csv"

OP_VIS="meshsave_back_2.mat"

# checks if output folder exists
if [ ! -d "$OutputsPath" ]; then
    echo "Creating output folder."
    mkdir $OutputsPath
fi

cd apriltags

# Back camera to detect the Hat and calibration
./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -b $BackStart -e $BackEnd -I "$BackVideo" -O "$AP_BackHatCalib" -f -d &


# Back camera for calibration
#####./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.04 -I "/home/marzban/Downloads/2019-10-31/BContGaze.mp4" -O /home/marzban/calibrateCameras/naofal-lab/output/2019-10-31/ContGaze/AprilCalibContGaze.csv -f -d &

# Road camera to detect the outdoor AprilTag
./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.16 -b $RoadStart -e $RoadEnd  -I "$RoadVideo" -O "$AP_RoadOutdoor" -f -d &

# Road camera for calibration
./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -b $RoadStart -e $RoadEnd -I "$RoadVideo" -O "$AP_RoadCalib" -f -d 

# Back camera to detect the outdoor AprilTag
#(shouldn't be used in new transformation, but running it in case I wanted to go back to old transformation)
#./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.16 -I "$BackVideo" -O "$AP_BackOutdoor" -f -d &

wait

echo "Finished running all 3 files"

cd ../visualize_2/
echo "Calculating center of mass. Output"
python3 Visualize_2.py "$AP_BackHatCalib" &
cp $OP_VIS $OutputsPath
cd ..


                                                                

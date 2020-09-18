# Run AprilTags on back-outdoor, back-cap and road-outdoor cameras
#tags sizes
#a- calibration and Cap: 0.032
#b- Outdoor tag: 0.16

echo "Starting Cont Gaze processing"
declare -a dataSets=("2019-12-05-001" "2019-11-22-002" "2019-11-18-001" "2019-11-16-001") #("2020-03-06-002" "2019-12-09-001" "2019-12-07-001" "2019-11-19-001") #("2019-10-03-001" "2019-10-02-001") #("2020-02-26-001" "2020-02-27-001" "2020-02-29-001" "2020-03-05-001" "2020-03-11-001")  
BackStartAll=(1 1 1 1) #
BackEndAll=(3600 3600 3600 3600) #
RoadStartAll=(14532 13855 16330 13366) #(15688 26665 28897 16490 11992) #
RoadEndAll=(35780 33807 36749 34425) #(36321 47551 44596 37398 32642) #

index=0
for dataset in ${dataSets[@]}; 
do
    videosPath="/media/sf_Gdataset/$dataset" 
    OutputsPath="$videosPath/ContGaze"
    BackVideo="$videosPath/back.mp4"
    RoadVideo="$videosPath/road.mp4"

    BackStart=${BackStartAll[index]}
    BackEnd=${BackEndAll[index]}
    RoadStart=${RoadStartAll[index]}
    RoadEnd=${RoadEndAll[index]}
	
    RoadEndCalib=`expr $RoadStart + 3600`
    echo "$RoadEndCalib"

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

    ## Back camera to detect the Hat and calibration
    ./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -b $BackStart -e $BackEnd -I "$BackVideo" -O "$AP_BackHatCalib" -f -d &


    ## Road camera to detect the outdoor AprilTag
    ./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.16 -b $RoadStart -e $RoadEnd  -I "$RoadVideo" -O "$AP_RoadOutdoor" -f -d &

    ## Road camera for calibration
    ./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -b $RoadStart -e $RoadEndCalib -I "$RoadVideo" -O "$AP_RoadCalib" -f -d &

    ### Back camera to detect the outdoor AprilTag
    ###(shouldn't be used in new transformation, but running it in case I wanted to go back to old transformation)
    ###./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.16 -I "$BackVideo" -O "$AP_BackOutdoor" -f -d &

    wait

    echo "Finished running all 3 files"

    
    cd ..

    ((index=index+1))

done

echo "Finished All Subjects"
                                                                

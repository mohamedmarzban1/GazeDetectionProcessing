


# Run AprilTags on back-outdoor, back-cap and road-outdoor cameras
#tags sizes
#a- calibration and Cap: 0.032
#b- Outdoor tag: 0.16

echo "Starting Cont Gaze processing"
declare -a dataSets=("2019-11-12-001" "2019-11-08-001" "2019-11-06-001" "2019-10-11-001") #("2019-12-10-001" "2019-11-05-001" "2019-10-03-02") #("2020-02-19-001" "2020-02-18-001" "2020-01-23-001")  
BackStartAll=(1 1 1 1) #(1 1 1) 
BackEndAll=(3600 3600 3600 3600) #(3600 3600 3600) 
RoadStartAll=(21266 15139 12905 27704) #(14197 21012 15724) 
RoadEndAll=(38926 31994 26088 40351) #(35566 36548 36618) 

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
    ./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -b $RoadStart -e $RoadEnd -I "$RoadVideo" -O "$AP_RoadCalib" -f -d &

    ### Back camera to detect the outdoor AprilTag
    ###(shouldn't be used in new transformation, but running it in case I wanted to go back to old transformation)
    ###./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.16 -I "$BackVideo" -O "$AP_BackOutdoor" -f -d &

    wait

    echo "Finished running all 3 files"

    
    cd ..

    ((index=index+1))

done

echo "Finished All Subjects"
                                                                

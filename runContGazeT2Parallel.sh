


# Run AprilTags on back-outdoor, back-cap and road-outdoor cameras
#tags sizes
#a- calibration and Cap: 0.032
#b- Outdoor tag: 0.16

echo "Starting Cont Gaze processing"
declare -a dataSets=("2020-02-08-001" "2020-02-10-001" "2020-02-14-001")  #("2020-02-10-001" "2020-02-14-001" "2020-02-22-001" "2020-03-12-001" "2019-12-06-001") 
BackStartAll=(18050 13568 16031) #(13568 16031 16252 17433 20951)
BackEndAll=(18090 13598 16041) #(36717 34067 37114) #(3600) #(34067 37114 37951 37177 41729)
RoadStartAll=(18302 13726 16537) #(12678) #(13726 16537 15935 17703 20586)
RoadEndAll=(36969 34225 37620) #(33510) #(34225 37620 37634 37447 41364)

index=0
for dataset in ${dataSets[@]}; 
do
    videosPath="/media/sf_DatasetInDrive/$dataset" 
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
    #./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -b $BackStart -e $BackEnd -I "$BackVideo" -O "$AP_BackHatCalib" -f -d &
    ./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -b $BackStart -e $BackEnd -I "$BackVideo" -O "$AP_BackHatCalib" -f &

    ## Road camera to detect the outdoor AprilTag
    #./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.16 -b $RoadStart -e $RoadEnd  -I "$RoadVideo" -O "$AP_RoadOutdoor" -f -d &


    ## Road camera for calibration
    #./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -b $RoadStart -e $RoadEnd -I "$RoadVideo" -O "$AP_RoadCalib" -f -d &






    ### Back camera to detect the outdoor AprilTag
    ###(shouldn't be used in new transformation, but running it in case I wanted to go back to old transformation)
    ###./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.16 -I "$BackVideo" -O "$AP_BackOutdoor" -f -d &

    wait

    echo "Finished running all 3 files"

    cd ../visualize_3/
    echo "Calculating center of mass. Output"
    python3 Visualize_2.py "$AP_BackHatCalib" &

    wait
    echo "Copying COM file"
    cp $OP_VIS $OutputsPath

    
    cd ..

    ((index=index+1))

done

echo "Finished All Subjects"
                                                                

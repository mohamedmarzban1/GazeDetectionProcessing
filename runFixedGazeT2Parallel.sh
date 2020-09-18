
declare -i noRotationFlag=0
####N.B.: Manually set the start and end frame of the calibration in this script
BackStartAll=(146160 150679 141740 128341 129252 146160 146160 146160 146160 146160 146160 146160 146160 146160 146160 146160 146160 146160 146160 146160 )  
BackEndAll=(172945 191544 171262 153083 166048 146160 146160 146160 146160 146160 146160 146160 146160 146160 146160 146160 146160 146160 146160 146160)
declare -a dataSets=("2019-05-22" "2019-07-23" "2019-05-30" "2019-06-11" "2019-06-14" "2019-07-09" "2019-07-10" "2019-07-11" "2019-07-15"  "2019-10-03" "2019-10-03-02" "2019-10-31" "2019-11-05") #("2019-12-06-001" "2020-01-18-001" "2020-01-24-001" "2020-01-25-001" "2020-01-27-001" "2020-01-28-001" "2020-02-01-001" "2020-02-07-001" "2020-02-08-001" "2020-02-10-001" "2020-02-14-001" "2020-02-22-001" "2020-03-12-001" ) #"2019-11-14-001" "2019-11-19-002" "2019-11-20-001" "2019-11-22-001" "2019-11-25-001" 

index=0
for dataset in ${dataSets[@]}; 
do 
    echo "dataset is $dataset"
    videosPath="/media/sf_UbuntuWinShare/$dataset"
    BackStart=${BackStartAll[index]}
    BackEnd=${BackEndAll[index]}
    BackVideo="$videosPath/back.mp4" 
    OutputsPath="$videosPath/FixedGaze"


    AP_BackHatCalib="$OutputsPath/AprilTag_Hat.csv" #AprilHatFixedGaze.csv"
    OP_VIS="meshsave_back_2.mat"
    STD_VIS="$OutputsPath/visualize_framesT2.csv"
    Ref_Calib_Back="/home/marzban/calibrateCameras/naofal-lab/config/BackReference0.032Corners_sorted.pickle" #"/home/marzban/calibrateCameras/naofal-lab/config/BackMarkers2019-6-20CornersSorted.pickle"
    KabaschRotTrans="$OutputsPath/KabaschRotTrans0.032.pickle" #KabaschRotTrans.pickle

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
    ((index=index+1))

done

echo "Finished All Subjects"



DataFolder="/media/sf_UbuntuWinShare/"

cd apriltags

#./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "/media/sf_UbuntuWinShare/refRoad/R1.MP4" -O "/media/sf_UbuntuWinShare/refRoad/AprilRoadref.csv" -f -d 

# Road camera to detect the outdoor AprilTag
./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-05-30/RContGaze.mp4" -O "${DataFolder}2019-05-30/AprilRoadCalib.csv" -f -d &

./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-06-11/RContGaze.mp4" -O "${DataFolder}2019-06-11/AprilRoadCalib.csv" -f -d &

wait

./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-06-14/RContGaze.mp4" -O "${DataFolder}2019-06-14/AprilRoadCalib.csv" -f -d &

./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-06-21/RContGaze.mp4" -O "${DataFolder}2019-06-21/AprilRoadCalib.csv" -f -d &

wait

./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-07-09/RContGaze.mp4" -O "${DataFolder}2019-07-09/AprilRoadCalib.csv" -f -d &

./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-07-10/RContGaze.mp4" -O "${DataFolder}2019-07-10/AprilRoadCalib.csv" -f -d &

wait

./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-07-11/RContGaze.mp4" -O "${DataFolder}2019-07-11/AprilRoadCalib.csv" -f -d &

./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-07-15/RContGaze.mp4" -O "${DataFolder}2019-07-15/AprilRoadCalib.csv" -f -d &

wait

./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-07-19/RContGaze.mp4" -O "${DataFolder}2019-07-19/AprilRoadCalib.csv" -f -d &



#wait

./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-08-27/RContGaze.mp4" -O "${DataFolder}2019-08-27/AprilRoadCalib.csv" -f -d &

#######./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-07-23/RContGaze.mp4" -O "${DataFolder}2019-07-23/AprilRoadCalib.csv" -f -d &

#######./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-10-30/RContGaze.mp4" -O "${DataFolder}2019-10-30/AprilRoadCalib.csv" -f -d &

#######./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "${DataFolder}2019-10-31/RContGaze.mp4" -O "${DataFolder}2019-10-31/AprilRoadCalib.csv" -f -d &

wait 

echo "Finished running all files"


                                                                

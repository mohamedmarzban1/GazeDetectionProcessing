 
videosPath="/media/sf_UbuntuWinShare/2019-05-22" 
RoadVideo="$videosPath/GH020301.MP4" # /RContGaze.mp4

cd apriltags

./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -b 18000 -e 21600  -I "$RoadVideo" -O "/media/sf_UbuntuWinShare/2019-05-22/AprilRoadCalib.csv" -f -d &

#./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.032 -I "$RoadVideo" -O "/media/sf_UbuntuWinShare/2019-05-22/AprilRoadCalib.csv" -f -d &

#./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.176 -I "$RoadVideo" -O "/media/sf_UbuntuWinShare/2019-05-22/AprilRoadOutdoor100.csv" -f -d &

#./build/bin/apriltags_demo -F 1000 -W 1920 -H 1080 -S 0.16 -I "$RoadVideo" -O "/media/sf_UbuntuWinShare/2019-05-22/AprilRoadOutdoor300.csv" -f -d

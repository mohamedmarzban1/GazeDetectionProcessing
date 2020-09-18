#runAprilTagsForMirrorCamera


videosPath="/media/sf_dataset/2020-02-07-001"
mirrorVideo="$videosPath/mirror.mp4" 
startFrame=1 
endFrame=100
mirrorOutput="$videosPath/AprilTag_mirror2.csv"

APRIL_TAG=./apriltags/build/bin/apriltags_demo

$APRIL_TAG -F 1000 -W 1920 -H 1080 -S 0.032 -I "$mirrorVideo" -O "$mirrorOutput" -b $startFrame -e $endFrame -f & 

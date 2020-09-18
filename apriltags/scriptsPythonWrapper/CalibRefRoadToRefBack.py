from Calibration import Calibration


configDir = "../../config"
Ref_Calib_Back = configDir + "/BackReference0.032Corners_sorted.pickle" 
AP_Road_32 = "/media/sf_UbuntuWinShare/refRoad/AprilRoadRef.csv"
KabaschRotTransBack = configDir + "/KabaschRotTransRefRoadToRefBack32.pickle"
OutDoorTagID = 300  
noRotationFlag = 0

Calibration(AP_Road_32, Ref_Calib_Back, KabaschRotTransBack, OutDoorTagID, noRotationFlag)

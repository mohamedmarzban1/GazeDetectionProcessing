import argparse

import pandas as pd



def standardize_roadT2(AP_ROAD_file_path, STD_ROAD_file_path, apriltag_id):
    print("Normalizing", AP_ROAD_file_path)
    
    STD_output = open(STD_ROAD_file_path, 'w+')
    header = "frameId\tdetectionId\tdistance\tx\ty\tz\n"
    STD_output.write(header)
    
    df_AP_Road = pd.read_csv(AP_ROAD_file_path, sep='\t')
    rows = len(df_AP_Road)
    df_AP_Road = df_AP_Road.T
    
    last_frame = -1
    row_counter = 0
    null_row = "nan    0.0    0.0    0.0    0.0"  
    #frame id    detection id    hamming distance    distance    x    y    z    yaw    pitch    roll
    while row_counter < rows:
        row = df_AP_Road[row_counter]
        frameId = int(row['frame id'])
        detectId = int(row['detection id'])
        
        if detectId == apriltag_id:
            for i in range(last_frame+1, frameId):
                STD_output.write(str(i) + '\t' + null_row + '\n')
            last_frame = frameId
            STD_output.write(str(frameId) + '\t' + str(detectId) + '\t' + str(row['distance']) + '\t' + str(row['x']) + '\t' + str(row['y']) + '\t' + str(row['z']) + '\n')

        row_counter = row_counter + 1



    
    
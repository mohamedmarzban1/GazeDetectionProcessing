import argparse
import csv

import numpy as np
import pandas as pd
import scipy.io as sio
import pickle

POSE_MATRIX_NAME = "pose_all"

def parse_kabsch_transform_dump(dump_path):
    transform = open(dump_path, "rb")

    rot = pickle.load(transform)
    print('rotation = ',rot,'\n')
    c_curr = pickle.load(transform)
    print('c_curr = ',c_curr,'\n')
    c_goal = pickle.load(transform)
    print('c_goal = ',c_goal,'\n')
    
    return (rot, c_curr, c_goal)

def apply_kabsch_tfm(vec, transform):
    (rot, c_curr, c_goal) = transform

    return np.matmul(rot, vec - c_curr) + c_goal


"""
    Takes in pos which is a 3 tuple representing
        (x, y, z)
    Returns a new tuple (r, phi, theta) which is the spherical
        representation of (x,y,z)
    - r is the magnitude of the vector
    - phi is the angle between the vector and the z+ axis, where a vector along z+ has a phi of 0 
    - theta is the right-handed rotation along the xy plane (rotation around the z+ axis)
"""
def calc_spherical(pos):
    xy = pos[0]**2 + pos[1]**2 

    sph = np.zeros(3)
    sph[0] = np.sqrt(xy + pos[2]**2) #
    #sph[1] = np.arctan2(np.sqrt(xy), pos[2]) # for elevation angle defined from Z-axis down
    sph[1] = np.arctan2(pos[2], np.sqrt(xy)) # for elevation angle defined from XY-plane up
    sph[2] = - np.arctan2(pos[1], pos[0])  # added a negative sign to make angles easily understandable

    return sph

"""
    ROW FORMAT for POSE_ALL
    frame id | x   |   y   |   z   |   a |   bi |   cj |   dk
    NOTE:   x,y,z are defined according to the OpenGL reference frame

    x:      double      -x is left, +x is right (rel. to camera)
    y:      double      -y is down, +y is up    (rel. to camera)
    z:      double      -z is forward, +z is back   (rel. to camera)
    a:    double      quarternion scalar
    bi:    double      ^i scalar in the vector portion
    cj:    double      ^j scalar in the vector portion
    dk:    double      ^z scalar in the vector portion

    (a + bi + cj + dk):    quarternion describing the rotation of the head relative to forward
"""

def get_road_data(POSE_ALL, ROAD, offset, face_csv_file, InputRotandTransf):
    vis_row_ptr = 0
    road_row_ptr = 0

    vis_frames = len(POSE_ALL)
    road_frames = len(ROAD)

    print("Total Center of Mass Frames", vis_frames)
    print("Total # of lines of Road Data", road_frames)

    ROAD = ROAD.T # transposing so we can iterate over (what were) rows rather of columns
    POSE_ALL = POSE_ALL.T

    if offset > 0: # back data starts before road video
        # need to move frame pointer ahead in visualize data to sync with road_to_back
        print("need to move visualize data ptr")
        vis_row_ptr = offset

    elif offset < 0: # road data starts before back video
        # need to move row pointer ahead in road_to_back data to sync with visualize
        print("need to move road row ptr")
        road_row_ptr = -offset

    face_header = "frame id\tBigTagX\tBigTagY\tBigTagZ\tcomX\tcomY\tcomZ\tr\ttheta\tphi\n"
    face_csv_file.write(face_header)
    
    # load the rotation and translation matrices from pickle file #
    RandT = parse_kabsch_transform_dump(InputRotandTransf)
    

    # doing frame by frame syncing
    print("Vis Frame %d, Road Row Ptr %d" % (vis_row_ptr, road_row_ptr))
    

    while vis_row_ptr < vis_frames and road_row_ptr < road_frames:
        vis_row = POSE_ALL[vis_row_ptr]
        road_row = ROAD[road_row_ptr]
        

        vis_f = vis_row['frame id']
        
        if str(road_row['detectionId']) == str(np.nan) or str(vis_row['x']) == str(np.nan):
            row = "%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (int(vis_f), "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan", "nan") 
            face_csv_file.write(row)
        else:
            road_trans = np.asarray((road_row['x'], road_row['y'], road_row['z']))
            vis_trans = np.asarray((vis_row['x'], vis_row['y'], vis_row['z']))
            
            ######MFM: need to perform kabsch algorithm here on road_trans to move it to back camera ########
            road_to_back = apply_kabsch_tfm(road_trans, RandT) 
                       
            face_to_april = road_to_back - vis_trans

            sph = calc_spherical(face_to_april)

            row = "%d\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\t%f\n" % (int(vis_f), road_to_back[0], road_to_back[1], road_to_back[2], 
                vis_row['x'], vis_row['y'], vis_row['z'], sph[0], sph[1], sph[2]) 
            face_csv_file.write(row)

        road_row_ptr = road_row_ptr + 1
        vis_row_ptr = vis_row_ptr + 1
    face_csv_file.close()
 
def unify_road_and_head_T2(REF_VIS, REF_ROAD, B_R_offset, OP_intialLabeling, InputRotandTransf):    
    ROAD_FILE = open(REF_ROAD, 'r')
    VISUALIZE = open(REF_VIS, 'r')
    
    Road = pd.read_csv(ROAD_FILE, sep='\t') # creating pandas dataframe from Road to Back CSV file
    POSE_ALL = pd.read_csv(VISUALIZE, sep='\t') # gettng head pose matrix from matlab file


    face_csv_file = open(OP_intialLabeling, 'w+') # opening output file for face csv data
    print("Syncing %s and %s with purported offset %d" % (REF_VIS, REF_ROAD, B_R_offset))

    get_road_data(POSE_ALL, Road, B_R_offset, face_csv_file, InputRotandTransf)
    

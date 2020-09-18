import pandas as pd
import pickle
import numpy as np

def parse_xyz(row):
    return (row["x"], row["y"], row["z"])

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



mycmd = 0 # flag to switch between running using bash script vs debugging using terminal
outputTransformedFile = 'output/visualize_frames_ref.csv'


if mycmd:
    inputFileToBeTransformed = 'output/visualize_frames.csv'
    inputPickleTransfomation = 'config/BackMarkers2019-6-20CornersSorted.pickle'
    outputTransformedFile = 'output/visualize_frames_ref.csv'

else:
    inputFileToBeTransformed = '/home/marzban/calibrateCameras/Outputs/D2019-10-31/ContGaze/visualize_frames.csv' #'../../output/visualize_frames.csv'
    inputPickleTransfomation = '/home/marzban/calibrateCameras/Outputs/D2019-10-31/ContGaze/KabaschRotTransCont.pickle'#'../../config/BackMarkers2019-6-20CornersSorted.pickle'
    outputTransformedFile = '/home/marzban/calibrateCameras/Outputs/D2019-10-31/ContGaze/visualize_frames_ref.csv'#'../../output/visualize_frames_ref.csv'


# load the rotation and translation matrices from pickle file #
pickle_in2 = open(inputPickleTransfomation,"rb")

RandT = parse_kabsch_transform_dump(inputPickleTransfomation)


inputValues = pd.read_csv(inputFileToBeTransformed, sep='\t')
numRowsInput = inputValues.shape[1]

#=====
for i, row in inputValues.iterrows():
    xyz = parse_xyz(row)
    target_back_ref = apply_kabsch_tfm(xyz, RandT)
    
    inputValues.ix[i, "x"] = xyz[0]
    inputValues.ix[i, "y"] = xyz[1]
    inputValues.ix[i, "z"] = xyz[2]

inputValues.to_csv(outputTransformedFile, sep='\t', index=False, na_rep = "nan")








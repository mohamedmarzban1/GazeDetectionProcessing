import pandas as pd
import pickle
import numpy as np

def parse_xyz(row):
    return (row["x"], row["y"], row["z"])

def parse_kabsch_transform_dump(dump_path):
    transform = open(dump_path, "rb")

    rot = pickle.load(transform)
    #print('rotation = ',rot,'\n')
    c_curr = pickle.load(transform)
    #print('c_curr = ',c_curr,'\n')
    c_goal = pickle.load(transform)
    #print('c_goal = ',c_goal,'\n')
    
    return (rot, c_curr, c_goal)

def apply_kabsch_tfm(vec, transform):
    (rot, c_curr, c_goal) = transform

    return np.matmul(rot, vec - c_curr) + c_goal


def move_to_reference(inputFile, refFile, pickleInput):

    # load the rotation and translation matrices from pickle file #
    #pickle_in2 = open(pickleInput,"rb")
    RandT = parse_kabsch_transform_dump(pickleInput)

    inputValues = pd.read_csv(inputFile, sep='\t')
    numRowsInput = inputValues.shape[1]

    #=====
    for i, row in inputValues.iterrows():
        xyz = parse_xyz(row)
        target_back_ref = apply_kabsch_tfm(xyz, RandT)
    
        inputValues.ix[i, "x"] = target_back_ref[0]
        inputValues.ix[i, "y"] = target_back_ref[1]
        inputValues.ix[i, "z"] = target_back_ref[2]

    inputValues.to_csv(refFile, sep='\t', index=False, na_rep = "nan")








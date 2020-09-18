import argparse
from Calibration import Calibration
from standardize_visualizeT2 import standardize_visualizeT2

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("AP_BackHatCalib", help="Back Apriltag output", type=str)
    parser.add_argument('Ref_Calib_Back', help='reference calibration  pickle file for back camera', type=str)
    parser.add_argument('KabaschRotTransBack', help='output rotation and translation matrices', type=str)
    parser.add_argument('OP_VIS', help='visulaize output mat file', type=str)
    parser.add_argument('STD_VIS', help='standardized visualize csv file', type=str)
    parser.add_argument('BackStart', help='start frame offset for back camera', type=int)

    return parser.parse_args()

def main():
    args = get_args()
    Calibration(args.AP_BackHatCalib, args.Ref_Calib_Back, args.KabaschRotTransBack)
    #standardize_visualizeT2(args.AP_BackHatCalib, args.OP_VIS, args.STD_VIS, args.BackStart)

if __name__ == '__main__':
    main()


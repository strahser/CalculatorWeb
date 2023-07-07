import os
import inspect
import sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
root_dir = os.path.dirname(parent_dir)
sys.path.insert(0, parent_dir)
sys.path.insert(0, root_dir)
from GSOPCalculator.GSOPControl.GSOPControl import GSOPControl

def gsop_main():
    gsop_control = GSOPControl()
    return gsop_control.calculate_gsop()

if __name__=="__main__":
    gsop = gsop_main()
    print(gsop)

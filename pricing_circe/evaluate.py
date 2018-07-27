__author__ = "Quynh Nguyen, Pradipta Ghosh and Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "2.0"

import shutil
import os
import random
import time
import glob


def evaluate_test():
    time.sleep(90)
    num = 0
    src = '/sample_input/1botnet.ipsum'
    dest = '/input/1botnet.ipsum'
    shutil.copyfile(src,dest)

def evaluate_random():
    """
    Copy files from folder ``sample_input`` to folder ``input`` at random intervals for evaluation 
    
    """
    interval = 60
    for src in glob.iglob('sample_input2/*.ipsum', recursive=True):
        n = random.randint(1,interval)
        count = 0
        while count<n:
            count = count+1
            time.sleep(1) 
        filename = src.split('/')[1]
        dest = "input/%s"%filename
        print('---- Generate random input files')
        shutil.copyfile(src,dest)
    print('---- Finish generating overlapped input files')
def evaluate_sequential(interval):
    """
    Copy files from folder ``sample_input`` to folder ``input`` one after another for evaluation 
    
    Args:
        interval (int): interval time to inject the sample input file
    
    """
    time.sleep(300)
    num = 0
    for src in glob.iglob('sample_input/*.ipsum', recursive=True):
        filename = src.split('/')[1]
        dest = "input/%s"%filename
        print('---- Generate random input files')
        shutil.copyfile(src,dest)
        count = 0
        num = num+1
        while count<interval:
            count = count+1
            time.sleep(1)
            file_count_out = len(os.listdir("output/"))
            if file_count_out ==  num:
                break 
    print('---- Finish generating sequential input files') 

if __name__ == '__main__':
    #evaluate_test()
    print('Sequential evaluation')
    evaluate_sequential(900)
    # time.sleep(60)
    # print('Overlap evaluation')
    # evaluate_random()

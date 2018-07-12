__author__ = "Quynh Nguyen and Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "2.0"

import pandas as pd
import glob

def analyze_circe_log(logspath):
    """Analyze circe log to generate meaningful evaluation results
    
    Args:
        logfile (str): path of log file
    """
    headers = ['Task_name','local_input_file','Enter_time','Execute_time','Finish_time','Elapse_time','Duration_time','Waiting_time ']
    df = pd.DataFrame(columns=headers)
    evaluation = []
    for logfile in glob.iglob(logspath, recursive=True): 
        start = False
        with open (logfile, 'rt') as f:  
            for line in f:
                line = line.rstrip('\n')
                if start == True:
                    info = line.split()
                    if len(info) == 8:
                        evaluation.append(info)
                if  line == 'Evaluation:':
                    start = True
        headers = evaluation.pop(0)
        
    print(df)
    
def main():
    logfile ='../logs/circehome_1524784809.log'
    analyze_circe_log(logfile)
if __name__ == '__main__':
    main()
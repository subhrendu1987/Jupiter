__author__ = "Quynh Nguyen, Pradipta Ghosh, Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "2.0"

import pandas as pd
def analyze_circe_evaluation(logfile):
    """Analyze circe log to generate meaningful evaluation results
    
    Args:
        logfile (str): path of log file
    """
    evaluation = []
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
    df = pd.DataFrame(evaluation, columns=headers)
    print(df)
    
def main():
    logfile ='../logs/circehome_1524784809.log'
    analyze_circe_evaluation(logfile)
if __name__ == '__main__':
    main()
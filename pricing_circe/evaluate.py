__author__ = "Quynh Nguyen, Pradipta Ghosh and Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "2.0"

import shutil
import os
import random
import time
import glob


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

def check_status_circe():
    """
    This function prints out all the tasks that are not running.
    If all the tasks are running: return ``True``; else return ``False``.
    """

    jupiter_config.set_globals()

    sys.path.append(jupiter_config.CIRCE_PATH)
    """
        This loads the kubernetes instance configuration.
        In our case this is stored in admin.conf.
        You should set the config file path in the jupiter_config.py file.
    """
    config.load_kube_config(config_file = jupiter_config.KUBECONFIG_PATH)
    namespace = jupiter_config.DEPLOYMENT_NAMESPACE


    # We have defined the namespace for deployments in jupiter_config

    # Get proper handles or pointers to the k8-python tool to call different functions.
    extensions_v1_beta1_api = client.ExtensionsV1beta1Api()
    v1_delete_options = client.V1DeleteOptions()
    core_v1_api = client.CoreV1Api()

    result = True
    for key, value in dag.items():
        # First check if there is a deployment existing with
        # the name = key in the respective namespac    # Check if there is a replicaset running by using the label app={key}
        # The label of kubernets are used to identify replicaset associate to each task
        label = "app=" + key

        resp = None

        resp = core_v1_api.list_namespaced_pod(namespace, label_selector = label)
        # if a pod is running just delete it
        if resp.items:
            a=resp.items[0]
            if a.status.phase != "Running":
                print("Pod Not Running", key)
                result = False

            # print("Pod Deleted. status='%s'" % str(del_resp_2.status))

    if result:
        print("All systems GOOOOO!!")
    else:
        print("Wait before trying again!!!!")

    return result    

if __name__ == '__main__':
    print('Sequential evaluation')
    evaluate_sequential(900)
    time.sleep(60)
    print('Overlap evaluation')
    evaluate_random()

__author__ = "Quynh Nguyen, Pradipta Ghosh, Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "2.0"

import sys
sys.path.append("../")

import time
import os
from os import path
from multiprocessing import Process
from k8s_profiler_scheduler import *
from k8s_wave_scheduler import *
from k8s_circe_scheduler import *
from k8s_exec_scheduler import *
from k8s_heft_scheduler import *
from pprint import *
import jupiter_config
import requests
import json
from pprint import *
from utilities import *
from k8s_get_service_ips import *
from functools import wraps
from delete_all_circe import *
from delete_all_waves import *
from delete_all_heft import *

NUM_SAMPLES = 1

def task_mapping_decorator(f):
    """Mapping the chosen scheduling modules based on ``jupiter_config.SCHEDULER`` in ``jupiter_config.ini``
    
    Args:
        f (function): either HEFT or WAVE scheduling modules specified from ``jupiter_config.ini``
    
    Returns:
        function: chosen scheduling modules
    """
    @wraps(f)
    def task_mapping(*args, **kwargs):
      if jupiter_config.SCHEDULER == 0:
        return f(*args, **kwargs)
      else:
        return f(args[0])
    return task_mapping

def empty_function():
    return []

def redeploy_system():
    """
        Redeploy the whole system
    """
    jupiter_config.set_globals()
    
    static_mapping = jupiter_config.STATIC_MAPPING
    
    """
        Tear down all current deployments
    """
    delete_all_circe()
    if jupiter_config.SCHEDULER == 0: # HEFT
        delete_all_heft()
        task_mapping_function  = task_mapping_decorator(k8s_heft_scheduler)
        exec_profiler_function = k8s_exec_scheduler
    else:# WAVE
        delete_all_waves()
        task_mapping_function = task_mapping_decorator(k8s_wave_scheduler)
        exec_profiler_function = empty_function

    # This loads the task graph and node list
    if not static_mapping:
        path1 = jupiter_config.APP_PATH + 'configuration.txt'
        path2 = jupiter_config.HERE + 'nodes.txt'

        # start the profilers
        profiler_ips = get_all_profilers()
        # profiler_ips = k8s_profiler_scheduler()


        # start the execution profilers
        execution_ips = get_all_execs()
        # execution_ips = exec_profiler_function()

        print('*************************')
        print('Network Profiling Information:')
        print(profiler_ips)
        print('Execution Profiling Information:')
        print(execution_ips)
        print('*************************')


        node_names = k8s_get_nodes_string(path2)
        print('*************************')


        #Start the task to node mapper
        task_mapping_function(profiler_ips,execution_ips,node_names)

        """
            Make sure you run kubectl proxy --port=8080 on a terminal.
            Then this is link to get the task to node mapping
        """

        line = "http://localhost:8080/api/v1/namespaces/"
        line = line + jupiter_config.MAPPER_NAMESPACE + "/services/home:" + str(jupiter_config.FLASK_SVC) + "/proxy"
        time.sleep(5)
        print(line)
        while 1:
            try:
                # print("get the data from " + line)
                r = requests.get(line)
                mapping = r.json()
                data = json.dumps(mapping)
                # print(mapping)
                # print(len(mapping))
                if len(mapping) != 0:
                    if "status" not in data:
                        break
            except:
                print("Some Exception")
        pprint(mapping)
        schedule = k8s_get_hosts(path1, path2, mapping)
        dag = k8s_read_dag(path1)
        dag.append(mapping)
        print("Printing DAG:")
        pprint(dag)
        print("Printing schedule")
        pprint(schedule)
        print("End print")

    
    else:
        import static_assignment
        # dag = static_assignment.dag
        # schedule = static_assignment.schedule

    # Start CIRCE
    k8s_circe_scheduler(dag,schedule)

def check_status_circe(dag):
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

def get_pod_logs(namespace, pod_name):
    ts = int(time.time())
    log_file = "../logs/circehome_%d.log" %(ts)
    bashCommand = "kubectl logs %s -n %s > %s"%(pod_name,namespace,log_file)
    os.system(bashCommand)


def export_circe_log():
    """Export circe home log for evaluation, should only use when for non-static mapping
    """
    jupiter_config.set_globals()
    path1 = jupiter_config.APP_PATH + 'configuration.txt'
    dag = k8s_read_dag(path1)
    # while 1:
    #     if check_status_circe(dag):
    #         break
    #     time.sleep(30)
    print('All deployments were created!!!!!!!!')
    config.load_kube_config(config_file = jupiter_config.KUBECONFIG_PATH)
    core_v1_api = client.CoreV1Api()
    resp = core_v1_api.list_namespaced_pod('quynh-profiler')
    for i in resp.items:
        if i.metadata.name.startswith('home'):
            circe_name = i.metadata.name
            break;
    while 1:
        get_pod_logs(jupiter_config.PROFILER_NAMESPACE,circe_name)
        time.sleep(300)

def main():
    """
        Generate logs, extract log information and redeploy system
    """
    export_circe_log()
    #redeploy_system()
if __name__ == '__main__':
    main()
__author__ = "Pradipta Ghosh, Pranav Sakulkar, Quynh Nguyen, Jason A Tran,  Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "2.1"

import sys
sys.path.append("../")

import time
import os
from os import path
from multiprocessing import Process
from write_heft_service_specs import *
from write_heft_specs import *
from kubernetes import client, config
from pprint import *
import os
import jupiter_config
from static_assignment import *
from utilities import *



def k8s_heft_scheduler(profiler_ips, ex_profiler_ips, node_names):
    """
        This script deploys HEFT in the system. 
    """
    jupiter_config.set_globals()

    """
        This loads the node list
    """
    nexthost_ips = ''
    nexthost_names = ''
    path2 = jupiter_config.HERE + 'nodes.txt'
    nodes = k8s_get_nodes(path2)
    pprint(nodes)

    """
        This loads the kubernetes instance configuration.
        In our case this is stored in admin.conf.
        You should set the config file path in the jupiter_config.py file.
    """
    config.load_kube_config(config_file = jupiter_config.KUBECONFIG_PATH)

    """
        We have defined the namespace for deployments in jupiter_config
    """
    namespace = jupiter_config.MAPPER_NAMESPACE

    """
        Get proper handles or pointers to the k8-python tool to call different functions.
    """
    api = client.CoreV1Api()
    k8s_beta = client.ExtensionsV1beta1Api()

    service_ips = {};

    """
        Loop through the list of nodes and run all WAVE related k8 deployment, replicaset, pods, and service.
        You can always check if a service/pod/deployment is running after running this script via kubectl command.
        E.g.,
            kubectl get svc -n "namespace name"
            kubectl get deployement -n "namespace name"
            kubectl get replicaset -n "namespace name"
            kubectl get pod -n "namespace name"
    """
    home_body = write_heft_service_specs(name = 'home', label = "heft_home")
    ser_resp = api.create_namespaced_service(namespace, home_body)
    print("Home service created. status = '%s'" % str(ser_resp.status))

    try:
        resp = api.read_namespaced_service('home', namespace)
    except ApiException as e:
        print("Exception Occurred")

    service_ips['home'] = resp.spec.cluster_ip
    home_ip = service_ips['home']
    home_name = 'home'

    del profiler_ips['home']
    profiler_ips_str = ' '.join('{0}:{1}'.format(key, val) for key, val in sorted(profiler_ips.items()))


    home_dep = write_heft_specs(name = 'home', label = "heft_home",
                                image = jupiter_config.HEFT_IMAGE,
                                host = jupiter_config.HOME_NODE,
                                node_names = node_names, 
                                home_ip = home_ip,
                                profiler_ips = profiler_ips_str,
                                execution_home_ip = ex_profiler_ips['home'])
    resp = k8s_beta.create_namespaced_deployment(body = home_dep, namespace = namespace)
    print("Home deployment created. status = '%s'" % str(resp.status))

    pprint(service_ips)

if __name__ == '__main__':
    # ips = {}
    # ips['home'] = '127.0.0.1'
    k8s_heft_scheduler(profiler_ips,execution_ips)

__author__ = "Quynh Nguyen and Bhaskar Krishnamachari"
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

from flask import Flask, request
from k8s_jupiter_deploy import *
from datetime import datetime

def periodical_check(interval):
	"""checking the health of system periodically
	
	Args:
	    interval (int): periodic duration
	"""
	jupiter_config.set_globals() 
	"""
        This loads the kubernetes instance configuration.
        In our case this is stored in admin.conf.
        You should set the config file path in the jupiter_config.py file.
    """
	config.load_kube_config(config_file = jupiter_config.KUBECONFIG_PATH)

	# Get proper handles or pointers to the k8-python tool to call different functions.
	core_v1_api = client.V1Probe()
if __name__ == '__main__':
	periodical_check(120)
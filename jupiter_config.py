"""
Top level config file (leave this file at the root directory). ``import config`` on the top of your file to include the global information included here.

"""
__author__ = "Pradipta Ghosh, Pranav Sakulkar, Quynh Nguyen, Jason A Tran, Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "2.0"


from os import path
import os
import configparser

HERE       = path.abspath(path.dirname(__file__)) + "/"
INI_PATH   = HERE + 'jupiter_config.ini'
DAG = 1 #using DAG application or XDAG application

def get_home_node(file_name):
    with open(file_name) as file:
        line = file.readline().split()
    return line[1]

def set_globals():
	"""Set global configuration information
	"""

	"""Configuration Paths"""

	config = configparser.ConfigParser()
	config.read(INI_PATH)
	"""User input for scheduler information"""
	global STATIC_MAPPING, SCHEDULER 

	STATIC_MAPPING          = int(config['CONFIG']['STATIC_MAPPING'])
	SCHEDULER               = int(config['CONFIG']['SCHEDULER'])

	"""Authorization information in the containers"""
	global USERNAME, PASSWORD

	USERNAME                = config['AUTH']['USERNAME']
	PASSWORD                = config['AUTH']['PASSWORD']

	"""Port and target port in containers for services to be used: Mongo, SSH and Flask"""
	global MONGO_SVC, MONGO_DOCKER, SSH_SVC, SSH_DOCKER, FLASK_SVC, FLASK_DOCKER
	
	MONGO_SVC               = config['PORT']['MONGO_SVC']
	MONGO_DOCKER            = config['PORT']['MONGO_DOCKER']
	SSH_SVC                 = config['PORT']['SSH_SVC']
	SSH_DOCKER              = config['PORT']['SSH_DOCKER']
	FLASK_SVC               = config['PORT']['FLASK_SVC']
	FLASK_DOCKER            = config['PORT']['FLASK_DOCKER']

	"""Modules path of Jupiter"""
	global NETR_PROFILER_PATH, EXEC_PROFILER_PATH, CIRCE_PATH, HEFT_PATH, WAVE_PATH, SCRIPT_PATH 

	NETR_PROFILER_PATH      = HERE + 'profilers/network_resource_profiler/'
	EXEC_PROFILER_PATH      = HERE + 'profilers/execution_profiler/'
	CIRCE_PATH              = HERE + 'circe/'
	HEFT_PATH               = HERE + 'task_mapper/heft/'
	WAVE_PATH               = HERE + 'task_mapper/wave/random_wave/'
	SCRIPT_PATH             = HERE + 'scripts/'

	if SCHEDULER == 1:
	    WAVE_PATH           = HERE + 'task_mapper/wave/random_wave/'
	elif SCHEDULER == 2:
	    WAVE_PATH           = HERE + 'task_mapper/wave/greedy_wave/'

	"""Kubernetes required information"""
	global KUBECONFIG_PATH, DEPLOYMENT_NAMESPACE, PROFILER_NAMESPACE, MAPPER_NAMESPACE, EXEC_NAMESPACE

	KUBECONFIG_PATH         = os.environ['KUBECONFIG']

	# Namespaces
	DEPLOYMENT_NAMESPACE    = 'quynh-circe'
	PROFILER_NAMESPACE      = 'quynh-profiler'
	MAPPER_NAMESPACE        = 'quynh-mapper'
	EXEC_NAMESPACE          = 'quynh-exec'

	""" Node file path and first task information """
	global HOME_NODE, HOME_CHILD

	HOME_NODE               = get_home_node(HERE + 'nodes.txt')
	HOME_CHILD              = 'localpro'

	global HOME_IMAGE, WORKER_IMAGE
	global PROFILER_HOME_IMAGE, PROFILER_WORKER_IMAGE
	global WAVE_HOME_IMAGE, WAVE_WORKER_IMAGE
	global EXEC_HOME_IMAGE, EXEC_WORKER_IMAGE
	global HEFT_IMAGE
	global HOME_IMAGE, WORKER_IMAGE
	global APP_PATH, APP_NAME


	if DAG == 0: # XDAG images

		"""CIRCE home and worker images"""
		HOME_IMAGE              = 'docker.io/anrg/circe_home:xdag'
		WORKER_IMAGE            = 'docker.io/anrg/circe_worker:xdag'

		"""DRUPE home and worker images"""
		PROFILER_HOME_IMAGE     = 'docker.io/anrg/profiler_home:xdag'
		PROFILER_WORKER_IMAGE   = 'docker.io/anrg/profiler_worker:xdag'

		"""WAVE home and worker images"""
		if SCHEDULER == 0 or SCHEDULER == 1:
			WAVE_HOME_IMAGE         = 'docker.io/anrg/wave_home:xdag_random'
			WAVE_WORKER_IMAGE       = 'docker.io/anrg/wave_worker:xdag_random'
		else:
			WAVE_HOME_IMAGE         = 'docker.io/anrg/wave_home:xdag_greedy'
			WAVE_WORKER_IMAGE       = 'docker.io/anrg/wave_worker:xdag_greedy'
		"""Execution profiler home and worker images"""

		EXEC_HOME_IMAGE         = 'docker.io/anrg/exec_home:xdag_random'
		EXEC_WORKER_IMAGE       = 'docker.io/anrg/exec_worker:xdag_random'

		"""HEFT docker image"""

		HEFT_IMAGE              = 'docker.io/anrg/heft:xdag'

		"""Application Information"""

		APP_PATH                = HERE  + 'app_specific_files/network_monitoring_app_xdag/'
		APP_NAME                = 'app_specific_files/network_monitoring_app_xdag'

	else:# DAG images
		"""CIRCE home and worker images"""
		HOME_IMAGE              = 'docker.io/anrg/circe_home:dag'
		WORKER_IMAGE            = 'docker.io/anrg/circe_worker:dag'

		"""DRUPE home and worker images"""
		PROFILER_HOME_IMAGE     = 'docker.io/anrg/profiler_home:dag'
		PROFILER_WORKER_IMAGE   = 'docker.io/anrg/profiler_worker:dag'

		"""WAVE home and worker images"""
		if SCHEDULER == 0 or SCHEDULER == 1:
			WAVE_HOME_IMAGE         = 'docker.io/anrg/wave_home:dag_random'
			WAVE_WORKER_IMAGE       = 'docker.io/anrg/wave_worker:dag_random'
		else:
			WAVE_HOME_IMAGE         = 'docker.io/anrg/wave_home:dag_greedy'
			WAVE_WORKER_IMAGE       = 'docker.io/anrg/wave_worker:dag_greedy'
		
		"""Execution profiler home and worker images"""
		EXEC_HOME_IMAGE         = 'docker.io/anrg/exec_home:dag_random'
		EXEC_WORKER_IMAGE       = 'docker.io/anrg/exec_worker:dag_random'

		"""HEFT docker image"""
		HEFT_IMAGE              = 'docker.io/anrg/heft:dag'

		"""Application Information"""
		APP_PATH                = HERE  + 'app_specific_files/network_monitoring_app_dag/'
		APP_NAME                = 'app_specific_files/network_monitoring_app_dag'

	# default APP
	# APP_PATH                = HERE  + 'app_specific_files/network_monitoring_app/'
	# APP_NAME                = 'app_specific_files/network_monitoring_app'


if __name__ == '__main__':
	set_globals()
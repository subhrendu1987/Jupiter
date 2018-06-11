#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    .. note:: This script runs on every computing node of the system.
"""

__author__ = "Quynh Nguyen, Pradipta Ghosh and Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "3.0"

import os
import json
from multiprocessing import Process
import multiprocessing
from flask import Flask, request
from os import path

app = Flask(__name__)

def set_global_info():
	"""Get information of corresponding profiler (network profiler, execution profiler)"""
	global profiler_ip, execution_ip, self_name,network_map
	profiler_ip = os.environ['PROFILERS'].split(' ')
    profiler_ip = [info.split(":") for info in profiler_ip]
	execution_ip = os.environ['EXECUTION']
	self_name = os.environ['SELF_NAME']
	node_list = [info[0] for info in profiler_ip]
    node_IP = [info[1] for info in profiler_ip]
    network_map = dict(zip(node_IP, node_list))

	global execution_info, network_info
	network_info = []
	execution_info = []

def get_exec_profile_data(self_name, exec_home_ip, MONGO_SVC_PORT):
    """Collect the execution profile from the home execution profiler's MongoDB
    
    Args:
        self_name (str): node name
        exec_home_ip (str): IP of execution home
        MONGO_SVC_PORT (str): mongo service port
    """

    conn = False
    while not conn:
        try:
            client_mongo = MongoClient('mongodb://'+exec_home_ip+':'+MONGO_SVC_PORT+'/')
            db = client_mongo.execution_profiler
            conn = True
        except:
            print('Error connection')
            time.sleep(60)

    print(db)
    while True:
	    try:
	    	logging =db[self_name].find()
	    except Exception as e:
            print('--- Execution profiler info not yet loaded into MongoDB!')
            time.sleep(60)

    for record in logging:
        #  Task, Execution Time, Output size
        info_to_csv=[col,record['Task'],record['Duration [sec]'],str(record['Output File [Kbit]'])]
        execution_info.append(info_to_csv)

    print('Execution information has already been provided')
    print(execution_info)
    

def get_network_profile_data(profiler_ip, MONGO_SVC_PORT, network_map):
    """Collect the network profile from local MongoDB peer
    
    Args:
        - profiler_ip (list): IPs of network profilers
        - MONGO_SVC_PORT (str): Mongo service port
        - network_map (dict): mapping of node IPs and node names
    """
    print(profiler_ip)
    for ip in profiler_ip:
        print('Check Network Profiler IP: '+ip[0]+ '-' +ip[1])
        client_mongo = MongoClient('mongodb://'+ip[1]+':'+MONGO_SVC_PORT+'/')
        db = client_mongo.droplet_network_profiler
        collection = db.collection_names(include_system_collections=False)
        num_nb = len(collection)-1
        while num_nb==-1:
            print('--- Network profiler mongoDB not yet prepared')
            time.sleep(60)
            collection = db.collection_names(include_system_collections=False)
            num_nb = len(collection)-1
        print('--- Number of neighbors: '+str(num_nb))
        num_rows = db[ip[1]].count()
        while num_rows < num_nb:
            print('--- Network profiler regression info not yet loaded into MongoDB!')
            time.sleep(60)
            num_rows = db[ip[1]].count()
        logging =db[ip[1]].find().limit(num_nb)
        for record in logging:
            # print(record)
            # Source ID, Source IP, Destination ID, Destination IP, Parameters
            info_to_csv=[network_map[record['Source[IP]']],record['Source[IP]'],network_map[record['Destination[IP]']], record['Destination[IP]'],str(record['Parameters'])]
            network_info.append(info_to_csv)
    print('Network information has already been provided')
    #print(network_info)
    with open('/heft/network_log.txt','w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(network_info)
    return


def pricing_calculate(file_name, task_name, profiler_ip,execution_ip,task_queue):
	"""Calculate price required to perform the task with given input
	
	Args:
	    profiler_ip (str): Network and resource profiler IP
	    execution_ip (TYPE): Execution profiler IP
	    task_queue (TYPE): Current task queue
	
	Returns:
	    float: calculated price
	"""
	return price

def receive_price_request(file_name, task_name):
    """Receive price request from pricing calculator
    
    Args:
        file_name (TYPE): Description
        task_name (TYPE): Description
    """


def execute_task(file_name, task_name):
    """Execute the task given the input file
    
    Args:
        file_name (str): Incoming file name
        task_name (str): Incoming task name
    """

def main():

if __name__ == '__main__':
    main()
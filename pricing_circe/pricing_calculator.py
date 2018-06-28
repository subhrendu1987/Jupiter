#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    .. note:: This script runs on every computing node of the system.
"""

__author__ = "Quynh Nguyen, Pradipta Ghosh and Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "3.0"

import sys
sys.path.append("../")
import configparser
import jupiter_config
import os
import json
from multiprocessing import Process, Manager
import multiprocessing
from flask import Flask, request
from os import path
import json
import _thread
import csv
from pymongo import MongoClient
import pandas as pd
import time


app = Flask(__name__)

def prepare_global_info():
    """Get information of corresponding profiler (network profiler, execution profiler)"""
    global profiler_ip, exec_home_ip, self_name,self_ip,network_map, num_nodes
    profiler_ip = os.environ['ALL_PROFILERS'].split(' ')
    profiler_ip = [info.split(":") for info in profiler_ip]
    exec_home_ip = os.environ['EXECUTION_HOME_IP']
    self_name = os.environ['SELF_NAME']
    self_ip = os.environ['SELF_IP']
    node_list = [info[0] for info in profiler_ip]
    node_IP = [info[1] for info in profiler_ip]
    network_map = dict(zip(node_IP, node_list))
    num_nodes = len(profiler_ip[0])

    global execution_info,manager, task_mul
    execution_info = []
    manager = Manager()
    task_mul = manager.dict()


def update_exec_profile_file():
    """Update the execution profile from the home execution profiler's MongoDB and store it in text file.
    """
    print('Update execution profile information in execution.txt')
    print(exec_home_ip)
    print(MONGO_SVC)
    print(num_nodes)


    num_profilers = 0
    conn = False
    while not conn:
        try:
            client_mongo = MongoClient('mongodb://'+exec_home_ip+':'+str(MONGO_SVC)+'/')
            db = client_mongo.execution_profiler
            conn = True
        except:
            print('Error connection')
            time.sleep(60)

    print(db)
    while num_profilers < num_nodes:
        try:
            collection = db.collection_names(include_system_collections=False)
            num_profilers = len(collection)
            print('--- Number of loaded collection: '+str(num_profilers))
        except Exception as e:
            print('--- Execution profiler info not yet loaded into MongoDB!')
            time.sleep(60)

    #print(collection)
    for col in collection:
        print('--- Check execution profiler ID : '+ col)
        logging =db[col].find()
        for record in logging:
            # Node ID, Task, Execution Time, Output size
            info_to_csv=[col,record['Task'],record['Duration [sec]'],str(record['Output File [Kbit]'])]
            execution_info.append(info_to_csv)
    print('Execution information has already been provided')
    # print(execution_info)
    with open('execution_log.txt','w') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerows(execution_info)
    return

def get_taskmap():
    """Get the task map from ``config.json`` and ``dag.txt`` files.
    
    Returns:
        - dict: tasks - DAG dictionary
        - list: task_order - (DAG) task list in the order of execution
        - list: super_tasks 
        - list: non_tasks - tasks not belong to DAG
    """
    configs = json.load(open('centralized_scheduler/config.json'))
    task_map = configs['taskname_map']
    execution_map = configs['exec_profiler']
    tasks_info = open('centralized_scheduler/dag.txt', "r")

    task_order = []#create the  (DAG) task list in the order of execution
    super_tasks = []
    tasks = {} #create DAG dictionary
    count = 0
    for line in tasks_info:
        if count == 0:
            count += 1
            continue

        data = line.strip().split(" ")
        if task_map[data[0]][1] == True and execution_map[data[0]] == False:
            if data[0] not in super_tasks:
                super_tasks.append(data[0])
        if task_map[data[0]][1] == False:
            continue

        tasks.setdefault(data[0], [])
        if data[0] not in task_order:
            task_order.append(data[0])
        for i in range(3, len(data)):
            if  data[i] != 'home' and task_map[data[i]][1] == True :
                tasks[data[0]].append(data[i])
    print("tasks: ", tasks)
    print("task order", task_order) #task_list
    print("super tasks", super_tasks)
    return tasks, task_order, super_tasks

def get_updated_exec_data():
    with open('execution_log.txt','r') as f:
        reader = csv.reader(f)
        execution = list(reader)
    # fix non-DAG tasks (temporary approach)
    execution_info = []
    for row in execution:
        if row[0]!='home':
            execution_info.append(row)
        else:
            print(row)
            if row[1] in super_tasks:
                for node in node_list:
                    execution_info.append([node,row[1],row[2],row[3]]) # to copy the home profiler data for the non dag task for each processor.
    print(execution_info)

def get_updated_network_profile_data(profiler_ip, MONGO_SVC_PORT, network_map):
    """Collect the network profile information from local MONGODB database
    
    Args:
        - profiler_ip (list): IPs of network profilers
        - MONGO_SVC_PORT (str): Mongo service port
        - network_map (dict): mapping of node IPs and node names
    """
    print("Collect network profile data")   
    network_info = []

    try:
        client_mongo = MongoClient('mongodb://'+self_ip+':'+MONGO_SVC_PORT+'/')
        db = client_mongo.droplet_network_profiler
        collection = db.collection_names(include_system_collections=False)
        num_nb = len(collection)-1
        if num_nb == -1:
            print('--- Network profiler mongoDB not yet prepared')
            return network_info
        num_rows = db[self_ip].count() 
        if num_rows < num_nb:
            print('--- Network profiler regression info not yet loaded into MongoDB!')
            return network_info
        logging =db[self_ip].find().limit(num_nb)  
        for record in logging:
            # print(record)
            # Source ID, Source IP, Destination ID, Destination IP, Parameters
            info_to_csv=[network_map[record['Source[IP]']],record['Source[IP]'],network_map[record['Destination[IP]']], record['Destination[IP]'],str(record['Parameters'])]
            network_info.append(info_to_csv) 
        print('Network information has already been provided')
        print("Network profiles: ", network_info)
        return network_info
    except Exception as e:
        print("Network request failed. Will try again, details: " + str(e))
    

def get_updated_resource_profile_data():
    """Requesting resource profiler data using flask for its corresponding profiler node
    """
    print("Collect resource profile data")  
    resource_info = [] 
    try:
        for c in range(0,num_retries):
            r = requests.get("http://" + self_ip + ":" + str(FLASK_SVC) + "/all")
            result = r.json()
            if len(result) != 0:
                resource_info=json.dumps(result)
                break
            time.sleep(60)

        if c == num_retries:
            print("Exceeded maximum try times.")

        print("Got profiler data from http://" + os.environ['PROFILER'] + ":" + str(FLASK_SVC))
        print("Resource profiles: ", resource_info)
        return resource_info

    except Exception as e:
        print("Resource request failed. Will try again, details: " + str(e))
    
    



def pricing_calculate(file_name, task_name):
    """Calculate price required to perform the task with given input based on network information, resource information, execution information and task queue size
    
    Args:
        file_name (str): incoming file name
        task_name (str): incoming task name
    
    Returns:
        float: calculated price
    """
    return price

def receive_price_request(file_name, task_name):
    """Receive price request from pricing calculator
    
    Args:
        file_name (str): incoming file name
        task_name (str): incoming task name
    """


def execute_task(file_name, task_name):
    """Execute the task given the input file
    
    Args:
        file_name (str): incoming file name
        task_name (str): incoming task name
    """

def main():
    ## Load all the configuration
    global username, password, ssh_port,num_retries, MONGO_DOCKER, MONGO_SVC, FLASK_SVC, FLASK_DOCKER
    # Load all the confuguration
    INI_PATH = '/jupiter_config.ini'
    config = configparser.ConfigParser()
    config.read(INI_PATH)
    username    = config['AUTH']['USERNAME']
    password    = config['AUTH']['PASSWORD']
    ssh_port    = int(config['PORT']['SSH_SVC'])
    num_retries = int(config['OTHER']['SSH_RETRY_NUM'])
    pricing_threshold = int(config['OTHER']['PRICING_THRESHOLD'])
    MONGO_SVC    = int(config['PORT']['MONGO_SVC'])
    MONGO_DOCKER = int(config['PORT']['MONGO_DOCKER'])
    FLASK_SVC    = int(config['PORT']['FLASK_SVC'])
    FLASK_DOCKER = int(config['PORT']['FLASK_DOCKER'])


    prepare_global_info()

    print('------------------------------------------------------------')
    print("\n Read execution profiler information : \n")
    _thread.start_new_thread(update_exec_profile_file,())
    

if __name__ == '__main__':
    main()
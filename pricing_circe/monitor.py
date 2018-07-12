#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    .. note:: This script runs on every node of the system.
"""

__author__ = "Quynh Nguyen, Pradipta Ghosh, Aleksandra Knezevic, Pranav Sakulkar, Jason A Tran and Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "3.0"

import multiprocessing
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import sys
import time
import json
import paramiko
import datetime
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
import netifaces as ni
import platform
from os import path
from socket import gethostbyname, gaierror, error
import multiprocessing
import time
import urllib.request
from urllib import parse
import configparser
from multiprocessing import Process, Manager
from flask import Flask, request



app = Flask(__name__)

def convert_bytes(num):
    """Convert bytes to Kbit as required by HEFT
    
    Args:
        num (int): The number of bytes
    
    Returns:
        float: file size in Kbits
    """
    return num*0.008

def file_size(file_path):
    """Return the file size in bytes
    
    Args:
        file_path (str): The file path
    
    Returns:
        float: file size in bytes
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)

def prepare_global():
    """
    Prepare global information
    """
    global task_price_summary
    task_price_summary = []

def issue_price_request(dest_node_host_port,file_name, file_size):
    """Issue pricing request to every computing node
    
    Args:
        dest_node_host_port (str): destination node and Flask port
        file_name (str): incoming file name
        file_size (int): size of incoming file
    
    Returns:
        str: the message if successful, "not ok" otherwise.
    
    Raises:
        Exception: if sending message to flask server on home is failed
    """
    try:

        print("Sending pricing request :"+ dest_node_host_port)
        url = "http://" + dest_node_host_port + "/receive_price_request"
        params = {'file_name':file_name ,'file_size':file_size, "task_name": taskname}
        params = parse.urlencode(params)
        req = urllib.request.Request(url='%s%s%s' % (url, '?', params))
        res = urllib.request.urlopen(req)
        res = res.read()
        res = res.decode('utf-8')
    except Exception as e:
        print("Sending message to flask server on destination node FAILED!!!")
        print(e)
        return "not ok"
    return res


def receive_updated_price():
    """Receive price from every computing node
    """
app.add_url_rule('/receive_updated_price', 'receive_updated_price', receive_updated_price)

def choose_exec_node():
    """Return the node with the best price
    """
    return chosen_node


def setup_exec_node(chosen_node,file_name,task_name):
    """Setup prepared for the chosen computing node, transfer input files
    
    Args:
        chosen_node (TYPE): node having best price
        file_name (str): Incoming file name
        task_name (str): Incoming task name
    """
def retrieve_results():
    """Retrieve results from computing node
    """

def send_monitor_data(msg):
    """
    Sending message to flask server on home

    Args:
        msg (str): the message to be sent

    Returns:
        str: the message if successful, "not ok" otherwise.

    Raises:
        Exception: if sending message to flask server on home is failed
    """
    try:
        print("Sending message", msg)
        url = "http://" + home_node_host_port + "/recv_monitor_data"
        params = {'msg': msg, "work_node": taskname}
        params = parse.urlencode(params)
        req = urllib.request.Request(url='%s%s%s' % (url, '?', params))
        res = urllib.request.urlopen(req)
        res = res.read()
        res = res.decode('utf-8')
    except Exception as e:
        print("Sending message to flask server on home FAILED!!!")
        print(e)
        return "not ok"
    return res

def send_runtime_profile(msg):
    """
    Sending runtime profiling information to flask server on home

    Args:
        msg (str): the message to be sent

    Returns:
        str: the message if successful, "not ok" otherwise.

    Raises:
        Exception: if sending message to flask server on home is failed
    """
    try:
        print("Sending message", msg)
        url = "http://" + home_node_host_port + "/recv_runtime_profile"
        params = {'msg': msg, "work_node": taskname}
        params = parse.urlencode(params)
        req = urllib.request.Request(url='%s%s%s' % (url, '?', params))
        res = urllib.request.urlopen(req)
        res = res.read()
        res = res.decode('utf-8')
    except Exception as e:
        print("Sending runtime profiling info to flask server on home FAILED!!!")
        print(e)
        return "not ok"
    return res



#for OUTPUT folder 
class Watcher1():
    
    DIRECTORY_TO_WATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'output/')

    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.observer = Observer()

    def run(self):
        """
            Continuously watching the ``OUTPUT`` folder, if there is a new file created for the current task, copy the file to the corresponding ``INPUT`` folder of the next task in the scheduled node
        """
        event_handler = Handler1()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()

class Handler1(FileSystemEventHandler):


    @staticmethod
    def on_any_event(event):
        """
            Check for any event in the ``OUTPUT`` folder
        """
        if event.is_directory:
            return None

        elif event.event_type == 'created':
             
            print("Received file as output - %s." % event.src_path)

            new_file = os.path.split(event.src_path)[-1]

            if '_' in new_file:
                temp_name = new_file.split('_')[0]
            else:
                temp_name = new_file.split('.')[0]
            

            global files_out

            #based on flag2 decide whether to send one output to all children or different outputs to different children in
            #order given in the config file
            flag2 = sys.argv[2]

            #if you are sending the final output back to scheduler
            if sys.argv[3] == 'home':
                
                IPaddr = sys.argv[4]
                user = sys.argv[5]
                password=sys.argv[6]
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                #Keep retrying in case the containers are still building/booting up on
                #the child nodes.
                retry = 0
                while retry < num_retries:
                    try:
                        ssh.connect(IPaddr, username=user, password=password, port=ssh_port)
                        sftp = ssh.open_sftp()
                        sftp.put(event.src_path, os.path.join('/output', new_file))
                        sftp.close()
                        break
                    except:
                        print('SSH Connection refused or File tranfer failed, will retry in 2 seconds')
                        time.sleep(2)
                        retry += 1
                
                ssh.close()

            elif flag2 == 'true':

                for i in range(3, len(sys.argv)-1,4):
                    IPaddr = sys.argv[i+1]
                    user = sys.argv[i+2]
                    password = sys.argv[i+3]
                    #port = int(sys.argv[i+4])

                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                    #Keep retrying in case the containers are still building/booting up on
                    #the child nodes.
                    retry = 0
                    while retry < num_retries:
                        try:
                            ssh.connect(IPaddr, username=user, password=password, port=ssh_port)
                            sftp = ssh.open_sftp()
                            sftp.put(event.src_path, os.path.join('/centralized_scheduler', 'input', new_file))
                            sftp.close()
                            break
                        except:
                            print('SSH Connection refused or File transfer failed, will retry in 2 seconds')
                            time.sleep(2)
                            retry += 1

                    ssh.close()

            else:
                num_child = (len(sys.argv) - 4) / 4
                files_out.append(new_file)

                if (len(files_out) == num_child):

                        
                    for i in range(3, len(sys.argv)-1,4):
                        myfile = files_out.pop(0)
                        event_path = os.path.join(''.join(os.path.split(event.src_path)[:-1]), myfile)
                        IPaddr = sys.argv[i+1]
                        user = sys.argv[i+2]
                        password = sys.argv[i+3]
                        #port = int(sys.argv[i+4])

                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                        #Keep retrying in case the containers are still building/booting up on
                        #the child nodes.
                        retry = 0
                        while retry < num_retries:
                            try:
                                ssh.connect(IPaddr, username=user, password=password, port=ssh_port)
                                sftp = ssh.open_sftp()
                                sftp.put(event_path, os.path.join('/centralized_scheduler','input', myfile))
                                sftp.close()
                                break
                            except:
                                print('SSH Connection refused or File transfer failed, will retry in 2 seconds')
                                time.sleep(2)
                                retry += 1
                
                        
                        ssh.close()

                    files_out=[]


#for INPUT folder
class Watcher(multiprocessing.Process):

    DIRECTORY_TO_WATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'input/')
    
    def __init__(self):
        multiprocessing.Process.__init__(self)
        self.observer = Observer()

    def run(self):
        """
            Continuously watching the ``INPUT`` folder.
            When file in the input folder is received, based on the DAG info imported previously, it either waits for more input files, or issue pricing request to all the computing nodes in the system.
        """
        
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':

            print("Received file as input - %s." % event.src_path)

            new_file = os.path.split(event.src_path)[-1]
            if '_' in new_file:
                temp_name = new_file.split('_')[0]
            else:
                temp_name = new_file.split('.')[0]

            
            ts = time.time()
            """
                Save the time the input file enters the queue
            """
            
            flag1 = sys.argv[1]
            
            if temp_name not in task_mul:
                task_mul[temp_name] = [new_file]
                runtime_info = 'rt_enter '+ temp_name+ ' '+str(ts)
                send_runtime_profile(runtime_info)
                count_dict[temp_name]=int(flag1)-1
            else:
                task_mul[temp_name] = task_mul[temp_name] + [new_file]
                count_dict[temp_name]=count_dict[temp_name]-1
            print(task_mul[temp_name])
            

            if count_dict[temp_name] == 0: # enough input files
                filename = task_mul[temp_name]
                if len(filename)==1: 
                    filenames = filename[0]
                else:
                    filenames = filename    
               
                # When receive an input file, issue pricing request instead of performing the task
                print(all_nodes)
                print(all_nodes_ips)
                for dest_node_host_port in dest_node_host_port_list:
                    issue_price_request(dest_node_host_port,filenames, file_size(event.src_path))

                # ts = time.time()
                # runtime_info = 'rt_exec '+ temp_name+ ' '+str(ts)
                # send_runtime_profile(runtime_info)
                # input_path = os.path.split(event.src_path)[0]
                # output_path = os.path.join(os.path.split(input_path)[0],'output')

                

                # dag_task = multiprocessing.Process(target=taskmodule.task, args=(filenames, input_path, output_path))
                # dag_task.start()
                # dag_task.join()
                # ts = time.time()
                # runtime_info = 'rt_finish '+ temp_name+ ' '+str(ts)
                # send_runtime_profile(runtime_info)


def main():
    """
        -   Load all the Jupiter confuguration
        -   Load DAG information. 
        -   Prepare all of the tasks based on given DAG information. 
        -   Prepare the list of children tasks for every parent task
        -   Generating monitoring process for ``INPUT`` folder.
        -   Generating monitoring process for ``OUTPUT`` folder.
        -   If there are enough input files for the first task on the current node, run the first task. 

    """

    INI_PATH = '/jupiter_config.ini'
    config = configparser.ConfigParser()
    config.read(INI_PATH)

    global FLASK_SVC, MONGO_PORT, username,password,ssh_port, num_retries, task_mul, count_dict

    FLASK_SVC   = int(config['PORT']['FLASK_SVC'])
    MONGO_PORT  = int(config['PORT']['MONGO_DOCKER'])
    username    = config['AUTH']['USERNAME']
    password    = config['AUTH']['PASSWORD']
    ssh_port    = int(config['PORT']['SSH_SVC'])
    num_retries = int(config['OTHER']['SSH_RETRY_NUM'])


    global taskmap, taskname, taskmodule, filenames,files_out, node_name, home_node_host_port, all_nodes, all_nodes_ips

    configs = json.load(open('/centralized_scheduler/config.json'))
    taskmap = configs["taskname_map"][sys.argv[len(sys.argv)-1]]
    print(taskmap)
    taskname = taskmap[0]
    print(taskname)
    if taskmap[1] == True:
        taskmodule = __import__(taskname)

    #target port for SSHing into a container
    filenames=[]
    files_out=[]
    node_name = os.environ['NODE_NAME']
    home_node_host_port = os.environ['HOME_NODE'] + ":" + str(FLASK_SVC)

    all_nodes = os.environ["ALL_NODES"].split(":")
    all_nodes_ips = os.environ["ALL_NODES_IPS"].split(":")

    global dest_node_host_port_list
    dest_node_host_port_list = [ip + ":" + str(FLASK_SVC) for ip in all_nodes_ips]


    if taskmap[1] == True:
        #queue_mul=multiprocessing.Queue()
        manager = Manager()
        task_mul = manager.dict()
        count_dict = manager.dict()

        #monitor INPUT as another process
        w=Watcher()
        w.start()

        #monitor OUTPUT in this process
        w1=Watcher1()
        w1.run()
    else:

        print(taskmap[2:])
        path_src = "/centralized_scheduler/" + taskname
        args = ' '.join(str(x) for x in taskmap[2:])

        if os.path.isfile(path_src + ".py"):
            cmd = "python3 -u " + path_src + ".py " + args          
        else:
            cmd = "sh " + path_src + ".sh " + args
        print(cmd)
        os.system(cmd)

if __name__ == '__main__':
    main()
    
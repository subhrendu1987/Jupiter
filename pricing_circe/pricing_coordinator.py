#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    .. note:: This script runs on every task controller of the system.
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
from multiprocessing import Process
import multiprocessing
from flask import Flask, request
from os import path

app = Flask(__name__)

def prepare_global():
    """
    Prepare global information
    """
    global task_price_summary
    task_price_summary = []

def issue_price_request(file_name, file_size, task_name):
    """Issue pricing request to every computing node
    
    Args:
        file_name (str): Incoming file name
        task_name (TYPE): Incoming task name
    """

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
def main():
    

if __name__ == '__main__':

    main()
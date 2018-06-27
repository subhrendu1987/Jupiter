#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Pradipta Ghosh, Quynh Nguyen and Bhaskar Krishnamachari"
__copyright__ = "Copyright (c) 2018, Autonomous Networks Research Group. All rights reserved."
__license__ = "GPL"
__version__ = "3.0"

from pprint import pprint
from dockerfile_parse import DockerfileParser

############################################ HOME DOCKER TEMPLATE #########################################################

template_home ="""\
# Instructions copied from - https://hub.docker.com/_/python/
FROM ubuntu:16.04

RUN apt-get -yqq update
RUN apt-get -yqq install python3-pip python3-dev libssl-dev libffi-dev
RUN apt-get install -y openssh-server mongodb
ADD pricing_circe/requirements.txt /requirements.txt
RUN apt-get -y install build-essential libssl-dev libffi-dev python-dev
RUN pip3 install --upgrade pip
RUN apt-get install -y sshpass nano 

# Taken from quynh's network profiler
RUN pip install cryptography


RUN pip3 install -r requirements.txt
RUN echo '{username}:{password}' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

# Create the mongodb directories
RUN mkdir -p /mongodb/data
RUN mkdir -p /mongodb/log

# Create the input, output, and runtime profiler directories
RUN mkdir -p /input
RUN mkdir -p /output
RUN mkdir -p /runtime

# Add input files
COPY  {app_file}/sample_input /sample_input
COPY  {app_file}/sample_input2 /sample_input2

# Add the mongodb scripts
ADD pricing_circe/runtime_profiler_mongodb /central_mongod
ADD pricing_circe/rt_profiler_update_mongo.py /run_update.py

ADD pricing_circe/readconfig.py /readconfig.py
ADD pricing_circe/scheduler.py /scheduler.py
ADD jupiter_config.py /jupiter_config.py
ADD pricing_circe/evaluate.py /evaluate.py

# Add the task speficific configuration files
ADD {app_file}/configuration.txt /configuration.txt

ADD nodes.txt /nodes.txt
ADD jupiter_config.ini /jupiter_config.ini

ADD pricing_circe/pricing_coordinator.py /centralized_scheduler/pricing_coordinator.py
ADD pricing_circe/start_home.sh /start.sh
RUN chmod +x /start.sh
RUN chmod +x /central_mongod

WORKDIR /

# tell the port number the container should expose
EXPOSE {ports}

# run the command
CMD ["./start.sh"]
"""



############################################ WORKER DOCKER TEMPLATE#########################################################

template_controller_worker ="""\
# Instructions copied from - https://hub.docker.com/_/python/
FROM ubuntu:16.04

RUN apt-get -yqq update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -yqq install python3-pip python3-dev libssl-dev libffi-dev 
RUN apt-get install -yqq openssh-client openssh-server bzip2 wget net-tools sshpass screen
RUN apt-get install -y vim
RUN apt-get install g++ make openmpi-bin libopenmpi-dev -y
RUN apt-get install sudo -y
RUN apt-get install iproute2 -y

## Install TASK specific needs. The hadoop is a requirement for the network profiler application
##RUN wget http://supergsego.com/apache/hadoop/common/hadoop-2.8.1/hadoop-2.8.1.tar.gz -P ~/
RUN wget https://archive.apache.org/dist/hadoop/core/hadoop-2.8.1/hadoop-2.8.1.tar.gz -P ~/
RUN tar -zxvf ~/hadoop-2.8.1.tar.gz -C ~/
RUN rm ~/hadoop-2.8.1.tar.gz
ADD pricing_circe/requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt
RUN echo '{username}:{password}' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN mkdir -p /centralized_scheduler/input
RUN mkdir -p /centralized_scheduler/output
RUN mkdir -p /centralized_scheduler/runtime
ADD pricing_circe/monitor.py /centralized_scheduler/monitor.py
RUN mkdir -p /home/darpa/apps/data

ADD pricing_circe/rt_profiler_data_update.py  /centralized_scheduler/rt_profiler_data_update.py

# IF YOU WANNA DEPLOY A DIFFERENT APPLICATION JUST CHANGE THIS LINE
ADD {app_file}/scripts/ /centralized_scheduler/

ADD jupiter_config.ini /jupiter_config.ini
ADD jupiter_config.py /jupiter_config.py

ADD pricing_circe/pricing_coordinator.py /centralized_scheduler/pricing_coordinator.py
ADD pricing_circe/start_worker.sh /start.sh
RUN chmod +x /start.sh

WORKDIR /

# tell the port number the container should expose
EXPOSE {ports}

# run the command
CMD ["./start.sh"]

"""

############################################ DOCKER GENERATORS #########################################################

template_computing_worker ="""\
# Instructions copied from - https://hub.docker.com/_/python/
FROM ubuntu:16.04

RUN apt-get -yqq update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -yqq install python3-pip python3-dev libssl-dev libffi-dev 
RUN apt-get install -yqq openssh-client openssh-server bzip2 wget net-tools sshpass screen
RUN apt-get install -y vim
RUN apt-get install g++ make openmpi-bin libopenmpi-dev -y
RUN apt-get install sudo -y
RUN apt-get install iproute2 -y

## Install TASK specific needs. The hadoop is a requirement for the network profiler application
##RUN wget http://supergsego.com/apache/hadoop/common/hadoop-2.8.1/hadoop-2.8.1.tar.gz -P ~/
RUN wget https://archive.apache.org/dist/hadoop/core/hadoop-2.8.1/hadoop-2.8.1.tar.gz -P ~/
RUN tar -zxvf ~/hadoop-2.8.1.tar.gz -C ~/
RUN rm ~/hadoop-2.8.1.tar.gz
ADD pricing_circe/requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt
RUN echo '{username}:{password}' | chpasswd
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

RUN mkdir -p /centralized_scheduler/input
RUN mkdir -p /centralized_scheduler/output
RUN mkdir -p /centralized_scheduler/runtime
RUN mkdir -p /home/darpa/apps/data

ADD pricing_circe/rt_profiler_data_update.py  /centralized_scheduler/rt_profiler_data_update.py

# IF YOU WANNA DEPLOY A DIFFERENT APPLICATION JUST CHANGE THIS LINE
ADD {app_file}/scripts/ /centralized_scheduler/

ADD jupiter_config.ini /jupiter_config.ini
ADD jupiter_config.py /jupiter_config.py

ADD pricing_circe/pricing_calculator.py /centralized_scheduler/pricing_calculator.py
ADD pricing_circe/start_computing_worker.sh /start.sh
RUN chmod +x /start.sh

WORKDIR /

# tell the port number the container should expose
EXPOSE {ports}

# run the command
CMD ["./start.sh"]

"""

############################################ DOCKER GENERATORS #########################################################


def write_circe_computing_worker_docker(**kwargs):
    """
        Function to Generate the Dockerfile of the worker nodes
    """
    dfp = DockerfileParser(path='computing_worker_node.Dockerfile')
    dfp.content =template_computing_worker.format(**kwargs)
    # print(dfp.content)

def write_circe_controller_worker_docker(**kwargs):
    """
        Function to Generate the Dockerfile of the worker nodes
    """
    dfp = DockerfileParser(path='controller_worker_node.Dockerfile')
    dfp.content =template_controller_worker.format(**kwargs)
    # print(dfp.content)


def write_circe_home_docker(**kwargs):
    """
        Function to Generate the Dockerfile of the home/master node of CIRCE
    """
    dfp = DockerfileParser(path='home_node.Dockerfile')
    dfp.content =template_home.format(**kwargs)


if __name__ == '__main__':
    write_circe_home_docker(username = 'root',
                      password = 'PASSWORD',
                      app_file='app_specific_files/network_monitoring',
                      ports = '22 8888')

    write_circe_controller_worker_docker(username = 'root',
                      password = 'PASSWORD',
                      app_file='app_specific_files/network_monitoring',
                      ports = '22 57021')
    write_circe_computing_worker_docker(username = 'root',
                      password = 'PASSWORD',
                      app_file='app_specific_files/network_monitoring',
                      ports = '22 57021')
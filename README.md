# Documentation to access ctrlX OS images

This repository contains the images to start ctrlX OS on a GitHub runner. In order to control access to these images this repostory is internal in the Bosch Rexroth GitHub organisation and is only accessable from outside via a deposited ssh key pair. 
The following will elaborate on the architecture to start a workflow with ctrlX OS and how to create and deposite ssh keys for access.

## Workflow Architecture

![404 image not found](https://github.com/jmohren/workflow-ctrlx-app/blob/master/pictures/workflow-architecture.png)

## Create New Access

Create new ssh key pair:
![404 image not found](https://github.com/jmohren/workflow-ctrlx-app/blob/master/pictures/ssh-key-pair.png)

Deposite public key in the ctrlx-imgs repository under settings and deploy keys:
![404 image not found](https://github.com/jmohren/workflow-ctrlx-app/blob/master/pictures/github-public-key.png)

Deposite private key in the customers repository under settings, secrets and actions (either in our GitHub organisation or their GitHub organisation):
![404 image not found](https://github.com/jmohren/workflow-ctrlx-app/blob/master/pictures/github-private-key.png)
#!/bin/bash

echo -e "Stop all running splunk containers\n"
docker stop $(docker ps -af "name=splunk")
echo -e "\nContainers stopped\n-----------\nStart deleting splunk containers\n"
docker rm $(docker ps -af "name=splunk")
echo -e "\nContainers deleted\n-----------\nStart deleting all splunk_deployment images\n"
docker rmi splunk_deployment
echo -e "\nImages deleted\n"

echo -e "Building with docker-compose"
docker-compose up -d
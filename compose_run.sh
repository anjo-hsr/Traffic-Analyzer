#!/bin/bash

echo -e "Stop all running splunk containers\n"
docker stop $(docker ps -af "name=splunk")
echo -e "\nContainers stopped\n-----------\nStart deleting splunk containers\n"
docker rm $(docker ps -af "name=splunk")
echo -e "\nContainers deleted\n-----------\nStart deleting all splunk_deployment images\n"
docker rmi splunk_deployment
echo -e "\nImages deleted\n"

echo -e "Building with docker-compose"

tar --exclude="./docker" --exclude="bin/files" --exclude="*.gitignore" --exclude="bin/test" --exclude="*/.*" --exclude="*/__pycache__" \
    -zcvf ./docker/init_files/traffic_analyzer/traffic-analyzer.tar.gz \
    ./appserver ./bin ./default ./local ./lookups ./metadata ./static \
    --transform s/./traffic_analyzer/

docker-compose up -d
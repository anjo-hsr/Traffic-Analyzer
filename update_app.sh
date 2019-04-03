#!/bin/bash

tar --exclude="./docker" --exclude="bin/files" --exclude="*.gitignore" --exclude="bin/test" --exclude="*/.*" --exclude="*/__pycache__" \
    -zcvf ./docker/init_files/traffic_analyzer/traffic_analyzer.tar.gz \
    ./appserver ./bin ./default ./local ./lookups ./metadata ./static \
    --transform s/./traffic_analyzer/

docker cp docker/init_files/traffic_analyzer/traffic_analyzer.tar.gz splunk:/tmp/traffic_analyzer/
docker exec -it splunk sudo /opt/splunk/bin/splunk install app /tmp/traffic_analyzer/traffic_analyzer.tar.gz -auth admin:AnJo-HSR -update 1
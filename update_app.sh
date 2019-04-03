#!/bin/bash

tar --exclude="./docker" --exclude="bin/files" --exclude="*.gitignore" --exclude="bin/test" --exclude="*/.*" --exclude="*/__pycache__" \
    -zcvf ./docker/init_files/traffic_analyzer/traffic-analyzer.tar.gz \
    ./appserver ./bin ./default ./local ./lookups ./metadata ./static \
    --transform s/./traffic_analyzer/

docker cp docker/splunk_apps/traffic-analyzer.tar.gz splunk:/tmp/splunk_apps/
docker exec -it splunk /opt/splunkt/bin/splunk install app /tmp/splunk_apps/traffic-analyzer.tar.gz -auth admin:AnJo-HSR -update 1
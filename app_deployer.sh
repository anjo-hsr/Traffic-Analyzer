#!/bin/bash

function stop_splunk(){
    echo -e "Stop all running splunk containers\n"
    docker stop $(docker ps -af "name=splunk")
    echo -e "\nContainers stopped\n-----------\nStart deleting splunk containers\n"
}

function delete_containers() {
    docker rm $(docker ps -af "name=splunk")
    echo -e "\nContainers deleted\n-----------\nStart deleting all splunk_deployment images\n"
    docker rmi splunk_deployment
    echo -e "\nImages deleted\n"
}

function building_splunk() {
    echo -e "Building with docker-compose"
    docker-compose up -d
    echo -e "Wait till docker container is running (~60s)"

    while [[ $(docker ps -q --filter health=starting --filter name=splunk --format "{{.Names}}" | grep splunk) ]]
    do
        sleep 1
    done
}

function create_tar() {
    echo -e "Create traffic_analyzer.tar.gz"
    tar --exclude="./docker" --exclude="bin/files" --exclude="*.gitignore" --exclude="bin/test" \
        --exclude="*/.*" --exclude="*/__pycache__" \
        -zcvf ./docker/init_files/traffic_analyzer/traffic_analyzer.tar.gz \
        -C backend/ bin \
        -C ../frontend/ appserver default local lookups metadata static \
        --transform "s,^,traffic_analyzer/,"

    echo -e "File traffic_analyzer.tar.gz file created"
}

function update_traffic_analyzer() {
    echo -e "Copy traffic_analyzer.tar.gz to docker container and restart splunk service"
    sleep 5
    docker cp docker/init_files/traffic_analyzer/traffic_analyzer.tar.gz splunk:/tmp/traffic_analyzer/
    docker exec splunk bash -c 'sudo /opt/splunk/bin/splunk install app /tmp/traffic_analyzer/traffic_analyzer.tar.gz -auth admin:AnJo-HSR -update 1'
    docker exec splunk bash -c 'sudo /opt/splunk/bin/splunk restart splunkd'
}

function import_csvs() {
    echo -e "Import standard csv files from ./docker/init_files/csv"
    docker exec splunk bash -c 'for csv in /tmp/csv/*.csv; do sudo /opt/splunk/bin/splunk add oneshot "$csv" -auth admin:AnJo-HSR; done'
}

case "$1" in
    start)
        stop_splunk
        delete_containers
        building_splunk
        create_tar
        update_traffic_analyzer
        import_csvs
        ;;

    update)
        create_tar
        update_traffic_analyzer
        ;;

    *)
        echo $"Usage: $0 {start|update}"
        exit 1
esac
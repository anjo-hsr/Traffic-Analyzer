#!/bin/bash

function stop_splunk(){
    echo -e "\nStop all running $containerName containers\n"
    docker stop $(docker ps -af "name=$containerName")
    echo -e "\nContainers stopped\n-----------\nStart deleting $containerName containers\n"
}

function delete_containers() {
    docker rm $(docker ps -af "name=$containerName")
    echo -e "\nContainers deleted\n-----------\nStart deleting all $imageName images\n"
    docker rmi ${imageName}
    echo -e "\nImages deleted\n"
}

function building_splunk() {
    echo -e "\nBuilding with docker-compose"
    docker-compose up -d
    echo -e "Wait till docker container is running (~60s)"

    while [[ $(docker ps -q --filter health=starting --filter name=${containerName} --format "{{.Names}}" | grep ${containerName}) ]]
    do
        sleep 1
    done
}

function create_tar() {
    echo -e "\nCreate traffic-analyzer.tar.gz"
    tar --exclude="./docker" --exclude="bin/files" --exclude="*.gitignore" --exclude="bin/test" \
        --exclude="*/.*" --exclude="*/__pycache__" \
        -zcvf ./docker/init_files/traffic-analyzer/traffic-analyzer.tar.gz \
        -C backend/ bin \
        -C ../frontend/ appserver default local lookups metadata static \
        --transform "s,^,traffic-analyzer/,"

    echo -e "File traffic-analyzer.tar.gz file created"
}

function remove_traffic-analyzer() {
    echo -e "\nRemove traffic-analyzer from docker container"
    docker exec ${containerName} bash -c 'sudo /opt/splunk/bin/splunk remove app traffic-analyzer -auth admin:AnJo-HSR'
}

function install_requirements() {
    echo -e "\nCopy requirements inside requirements.txt and install them"
    docker cp ./requirements.txt ${containerName}:/tmp/
    docker exec ${containerName} bash -c 'sudo pip3 install -r /tmp/requirements.txt'
}

function update_traffic-analyzer() {
    echo -e "\nCopy traffic-analyzer.tar.gz to docker container and restart splunk service"
    sleep 5
    docker cp ./docker/init_files/traffic-analyzer/traffic-analyzer.tar.gz ${containerName}:/tmp/traffic-analyzer/
    docker exec ${containerName} bash -c 'sudo /opt/splunk/bin/splunk install app /tmp/traffic-analyzer/traffic-analyzer.tar.gz -auth admin:AnJo-HSR -update 1'
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/ -type d -exec sudo chmod 755 {} \;'
    docker exec ${containerName} bash -c 'sudo find /tmp/ -type d -exec sudo chmod 777 {} \;'

    #Must be done till tshark is updated to version 3.0.0 for debian
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/ -type f -exec sed -i 's/tls./ssl./g' {} +'

    docker exec ${containerName} bash -c 'sudo /opt/splunk/bin/splunk restart splunkd'
}

function import_csvs() {
    echo -e "\nImport standard csv files from ./docker/init_files/csvs"
    docker exec ${containerName} bash -c 'for csv in /tmp/csvs/*.csv; do sudo /opt/splunk/bin/splunk add oneshot "$csv" -auth admin:AnJo-HSR; done'
}

containerName="splunk_traffic-analyzer"
imageName="${containerName}_image"

case "$1" in
    start)
        stop_splunk
        delete_containers
        building_splunk
        install_requirements
        create_tar
        update_traffic-analyzer
        import_csvs
        ;;

    update)
        install_requirements
        create_tar
        update_traffic-analyzer
        ;;

    force-update)
        install_requirements
        create_tar
        remove_traffic-analyzer
        update_traffic-analyzer
        ;;

    *)
        echo $"Usage: $0 {start|update|force-update}"
        exit 1
esac
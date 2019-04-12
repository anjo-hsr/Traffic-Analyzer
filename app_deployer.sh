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
}

function wait_till_container_is_running() {
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

    set_rights
    fix_tshark

    docker exec ${containerName} bash -c 'sudo /opt/splunk/bin/splunk restart splunkd'
}

function set_rights() {
    echo -e "\nSet rights on folders and files"
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/ -type d -exec sudo chmod 775 {} \;'
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/lookups -type d -exec sudo chmod 777 {} \;'

    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/ -type f -exec sudo chmod 664 {} \;'
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/main/*.py -type f -exec sudo chmod 775 {} \;'
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/main/*/*.py -type f -exec sudo chmod 775 {} \;'

    docker exec ${containerName} bash -c 'sudo find /tmp/ -type d -exec sudo chmod 777 {} \;'
}

function fix_tshark() {
    #Must be done till tshark is updated to version 3.0.0 for debian
    echo -e "\nReplace tls. with ssl for tshark versions 2.x"
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/ -type f -exec sed -i 's/tls\.handshake/ssl\.handshake/g' {} +'
}

containerName="splunk_traffic-analyzer"
imageName="${containerName}_image"

case "$1" in
    start)
        stop_splunk
        delete_containers
        building_splunk
        create_tar
        wait_till_container_is_running
        install_requirements
        update_traffic-analyzer
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
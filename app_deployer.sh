#!/bin/bash

function stop_splunk(){
    echo -e "\nStop all running $containerName containers\n"
    docker stop $(docker ps -aq -f "name=$containerName")
    echo -e "\nContainers stopped\n-----------\nStart deleting $containerName containers\n"
}

function delete_containers() {
    docker rm $(docker ps -aq -f "name=${containerName}")
    echo -e "\nContainers deleted\n-----------"
}

function delete_images() {
    echo -e "\nStart deleting all ${imageName} images"
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
    if [[ -z "$2" ]]; then
        tarPath="./docker/init_files/traffic-analyzer"
    else
        tarPath=$2
    fi
    
    echo -e "\nCreate traffic-analyzer.tar.gz"
    if ! [[ -z "$1" ]] && [[ "$1" == "update" ]] ; then
        create_update_tar ${tarPath}
        tarType="Update"
    else
        create_normal_tar ${tarPath}
        tarType="Normal"
    fi

    echo -e "${tarType} file traffic-analyzer.tar.gz created under ${tarPath}"
}

function create_normal_tar() {
    tarPath=$1
    tar --exclude="./docker" --exclude="bin/files/*" --exclude="*.gitignore" --exclude="bin/test" \
        --exclude="*/.*" --exclude="*/__pycache__" \
        -zcvf "${tarPath}/traffic-analyzer.tar.gz" \
        -C backend/ bin \
        -C ../frontend/ appserver default local lookups metadata static \
        --transform "s,^,traffic-analyzer/,"
}

function create_update_tar() {
    tarPath=$1
    tar --exclude="./docker" --exclude="bin/files/*" --exclude="*.gitignore" --exclude="bin/test" \
        --exclude="*/.*" --exclude="*/__pycache__" --exclude="local/*.conf"\
        -zcvf "${tarPath}/traffic-analyzer.tar.gz" \
        -C backend/ bin \
        -C ../frontend/ appserver default lookups metadata static \
        --transform "s,^,traffic-analyzer/,"
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
    fix_line_endings

    docker exec ${containerName} bash -c 'sudo /opt/splunk/bin/splunk restart splunkd'
}

function set_rights() {
    echo -e "\nSet rights on folders and files"
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/ -type d -exec sudo chmod 775 {} \;'
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/lookups -type d -exec sudo chmod 777 {} \;'

    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/ -type f -exec sudo chmod 664 {} \;'
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/ -name "*.sh" -type f -exec sudo chmod 775 {} \;'
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/ -name "*.py" -type f -exec sudo chmod 775 {} \;'

    docker exec ${containerName} bash -c 'sudo find /tmp/ -type d -exec sudo chmod 777 {} \;'
}

function fix_line_endings(){
    echo -e "\nSet line endings"
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/ -type f -print0 | xargs -0 sudo dos2unix > /dev/null 2>&1'
}

function fix_tshark() {
    #Must be done till tshark is updated to version 3.0.0 for debian
    echo -e "\nReplace tls with ssl and dhcp.option.dhcp with bootp.option.dhcp for tshark versions 2.x"
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/ -type f -exec sed -i 's/tls\.handshake/ssl\.handshake/g' {} +'
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/ -type f -exec sed -i 's/tls\.record/ssl\.record/g' {} +'
    docker exec ${containerName} bash -c 'sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/ -type f -exec sed -i 's/dhcp\.option\.dhcp/bootp\.option\.dhcp/g' {} +'
}

function copy_pcaps() {
    docker cp ./docker/init_files/pcaps/ ${containerName}:/tmp/
}

function test_splunk_app() {
    seconds=$1
    trafficAnalyzer=`docker exec ${containerName} bash -c "sudo /opt/splunk/bin/splunk package app ${appName} -auth admin:AnJo-HSR"`

    echo -e "\nSleep for $seconds seconds till the additional lists are downloaded and all lists are imported."
    sleep ${seconds}
    tcpEntry=`docker exec ${containerName} bash -c "sudo /opt/splunk/bin/splunk search 'sourcetype=\"list\" Decimal=\"6\" Keyword=\"TCP\"' -auth admin:AnJo-HSR"`
    tcpString="6,TCP,Transmission Control,,[RFC793]"

    macEntry=`docker exec ${containerName} bash -c "sudo /opt/splunk/bin/splunk search 'sourcetype=\"list\" eth_short=\"00:00:0c\"' -auth admin:AnJo-HSR"`
    macString='00:00:0c,"Cisco Systems, Inc"'

    cipherSuiteEntry=`docker exec ${containerName} bash -c "sudo /opt/splunk/bin/splunk search 'sourcetype=\"list\" cipher_suite_number=\"49200\"' -auth admin:AnJo-HSR"`
    cipherSuiteString="49200,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,Y"

    if [[ "${trafficAnalyzer}" == *"App '${appName}' is packaged."* ]] && [[ "${tcpEntry}" == "${tcpString}" ]] && [[ "${macEntry}" == "${macString}" ]] && [[ "${cipherSuiteEntry}" == "${cipherSuiteString}" ]]; then
        echo "App test was successful."
    else
        echo "App test failed."
        return 1
    fi
}

function build_splunk() {
        building_splunk
        create_tar
        copy_pcaps
        wait_till_container_is_running
        install_requirements
        update_traffic-analyzer
        test_splunk_app 60
}

containerName="splunk_traffic-analyzer"
imageName="${containerName}_image"
appName="traffic-analyzer"

case "$1" in
    recreate)
        stop_splunk
        delete_containers
        delete_images
        build_splunk
        ;;

    create)
        stop_splunk
        delete_containers
        build_splunk
        ;;

    update)
        install_requirements
        create_tar "update"
        update_traffic-analyzer
        test_splunk_app 5
        ;;

    force-update)
        install_requirements
        create_tar "normal"
        remove_traffic-analyzer
        update_traffic-analyzer
        test_splunk_app 5
        ;;

    generate-tar)
        create_tar "normal" $2
        ;;

    copy-pcaps)
        copy_pcaps
        ;;

    test-app)
        test_splunk_app 5
        ;;

    *)
        echo -e    $"Usage: $0 {create|update|force-update|generate-tar|copy-pcaps|test-app}\n"\
                    "   - create:         Remove ${containerName} containers and run new container from image with installed ${appName}\n"\
                    "   - recreate:       Remove ${containerName} containers and ${imageName} images and generates new image and container with installed ${appName}\n"\
                    "   - update:         Update ${appName} splunk app\n"\
                    "   - force-update:   Remove and reinstall ${appName} splunk app\n"\
                    "   - generate-tar:   Generates only tar.gz app file. Define path with.\n"\
                    "   - copy-pcaps:     Copy pcaps from ./docker/docker_init folder into container\n"\
                    "   - test-app:       Test splunk app by checking some imported events."
        exit 1
esac

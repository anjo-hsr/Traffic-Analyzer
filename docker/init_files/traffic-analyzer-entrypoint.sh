#!/bin/bash

function install_traffic-analyzer() {
    echo -e "\nInstall traffic-analyzer.tar.gz and restart splunk service"
    sleep 5
    sudo /opt/splunk/bin/splunk install app /tmp/traffic-analyzer/traffic-analyzer.tar.gz -auth admin:AnJo-HSR -update 1

    set_rights
    fix_tshark
    fix_line_endings

    sudo /opt/splunk/bin/splunk restart splunkd
}

function set_rights() {
    echo -e "\nSet rights on folders and files"
    sudo find /opt/splunk/etc/apps/traffic-analyzer/ -type d -exec sudo chmod 775 {} \;
    sudo find /opt/splunk/etc/apps/traffic-analyzer/lookups -type d -exec sudo chmod 777 {} \;

    sudo find /opt/splunk/etc/apps/traffic-analyzer/ -type f -exec sudo chmod 664 {} \;
    sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/ -name "*.sh" -type f -exec sudo chmod 775 {} \;
    sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/ -name "*.py" -type f -exec sudo chmod 775 {} \;

    sudo find /tmp/ -type d -exec sudo chmod 777 {} \;
}

function fix_tshark() {
    #Must be done till tshark is updated to version 3.0.0 for debian
    echo -e "\nReplace tls with ssl and dhcp.option.dhcp with bootp.option.dhcp for tshark versions 2.x"
    sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/ -type f -exec sed -i 's/tls\.handshake/ssl\.handshake/g' {} +
    sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/ -type f -exec sed -i 's/dhcp\.option\.dhcp/bootp\.option\.dhcp/g' {} +
}

function fix_line_endings(){
    echo -e "\nSet line endings"
    sudo find /opt/splunk/etc/apps/traffic-analyzer/bin/ -type f -print0 | xargs -0 sudo dos2unix > /dev/null 2>&1
}

if [[ -z "$SPLUNK_PASSWORD" ]]; then
    echo -e "No Password for Splunk login set. Please try again. Example:\n" \
        "docker run -p 8000:8000 -p 8089:8089 -e SPLUNK_PASSWORD=AnJo-HSR traffic-analyzer"
    exit 1
fi


/sbin/entrypoint.sh start-and-exit
install_traffic-analyzer

sudo -u splunk tail -n 0 -f ${SPLUNK_HOME}/var/log/splunk/splunkd_stderr.log &
wait
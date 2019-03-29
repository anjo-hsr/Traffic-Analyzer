FROM splunk/splunk:latest

ARG INIT_DIR
ARG CONFIG_DIR
ARG PORT
ARG SPLUNK_PASSWORD
ARG SPLUNK_START_ARGS

EXPOSE $PORT

RUN sudo mkdir -p $INIT_DIR
ADD init_files/ $INIT_DIR

RUN sudo mkdir -p $CONFIG_DIR
ADD config $CONFIG_DIR

RUN sudo apt update
RUN sudo apt install tshark -y
RUN sudo apt install python3 -y


ENV PORT $PORT
ENV SPLUNK_PASSWORD $SPLUNK_PASSWORD
ENV SPLUNK_START_ARGS $SPLUNK_START_ARGS
ENV SPLUNK_APPS_URL "https://files.orgelbauergoll.ch/pcap-analyzer-for-splunk_4110.tgz"

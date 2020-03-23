FROM splunk/splunk:8.0-debian

ARG INIT_DIR
ARG WEB_PORT
ARG REST_API_PORT
ARG SPLUNK_PASSWORD
ARG SPLUNK_START_ARGS

EXPOSE $WEB_PORT
EXPOSE $REST_API_PORT

RUN sudo mkdir -p $INIT_DIR
ADD init_files $INIT_DIR

RUN sudo apt update
RUN sudo apt install dos2unix -y
RUN sudo apt install tshark -y
RUN sudo apt install python3 python3-pip -y

ENV SPLUNK_PASSWORD $SPLUNK_PASSWORD
ENV SPLUNK_START_ARGS $SPLUNK_START_ARGS

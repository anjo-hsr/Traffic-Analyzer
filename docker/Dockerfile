FROM splunk/splunk:latest

ARG INIT_DIR
ARG WEB_PORT
ARG REST_API_PORT
ARG SPLUNK_PASSWORD
ARG SPLUNK_START_ARGS

EXPOSE $WEB_PORT
EXPOSE $REST_API_PORT

RUN sudo mkdir -p $INIT_DIR
ADD init_files $INIT_DIR

RUN sudo cat /etc/*release
RUN sudo yum update
RUN sudo yum install dos2unix -y
RUN sudo yum install tshark -y
RUN sudo yum install python3 python3-pip -y

ENV SPLUNK_PASSWORD $SPLUNK_PASSWORD
ENV SPLUNK_START_ARGS $SPLUNK_START_ARGS
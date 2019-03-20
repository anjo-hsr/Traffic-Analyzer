FROM splunk/splunk:latest

ARG WORKDIR
ARG PORT
ARG SPLUNK_PASSWORD
ARG SPLUNK_START_ARGS

EXPOSE $PORT


RUN ["mkdir", "/tmp/pcaps"]
ADD pcaps $WORKDIR

RUN ["sudo", "apt", "update"]
RUN ["sudo", "apt", "install", "tshark", "-y"]


ENV PORT $PORT
ENV SPLUNK_PASSWORD $SPLUNK_PASSWORD
ENV SPLUNK_START_ARGS $SPLUNK_START_ARGS
ENV SPLUNK_APPS_URL "https://files.orgelbauergoll.ch/pcap-analyzer-for-splunk_4110.tgz"

#!/bin/bash
SOURCE_FOLDER=$(dirname "${BASH_SOURCE[0]}")
python3 ${SOURCE_FOLDER}/main/traffic_analyzer.py download &>/dev/null
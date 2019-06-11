# Traffic-Analyzer <img width="32" src="frontend/static/appIcon.png">
[![Build Status](https://img.shields.io/travis/anjo-hsr/Traffic-Analyzer/master.svg?logo=travis)](https://travis-ci.org/anjo-hsr/Traffic-Analyzer)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=anjo-hsr_Traffic-Analyzer&metric=alert_status)](https://sonarcloud.io/dashboard?id=anjo-hsr_Traffic-Analyzer)
[![Python 3.7](https://img.shields.io/badge/python-3.7-yellow.svg?logo=python)](https://www.python.org/)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-yellow.svg?logo=python)](https://www.python.org/dev/peps/pep-0008/)
[![IP Location Finder](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fraw.githubusercontent.com%2Fanjo-hsr%2FTraffic-Analyzer%2Fmaster%2FbadgeEndpoint%2Fkeycdn.json)](https://tools.keycdn.com/geo)

## Deployment script
Start using traffic analyzer with the given [app_deployer.sh](https://github.com/anjo-hsr/Traffic-Analyzer/blob/master/app_deployer.sh) script.  
- Use the parameter *start* to setup a new docker image and deploy it on port 8000 on the machine running docker.  
- Use the parameter *update* to update the app traffic-analyzer inside the docker container.  
- Use the parameter *force-update* to uninstall the app traffic-analyzer first before reinstalling it inside the docker container.  
- Use the parameter *copy-pcaps* to copy new pcaps into the docker container from the given folder ./docker/init_files/pcaps  
  
## Access the container
The container will be deployed on *:8000* on the machine running docker.
HTTPS can be implemented by using a reverse proxy or by following [this manual](https://docs.splunk.com/Documentation/Splunk/latest/Security/TurnonbasicencryptionwithSplunkWeb)
Changing the port can be done by changing the variable *WEB_PORT* in the .env file

## Login credentials
The default login credentials are:
- username: **admin**
- password: **AnJo-HSR**

To change them please edit the .env file. The password must follow the given [password policy from splunk](https://docs.splunk.com/Documentation/Splunk/latest/Security/Configurepasswordsinspecfile) otherwise the container will not start.

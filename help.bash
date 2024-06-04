#bin/bash

sudo docker build -t crm .
sudo docker tag crm prousername/crm
sudo docker push prousername/crm
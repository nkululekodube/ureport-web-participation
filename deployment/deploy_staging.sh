#! /bin/bash
pip install ansible==1.9.2
sudo ansible-playbook -e 'host_key_checking=False' deploy.yml -i hosts 

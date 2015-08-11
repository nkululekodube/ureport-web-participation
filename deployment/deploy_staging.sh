#! /bin/bash
pip install ansible==1.9.2
ansible-playbook deploy.yml -i hosts 

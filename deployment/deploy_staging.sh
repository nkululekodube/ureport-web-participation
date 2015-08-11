#! /bin/bash
pip install ansible==1.9.2
sudo ansible-playbook deploy.yml -i hosts -vvvv

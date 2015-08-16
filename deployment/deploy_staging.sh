#! /bin/bash
pip install ansible==1.9.2
sudo -i hosts -l staging ansible-playbook --vault-password-file=vault_file

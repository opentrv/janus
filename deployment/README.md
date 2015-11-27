## Deploying to the Janus (production) server
`ansible-playbook playbooks/site.yml -i inventories/virtual_machine.ini --ask-sudo-pass`

## Deploying to a local vm
`ansible-playbook playbooks/site.yml -i inventories/virtual_machine.ini`
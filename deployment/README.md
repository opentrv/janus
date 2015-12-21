## Deploying to the Janus (production) server
`ansible-playbook playbooks/site.yml -i inventories/janus.ini --ask-sudo-pass`

Be sure to commit your changes to the git repository first; deployment involves fetching the data from the github repository and updating the source code on the server.

## Deploying to a local vm
`ansible-playbook playbooks/site.yml -i inventories/virtual_machine.ini`
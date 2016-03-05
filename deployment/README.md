## Deploying to the Janus (production) server
`ansible-playbook playbooks/site.yml -i inventories/janus.ini --ask-sudo-pass`

Be sure to commit your changes to the git repository first; deployment involves fetching the data from the github repository and updating the source code on the server. Note this will overwrite any changes made locally to the code repository on the server.

## Deploying to a local vm
`ansible-playbook playbooks/site.yml -i inventories/virtual_machine.ini`

This requires you have a virtual machine set up as described in the `virtual_machine.ini` inventory file. The better way to do this would be to have an inventory file generated for your instance of a virtual machine and have this file stored outside of the code repository. Alternatively you could instead use environment variables in the inventory file so that they are dynamic files.

## Deploying to pogon server

`ansible-playbook playbooks/site.yml -i inventories/pogon-blue.ini --vault-password-file=<file on your system>`

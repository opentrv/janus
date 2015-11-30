Copy this VagrantFile to the location where you want to install your virtual machine e.g.

`/home/david/opentrv/virtual_machine`

edit the file so that the share folder points to where you have the file locally, e.g.

`config.vm.synced_folder "/home/dvoong/opentrv/source", "/srv/opentrv/source",
                          :mount_options => ["uid=510,gid=510"]`

run,

`vagrant up`

edit the ansible inventory file at location,

`/home/dvoong/opentrv/source/deployment/inventories/virtual_machine.ini`

to match the location of the private key.

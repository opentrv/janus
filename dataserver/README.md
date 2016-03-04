# Data Server README

The `dataserver` component manages the read and write functionality of the OpenTRV projects. e.g. it contains modules for the starting, maintaining and configuration of the UDP server as well as the managing the process of populating the database with data. The data models used for storing data are however contained within the respective OpenTRV applications, e.g. the  [opentrv_sensor] (https://github.com/opentrv/janus/tree/master/opentrv_sensor) application contains the models for storing data from the REV devices.

* [`udpserver.py`] (https://github.com/opentrv/janus/blob/master/dataserver/udpserver.py): udpserver module, contains the `UDPServer` class and methods for the `DatagramProtocol` class which manages how incoming UDP messages are handled.
* [`urls.py`] (https://github.com/opentrv/janus/blob/master/dataserver/urls.py): contains API URL paths
* [`management/commands`] (https://github.com/opentrv/janus/tree/master/dataserver/management/commands): Contains scripts for starting the UDP server and for sending UDP packets.

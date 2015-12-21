# Data Server README

The `dataserver` component manages the read and write functionality of the OpenTRV projects. e.g. it contains modules for the starting, maintaining and configuration of the UDP server as well as the managing the process of populating the database with data. The data models used for storing data are however contained within the respective OpenTRV applications, e.g. the  [opentrv_sensor] (https://github.com/dvoong/opentrv/tree/master/opentrv_sensor) application contains the models for storing data from the REV devices.

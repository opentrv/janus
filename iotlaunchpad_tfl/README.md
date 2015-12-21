# IOTLaunchpad TFL

This application monitors bus shelter environments, in particular its occupany both live and as a function of time.

* [`data`](https://github.com/dvoong/opentrv/tree/master/iotlaunchpad_tfl/data): Contains bus shelter data for initial trials of the IOTLaunchpad sensors
* [`fixtures`](https://github.com/dvoong/opentrv/tree/master/iotlaunchpad_tfl/fixtures): Contains initial bus shelter data for use in testing
* [`management/commands/initialise_db.py`] (https://github.com/dvoong/opentrv/blob/master/iotlaunchpad_tfl/management/commands/initialise_db.py): Initialise the database with initial bus shelter data
* [`scripts/get_station_info.py`] (https://github.com/dvoong/opentrv/blob/master/iotlaunchpad_tfl/scripts/get_station_info.py): Gets bus shelter information from the [TFL API](https://api.tfl.gov.uk/) such as longitude and latitude
* [`static`](https://github.com/dvoong/opentrv/tree/master/iotlaunchpad_tfl/static/iotlaunchpad_tfl) and [`templates`](https://github.com/dvoong/opentrv/tree/master/iotlaunchpad_tfl/templates/iotlaunchpad_tfl) directories: Contains html templates and javascript for the client front end

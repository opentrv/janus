# README

This application contains components for creating, modifying and reading data from the OpenTRV REV sensors.

* [`models.py`](https://github.com/dvoong/opentrv/blob/master/opentrv_sensor/models.py): Defines the database structure for storing the data.
* [`fixtures`](https://github.com/dvoong/opentrv/tree/master/opentrv_sensor/fixtures): Trial data for testing purposes
* [`sample_data`](https://github.com/dvoong/opentrv/tree/master/opentrv_sensor/sample_data): Sample data provided from tests run by Damon in January 2015
* [`urls.py`](https://github.com/dvoong/opentrv/blob/master/opentrv_sensor/urls.py): API URLs
* [`views.py`](https://github.com/dvoong/opentrv/blob/master/opentrv_sensor/views.py): API backend methods

## API Methods

### `GET /dataserver/api/opentrv/data`

Returns a list of measurements.

Parameters

* `date`: *optional*: Filter measurements on the date
* `datetime-first`: *optional*: Filter measurements after this datetime
* `datetime-last`: *optional*: Filter measurements before this datetime
* `type`: *optional*, *multivalue*: Filter measurements on the measurement type(s), e.g. "temperature"
* `sensor-id`: *optional*, *multivalue*: Filter measurements on the sensor-id(s)

### `GET /dataserver/api/opentrv/data/types`

Returns a list of measurement types in a set of measurements.

Parameters

* `datetime-first`: *optional*: Filter measurements after this datetime
* `datetime-last`: *optional*: Filter measurements before this datetime
* `type`: *optional*, *multivalue*: Filter measurements on the measurement type(s), e.g. "temperature"
* `sensor-id`: *optional*, *multivalue*: Filter measurements on the sensor-id(s)

### `GET /dataserver/api/opentrv/data/sensor-ids`

Returns a list of sensor-ids in a set of measurements.

Parameters

* `datetime-first`: *optional*: Filter measurements after this datetime
* `datetime-last`: *optional*: Filter measurements before this datetime
* `type`: *optional*, *multivalue*: Filter measurements on the measurement type(s), e.g. "temperature"
* `sensor-id`: *optional*, *multivalue*: Filter measurements on the sensor-id(s)

### `GET /dataserver/api/opentrv/data/dates`

Returns a the first and last datetimes in a set of measurements.

Parameters

* `datetime-first`: *optional*: Filter measurements after this datetime
* `datetime-last`: *optional*: Filter measurements before this datetime
* `type`: *optional*, *multivalue*: Filter measurements on the measurement type(s), e.g. "temperature"
* `sensor-id`: *optional*, *multivalue*: Filter measurements on the sensor-id(s)

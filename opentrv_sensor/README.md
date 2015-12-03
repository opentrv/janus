# README

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

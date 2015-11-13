import json
from dateutil import parser as date_parser
from django.db import models

# Create your models here.
class Measurement(models.Model):
    datetime = models.DateTimeField()
    sensor_id = models.CharField(max_length=10)
    type = models.CharField(max_length=20)
    value = models.FloatField()

    class Meta:
        unique_together = (("datetime", "type", "sensor_id"),)

    @staticmethod
    def create_from_udp(msg):
        # '[ "2015-01-01T00:00:43Z", "", {"@":"0a45","+":2,"vac|h":9} ]'
        json_object = json.loads(msg)
        datetime = date_parser.parse(json_object[0])
        sensor_id = json_object[2]['@']
        measurements = {}
        for key, val in json_object[2].iteritems():
            if key != '@' and key != '+':
                measurements[key] = val

        output = []
        for key, val in measurements.iteritems():
            if '|' in key:
                type_, units = key.split('|')
            else:
                type_ = key
                units = None

            type_ = {'vac': 'vacancy', 'T': 'temperature', 'L': 'light'}[type_]
            if type_ == 'temperature' and units == 'C16':
                val = val / 16.

            measurement = Measurement(datetime=datetime, sensor_id=sensor_id, type=type_, value=val)
            measurement.save()
            output.append(measurement)

        return output


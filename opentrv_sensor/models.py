import json
from dateutil import parser as date_parser
from django.db import models

def get_current_datetime():
    pass

def convert_datetime(datetime_string):
    pass

# Create your models here.
class Measurement(models.Model):
    '''
    vac = vacancy
    T = temperature
    B = Battery
    L = light
    v = valve open percent, 
    H = relative humidity, 
    tT = target temp, 
    vC = cumulative valve travel, 
    O = occupancy 0 = i don't know , 1 probably vacant, 2: probably occupancy, 3: definite occupancy
    '''
    datetime = models.DateTimeField()
    sensor_id = models.CharField(max_length=10)
    type = models.CharField(max_length=20)
    value = models.FloatField()

    class Meta:
        unique_together = (("datetime", "type", "sensor_id"),)

    @classmethod
    def to_dict(cls, measurement):
        if hasattr(measurement, '__iter__'): #isinstance(measurement, list):
            measurements = measurement
            output = []
            for measurement in measurements:
                output += [cls.to_dict(measurement)]
            return output
        return {
            'datetime': measurement.datetime.isoformat(),
            'sensor_id': measurement.sensor_id,
            'type': measurement.type,
            'value': measurement.value,
        }

    @staticmethod
    def create_from_log(msg):

        datetime, host_id, measurements  = json.loads(msg)
        msg = msg[msg.index('{'):msg.index('}') + 1]
        datetime = convert_datetime(datetime)
        output = Measurement.create_from_udp(msg, datetime=datetime)
        
        return output
    
    @staticmethod
    def create_from_udp(msg, datetime=None):
        output = {'success': [], 'failure': []}
        json_object = json.loads(msg)
        measurements = {}
        for key, val in json_object.iteritems():
            if key == '@':
                sensor_id = val
            elif key == '+':
                continue
            else:
                measurements[key] = val

        for key, val in measurements.iteritems():
            if '|' in key:
                type_, units = key.split('|')
            else:
                type_, units = (key, None)
            try:
                type_ = {'vac': 'vacancy',
                         'T': 'temperature',
                         'L': 'light',
                         'B': 'battery',
                         'v': 'valve_open_percent',
                         'H': 'relative_humidity',
                         'tT': 'target_temperature',
                         'vC': 'valve_travel',
                         'O': 'occupancy'
                }[type_]

                if type_ == 'temperature' or type_ == 'target_temperature':
                    if units == 'C16':
                        val = val / 16.
                    elif units == 'C':
                        pass
                    else:
                        raise Exception('Unrecognised unit of temperature')
                if type_ == 'battery':
                    if units == 'cV':
                        val = val * 0.01
                    elif units == 'V':
                        pass
                    elif units == 'mV':
                        val = val * 0.001
                    else:
                        raise Exception('Unrecognised unit of battery')

                measurement = Measurement(datetime=get_current_datetime() if datetime == None else datetime, sensor_id=sensor_id, type=type_, value=val)                
                measurement.save()
                output['success'].append(measurement)
            except KeyError as e:
                output['failure'].append({
                    'type': key,
                    'value': val
                })

        return output

        # json_object = json.loads(msg)
        # datetime = date_parser.parse(json_object[0])
        # sensor_id = json_object[2]['@']
        # measurements = {}
        # for key, val in json_object[2].iteritems():
        #     if key != '@' and key != '+':
        #         measurements[key] = val

        # output = {'success': [], 'failure': []}
        # for key, val in measurements.iteritems():
        #     if '|' in key:
        #         type_, units = key.split('|')
        #     else:
        #         type_ = key
        #         units = None

        #     try:
        #         type_ = {'vac': 'vacancy',
        #                  'T': 'temperature',
        #                  'L': 'light',
        #                  'B': 'battery',
        #                  'v': 'valve_open_percent',
        #                  'H': 'relative_humidity',
        #                  'tT': 'target_temperature',
        #                  'vC': 'valve_travel',
        #                  'O': 'occupancy'
        #         }[type_]
        #         if type_ == 'temperature' or type_ == 'target_temperature':
        #             if units == 'C16':
        #                 val = val / 16.
        #             elif units == 'C':
        #                 pass
        #             else:
        #                 raise Exception('Unrecognised unit of temperature')
        #         if type_ == 'battery':
        #             if units == 'cV':
        #                 val = val * 0.01
        #             elif units == 'V':
        #                 pass
        #             elif units == 'mV':
        #                 val = val * 0.001
        #             else:
        #                 raise Exception('Unrecognised unit of battery')

        #         measurement = Measurement(datetime=datetime, sensor_id=sensor_id, type=type_, value=val)
        #         measurement.save()
        #         output['success'].append(measurement)
        #     except KeyError as e:
        #         output['failure'].append({
        #             'type': key,
        #             'value': val
        #         })

        # return output


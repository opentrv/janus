import json

msg = bytes(b'{"@":"c2a1","+":5,"T|C16":124,"H|%":81,"O":1}')


json_object = json.loads(msg)
measurements = {}
for key, val in json_object.iteritems():
    if key == '@':
        sensor_id = val
    elif key == '+':
        continue
    else:
        measurements[key] = val


#this for loop is iterated for every reading
for key, val in measurements.iteritems():
    if '|' in key:
        type_, units = key.split('|')
    else:
        type_, units = (key, None)

    type_ = {'vac': 'vacancy',
                         'T': 'temperature',
                         'L': 'light',
                         'B': 'battery',
                         'v': 'valve_open_percent',
                         'H': 'relative_humidity',
                         'tT': 'target_temperature',
                         'vC': 'valve_travel',
                         'O': 'occupancy',
                         'b': 'boiler',
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
    if type_ == 'boiler':
        if val not in [0, 1]:
            raise Exception('Invalid value for boiler: {}, allowed values: [0, 1]'.format(val))

    


import pprint
import json
import requests

stops_filepath = '../data/bus_stops.json'
pp = pprint.PrettyPrinter(indent=4)

with open(stops_filepath, 'rb') as f:
    x = ''.join(f.readlines())
    stops = json.loads(x)

print json.dumps(stops, sort_keys=True, indent=4, separators=(',', ': '))

for group in stops:
    print 'group:', group
    for stop in stops[group]['stops']:
        print '\tstop: {name} ({naptan})'.format(**stop),
        response = requests.get('https://api.tfl.gov.uk/StopPoint/{}?app_id=&app_key='.format(stop['naptan']))
        response_json = response.json()
        naptan, name, lat, lon =  response_json['id'], response_json['commonName'], response_json['lat'], response_json['lon']
        stop['lat'] = lat
        stop['lon'] = lon
        stop['name'] = name
        stop['naptan'] = naptan
        print ', [{}, {}]'.format(lat, lon)

        assert name == stop['name'], 'error, name: {}, stop["name"]: {}'.format(name, stop['name'])
        
#print json.dumps(stops, sort_keys=True, indent=4, separators=(',', ': '))
print json.dumps(stops, sort_keys=True, indent=4)

with open('../data/bus_stops_updated.json', 'wb') as f:
    f.write(json.dumps(stops, sort_keys=True, indent=4))

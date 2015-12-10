import json
import requests

stops_filepath = '../data/bus_stops.json'

f = open(stops_filepath, 'rb')

x = ''.join(f.readlines())
print 'x:', x
stops = json.loads(x)

print stops

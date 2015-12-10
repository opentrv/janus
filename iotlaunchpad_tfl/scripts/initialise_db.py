import json
from argparse import ArgumentParser
from iotlaunchpad_tfl.models import BusStopGroup, BusStop

def main():
    parser = ArgumentParser()
    parser.add_argument('json_filepath', nargs='?', default='../data/bus_stops_updated.json')
    args = parser.parse_args()

    with open(args.json_filepath, 'rb') as f:
        bus_stops = json.loads(''.join(f.readlines()))

    for group_name in bus_stops:
        bus_stop_group = BusStopGroup(name=group_name)
        bus_stop_group.save()
        for bus_stop in bus_stops[group_name]['bus_stops']:
            bus_stop = BusStop(naptan_id=bus_stop['naptan'],
                               name=bus_stop['name'],
                               latitude=bus_stop['lat'],
                               longitude=bus_stop['lon']
            )
            bus_stop.save()

if __name__ == '__main__':
    main()

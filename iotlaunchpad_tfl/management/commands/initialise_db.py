import json
from argparse import ArgumentParser
from django.core.management.base import BaseCommand
from iotlaunchpad_tfl.models import BusStopGroup, BusStop, BusStopToBusStopGroup

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('json_filepath', nargs='?', default='iotlaunchpad_tfl/data/bus_stops_updated.json')

    def handle(self, json_filepath, *args, **kwargs):

        with open(json_filepath, 'rb') as f:
            bus_stops = json.loads(''.join(f.readlines()))

        for group_name in bus_stops:
            bus_stop_group = BusStopGroup.objects.get_or_create(name=group_name)[0]
            for bus_stop in bus_stops[group_name]['stops']:
                bus_stop = BusStop.objects.update_or_create(naptan_id=bus_stop['naptan'],
                                   name=bus_stop['name'],
                                   latitude=bus_stop['lat'],
                                   longitude=bus_stop['lon']
                )[0]

                bus_stop_to_bus_stop_group = BusStopToBusStopGroup.objects.get_or_create(bus_stop=bus_stop, bus_stop_group=bus_stop_group)



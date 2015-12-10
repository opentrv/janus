import unittest
from iotlaunchpad_tfl.tests.test_models import TestModel
from iotlaunchpad_tfl.models import BusStop, BusStopGroup, BusStopToBusStopGroup

class TestBusStopGroup(TestModel):
    pass

class TestInit(TestBusStopGroup):

    def test(self):

        bus_stop1 = BusStop(name="Southwark Underground Station", latitude=51.50398, longitude=-0.104935, naptan_id="490013323SA")
        bus_stop2 = BusStop(**{
            "latitude": 51.50398,
            "longitude": -0.104935,
            "name": "Southwark Underground Station",
            "naptan_id": "490013323SB"
        })
        bus_stop3 = BusStop(**{
            "latitude": 51.504269,
            "longitude": -0.113356,
            "name": "Waterloo",
            "naptan_id": "490000254QA"
        })
        bus_stop_group = BusStopGroup(name="palestra")

        bus_stop1.save()
        bus_stop2.save()
        bus_stop3.save()
        bus_stop_group.save()
        
        x = BusStopToBusStopGroup(bus_stop=bus_stop1, bus_stop_group=bus_stop_group)
        y = BusStopToBusStopGroup(bus_stop=bus_stop2, bus_stop_group=bus_stop_group)
        z = BusStopToBusStopGroup(bus_stop=bus_stop3, bus_stop_group=bus_stop_group)
        x.save()
        y.save()
        z.save()

        ids = [x.bus_stop.naptan_id for x in BusStopToBusStopGroup.objects.filter(bus_stop_group=bus_stop_group)]
        self.assertEqual(ids, [bus_stop1.naptan_id, bus_stop2.naptan_id, bus_stop3.naptan_id])
        

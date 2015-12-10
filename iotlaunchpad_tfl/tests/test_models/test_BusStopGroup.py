import unittest
from iotlaunchpad_tfl.tests.test_models import TestModel
from iotlaunchpad_tfl.models import BusStopGroup

class TestBusStopGroup(TestModel):
    pass

class TestInit(TestBusStopGroup):

    def test(self):

        bus_stop_group = BusStopGroup(name="Shoreditch")

        self.assertEqual(bus_stop_group.name, "Shoreditch")

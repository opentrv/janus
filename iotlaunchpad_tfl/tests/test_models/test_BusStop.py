import unittest
from iotlaunchpad_tfl.tests.test_models import TestModel
from iotlaunchpad_tfl.models import BusStop

class TestBusStop(TestModel):
    pass

class TestInit(TestBusStop):

    def test(self):

        bus_stop = BusStop(naptan_id="490011218A",
                           name="Bank",
                           latitude=51.513395,
                           longitude=-0.089095
        )

        self.assertEqual(bus_stop.naptan_id, "490011218A")
        self.assertEqual(bus_stop.name, "Bank")
        self.assertEqual(bus_stop.latitude, 51.513395)
        self.assertEqual(bus_stop.longitude, -0.089095)

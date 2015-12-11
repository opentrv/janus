import unittest
from iotlaunchpad_tfl.tests.test_models import TestModel
from iotlaunchpad_tfl.models import BusStop

class TestBusStop(TestModel):
    @staticmethod
    def _simple_bus_stop():
        return BusStop(naptan_id="490011218A",
                           name="Bank",
                           latitude=51.513395,
                           longitude=-0.089095
        )

class TestInit(TestBusStop):

    def test(self):

        bus_stop = self._simple_bus_stop()

        self.assertEqual(bus_stop.naptan_id, "490011218A")
        self.assertEqual(bus_stop.name, "Bank")
        self.assertEqual(bus_stop.latitude, 51.513395)
        self.assertEqual(bus_stop.longitude, -0.089095)

class TestJson(TestBusStop):

    def test(self):

        bus_stop = self._simple_bus_stop()
        expected_output = {
            'naptan_id': '490011218A',
            'name': 'Bank',
            'latitude': 51.513395,
            'longitude': -0.089095
        }
        
        output = bus_stop.json()

        self.assertEqual(output, expected_output)

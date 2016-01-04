import requests
from django.test import TestCase

class TestHouseRelationship(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self):

        # admin user goes to installation page /brent/installation
        # admin user fills in form, sensor-id, location, house, date
        # user submits form
        # user goes to the sensor information page /brent/sensor-info?sensor-id=0a49
        # the sensor's history is displayed
        self.fail('TODO')
        

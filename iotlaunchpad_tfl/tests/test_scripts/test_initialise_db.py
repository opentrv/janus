import django.test
import mock
from iotlaunchpad_tfl.scripts import initialise_db
from iotlaunchpad_tfl.models import BusStopGroup, BusStop

class TestScript(django.test.TestCase):
    pass

@mock.patch('iotlaunchpad_tfl.scripts.initialise_db.ArgumentParser')
@mock.patch('iotlaunchpad_tfl.scripts.initialise_db.open')
@mock.patch('iotlaunchpad_tfl.scripts.initialise_db.json')
class TestInitialiseDB(TestScript):

    def setUp(self):
        self.json_object = {
            'shoreditch': {
                'bus_stops': [
                    {'naptan': 'asdf1', 'name': 'asdf1', 'lat': 0.1, 'lon': 0.1},
                    {'naptan': 'asdf2', 'name': 'asdf2', 'lat': 0.2, 'lon': 0.2},
                    {'naptan': 'asdf3', 'name': 'asdf3', 'lat': 0.3, 'lon': 0.3},
                ]
            }
        }

    def test_accepts_a_filepath_arg(self, json, open, ArgumentParser):
        parser = mock.Mock()
        ArgumentParser.return_value = parser

        initialise_db.main()

        parser.add_argument.assert_called_once_with('json_filepath', nargs='?', default='../data/bus_stops_updated.json')

    def test_opens_and_loads_json_file(self, json, open, ArgumentParser):

        parser = mock.Mock()
        ArgumentParser.return_value = parser
        f = mock.Mock()
        open.return_value = mock.Mock(__exit__=mock.Mock(), __enter__=mock.Mock(return_value=f))
        f.readlines.return_value = ['a', 'b']
        
        initialise_db.main()

        open.assert_called_once_with(parser.parse_args().json_filepath, 'rb')
        json.loads.assert_called_once_with(''.join(f.readlines()))


    def test_creates_bus_stop_groups_with_json_object(self, json, open, ArgumentParser):

        json.loads.return_value = self.json_object

        initialise_db.main()

        self.assertEqual(len(BusStopGroup.objects.all()), 1)
        self.assertEqual(BusStopGroup.objects.first().name, 'shoreditch')

    def test_creats_bus_stops(self, json, open, ArgumentParser):

        json.loads.return_value = self.json_object

        initialise_db.main()

        self.assertEqual(len(BusStop.objects.all()), 3)
        BusStop.objects.get(naptan_id='asdf1')
        BusStop.objects.get(naptan_id='asdf2')
        BusStop.objects.get(naptan_id='asdf3')
        
        self.fail('TODO:')

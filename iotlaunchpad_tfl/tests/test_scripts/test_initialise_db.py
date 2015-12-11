import django.test
import mock
from iotlaunchpad_tfl.management.commands import initialise_db
from iotlaunchpad_tfl.models import BusStopGroup, BusStop, BusStopToBusStopGroup

class TestInitialiseDBAddArguments(django.test.TestCase):

    def test(self):
        parser = mock.Mock()

        command = initialise_db.Command()
        command.add_arguments(parser)

        parser.add_argument.assert_any_call('json_filepath', nargs='?', default='../data/bus_stops_updated.json')

@mock.patch('iotlaunchpad_tfl.management.commands.initialise_db.ArgumentParser')
@mock.patch('iotlaunchpad_tfl.management.commands.initialise_db.open')
@mock.patch('iotlaunchpad_tfl.management.commands.initialise_db.json')
class TestInitialiseDBHandle(django.test.TestCase):

    def setUp(self):
        self.json_object = {
            'shoreditch': {
                'stops': [
                    {'naptan': 'asdf1', 'name': 'asdf1', 'lat': 0.1, 'lon': 0.1},
                    {'naptan': 'asdf2', 'name': 'asdf2', 'lat': 0.2, 'lon': 0.2},
                    {'naptan': 'asdf3', 'name': 'asdf3', 'lat': 0.3, 'lon': 0.3},
                ]
            }
        }

    def test_accepts_a_filepath_arg(self, json, open, ArgumentParser):

        command = initialise_db.Command()
        command.handle(json_filepath='asdf')

    def test_opens_and_loads_json_file(self, json, open, ArgumentParser):

        parser = mock.Mock()
        ArgumentParser.return_value = parser
        f = mock.Mock()
        open.return_value = mock.Mock(__exit__=mock.Mock(), __enter__=mock.Mock(return_value=f))
        f.readlines.return_value = ['a', 'b']

        command = initialise_db.Command()
        command.handle(json_filepath='asdf')

        open.assert_called_once_with('asdf', 'rb')
        json.loads.assert_called_once_with(''.join(f.readlines()))


    def test_creates_bus_stop_groups_with_json_object(self, json, open, ArgumentParser):

        json.loads.return_value = self.json_object

        command = initialise_db.Command()
        command.handle(json_filepath='asdf')

        self.assertEqual(len(BusStopGroup.objects.all()), 1)
        self.assertEqual(BusStopGroup.objects.first().name, 'shoreditch')

    def test_creats_bus_stops(self, json, open, ArgumentParser):

        json.loads.return_value = self.json_object

        command = initialise_db.Command()
        command.handle(json_filepath='asdf')

        self.assertEqual(len(BusStop.objects.all()), 3)
        BusStop.objects.get(naptan_id='asdf1')
        BusStop.objects.get(naptan_id='asdf2')
        BusStop.objects.get(naptan_id='asdf3')

    def test_creates_bus_stop_to_bus_stop_group_object(self, json, open, ArgumentParser):

        json.loads.return_value = self.json_object
        
        command = initialise_db.Command()
        command.handle(json_filepath='asdf')

        relationships = BusStopToBusStopGroup.objects.all()
        self.assertEqual(len(relationships), 3)
        
        self.assertEqual(relationships[0].bus_stop, BusStop.objects.get(naptan_id='asdf1'))
        self.assertEqual(relationships[1].bus_stop, BusStop.objects.get(naptan_id='asdf2'))
        self.assertEqual(relationships[2].bus_stop, BusStop.objects.get(naptan_id='asdf3'))
        self.assertEqual(relationships[0].bus_stop_group, BusStopGroup.objects.get(name='shoreditch'))
        self.assertEqual(relationships[1].bus_stop_group, BusStopGroup.objects.get(name='shoreditch'))
        self.assertEqual(relationships[2].bus_stop_group, BusStopGroup.objects.get(name='shoreditch'))
        

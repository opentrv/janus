import time
import os
import subprocess
import requests
from django.test import TestCase, LiveServerTestCase

tests_dir = '.temp/tests'
if not os.path.exists(tests_dir):
    os.makedirs(tests_dir)

class FunctionalTest(LiveServerTestCase):
    log_filename = 'udp_server.log'
    error_log_filename = 'udp_server_errors.log'
    maxDiff = None

    def check_data_response(self, params, expected):
        response = requests.get(self.DATA_API_URL, params=params)
        try:
            self.assertEqual(response.json(), expected)
        except ValueError as e:
            raise Exception('{}\n{}'.format(e, response.text))
    
    def test(self):
        
        # start the udp server
        self.udp_server_process = subprocess.Popen([
            'python',
            'manage.py',
            'start_udp_server',
            '--log', self.log_filepath,
            '--error-log', self.error_log_filepath,
            '--settings',
            'opentrv.settings.test',
        ])
        time.sleep(1)

        # check the server started up okay
        self.assertIsNone(self.udp_server_process.poll())
        
        # check udp server starts a log
        self.assertTrue(os.path.exists(self.log_filepath), 'log_filepath not found: {}'.format(self.log_filepath))

        # send message to the udp server
        msg = "Hello world"
        subprocess.check_call(['python', 'manage.py', 'send_udp', msg])
        # TODO: Needs to be able to send to a remote UDP server, i.e. take a host argument

        # check message is written to the log file
        f = open(self.log_filepath, 'rb')
        line = f.readline()
        self.assertIn(msg, line)

        # send some opentrv data to the udp server
        msg = '[ "2015-01-01T00:00:43Z", "", {"@":"0a45","+":2,"vac|h":9,"T|C16":201,"L":0} ]'
        subprocess.check_call(['python', 'manage.py', 'send_udp', msg])

        # use the api to extract the data
        expected = {'status': 200, 'content':
                    [
                        {
                            'datetime': "2015-01-01T00:00:43+00:00",
                            'sensor_id': "0a45",
                            'type': 'vacancy',
                            'value': 9.0,
                        },
                        {
                            'datetime': "2015-01-01T00:00:43+00:00",
                            'sensor_id': "0a45",
                            'type': 'temperature',
                            'value': 12.5625,
                        },
                        {
                            'datetime': "2015-01-01T00:00:43+00:00",
                            'sensor_id': "0a45",
                            'type': 'light',
                            'value': 0.0,
                        }
                    ],
                    'errors': []
        }

        self.check_data_response({'date': '2015-01-01'}, expected)

        # filter on datetime-first and datetime-last
        params={'datetime-first': '2015-01-01T00:00:40', 'datetime-last': '2015-01-01T00:00:50'}
        expected = expected # user previous expected
        self.check_data_response(params, expected)

        # filter on datetime-first and datetime-last where there is no data
        params={'datetime-first': '2015-01-01T00:00:50', 'datetime-last': '2015-01-01T00:00:55'}
        expected = {'status': 200, 'content': [], 'errors': []}
        self.check_data_response(params, expected)
        
        self.fail('TODO: graceful handling of invalid datetime-first and datetime-last parameters')

        self.fail('TODO: filter on measurement type(s)')
        self.fail('TODO: graceful handling of invalid measurement type(s)')

        self.fail('TODO: filter on sensor_id(s)')
        self.fail('TODO: graceful handling of invalid sensor_id(s)')

        self.fail('TODO: get a list of measurement types (/dataserver/api/opentrv/data/types)')
        self.fail('TODO: filter on datetime-first, datetime-last and sensor_id(s)')

        self.fail('TODO: get a list of sensor_ids (/dataserver/api/opentrv/data/sensor_ids)')
        self.fail('TODO: filter on datetime-first, datetime-last and type(s)')
        
        self.fail('TODO: get the first and last dates of avaiable data (/dataserver/api/opentrv/data/dates)')
        self.fail('TODO: filter on measurement type(s) and sensor_id(s)')
        
        self.fail('TODO')

    def __init__(self, *args, **kwargs):
        dirs = os.listdir(tests_dir)
        test_numbers = []
        for dir in dirs:
            try:
                test_number = int(dir)
                test_numbers.append(test_number)
            except:
                pass
        self.test_dir = tests_dir + '/{}'.format(len(test_numbers))
        os.makedirs(self.test_dir)
        self.log_filepath = self.test_dir + '/{}'.format(self.log_filename)
        self.error_log_filepath = self.test_dir + '/{}'.format(self.error_log_filename)
        LiveServerTestCase.__init__(self, *args, **kwargs)
        
    def setUp(self):
        self.DATA_API_URL = os.path.join(self.live_server_url, 'dataserver', 'api', 'opentrv', 'data')

    def tearDown(self):

        # kill the server process
        self.udp_server_process.kill()


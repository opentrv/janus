import time
import datetime
import os
import mock
import subprocess
import requests
import copy
from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from django.utils import timezone
from dateutil.parser import parse as date_parser

tests_dir = '.temp/tests'
if not os.path.exists(tests_dir):
    os.makedirs(tests_dir)

class FunctionalTest(LiveServerTestCase):
    log_filename = 'udp_server.log'
    error_log_filename = 'udp_server_errors.log'
    maxDiff = None

    def check_data_response(self, params, expected, timedelta=None):
        '''
        Check an API call with a given set of parameters returns expected content
        '''
        response = requests.get(self.DATA_API_URL, params=params).json()
        if timedelta == None:
            self.assertEqual(response, expected)
        else:
            self.assertEqual(response['status'], expected['status'])
            self.assertEqual(response['errors'], expected['errors'])
            self.assertEqual(len(response['content']), len(expected['content']))
            for i, measurement in enumerate(response['content']):
                response_datetime = date_parser(response['content'][i]['datetime'])
                expected_datetime = date_parser(expected['content'][i]['datetime'])
                self.assertTrue(response_datetime >= expected_datetime)
                self.assertTrue(response_datetime < expected_datetime + timedelta)
                self.assertEqual(response['content'][i].keys(), expected['content'][i].keys())
                for key, val in response['content'][i].iteritems():
                    if key != 'datetime':
                        self.assertEqual(response['content'][i][key], expected['content'][i][key])
        return response

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
        now = timezone.now()
        msg = '{"@":"0a45","+":2,"vac|h":9,"T|C16":201,"L":0}'
        subprocess.check_call(['python', 'manage.py', 'send_udp', msg])

        # use the api to extract the data
        expected = {
            'status': 200,
            'errors': [],
            'content': [
                {
                    'sensor_id': "0a45",
                    'type': 'vacancy',
                    'value': 9.0,
                    'datetime': now.isoformat()
                },
                {
                    'sensor_id': "0a45",
                    'type': 'temperature',
                    'value': 12.5625,
                    'datetime': now.isoformat()
                },
                {
                    'sensor_id': "0a45",
                    'type': 'light',
                    'value': 0.0,
                    'datetime': now.isoformat()
                }
            ]
        }

        initial_measurements = copy.deepcopy(expected['content']) # save this for later tests

        response1 = self.check_data_response({}, expected, timedelta=datetime.timedelta(seconds=1))
        self.check_data_response({'date': datetime.date.today().isoformat()}, expected, timedelta=datetime.timedelta(seconds=1))

        # filter on datetime-first and datetime-last
        params={'datetime-first': '2015-01-01T00:00:40', 'datetime-last': datetime.date.today() + datetime.timedelta(days=1)}# '2015-01-01T00:00:50'}
        expected = expected # user previous expected
        self.check_data_response(params, expected, timedelta=datetime.timedelta(seconds=1))

        # filter on datetime-first and datetime-last where there is no data
        params={'datetime-first': '2015-01-01T00:00:50', 'datetime-last': '2015-01-01T00:00:55'}
        expected = {'status': 200, 'content': [], 'errors': []}
        self.check_data_response(params, expected, timedelta=datetime.timedelta(seconds=1))

        # graceful handling of invalid datetimes
        params={'datetime-first': 'yo', 'datetime-last': 'xo'}
        expected = {'status': 300, 'content': None, 'errors': ['ValueError: Unknown string format, datetime-first: yo',
                                                               'ValueError: Unknown string format, datetime-last: xo']}
        self.check_data_response(params, expected)

        #filter on measurement type(s)
        params={'type': ['temperature', 'light']}
        expected={'status': 200, 'content':[
            {
                'datetime': now.isoformat(),
                'sensor_id': "0a45",
                'type': 'temperature',
                'value': 12.5625,
            },
            {
                'datetime': now.isoformat(),
                'sensor_id': "0a45",
                'type': 'light',
                'value': 0.0,
            }
        ], 'errors': []}
        self.check_data_response(params, expected, timedelta=datetime.timedelta(seconds=1))

        # measurements that do not exist return nothing
        params={'type': ['does not exist']}
        expected={'status': 200, 'content': [], 'errors': []}
        self.check_data_response(params, expected)

        msgs = [
            '{"@":"819c","T|C16":71,"L":5,"B|cV":256}',
            '{"@":"414a","+":4,"vac|h":3,"v|%":0,"tT|C":7,"vC|%":50}',
            '{"@":"0d49","+":2,"vac|h":22,"T|C16":203,"L":0}',
            '{"@":"2d1a","+":1,"tT|C":7,"vC|%":102,"T|C16":292}',
            '{"@":"0d49","+":3,"B|mV":2601,"v|%":0,"tT|C":7,"O":1}',
        ]
        for msg in msgs:
            subprocess.check_call(['python', 'manage.py', 'send_udp', msg])            
        
        # filter on sensor_id(s)
        params={'sensor-id': ['0a45', '0a46']}
        expected = {'status': 200, 'content': initial_measurements, 'errors': []}
        self.check_data_response(params, expected, timedelta=datetime.timedelta(seconds=1))

        # get a list of measurement types
        response = requests.get(self.live_server_url + '/dataserver/api/opentrv/data/types')
        types = response.json()['content']
        self.assertEqual(len(types), 8, types)
        for type_ in ['temperature',
                      'vacancy',
                      'light',
                      'target_temperature',
                      'battery',
                      'occupancy',
                      'valve_open_percent',
                      'valve_travel']:
            self.assertIn(type_, types, type_)
        
        # get a list of sensor_ids
        response = requests.get(self.live_server_url + '/dataserver/api/opentrv/data/sensor-ids')
        self.assertEqual(len(response.json()['content']), 5, response.json()['content'])
        for sensor_id in ['0a45', '819c', '414a', '0d49', '2d1a']:
            self.assertIn(sensor_id, response.json()['content'])
        # filter sensor_ids on measurement type
        response = requests.get(self.live_server_url + '/dataserver/api/opentrv/data/sensor-ids', params={'type': 'battery'})
        self.assertEqual(len(response.json()['content']), 2, response.json()['content'])
        for sensor_id in ['819c', '0d49']:
            self.assertIn(sensor_id, response.json()['content'])
        
        # get first and last datetimes
        first_measurement = response1['content'][0]
        last_measurement = requests.get(self.DATA_API_URL, params={'sensor-id': '0d49', 'type': 'occupancy'}).json()['content'][0]
        response = requests.get(self.live_server_url + '/dataserver/api/opentrv/data/dates')
        self.assertEqual(response.json()['content'], [first_measurement['datetime'], last_measurement['datetime']])
        
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
        # subprocess.call(['python', 'manage.py', 'flush', '--noinput', '--settings', 'opentrv.settings.test'])

class BrentTest(LiveServerTestCase):

    fixtures = ['2015-01-01.json']

    def test(self):

        self.fail('TODO: selenium tests, filtering data, displaying graph, etc.')


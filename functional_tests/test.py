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

    def test(self):
        
        # start the udp server
        self.udp_server_process = subprocess.Popen(['python', 'manage.py', 'start_udp_server', '--log', self.log_filepath])
        time.sleep(1)

        # check the server started up okay
        self.assertIsNone(self.udp_server_process.poll())
        
        # check udp server starts a log
        self.assertTrue(os.path.exists(self.log_filepath), 'log_filepath not found: {}'.format(self.log_filepath))

        # send message to the udp server
        msg = "Hello world"
        subprocess.check_call(['python', 'manage.py', 'send_udp', msg])

        # check message is written to the log file
        f = open(self.log_filepath, 'rb')
        line = f.readline()
        self.assertIn(msg, line)

        # send some opentrv data to the udp server
        msg = '[ "2015-01-01T00:00:43Z", "", {"@":"0a45","+":2,"vac|h":9,"T|C16":201,"L":0} ]'
        subprocess.check_call(['python', 'manage.py', 'send_udp', msg])

        # use the api to extract the data
        response = requests.get(os.path.join(self.live_server_url, 'dataserver', 'api', 'opentrv'), params={'date': '2015-01-01'})
        expected = [
            {
                'datetime': "2015-01-01T00:00:43Z",
                'sensor_id': "0a45",
                'vacancy': 9
            },
            {
                'datetime': "2015-01-01T00:00:43Z",
                'sensor_id': "0a45",
                'temperature': 12.5625
            },
            {
                'datetime': "2015-01-01T00:00:43Z",
                'sensor_id': "0a45",
                'light': 0
            }
        ]

        try:
            self.assertEqual(response.json(), expected)
        except ValueError as e:
            raise Exception('{}\n{}'.format(e, response.text))
        
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
    
        LiveServerTestCase.__init__(self, *args, **kwargs)
        
    def setUp(self):
        # if not os.path.exists(self.tests_dir):
        #     os.makedirs
        pass
        
    def tearDown(self):

        # remove any log files generated
        # os.remove(self.log_filepath)

        # kill the server process
        self.udp_server_process.kill()

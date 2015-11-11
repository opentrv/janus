import time
import os
import subprocess
from django.test import TestCase

class FunctionalTest(TestCase):
    log_filepath = '../logs/udp_server.log'

    def test(self):
        
        # start the udp server
        self.udp_server_process = subprocess.Popen(['python', 'manage.py', 'start_udp_server'])
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
        
        self.fail('TODO')

    def tearDown(self):

        # remove any log files generated
        os.remove(self.log_filepath)

        # kill the server process
        self.udp_server_process.kill()

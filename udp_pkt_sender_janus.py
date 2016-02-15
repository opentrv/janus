import os, sys
script_path = os.path.join(os.getcwd(), sys.argv[0])
sample_data_dir = os.path.dirname(script_path)
project_dir = os.path.dirname(os.path.dirname(sample_data_dir))
sys.path.append(project_dir)
# os.environ['DJANGO_SETTINGS_MODULE'] = 'opentrv.settings.base'
import socket
# from django.core.management.base import BaseCommand

# import django
# django.setup()
HOST = "178.62.98.162"
#HOST = "127.0.0.1"
UDP_PORT = 9999
#TEST_PKT = ["2015-01-01T00:00:43Z", "", {"@":"0a45","+":2,"vac|h":9,"T|C16":201,"L":0}]
TEST_PKT = 'Hello world'

sample_data_filepath = os.path.join(sample_data_dir, 'test_pkts2.json')



class UdpCommand():
    help = 'Sends UDP packet to a host and port'
                    
    def add_arguments(self, parser):
        parser.add_argument('msg', nargs='?', default=TEST_PKT)
        parser.add_argument('--host', default=HOST)
        parser.add_argument('--port', default=UDP_PORT)
        
    def handle(self):
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.sendto(options['msg'], (options['host'], options['port']))
        self.send_udp_file()
        
    def send_udp_file(self):
        f = open(sample_data_filepath, 'rb')    
        lines = [line.replace('\n', '') for line in f]
        n_successes = 0
        n_failures = 0
        success_types = set()
        failure_types = set()
        for line in lines[:]:
            print line
            sentpkt = self.send_udp_pkt(line)
            
        
    def send_udp_pkt(self, msg):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(msg, (HOST, UDP_PORT))

udpcmd = UdpCommand()
udpcmd.handle()
print "sent command"

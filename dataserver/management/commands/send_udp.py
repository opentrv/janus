import socket
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Sends UDP packet to a host and port'
                    
    def add_arguments(self, parser):
        parser.add_argument('msg', nargs='?', default='Hello world')
        parser.add_argument('--host', default='127.0.0.1')
        parser.add_argument('--port', default=9999)
        
    def handle(self, *args, **options):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(options['msg'], (options['host'], options['port']))

import socket
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Sends UDP packet to a host and port'
                    
    def add_arguments(self, parser):
        parser.add_argument('msg', nargs='?', default='Hello world')
        # TODO: Needs to take a host argument
        
    def handle(self, *args, **options):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(options['msg'], ('127.0.0.1', 9999))
        # TODO: Needs to be able to send to a remote host

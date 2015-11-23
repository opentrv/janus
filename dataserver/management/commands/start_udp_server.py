import logging
from dataserver.udpserver import UDPServer
from dataserver.udpserver import logger
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Starts the UDP server'
                    
    def add_arguments(self, parser):
        parser.add_argument('--log', default='udp_server.log', help='udp server log')
        parser.add_argument('--error-log', default='udp_server_errors.log', help='udp server errors log')
                
    def handle(self, *args, **options):

        logger.setLevel(logging.INFO)
        
        log_filepath = options['log']
        info_handler = logging.FileHandler(log_filepath)
        info_handler.setLevel(logging.INFO)
        logger.addHandler(info_handler)
        info_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))

        error_log_filepath = options['error_log']
        error_handler = logging.FileHandler(error_log_filepath)
        error_handler.setLevel(logging.WARNING)
        logger.addHandler(error_handler)
        error_handler.setFormatter(logging.Formatter('%(levelname)s: %(asctime)s: %(message)s'))

        UDPServer().start()


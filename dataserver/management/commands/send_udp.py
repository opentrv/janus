import socket
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Sends UDP packet to a host and port'
                    
    def add_arguments(self, parser):
        parser.add_argument('msg', nargs='?', default='Hello world')
        # parser.add_argument('--start', help='Start datetime, ISO 8601 format (default: now)', default=None)
        # parser.add_argument('--frequency', type=int, help='Scraping Frequency in seconds (default: 1 day)', default=86400)
                
    def handle(self, *args, **options):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(options['msg'], ('127.0.0.1', 9999))

#         logger.setLevel(logging.INFO)
#         handler = logging.StreamHandler()
#         handler.setLevel(logging.INFO)
#         logger.addHandler(handler)
#         formatter = logging.Formatter('%(levelname)s: %(name)s: %(message)s')
#         handler.setFormatter(formatter)
#         bg_logger.setLevel(logging.INFO)
#         bg_logger.addHandler(handler)
#         # logger.propagate = False
#         # file_handler = logging.FileHandler(options['log'])
#         # file_handler.setLevel(logging.INFO)
#         # file_handler.setFormatter(formatter)
#         # logger.addHandler(file_handler)
#         # bg_logger.addHandler(file_handler)

#         logger.info('Start BG data aggregation process')
        
#         while True:
#             update_daily_summaries()
#             time.sleep(86400.0)
#         # start_datetime = convert_start_to_datetime(start=options['start'])
#         # scraper = Scraper()
#         # wait_till_start_time(start_datetime)
#         # while True:
#         #     previous_session = Session.get_previous_session()
#         #     scraper.configure(start_datetime, previous_session)
#         #     scraper.scrape()
#         #     wait_till_next_session(options['frequency'])

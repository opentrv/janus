import os, sys
script_path = os.path.join(os.getcwd(), sys.argv[0])
sample_data_dir = os.path.dirname(script_path)
project_dir = os.path.dirname(os.path.dirname(sample_data_dir))
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'opentrv.settings.base'
import django
django.setup()

from opentrv_sensor.models import Measurement

sample_data_filepath = os.path.join(sample_data_dir, '201501.json')

if __name__ == '__main__':

    f = open(sample_data_filepath, 'rb')

    lines = [line.replace('\n', '') for line in f]

    Measurement.objects.all().delete()

    n_successes = 0
    n_failures = 0
    success_types = set()
    failure_types = set()
    for line in lines[:]:
        print line
        measurements = Measurement.create_from_udp(line)
        n_successes += len(measurements['success'])
        n_failures += len(measurements['failure'])
        for x in measurements['failure']:
            failure_types.add(x['type'])
        # for x in measurements['success']:
        #     success_types.add(x.type)

    print 'n_successes:', n_successes
    print 'n_failures:', n_failures
    print 'failure_types:', failure_types
    # print 'success_types:', success_types

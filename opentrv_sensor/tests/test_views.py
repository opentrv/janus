from django.http import HttpRequest
from django.test import TestCase
from opentrv_sensor import views

class TestAPI(TestCase):

    def test(self):

        request = HttpRequest()
        request.GET['date'] = '2015-01-01'

        response = views.api(request)

        self.fail('TODO')

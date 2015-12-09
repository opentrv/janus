import mock
from iotlaunchpad_tfl import views
from unittest import TestCase

@mock.patch('iotlaunchpad_tfl.views.render')
class TestHomeView(TestCase):

    def test(self, render):
        request = mock.Mock()
    
        response = views.home(request)

        render.assert_called_once_with(request, 'iotlaunchpad_tfl/home.html')
        response = render.return_value
        

        

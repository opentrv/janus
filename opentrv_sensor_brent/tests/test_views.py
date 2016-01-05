import mock
from django.contrib.auth.models import User
from django.test import TestCase

@mock.patch('opentrv_sensor_brent.views.authenticate')
class SignInTest(TestCase):

    def test_template_used(self, authenticate):

        response = self.client.get('/brent/sign-in')
        self.assertTemplateUsed(response, 'brent/sign-in.html')

    def test_successfull_authentication_of_user_redirects(self, authenticate):

        user = User.objects.create_user(username="voong.david@gmail.com", password="secret")

        response = self.client.post('/brent/sign-in', data={"email": "voong.david@gmail.com", "password": "secret"})

        self.assertRedirects(response, '/brent', target_status_code=301)

    def test_unsuccessful_authentication_returns_errors(self, authenticate):
        authenticate.return_value = None
        
        response = self.client.post('/brent/sign-in', data={'email': 'doesnotexist@gmail.com', 'password': 'doesnotexist'})

        self.assertTrue(len(response.context['errors']) > 0)

    def test_post_attemps_to_authenticate_user(self, authenticate):

        response = self.client.post('/brent/sign-in', data={'email': 'doesnotexist@gmail.com', 'password': 'doesnotexist'})

        authenticate.assert_called_once_with(username='doesnotexist@gmail.com', password='doesnotexist')
        
    def test_if_user_does_not_have_permission_redirect(self, authenticate):

        user = mock.Mock()
        authenticate.return_value = user
        user.has_perm.return_value = False

        response = self.client.post('/brent/sign-in', data={'email': 'doesnotexist@gmail.com', 'password': 'doesnotexist'})

        self.assertRedirects(response, '/brent/user-permissions')

    def test_if_user_is_authenticated_and_has_permissions_redirect(self, authenticate):

        user = mock.Mock()
        user.has_perm.return_value = True
        authenticate.return_value = user

        response = self.client.post('/brent/sign-in', data={'email': 'asdf', 'password': 'asdf'})

        self.assertRedirects(response, '/brent', target_status_code=301)

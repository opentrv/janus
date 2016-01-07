import mock
from django.contrib.auth.models import User
from django.test import TestCase
from opentrv_sensor_brent.views import sign_in_or_sign_up, sign_up, sign_in, home, logout_view

@mock.patch('opentrv_sensor_brent.views.render')
@mock.patch('opentrv_sensor_brent.views.redirect')
@mock.patch('opentrv_sensor_brent.views.datetime')
class HomeTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_unauthenticated_user_redirects(self, datetime, redirect, render):
        ''' if user is authenticated but does not have permission redirect to the user-permissions page '''
        request = mock.Mock()
        request.user.is_authenticated.return_value = False

        response = home(request)

        redirect.assert_called_once_with('/brent/sign-in')

    def test_authenticated_user_with_permissions_is_redirected_to_user_permissions(self, datetime, redirect, render):
        ''' if user is authenticated check the user has permission to view page '''
        request = mock.Mock()
        request.user = mock.Mock()
        request.user.is_authenticated.return_value = True
        request.user.has_perm.return_value = False
        
        response = home(request)

        request.user.has_perm.assert_called_once_with('opentrv_sensor.view_measurement')
        redirect.assert_called_once_with('/brent/user-permissions')

    def test_authenticated_and_permitted_user_renders_homepage(self, datetime, redirect, render):
        ''' if user is authenticated and has permission to view the page render the page with correct context '''
        request = mock.Mock()
        request.user = mock.Mock()
        request.user.is_authenticated.return_value = True
        request.user.has_perm.return_value = True
        datetime.datetime = mock.Mock()
        datetime.datetime.return_value = mock.Mock(__add__=mock.Mock())

        response = home(request)

        render.assert_called_once_with(request, 'brent/home.html', {
            'today': datetime.datetime.return_value.isoformat.return_value.replace.return_value,
            'tomorrow': datetime.datetime.return_value.__add__.return_value.isoformat.return_value.replace.return_value
        })
        
@mock.patch('opentrv_sensor_brent.views.sign_up')
@mock.patch('opentrv_sensor_brent.views.sign_in')
class SignInOrSignUpTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_sign_up_post_parameters(self, sign_in, sign_up):
        ''' if 'password-confirmation' is in the POST parameters call the sign_up method with the request '''
        request = mock.Mock()
        request.POST = {'password-confirmation': 'asdf'}

        sign_in_or_sign_up(request)

        sign_up.assert_called_once_with(request)
        assert not sign_in.called

    def test_sign_in_post_parameters(self, sign_in, sign_up):
        ''' if 'password-confirmation' is not in the POST parameters call the sign_in method with the request '''
        request = mock.Mock()
        request.POST = {}

        sign_in_or_sign_up(request)

        sign_in.assert_called_once_with(request)
        assert not sign_up.called
        
@mock.patch('opentrv_sensor_brent.views.authenticate')
@mock.patch('opentrv_sensor_brent.views.login')
class SignInTest(TestCase):

    def test_template_used(self, login, authenticate):

        response = self.client.get('/brent/sign-in')
        self.assertTemplateUsed(response, 'brent/sign-in.html')

    def test_successfull_authentication_of_user_redirects(self, login, authenticate):

        user = User.objects.create_user(username="voong.david@gmail.com", password="secret")

        response = self.client.post('/brent/sign-in', data={"email": "voong.david@gmail.com", "password": "secret"})

        self.assertRedirects(response, '/brent', target_status_code=301)

    def test_successful_authentication_logs_in_user(self, login, authenticate):
        request = mock.Mock()
        request.method = 'POST'
        request.POST = mock.Mock(__getitem__=mock.Mock())
        user = mock.Mock()
        authenticate.return_value = user

        response = sign_in(request)
        
        login.assert_called_once_with(request, user)

    def test_unsuccessful_authentication_returns_errors(self, login, authenticate):
        authenticate.return_value = None
        
        response = self.client.post('/brent/sign-in', data={'email': 'doesnotexist@gmail.com', 'password': 'doesnotexist'})

        self.assertTrue(len(response.context['errors']) > 0)

    def test_post_attemps_to_authenticate_user(self, login, authenticate):

        response = self.client.post('/brent/sign-in', data={'email': 'doesnotexist@gmail.com', 'password': 'doesnotexist'})

        authenticate.assert_called_once_with(username='doesnotexist@gmail.com', password='doesnotexist')

    def test_if_user_does_not_have_permission_redirect(self, login, authenticate):

        user = mock.Mock()
        authenticate.return_value = user
        user.has_perm.return_value = False

        response = self.client.post('/brent/sign-in', data={'email': 'doesnotexist@gmail.com', 'password': 'doesnotexist'})

        self.assertRedirects(response, '/brent/user-permissions')

    def test_if_user_is_authenticated_and_has_permissions_redirect(self, login, authenticate):

        user = mock.Mock()
        user.has_perm.return_value = True
        authenticate.return_value = user

        response = self.client.post('/brent/sign-in', data={'email': 'asdf', 'password': 'asdf'})

        self.assertRedirects(response, '/brent', target_status_code=301)

    @mock.patch('opentrv_sensor_brent.views.redirect')
    def test_get_with_an_authenticated_user_with_permissions_redirect_to_homepage(self, redirect, login, authenticate):
        request = mock.Mock()
        request.method = 'GET'
        request.user = mock.Mock()
        request.user.is_authenticated.return_value = True
        request.user.has_perm.return_value = True

        response = sign_in(request)

        request.user.has_perm.assert_called_once_with('opentrv_sensor.view_measurement')
        redirect.assert_called_once_with('/brent')

    @mock.patch('opentrv_sensor_brent.views.redirect')
    def test_get_with_an_authenticated_user_without_permissions_redirects_to_user_permissions(self, redirect, login, authenticate):
        request = mock.Mock()
        request.method = 'GET'
        request.user = mock.Mock()
        request.user.is_authenticated.return_value = True
        request.user.has_perm.return_value = False

        response = sign_in(request)

        redirect.assert_called_once_with('/brent/user-permissions')

    @mock.patch('opentrv_sensor_brent.views.render')
    def test_get_with_an_unauthenticated_user_renders_sign_in_sign_up_form(self, render, login, authenticate):
        request = mock.Mock()
        request.method = 'GET'
        request.user = mock.Mock()
        request.user.is_authenticated.return_value = False

        response = sign_in(request)

        render.assert_called_once_with(request, 'brent/sign-in.html')
        
@mock.patch('opentrv_sensor_brent.views.User')
class SignUpTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_redirects_to_user_permissions_when_sign_up_is_successful(self, User):
        ''' it should redirect to the user-permissions page when sign up is successful '''
        
        response = self.client.post('/brent/sign-in', data={'email': 'asdf', 'password': 'asdf', 'password-confirmation': 'asdf'})
        
        self.assertRedirects(response, '/brent/user-permissions')
    
    def test_creates_user_object_with_email_and_password(self, User):
        ''' it should create and save a user object with the email and password provided '''
        request = mock.Mock()
        request.POST = {
            'email': 'voong.david@gmail.com',
            'password': 'secret',
            'password-confirmation': 'secret'
        }
        User.objects.filter.return_value = []

        response = sign_up(request)

        User.objects.create_user.assert_called_once_with(username='voong.david@gmail.com', password='secret')

    @mock.patch('opentrv_sensor_brent.views.render')
    def test_renders_sign_in_page_with_context_when_error_occurs(self, render, User):
        '''it should return the sign_in page with the context when sign up fails '''
        request = mock.Mock()
        request.POST = {
            'email': 'voong.david@gmail.com',
            'password': 'secret',
            'password-confirmation': 'secret'
        }
        User.objects.create_user.side_effect = Exception('sign_up failure')

        response = sign_up(request)

        render.assert_called_once_with(request, 'brent/sign-in.html', {'sign_up_email': 'voong.david@gmail.com', 'sign_up_errors': ['sign_up failure']})
        response = render.return_value
        
    @mock.patch('opentrv_sensor_brent.views.render')
    def test_raises_error_when_passwords_do_not_match(self, render, User):
        ''' it should raise an error when the password and password-confirmation do not match '''
        request = mock.Mock()
        request.POST = {
            'email': 'voong.david@gmail.com',
            'password': 'secret',
            'password-confirmation': 'secret2'
        }

        response = sign_up(request)
        
        render.assert_called_once_with(request, 'brent/sign-in.html', {'sign_up_email': 'voong.david@gmail.com', 'sign_up_errors': ['Password confirmation does not match']})
        response = render.return_value

    @mock.patch('opentrv_sensor_brent.views.render')
    def test_if_user_exists_already_raise_error(self, render, User):
        User.objects.filter.return_value = [mock.Mock()]
        request = mock.Mock()
        request.POST = {
            'email': 'voong.david@gmail.com',
            'password': 'secret',
            'password-confirmation': 'secret'
        }

        response = sign_up(request)

        render.assert_called_once_with(request, 'brent/sign-in.html', {'sign_up_email': 'voong.david@gmail.com', 'sign_up_errors': ['This email address is already registered']})

@mock.patch('opentrv_sensor_brent.views.redirect')        
@mock.patch('opentrv_sensor_brent.views.logout')        
class LogoutTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test(self, mock_logout, redirect):

        request = mock.Mock()

        response = logout_view(request)

        mock_logout.assert_called_once_with(request)
        redirect.assert_called_once_with('/brent/sign-in')
        self.assertEqual(response, redirect.return_value)

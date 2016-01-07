import os, time
from selenium import webdriver
from django.test import TestCase, LiveServerTestCase

class ApiTest(LiveServerTestCase):

    # put some measurement data in here
    fixtures = []

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_redirect(self, url, timeout=2):
        elapsed = 0
        while elapsed < timeout:
            current_url = self.browser.current_url.rstrip('/')
            if current_url  == url:
                return True
            time.sleep(0.5)
            elapsed += 0.5
        raise Exception('Redirect failed: current_url: {}, target_url: {}'.format(current_url, url))

    def test(self):

        # goto the brent homepage
        homepage_url = os.path.join(self.live_server_url, 'brent')
        self.browser.get(homepage_url)

        # user is redirected to sign in page /brent/sign-in
        self.wait_for_redirect(os.path.join(self.live_server_url, 'brent/sign-in'))

        # user fills in sign in form
        sign_in_form = self.browser.find_element_by_id('sign-in-form')
        email_input = sign_in_form.find_element_by_id('email-input')
        pass_input = sign_in_form.find_element_by_id('password-input')
        form_errors = sign_in_form.find_element_by_id('form-errors')
        email_input.send_keys('voong.david@gmail.com')
        pass_input.send_keys('secret')

        # user submits form
        pass_input.send_keys('\n')

        # error msg: user does not exist
        sign_in_form = self.browser.find_element_by_id('sign-in-form')
        form_errors = sign_in_form.find_element_by_id('form-errors')
        self.assertEqual(form_errors.text, "Unrecognised Email and Password")

        # user fills in sign up form
        sign_up_form = self.browser.find_element_by_id('sign-up-form')
        email_input = sign_up_form.find_element_by_id('email-input')
        password_input = sign_up_form.find_element_by_id('password-input')
        password_input_confirmation = sign_up_form.find_element_by_id('password-input-confirmation')
        email_input.send_keys('voong.david@gmail.com')
        password_input.send_keys('secret')
        password_input_confirmation.send_keys('secret')
        sign_up_form.submit()

        # user is returned a message saying they need to wait to be verified by
        # an administrator of the website, email address for more info included
        self.assertEqual(self.browser.current_url.rstrip('/'), os.path.join(self.live_server_url, 'brent/user-permissions'))

        # user signs in
        self.browser.get(self.live_server_url + '/brent/sign-in')
        sign_in_form = self.browser.find_element_by_id('sign-in-form')
        email_input = sign_in_form.find_element_by_id('email-input')
        password_input = sign_in_form.find_element_by_id('password-input')
        email_input.send_keys('voong.david@gmail.com')
        password_input.send_keys('secret\n')
        
        # user is redirected to the verification required page /brent/user-verfication
        self.assertEqual(self.browser.current_url.rstrip('/'), os.path.join(self.live_server_url, 'brent/user-permissions'))
        
        # user manually goes directly to the /brent page
        self.browser.get(self.live_server_url + '/brent')

        # user is redirected to the verification required page /brent/user-verfication
        self.assertEqual(self.browser.current_url.rstrip('/'), os.path.join(self.live_server_url, 'brent/user-permissions'))

        # an administrator verifies the user
        from django.contrib.auth.models import User, Permission
        dvoong = User.objects.get(username="voong.david@gmail.com")
        permission = Permission.objects.get(codename="view_measurement")
        dvoong.user_permissions.add(permission)
        dvoong.save()
        dvoong = User.objects.get(username="voong.david@gmail.com")

        # user manually goes directly to the /brent page
        self.browser.get(self.live_server_url + '/brent')
        
        # home page loads
        self.assertEqual(self.browser.current_url.rstrip('/'), os.path.join(self.live_server_url, 'brent'))

        # user logs out
        logout_button = self.browser.find_element_by_id('logout')
        logout_button.click()

        # user redirected to sign in page
        self.assertEqual(self.browser.current_url.rstrip('/'), os.path.join(self.live_server_url, 'brent/sign-in'))

        # user attempts to go back to home page
        self.browser.get(self.live_server_url + '/brent')
        
        # user redirected to sign in page
        self.assertEqual(self.browser.current_url.rstrip('/'), os.path.join(self.live_server_url, 'brent/sign-in'))

        # user attempts to sign up with the same email address
        sign_up_form = self.browser.find_element_by_id('sign-up-form')
        email_input = sign_up_form.find_element_by_id('email-input')
        password_input = sign_up_form.find_element_by_id('password-input')
        password_input_confirmation = sign_up_form.find_element_by_id('password-input-confirmation')
        email_input.send_keys('voong.david@gmail.com')
        password_input.send_keys('secret')
        password_input_confirmation.send_keys('secret')
        sign_up_form.submit()

        # the sign in page is reloaded with errors
        self.assertEqual(self.browser.current_url.rstrip('/'), os.path.join(self.live_server_url, 'brent/sign-in'))
        sign_up_form = self.browser.find_element_by_id('sign-up-form')
        email_input = sign_up_form.find_element_by_id('email-input')
        password_input = sign_up_form.find_element_by_id('password-input')
        password_input_confirmation = sign_up_form.find_element_by_id('password-input-confirmation')
        form_errors = sign_up_form.find_element_by_id('form-errors')
        self.assertEqual(email_input.get_attribute('value'), 'voong.david@gmail.com')
        self.assertEqual(password_input.text, '')
        self.assertEqual(password_input_confirmation.text, '')
        errors = form_errors.find_elements_by_tag_name('li')
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].text, 'This email address is already registered')

        # user attempts to create a new user but with different passwords
        email_input.clear()
        email_input.send_keys('abc@abc.co.uk')
        password_input.send_keys('secret')
        password_input_confirmation.send_keys('invalid password confirmation')
        sign_up_form.submit()

        # sign-in reloads with errors
        sign_up_form = self.browser.find_element_by_id('sign-up-form')
        email_input = sign_up_form.find_element_by_id('email-input')
        password_input = sign_up_form.find_element_by_id('password-input')
        password_input_confirmation = sign_up_form.find_element_by_id('password-input-confirmation')
        form_errors = sign_up_form.find_element_by_id('form-errors')
        errors = form_errors.find_elements_by_tag_name('li')
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].text, 'Password confirmation does not match')

        # user corrects passwords and resubmits
        password_input.send_keys('secret')
        password_input_confirmation.send_keys('secret')
        sign_up_form.submit()

        # user is redirected to the user-permissions page
        self.assertEqual(self.browser.current_url.rstrip('/'), os.path.join(self.live_server_url, 'brent/user-permissions'))
        
    

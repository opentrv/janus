from django.test import TestCase

class SignInTest(TestCase):

    def test_template_used(self):

        response = self.client.get('/brent/sign-in')
        self.assertTemplateUsed(response, 'brent/sign-in.html')

    def test_post_authenticates_user(self):

        self.fail('TODO')

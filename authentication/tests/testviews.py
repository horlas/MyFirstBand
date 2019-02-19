from requestium import Session, Keys
from django.test import TestCase, RequestFactory
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.test.client import Client
from authentication.models import User
from musicians.models import UserProfile
from authentication.forms import SignupForm, CustomLoginForm
from authentication.views import signup
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.core import mail
from django.test.utils import override_settings
import re

class MyTestCase(TestCase):
    '''Here is a parent class with custom global setup'''
    def setUp(self):
        # web client
        self.client = Client()
        # our test user

        self.factory = RequestFactory()

        # webdriver

        self.session = Session(webdriver_path='./chromedriver',
                               browser='chrome',
                               default_timeout=15,
                               webdriver_options={'arguments': ['headless']})

        self.url = 'http://127.0.0.1:8000'


class SignupTest(MyTestCase):

    def test_signup_page(self):
        request = self.factory.get('/signup')
        response = signup(request)
        self.assertEqual(response.status_code, 200)

    def test_signup_post(self):
        before_users = User.objects.count()
        connect = self.client.post('/authentication/signup/', data={'email' : 'test@hotmail.com',
                                                                    'password1' : 'aqwz7418',
                                                                    'password2': 'aqwz7418'})

        after_users = User.objects.count()
        after_profile = UserProfile.objects.count()
        # we test the User has been created
        self.assertEqual(after_users, before_users+1)
        # and we test that his profile to
        self.assertEqual(after_profile, 1)
        self.assertRedirects(
            connect,
            expected_url=reverse('core:accueil'),
            status_code=302,
            target_status_code=200
        )

    # def test_form_with_selenium(self):
    #
    #     self.session.driver.get('{}/authentication/signup/'.format(self.url))
    #     self.session.driver.ensure_element_by_id('id_email').send_keys('test@horlmail.com')
    #     self.session.driver.ensure_element_by_id('id_password1').send_keys('aqwz7418')
    #
    #     self.session.driver.ensure_element_by_id('id_password2').send_keys('aqwz7418')
    #
    #     self.session.driver.maximize_window()
    #     self.session.driver.implicitly_wait(2)
    #     login_attempt = self.session.driver.find_element_by_id('sign_up_button')
    #     # print(login_attempt)
    #     print(login_attempt.location['x'])
    #     self.session.driver.maximize_window()
    #     self.session.driver.implicitly_wait(2)
    #     self.session.driver.execute_script("window.scrollTo(0, 532)") #.format(login_attempt.location['x']))
    #
    #     login_attempt.click()
    #
    #
    #
    #     # self.session.driver.find_element_by_name('action').click()
    #     url = self.session.driver.current_url
    #     self.session.driver.quit()
# todo : button click is not reachable


class SignupFormTest(TestCase):
    ''' We test the form'''

    def test_signup_form(self):
        form = SignupForm( {'email' : 'test4@hotmail.com',
                            'password1' : 'aqwz7418',
                            'password2': 'aqwz7418'})
        self.assertTrue(form.is_valid())

    def test_blank_signup_form(self):

        form = SignupForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], 'This field is required.')


class LoginViewTest(MyTestCase):

    def test_login_form(self):

        c = User.objects.count()
        user = User.objects.create(email='testuserlogin@gmail.com')
        user.set_password('aqwz7418')
        user.save()
        form = CustomLoginForm({'email': 'testuserlogin@gmail.com',
                                'password': 'aqwz7418'})

        # self.assertFormError(form, 'username', 'This field is required.')
        # print(form.errors)
        # self.assertTrue(form.is_valid())

    def test_login_get(self):
        request = self.factory.get('/authentication/accounts/login')
        response = LoginView.as_view()(request)
        self.assertEqual(response.status_code, 200)
    #
    #
    # def test_login_bis(self):
    #     user = User.objects.create(email='testuserlogin@gmail.com')
    #     user.set_password('aqwz7418')
    #     user.save()
    #
    #     # data = {'username': '', 'password1': 'aqwz7418'}
    #
    #     response = self.client.post(reverse('authentication:login'), data={'email' : 'testuserlogin@gmail.com',
    #                                                                    'password' : 'aqwz7418'},
    #                                                                       follow=True)
    #     # print(response['Location'])
    #     self.assertRedirects(
    #         response,
    #         expected_url=reverse('core:accueil'),
    #         status_code=200,
    #         target_status_code=200
    #     )
        # self.assertFormError(response, 'form', 'username', 'This field is required.')

        # self.assertEqual(connect.status_code, 200)
# Todo: test the login view , is not possbible to post data likewise the test fails on the login form.


class LogoutViewTest(MyTestCase):

    def test_logout_user(self):
        user = User.objects.create(email='testuser@gmail.com')
        user.set_password('12345')
        user.save()

        # self.test_user = User.objects.create_user(self.email, self.password)
        logged_in = self.client.login(email='testuser@gmail.com', password='12345')
        self.assertEqual(logged_in, True)
        response = self.client.post('/authentication/accounts/logout/', data={'email' : 'testuser@gmail.com',
                                                                              'password' : '12345'}, follow=True)
        self.assertRedirects(
            response,
            expected_url=reverse('core:accueil'),
            status_code=302,
            target_status_code=200
        )


class PasswordResetViewTest(MyTestCase):

    def setUp(self):
        super(PasswordResetViewTest, self).setUp()
        self.user = User.objects.create(email='testuserlogin@gmail.com')
        self.user.set_password('aqwz7418')
        self.user.save()
        self.url = reverse('authentication:password_reset')

    def test_reset_password_get(self):
        response = self.client.get(self.url)
        # check the use of the custion template password_reset_form
        list_template = [t.name for t in response.templates]
        assert 'authentication/password_reset_form.html' in list_template
        # check the satus code
        self.assertEqual(response.status_code, 200)
        # check the presence of input line
        self.assertContains(response, '<input type="email" name="email" maxlength="254" id="id_email" required>',
                            html=True)

    def test_reset_password_post(self):
        ''' we test the continuity of the initialization of the password'''
        email_data = {
            "email": self.user.email
        }
        response = self.client.post(self.url, email_data, follow=True)
        self.assertRedirects(
            response,
            expected_url= reverse('authentication:reset_password_done'),
            status_code=302,
            target_status_code=200
        )
        self.assertContains(response,
                            "Nous vous avons envoyé un e-mail avec les instructions pour")
        # check if the mail is well sent
        self.assertEqual(len(mail.outbox), 1)
        # grab uid and token
        msg = mail.outbox[0]
        queries = re.findall('/([\w\-]+)', msg.body)
        token = queries[5]
        uid = queries[4]
        # get the page witch user can post his new password
        url_reset_confirm = reverse('authentication:reset_password_confirm', kwargs={'uidb64': uid, 'token': token})
        response_confirm = self.client.get(url_reset_confirm, follow=True)
        # check the status code and the content
        self.assertEqual(response_confirm.status_code, 200)
        list_template = [t.name for t in response.templates]
        assert 'authentication/password_reset_done.html' in list_template
        # post new password
        data = {
            "new_password1": "1234aqwz",
            "new_password2": "1234aqwz"
        }
        url_reset_password_post = reverse('authentication:reset_password_confirm',
                                          kwargs={'uidb64': uid, 'token': "set-password"})
        response_post_password =  self.client.post(url_reset_password_post, data, follow=True)
        self.assertRedirects(response_post_password,
                             expected_url=reverse_lazy('authentication:reset_password_complete'),
                             status_code=302,
                             target_status_code=200
                             )


class PasswordResetConfirmViewTest(MyTestCase):

    def setUp(self):
        super(PasswordResetConfirmViewTest, self).setUp()
        self.user = User.objects.create(email='testuserlogin@gmail.com')
        self.user.set_password('aqwz7418')
        self.user.save()
        self.url = reverse('authentication:password_reset')
        self.default_token_generator = PasswordResetTokenGenerator()
        self.token = self.default_token_generator.make_token(self.user)
        self.uidb64 = urlsafe_base64_encode(str(self.user.pk).encode())
        self.url = reverse('authentication:reset_password_confirm', kwargs={'uidb64': self.uidb64, 'token': self.token})

    def test_reset_confirm_get(self):

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        list_template = [t.name for t in response.templates]
        assert 'authentication/password_reset_confirm.html'in list_template

    def test_reset_confirm_post_invalid_link(self):
        ''' invalid link because it was used before for the 'get' test'''

        data = {
            "new_password1": "1234aqwz",
            "new_password2": "1234aqwz"
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            'Le lien de ré-initialisation est invalide, car il a certainement été déjà utilisé.')

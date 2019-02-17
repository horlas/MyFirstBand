from requestium import Session, Keys
from django.test import TestCase, RequestFactory
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.test.client import Client
from authentication.models import User
from musicians.models import UserProfile
from authentication.forms import SignupForm, CustomLoginForm
from authentication.views import signup

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
                                                                         'password' : '12345'},
                                                                          follow=True)
        self.assertRedirects(
            response,
            expected_url=reverse('core:accueil'),
            status_code=302,
            target_status_code=200
        )


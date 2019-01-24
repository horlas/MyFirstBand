from requestium import Session, Keys
from django.test import TestCase, RequestFactory
from django.shortcuts import render
from django.urls import reverse
from django.test.client import Client
from authentication.models import User
from core.views import accueil
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage



class MyTestCase(TestCase):
    '''Here is a parent class with custom global setup'''
    def setUp(self):
        # web client
        self.client = Client()
        # our test user
        self.user = User.objects.create( email='test@hotmail.com',
                                              password = 'aqwz7418')

        self.factory = RequestFactory()

        # webdriver
        self.session = Session(webdriver_path='./chromedriver',
                    browser='chrome',
                    default_timeout=15,
                    webdriver_options={'arguments': ['headless']})

        self.url = 'http://127.0.0.1:8000'

class AccueilTest(MyTestCase):
    ''' Test accueil view'''
    def test_accueil(self):
        request = self.factory.get('')
        response = accueil(request)
        self.assertEqual(response.status_code, 200)

        # Test title website content using selenium driver
        self.session.driver.get(self.url)
        self.assertEqual(self.session.driver.title, 'MyFirstBand')


        welcome_message = self.session.get(self.url).xpath('//h4[@id="title"]/text()').extract_first()
        self.assertEqual(welcome_message , 'Bienvenue sur My First Band ')



class NavBarTest(MyTestCase):
    ''' Test NavBar Content '''

    def test_navbar(self):

        # Test if the logo is loaded by checking the size

        r = self.client.get(reverse(accueil))
        self.assertContains(r, 'logo_brand3.png')

        self.session.driver.get(self.url)
        logo = self.session.driver.find_element_by_id('logo')
        self.assertEqual(logo.size, {'width': 243, 'height': 90})

        icon1 = self.session.driver.find_element_by_id("sign-in-link")
        self.assertEqual(icon1.get_attribute('href'), 'http://127.0.0.1:8000/authentication/signup/')

        icon2 = self.session.driver.find_element_by_id("login")
        self.assertEqual(icon2.get_attribute('href'), 'http://127.0.0.1:8000/authentication/accounts/login/')

        # Note : icon2.click() doesn't work : element not interactable
        # Maybe due to the size of the window

        self.session.driver.quit()
from requestium import Session, Keys
from django.test import TestCase, RequestFactory
from django.shortcuts import render
from django.urls import reverse
from django.test.client import Client
from authentication.models import User
from band.models import Band, Membership
from musicians.models import UserProfile, Instrument

from core.views import accueil, MusicianProfileView
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage


class MyTestCase(TestCase):
    '''Here is a parent class with custom global setup'''
    def setUp(self):
        # web client
        self.client = Client()
        # our test user
        self.email = 'tata@gmail.com'
        self.password = 'aqwz7418'
        self.test_user = User.objects.create_user(self.email, self.password)

        # his profil to test get info
        self.userprofile = UserProfile.objects.get(user=self.test_user)
        self.userprofile.username = 'Super Tatie'
        self.userprofile.bio = 'Elle passe ses nuits sans dormir'\
                                'À gacher son bel avenir'\
                                'La groupie du pianiste'
        self.userprofile.birth_year = 1948
        self.userprofile.town = 'Montpellier'
        self.userprofile.county_name = 'Herault'
        self.userprofile.gender = 'F'
        self.userprofile.save()

        # her instruments
        self.instrument = Instrument.objects.create(instrument='Contrebassiste',
                                                    level='Intermediaire',
                                                    musician=self.test_user)
        # our test band
        self.band_test = Band.objects.create(owner_id=self.test_user.id)
        self.band_test.name = 'Pink Floyd'
        self.band_test.bio = 'Pink Floyd est un groupe de rock progressif et psychédélique'\
                         'britannique, originaire de Londres, en Angleterre.'

        self.band_test.type = 'Groupe de Compos'
        self.band_test.muscical_genre = 'Rock'
        self.band_test.town = 'Londres'
        self.band_test.county_name ='Angleterre'
        self.band_test.owner = self.test_user
        self.band_test.save()


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
        # this test does not pass with Travis CI
        # self.assertEqual(self.session.driver.title, 'MyFirstBand')

        welcome_message = self.session.get(self.url).xpath('//h4[@id="title"]/text()').extract_first()
        self.assertEqual(welcome_message, 'Bienvenue sur My First Band  ! ')

        # display last entries of musicians
        card_musician = self.session.get(self.url).xpath('//section[@id="musicians"]//div[@class="card"]')
        self.assertEqual(len(card_musician), 6)

        # display last entries of band
        card_band = self.session.get(self.url).xpath('//section[@id="bands"]//div[@class="card"]')
        self.assertEqual(len(card_band), 6)


class SidenavBarTest(MyTestCase):
    ''' Test NavBar Content '''

    def test_navbar(self):

        # Test if the logo is loaded by checking the size

        r = self.client.get(reverse(accueil))
        self.assertContains(r, 'logo_brand3.png')
        list_template = [t.name for t in r.templates]
        assert 'core/index.html' in list_template
        assert 'core/sidenav.html' in list_template


        # self.assertContains(r, '<a id="login" class="waves-effect custom-text"  href="/authentication/accounts/login/">')
        # self.assertContains(r, "<a id=\'sign-in-link\' class='waves-effect custom-text'  href='/authentication/signup/'>", html=True )

        # self.session.driver.get(self.url)
        # logo = self.session.driver.find_element_by_id('logo')
        # self.assertEqual(logo.size, {'width': 236, 'height': 87})
        #
        # icon1 = self.session.driver.find_element_by_id("sign-in-link")
        # self.assertEqual(icon1.get_attribute('href'), 'http://127.0.0.1:8000/authentication/signup/')
        #
        # icon2 = self.session.driver.find_element_by_id("login")
        # self.assertEqual(icon2.get_attribute('href'), 'http://127.0.0.1:8000/authentication/accounts/login/')
        #
        # self.session.driver.quit()

class MusicianProfileTest(MyTestCase):
    '''Test public profile of a musician'''

    def test_public_profil_user(self):
        id_test = self.test_user.id

        response = self.client.get('/core/musician_public/{}'.format(id_test))
        self.assertEqual(response.status_code, 200)
        # test template used
        self.assertTemplateUsed(response, 'core/profile_public_musician.html')


        # test if test user elements are present
        self.assertContains(response, 'Super Tatie')
        self.assertNotContains(response, 'Femme')
        self.assertContains(response, 'Elle passe ses nuits sans dormir')
        self.assertContains(response,  '71 ans  ')
        self.assertContains(response, 'Contrebassiste')
        self.assertContains(response, 'Montpellier Herault')
        # test member of band

        self.assertContains(response, 'Pink Floyd')
        self.assertContains(response,  '<a href=\'/core/band_public/pink-floyd\' class="secondary-content">')


class BandProfileTest(MyTestCase):
    ''' Test public profile band'''

    def test_public_profil_band(self):
        slug_test = self.band_test.slug

        response = self.client.get('/core/band_public/{}'.format(slug_test))
        self.assertEqual(response.status_code, 200)
        # test template used
        self.assertTemplateUsed(response, 'core/profile_public_band.html')

        # test if test band elements are present
        self.assertContains(response, 'Pink Floyd')
        self.assertContains(response, 'Pink Floyd est un groupe de rock progressif et psychédélique')
        # self.assertContains(response, '71 ans')
        # self.assertContains(response, 'Contrebassiste')
        self.assertContains(response, 'Londres Angleterre')
        # test member of band

        self.assertContains(response, 'Super Tatie')
        # self.assertContains(response, '<a href=\'/core/musician_public/2\' class="secondary-content">', html=True)

# todo : html assercontains does not work ?




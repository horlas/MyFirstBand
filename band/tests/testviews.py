from requestium import Session, Keys
from django.test import TestCase, RequestFactory
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.test.client import Client
from authentication.models import User
from musicians.models import UserProfile, Instrument
from band.models import Band, Membership
from band.forms import ProfileBandForm

from musicians.forms import ProfileForm, AvatarForm, LocalForm, InstruCreateForm, InstruDeleteForm
from musicians.views import profile, UpdateAvatarView
from core.utils import get_age
from django.core.files.uploadedfile import SimpleUploadedFile
import requests

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


class BandListTest(MyTestCase):

    def setUp(self):
        super(BandListTest, self).setUp()
        self.login = self.client.login(username=self.email, password=self.password)
        self.response = self.client.get('/band/listgroups/')

    def test_bandlist_page(self):

        self.assertEqual(self.login, True)

        self.assertEqual(self.response.status_code, 200)

    def test_bandlist_content(self):

        list_template  = [t.name for t in self.response.templates]
        assert 'band/band_list.html' in list_template
        assert 'core/sidenav_connected.html' in list_template

        self.assertContains(self.response, ' <span class="title">Pink Floyd</span>')
        self.assertContains(self.response, '<i class="material-icons left">add</i>Creer un groupe</a>')




    # def test_bandlist_button(self):
        ''' To test the possibilities to create Band'''
        # self.assertEqual(self.login, True)
        # response = self.session.driver.get('{}/band/listgroups/'.format(self.url))
        # print(response)
        # todo : it 's seems user is not connected
        # create_band_attempt = self.session.driver.find_element_by_xpath('//a[@href="/band/add"]')
        # create_band_attempt.click()
        # url = self.session.driver.current_url
        # print(url)
        # self.session.driver.quit()


class BandCreateTest(MyTestCase):

    def setUp(self):
        super(BandCreateTest, self).setUp()
        self.fake_data_addband = {'name' : 'Noname',
                                  'bio' : 'Something great about the band',
                                  'type' : 'Groupe de Compos',
                                   'musical_genre' : 'Rap' }
        self.login = self.client.login(username=self.email, password=self.password)
        self.url = '/band/add/'
        # self.response = self.client.get('/band/add/')

    def test_bandadd_page(self):
        ''' Test the get response and connected user'''

        self.assertEqual(self.login, True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_bandadd_content(self):
        ''' Test the content of this page '''
        response = self.client.get(self.url)
        list_template = [t.name for t in response.templates]
        assert 'band/create_band.html' in list_template
        assert 'core/sidenav_connected.html' in list_template

        self.assertContains(response, ' <form action=\'/band/add/\' method="post" enctype="multipart/form-data" >')
        self.assertContains(response, '<input id="first" type="button" class="btn custom-btn custom-text " value="trouver">')

    def test_post_bandadd_form(self):
        ''' Test the post datas and correct redirection'''
        data = self.fake_data_addband
        response = self.client.post(self.url, data, follow=True)

        self.assertRedirects(
            response,
            expected_url=reverse('band:list_bands'),
            status_code=302,
            target_status_code=200
        )

    def test_band_add_form_valid(self):
        ''' test only the form '''
        form = ProfileBandForm(self.fake_data_addband)
        self.assertTrue(form.is_valid)

    def test_band_add_form_invalid(self):
        ''' test with a name witch already exist and return error'''
        data = {'name': 'Pink Floyd'}
        form = ProfileBandForm(data)
        self.assertEqual(form.errors['name'][0], 'Band with this Nom du Groupe already exists.')

    def test_post_bandadd_invalid_form(self):
        ''' Test with a band's name witch already exist did not redirect '''
        data = {'name': 'Pink Floyd'}
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(len(response.redirect_chain), 0)


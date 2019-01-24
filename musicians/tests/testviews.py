from requestium import Session, Keys
from django.test import TestCase, RequestFactory
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.test.client import Client
from authentication.models import User
from musicians.models import UserProfile, Instrument
from musicians.forms import ProfileForm, AvatarForm, LocalForm, InstruCreateForm, InstruDeleteForm
from musicians.views import profile
from core.utils import get_age


class MyTestCase(TestCase):
    '''Here is a parent class with custom global setup'''
    def setUp(self):
        # web client
        self.client = Client()
        # our test user
        self.email = 'jean-pierre@hotmail.com'
        self.password = 'aqwz7418'
        self.test_user = User.objects.create_user(self.email, self.password)

        # his profil to test get info
        self.userprofile = UserProfile.objects.get(user = self.test_user)
        self.userprofile.username ='Test'
        self.userprofile.bio = 'Allô Papa Tango Charlie '\
                                'Allô Papa Tango Charlie'\
                                'Répondez, nous vous cherchons'
        self.userprofile.birth_year = 1974
        self.userprofile.town = 'Montpellier'
        self.userprofile.county_name = 'Herault'
        self.userprofile.gender ='H'
        self.userprofile.save()

        # his instruments
        self.instrument = Instrument.objects.create(instrument='Pianiste',
                                                    level='Debutant',
                                                    musician=self.test_user)


        self.factory = RequestFactory()

        # webdriver

        self.session = Session(webdriver_path='./chromedriver',
                    browser='chrome',
                    default_timeout=15,
                    webdriver_options={'arguments': ['headless']})

        self.url = 'http://127.0.0.1:8000'


class ProfileViewTest(MyTestCase):
    ''' Test profile view '''

    def test_profile_page(self):

        request = self.factory.get('/musicians/profile/')
        request.user = self.test_user
        profile_user = self.userprofile

        # set a full profile to test the datas returned
        request.user.userprofile.birth_year = 1948
        request.user.userprofile.username = "Papa Tango"
        request.user.userprofile.bio = 'Allô Papa Tango Charlie ' \
                                       'Allô Papa Tango Charlie'\
                                        'Répondez, nous vous cherchons'

        request.user.userprofile.county_name = 'Hérault'
        request.user.userprofile.town = 'Sussargues'
        request.user.userprofile.save()
        Instrument.objects.create(instrument= "Pianiste",
                                  level ="Debutant",
                                  musician = request.user)



        return_age = '{} ans'.format(get_age(1948))

        response = profile(request)
        self.assertEqual(response.status_code, 200)

        # test if the age is correctly returned
        self.assertContains(response, return_age)

        # test if is no avatar upload the default avatar is present
        self.assertContains(response, '/static/core/img/0.jpg')

        # test if e-mail is present
        self.assertContains(response, request.user.email)

        # test if bio is present
        self.assertContains(response, 'Allô Papa Tango Charlie'\
                                       'Répondez, nous vous cherchons')

        # test if town is present
        self.assertContains(response, 'Sussargues')

        # test if county_name is present
        self.assertContains(response, 'Hérault')

        # test if the instrument and level are presents
        self.assertContains(response, 'Pianiste')

        # test if the edit icon link is present
        self.assertContains(response, "/musicians/update_profile/" )

class UpdateProfilViewTest(MyTestCase):
    ''' Test get forms '''

    def test_update_profil_page(self):
        login = self.client.login(username=self.email, password=self.password)
        # test if the user is logged
        self.assertEqual(login, True)
        response = self.client.get('/musicians/update_profile/')
        # test the status code
        self.assertEqual(response.status_code, 200)

        # Test the initial datas in the forms
        # test if bio is present
        self.assertContains(response, "Allô Papa Tango Charlie ")


        # print(response.context)

        # test if county_name is present
        self.assertContains(response, "Herault")
        #
        # # test if the instrument and level are presents
        self.assertContains(response, 'Pianiste : Debutant')

        # test birth year is present
        self.assertContains(response, '1974')

        # test name is present
        self.assertContains(response, 'Test')

        # test if the forms are in the context of the view
        self.assertIsInstance(response.context['profile_form'], ProfileForm)
        self.assertIsInstance(response.context['avatar_form'], AvatarForm)
        self.assertIsInstance(response.context['local_form'], LocalForm)
        self.assertIsInstance(response.context['instru_form'], InstruCreateForm)
        self.assertIsInstance(response.context['del_instru_form'], InstruDeleteForm)


        # Now let's test each form post

    def test_avatar_form_post(self):







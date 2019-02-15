from requestium import Session, Keys
from django.test import TestCase, RequestFactory
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.test.client import Client
from authentication.models import User
from musicians.models import UserProfile, Instrument
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
        pk = self.test_user.pk
        request = self.factory.get('/musicians/profile/{}'.format(pk))
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

        response = profile(request, pk)
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

    def setUp(self):
        super(UpdateProfilViewTest, self).setUp()
        self.login = self.client.login(username=self.email, password=self.password)
        self.fake_data_profile_form = {'gender': 'F',
                'username': 'Toto',
                'bio': "Et dire qu'il y a un groupe qui s'appelle Toto",
                'birth_year': '1971'}
        self.fake_data_local_form = {'code' : 34070,
                                     'town' : 'Montpellier',
                                     'county_name' : 'Hérault'}

    def test_update_profil_page(self):
        # login = self.client.login(username=self.email, password=self.password)
        # test if the user is logged
        self.assertEqual(self.login, True)
        response = self.client.get('/musicians/update_profile/{}'.format(self.test_user.pk))
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

    def test_avatar_form_bis(self):
        test_img = SimpleUploadedFile('test.png', b'file_content', content_type='/test_img/test.png')
        img = {'avatar': test_img}
        request = self.factory.post(reverse('musicians:update_avatar'), img)
        request.user = self.test_user
        response = UpdateAvatarView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_avatar_form_post(self):
        # test if the user is logged
        self.assertEqual(self.login, True)
        # make sure the user has no avatar image
        qs = UserProfile.objects.filter(id= self.test_user.id)
        for i in qs:
            self.assertEqual(i.avatar.name, '')
        url = reverse("musicians:update_avatar")

        # In Python 3.5+, you must use the bytes object instead of str. Replace "file_content" with b"file_content"
        test_img = SimpleUploadedFile('test.png', b'file_content', content_type='/test_img/test.png')

        img = {'avatar' : test_img}
        #  post the form with test img
        response = self.client.post(url, img, follow=True)
        print(response.redirect_chain)

        # Todo : the post form doesn't redirect to the update_profil page

        self.assertEqual(response.status_code, 200)
        # print(response['location'])

        # self.assertRegex(response.redirect_chain, r'/users/profile/$')
        # self.assertRedirects(
        #     response,
        #     expected_url=reverse("musicians:update_profile", kwargs={'pk': self.test_user.pk} ),
        #      status_code=302,
        #      target_status_code=200
        # )
        # image_src = response.context.get('image_src')
        # print(image_src)

    def test_post_profile_form(self):
        # test if the user is logged
        self.assertEqual(self.login, True)
        url = reverse("musicians:update_data")
        data = self.fake_data_profile_form
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(
            response,
            expected_url=reverse('musicians:update_profile', kwargs={'pk': self.test_user.pk}),
            status_code=302,
            target_status_code=200
        )
        # test the success message
        self.assertContains(response, 'Vos données ont été mises à jour!')

    def test_profile_form_valid(self):
        # test only the form
        form = ProfileForm(self.fake_data_profile_form)
        self.assertTrue(form.is_valid())

    def test_profile_form_not_valid(self):
        # test with bad values
        self.fake_data_profile_form['gender']= ""
        form = ProfileForm(self.fake_data_profile_form)
        self.assertEqual(form.errors['gender'][0], 'This field is required.')

        self.fake_data_profile_form['birth_year'] = "19"
        form = ProfileForm(self.fake_data_profile_form)
        self.assertEqual(form.errors['birth_year'][0], 'Ensure this value is greater than or equal to 1918.')

        self.fake_data_profile_form['birth_year'] = "2028"
        form = ProfileForm(self.fake_data_profile_form)
        self.assertEqual(form.errors['birth_year'][0], 'Ensure this value is less than or equal to 2019.')

    def test_geoapi(self):
        ''' We use GeoApi in JS script, we test 200 code'''
        url = 'https://geo.api.gouv.fr/communes?codePostal=34070'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_local_form(self):
        # test if the user is logged
        self.assertEqual(self.login, True)
        url = reverse("musicians:update_location")
        data = self.fake_data_local_form
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(
            response,
            expected_url=reverse('musicians:update_profile',  kwargs={'pk': self.test_user.pk}),
            status_code=302,
            target_status_code=200
        )

        # test the success message
        self.assertContains(response, 'Votre localité a été mise à jour!')

    def test_post_instru_form(self):
        # test if the user is logged
        self.assertEqual(self.login, True)
        url = reverse("musicians:add_instru")
        data = {'instrument' : 'Flutiste',
                'level': 'Débutant'}
        before_instru = Instrument.objects.filter(musician=self.test_user)

        #### Warning keep this line , we don't know why but without the print the test failed ####
        print(len(before_instru))

        response = self.client.post(url, data, follow=True)
        self.assertRedirects(
            response,
            expected_url=reverse('musicians:update_profile', kwargs={'pk': self.test_user.pk}),
            status_code=302,
            target_status_code=200
        )
        # check if the instrument is well added
        after_instru = Instrument.objects.filter(musician=self.test_user)
        # print(len(after_instru))
        self.assertEqual(len(after_instru), len(before_instru)+1)
        # test the success message
        self.assertContains(response, "Votre Instrument a été ajouté ! ")
        self.assertContains(response, 'Flutiste : Débutant')
        self.assertContains(response, 'Pianiste : Debutant')


    def test_post_del_instru_form(self):
        self.assertEqual(self.login, True)
        url = reverse("musicians:del_instru")
        before_instru = Instrument.objects.filter(musician=self.test_user)
        # as in the view we get the id of the instrument user wants to delete
        for i in before_instru:
            instru_id = i.id
        # print(len(before_instru))
        data = {'instrument' : instru_id}
        response = self.client.post(url, data, follow=True)
        self.assertRedirects(
            response,
            expected_url=reverse('musicians:update_profile', kwargs={'pk': self.test_user.pk}),
            status_code=302,
            target_status_code=200
        )
        self.assertContains(response, "Votre Instrument a été supprimé ! ")
        after_instru = Instrument.objects.filter(musician=self.test_user)
        # print(len(after_instru))
        self.assertEqual(len(after_instru), len(before_instru)-1)
        self.assertNotContains(response, 'Pianiste : Debutant')
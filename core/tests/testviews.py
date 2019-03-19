from requestium import Session
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test.client import Client
from authentication.models import User
from band.models import Band
from musicians.models import UserProfile, Instrument
from announcement.models import MusicianAnnouncement
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from core.views import accueil, search



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
        self.userprofile.code = 34070
        self.userprofile.gender = 'F'

        # In Python 3.5+, you must use the bytes object instead of str. Replace "file_content" with b"file_content"
        # test_img = SimpleUploadedFile('test.png', b'file_content', content_type='/test_img/test.png')
        # self.userprofile.avatar = os.path.join(BASE_DIR, "/user_avatar/0.jpg")
        fileDir = os.path.dirname(os.path.realpath('__file__'))
        filename = os.path.join(fileDir, 'core/static/core/img/0.jpg')
        test_img = SimpleUploadedFile('test.png', content=open(filename, 'rb').read(),
                                      content_type='core/static/core/img/0.jpg')
        self.userprofile.avatar = test_img


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
        self.band_test.musical_genre = 'Rap'
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
        # create some context:
        MusicianAnnouncement.objects.create(title='Coucou', content='Coucou Toi!', author=self.test_user)
        MusicianAnnouncement.objects.create(title='title2', content='content', author=self.test_user)
        MusicianAnnouncement.objects.create(title='title3', content='content', author=self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        list_template = [t.name for t in response.templates]
        assert 'core/sidenav.html' in list_template
        assert 'core/base.html' in list_template
        assert 'core/index.html' in list_template
        # test return of context
        self.assertEqual(len(response.context['last_announcement']), 3)
        self.assertEqual(len(response.context['last_bands']), 1)
        self.assertEqual(len(response.context['last_users']), 1)
        self.assertContains(response, 'Bienvenue sur My First Band')
        self.assertContains(response, 'Pink Floyd')
        self.assertContains(response, 'Super Tatie')
        self.assertContains(response, 'Coucou')
        # this test does not pass with Travis CI
        # Test title website content using selenium driver
        # self.session.driver.get(self.url)
        #
        # # self.assertEqual(self.session.driver.title, 'MyFirstBand')
        #
        # welcome_message = self.session.get(self.url).xpath('//h4[@id="title"]/text()').extract_first()
        # self.assertEqual(welcome_message, 'Bienvenue sur My First Band  ! ')
        #
        # # display last entries of musicians
        # card_musician = self.session.get(self.url).xpath('//section[@id="musicians"]//div[@class="card"]')
        # self.assertEqual(len(card_musician), 6)
        #
        # # display last entries of band
        # card_band = self.session.get(self.url).xpath('//section[@id="bands"]//div[@class="card"]')
        # self.assertEqual(len(card_band), 6)


class TestPrivacyPolicy(MyTestCase):
    def test_privacy_policy(self):
        url = reverse('core:privacy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class TestSearchView(MyTestCase):

    def setUp(self):
        super(TestSearchView, self).setUp()
        self.url = reverse('core:search')
        # specially for ajax view
        self.kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        # create some context:
        self.a1 = MusicianAnnouncement.objects.create(title="Coucou", content="Coucou Toi!", author=self.test_user,code='30600', town="Nimes", county_name="Gard")
        self.a2 = MusicianAnnouncement.objects.create(title="title2", content="content", author=self.test_user,code='30600', town="Nimes", county_name="Gard")
        self.a3 = MusicianAnnouncement.objects.create(title="title3", content="content", author=self.test_user, code="30600", town="Nimes", county_name="Gard")

        first_created_at = self.a1.created_at.strftime("%d %B %Y")
        second_created_at = self.a2.created_at.strftime("%d %B %Y")
        third_created_at = self.a3.created_at.strftime("%d %B %Y")

        # be careful order is reversed
        self.layout_response = [
            {"tag": "annonces", "title": self.a3.title, "created_at": third_created_at,
             "county_name": self.a3.county_name,"id": self.a3.id, "town": self.a3.town},
            {"tag": "annonces", "title": self.a2.title, "created_at": second_created_at, "county_name": self.a2.county_name,
             "id": self.a2.id,"town": self.a2.town},
            {"tag": "annonces", "title": self.a1.title, "created_at": first_created_at,"county_name": self.a1.county_name,
             "id": self.a1.id,"town": self.a1.town}
            ]

    def test_annonces_without_cp(self):
        ''' case test query 'Annonces' without cp, the view return all announcements '''
        data = {'item': 'Annonces', 'cp': ''}
        request = self.factory.post(self.url, data, **self.kwargs)
        response = search(request)
        self.assertEqual(response.status_code, 200)
        response_content = str(response.content, encoding='utf8')
        self.assertJSONEqual(response_content, self.layout_response)

    def test_annonces(self):
        ''' case test query 'Annonces' with cp, the view return all announcements of county code '''
        data = {'item': 'Annonces', 'cp': '30'}
        request = self.factory.post(self.url, data, **self.kwargs)
        response = search(request)
        self.assertEqual(response.status_code, 200)
        response_content = str(response.content, encoding='utf8')
        self.assertJSONEqual(response_content, self.layout_response)

    def test_musicians(self):
        ''' test case with 'Musiciens' and cp code'''
        data = {'item': 'Musiciens', 'cp': '34'}
        request = self.factory.post(self.url, data, **self.kwargs)
        response = search(request)
        self.assertEqual(response.status_code, 200)
        response_content = str(response.content, encoding='utf8')
        # print(response_content)
        layout_response = [{"town": "Montpellier",
                            "instrument": {str(self.instrument.id): "Contrebassiste"},
                            "pk": self.test_user.pk, "tag": "musicians",
                            "avatar":  self.userprofile.avatar.url,
                            "name": "Super Tatie", "county_name": "Herault"}]
        self.assertJSONEqual(response_content, layout_response)

        # without avatar image

    def test_band(self):
        ''' test case with 'Groupes' without cp code without avatar image'''
        data = {'item': 'Groupes', 'cp': ''}
        request = self.factory.post(self.url, data, **self.kwargs)
        response = search(request)
        self.assertEqual(response.status_code, 200)
        response_content = str(response.content, encoding='utf8')
        layout_response = [{"bio": self.band_test.bio,
                            "type": "Groupe de Compos",
                            "name": self.band_test.name,
                            "tag": "groupes",
                            "avatar": "static/core/img/0_band.jpg",
                            "slug": self.band_test.slug,
                            "musical_genre": self.band_test.musical_genre,
                            "town": "Londres",
                            "county_name": "Angleterre"}]
        self.assertJSONEqual(response_content, layout_response)

    def test_view_fail(self):
        ''' in the impossible case where the view will return a 'fail
        we mock this without get the XMLHttpRequest '''
        data = {'item': 'Groupes', 'cp': ''}
        request = self.factory.post(self.url, data)
        response = search(request)
        self.assertEqual(response.status_code, 200)
        response_content = str(response.content, encoding='utf8')
        self.assertEqual(response_content, '"fail"')


class SidenavBarTest(MyTestCase):
    ''' Test NavBar Content '''

    def test_navbar(self):

        # Test if the logo is loaded by checking the size

        r = self.client.get(reverse(accueil))
        self.assertContains(r, 'logo_small.png')
        list_template = [t.name for t in r.templates]
        assert 'core/index.html' in list_template
        assert 'core/sidenav.html' in list_template


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




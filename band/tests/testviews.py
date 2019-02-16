from requestium import Session, Keys
from django.test import TestCase, RequestFactory
from django.contrib.auth.views import LoginView
from django.urls import reverse
from django.test.client import Client
from authentication.models import User
from musicians.models import UserProfile, Instrument
from band.models import Band, Membership
from band.forms import ProfileBandForm
from band.views import BandUpdateView, AddMemberView, autocomplete_username, MembershipDelete
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
import json

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

        # add a second members to test some features
        self.email3 = 'paul@gmail.com'
        self.password3 = 'aqwz7418'
        self.test_user3 = User.objects.create_user(self.email3, self.password3)
        self.test_user3.userprofile.username = 'Super Toto'
        self.test_user3.userprofile.save()

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

    def test_post_band_add_invalid_form(self):
        ''' Test with a band's name witch already exist did not redirect '''
        data = {'name': 'Pink Floyd'}
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(len(response.redirect_chain), 0)


class BandDetailTest(MyTestCase):

    def setUp(self):
        super(BandDetailTest, self).setUp()

        self.login = self.client.login(username=self.email, password=self.password)
        self.url = '/band/{}'.format(self.band_test.slug)

    def test_band_detail_page(self):
        ''' Test the get response and connected user'''

        self.assertEqual(self.login, True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_band_detail_content(self):
        ''' Test the content of this page '''
        response = self.client.get(self.url)
        list_template = [t.name for t in response.templates]
        assert 'band/band_detail.html' in list_template
        assert 'band/sidenav_band.html' in list_template
        # because avatar is not umpload we have the button'mettre à jour'
        self.assertContains(response, 'Mettre à jour le  groupe')
        # link to the profil member to ensure that members are displayed
        self.assertContains(response, ' href=\'/core/musician_public/')


class BandUpdateTest(MyTestCase):

    def setUp(self):
        super(BandUpdateTest, self).setUp()
        self.test_img = SimpleUploadedFile('test.png', b'file_content', content_type='/test_img/test.png')

        self.fake_data_updateband = {'name': 'Noname',
                                  'bio': 'Something great about the band',

                                  'type': 'Groupe de Compos',
                                  'musical_genre': 'Rap'}

        self.login = self.client.login(username=self.email, password=self.password)
        self.url = '/band/edit/{}'.format(self.band_test.slug)

    def test_band_edit_page(self):
        ''' Test the get response and connected user'''

        self.assertEqual(self.login, True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_band_detail_content(self):
        ''' Test the content of this page '''
        response = self.client.get(self.url)
        list_template = [t.name for t in response.templates]
        assert 'band/edit_band.html' in list_template
        assert 'band/sidenav_band.html' in list_template
        # check instance band datas
        self.assertContains(response, 'Pink Floyd')
        self.assertContains(response, 'Rap')
        # test if the form is well rendered
        self.assertContains(response, '<form action=\'/band/edit/pink-floyd\' method="post" enctype="multipart/form-data" >\n')

    def test_post_band_update_form(self):
        ''' Test the post datas and correct redirection'''
        data = self.fake_data_updateband
        response = self.client.post(self.url, data, follow=True)

        self.assertRedirects(
            response,
            expected_url='/band/noname',
            status_code=302,
            target_status_code=200
        )
        # todo : Post avatar there is for the moment no solution
    # def test_post_bandupdate_avatar_form(self):
    #     ''' Test only the upload of avatar with Factory request'''
    #     img = {'avatar' : self.test_img}
    #     url = 'http://127.0.0.1:8000/{}'.format(self.url)
    #     print(self.url)
    #     request = self.factory.post(reverse('band:edit_band', kwargs={"slug" :self.band_test.slug}), img)
    #     request.user = self.test_user
    #     response = BandUpdateView.as_view()(request)
    #     self.assertEqual(response.status_code, 200)
    def test_band_add_form_valid(self):
        ''' test only the form '''
        form = ProfileBandForm(self.fake_data_updateband)
        self.assertTrue(form.is_valid)

    def test_band_add_form_invalid(self):
        ''' test with a name witch already exist and return error'''
        data = {'name': 'Pink Floyd'}
        form = ProfileBandForm(data)
        self.assertEqual(form.errors['name'][0], 'Band with this Nom du Groupe already exists.')

    def test_band_add_form_invalid2(self):
        ''' test with a name witch already exist and return error'''
        # todo :  we must see why we can not upload a file
        data = {'avatar': self.test_img}
        form = ProfileBandForm(data)
        self.assertEqual(form.errors['name'][0], 'This field is required.')

class ManageBandTest(MyTestCase):

    def setUp(self):
        super(ManageBandTest, self).setUp()
        # add a second members to test some features
        self.email2 = 'jean-pierre@gmail.com'
        self.password2 = 'aqwz7418'
        self.test_user2 = User.objects.create_user(self.email2, self.password2)
        # his profil to test get info
        self.userprofile2 = UserProfile.objects.get(user=self.test_user2)
        self.userprofile2.username = 'Jean-Pierre'
        self.userprofile2.save()
        # add test_user2 to the band
        member2 = Membership(musician=self.test_user2,
                             band= self.band_test)
        member2.save()


        self.fake_data_updateband = {'name': 'Noname',
                                  'bio': 'Something great about the band',

                                  'type': 'Groupe de Compos',
                                  'musical_genre': 'Rap'}

        self.login = self.client.login(username=self.email, password=self.password)
        self.url = '/band/manage/{}'.format(self.band_test.slug)

    def test_manage_band_page(self):
        ''' Test the get response and connected user'''

        self.assertEqual(self.login, True)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_manage_band_content(self):
        response = self.client.get(self.url)
        list_template = [t.name for t in response.templates]
        assert 'band/manage_band.html' in list_template
        assert 'band/sidenav_band.html' in list_template
        # # check instance band datas
        # test if the members are correctly displayed
        self.assertContains(response,
                            ' <span class="title">Jean-Pierre</span>',
                            html=True)

        self.assertContains(response, '<span class ="title" > Super Tatie </span>', html=True)
        # test if the add form is correctly displayed
        # self.assertContains(response, '< form action =\'/band/add_member/submit\' method="post"')

        # test if the delete form members is correctly displayed
        # self.assertContains(response,
        #                     '<form method="post" action="/band/delete_member/19">',
        #                     html=True)
        self.assertContains(response,
                            '<h4> Voulez vous supprimer Jean-Pierre du groupe ?</h4>',
                            html=True)
        # test if change owner is correctly displayed
        self.assertContains(response,
                            '<option value="Super Tatie">Super Tatie</option>',
                            html=True)
        # test if delete band form is correctly displayed
        self.assertContains(response,
                         '<h4> Voulez vous supprimer Pink Floyd ? Vous perdrez toutes les données du groupe.</h4>', html=True )
        # self.assertContains(response,
        #                     ' <form method="post" action="/band/delete_band/18">',
        #                     html=True)
        # self.assertTrue('<form method="post" action="/band/delete_band/18">' in response.content)



        # Todo : some test html don't work especially form


class AddMemberTest(MyTestCase):

    def test_post_form(self):
        ''' Test only the view witch add member with Factory request.
        In this test we add test-user3 to band_test'''

        # count before create membership
        before = Membership.objects.count()
        data = {'musician' : self.test_user3.userprofile.username,
                'raison_invitation' : 'super chouette',
                'band' : self.band_test}

        request = self.factory.post(reverse('band:add_member'), data)
        request.user = self.test_user

        # adding session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        # adding messages
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        for m in messages:
            print(m)

        response = AddMemberView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        after = Membership.objects.count()
        # the membership is well create
        self.assertEqual(after, before+1)

class AutocompleteTest(MyTestCase):
    ''' we test the fucntion witch autocomplete fields with member names , query on database)'''

    def test_autocomplete_username(self):
        # specially for ajax view
        kwargs = {'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'}
        url = reverse('band:search')
        get_data = {'term': 'su' }
        request = self.factory.get(url, get_data, **kwargs)
        request.user = self.test_user
        response = autocomplete_username(request)
        self.assertEqual(response.status_code, 200)
        # test the return of ajax call
        response_content = str(response.content, encoding='utf8')
        self.assertJSONEqual(response_content, [{"id": 3, "label": "Super Tatie", "value": "Super Tatie"}, {"id": 4, "label": "Super Toto", "value": "Super Toto"}] )


class MembershipDeleteTest(MyTestCase):
    ''' We test the feature : delete a member . First we add the member'''

    def setUp(self):
        super(MembershipDeleteTest, self).setUp()
        # add a second members to test some features
        self.email2 = 'jean-pierre@gmail.com'
        self.password2 = 'aqwz7418'
        self.test_user2 = User.objects.create_user(self.email2, self.password2)
        # his profil to test get info
        self.userprofile2 = UserProfile.objects.get(user=self.test_user2)
        self.userprofile2.username = 'Jean-Pierre'
        self.userprofile2.save()
        # add test_user2 to the band
        self.member2 = Membership(musician=self.test_user2,
                             band=self.band_test)
        self.member2.save()

    def test_delete_view_get(self):
        # before delete it , ensure the member exists
        t = Membership.objects.filter(musician=self.test_user2).exists()
        self.assertTrue(t, True)
        request = self.factory.post('band/delete_member/', args={'pk':self.member2.id})
        # adding connected user
        request.user = self.test_user
        # adding session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        # adding messages
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        # test the view
        response = MembershipDelete.as_view()(request, pk=self.member2.id)
        # test the redirection
        self.assertEqual(response.status_code, 302)
        # ensure that the member is deleted
        t1 = Membership.objects.filter(musician=self.test_user2).exists()
        self.assertFalse(t1, False)
        # request.user = self.test_user
        #     # print(self.member2.pk)
        # response = MembershipDelete.as_view()(request)
        # self.assertEqual(response.status_code, 302)
        # url = '/band/delete_member/{}'.format(m.id)
        # response = self.client.post(url, follow=True)
        # print(response.status_code)
        # self.assertContains(response, 'sdfsfdsf')

    # def test_delete_member(self):
    #     before = Membership.objects.filter(band=self.band_test).count()
    #
    #     # url = reverse('band:del_member', kwargs = {'int': self.member2.pk})
    #     # url = '/band/delete_member/{}'.format(self.member2.pk)
    #     request = self.factory.post(reverse('band:del_member'), kwargs={'int': self.member2.pk})
    #     request.user = self.test_user
    #     # print(self.member2.pk)
    #     response = MembershipDelete.as_view()(request)
    #     self.assertEqual(response.status_code, 302)
    #     #

# todo : test deleteview always return 404

# class BandDeleteTest(MyTestCase):
#     ''' We test the feature : delete a member . First we add the member'''
#
#     def setUp(self):
#         super(BandDeleteTest, self).setUp()
#         # add a second members to test some features
#         self.email2 = 'jean-pierre@gmail.com'
#         self.password2 = 'aqwz7418'
#         self.test_user2 = User.objects.create_user(self.email2, self.password2)
#         # his profil to test get info
#         self.userprofile2 = UserProfile.objects.get(user=self.test_user2)
#         self.userprofile2.username = 'Jean-Pierre'
#         self.userprofile2.save()
#         # add test_user2 to the band
#         self.member2 = Membership(musician=self.test_user2,
#                              band=self.band_test)
#         self.member2.save()
#
#
#     def test_delete_band(self):





# def test_post_bandupdate_avatar_form(self):
    #     ''' Test only the upload of avatar with Factory request'''
    #     img = {'avatar' : self.test_img}
    #     url = 'http://127.0.0.1:8000/{}'.format(self.url)
    #     print(self.url)
    #     request = self.factory.post(reverse('band:edit_band', kwargs={"slug" :self.band_test.slug}), img)
    #     request.user = self.test_user
    #     response = BandUpdateView.as_view()(request)
    #     self.assertEqual(response.status_code, 200)
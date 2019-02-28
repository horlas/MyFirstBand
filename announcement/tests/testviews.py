from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.urls import reverse, reverse_lazy
from django.test.client import Client

from authentication.models import User
from musicians.models import UserProfile, Instrument
from announcement.models import MusicianAnswerAnnouncement, MusicianAnnouncement
from announcement.forms import MusicianAnnouncementForm
from announcement import views


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
        self.userprofile.county_name = 'Hérault'
        self.userprofile.gender = 'F'
        self.userprofile.save()

        # her instruments
        self.instrument = Instrument.objects.create(instrument='Contrebassiste',
                                                    level='Intermediaire',
                                                    musician=self.test_user)

        # we need to create some announcement
        self.a1 = MusicianAnnouncement.objects.create(title='title1', content='Coucou Toi!', author=self.test_user)
        self.a2 = MusicianAnnouncement.objects.create(title='title2', content='content', author=self.test_user)
        self.a3 = MusicianAnnouncement.objects.create(title='title3', content='content', author=self.test_user)

        # log user
        self.login = self.client.login(username=self.email, password=self.password)

        # Factory
        self.factory = RequestFactory()


class AnnouncementCreateTest(MyTestCase):
    ''' Test create new ads and valid the form to do this'''

    def setUp(self):
        super(AnnouncementCreateTest, self).setUp()
        self.url = reverse('announcement:create_announcement')
        self.response = self.client.get(self.url)
        self.data =  {'content': 'blablabla',
              'title': 'Contrebassiste cherche groupe'}

    def test_view_create_announcement(self):
        ''' test the response and the contains'''

        self.assertEqual(self.login, True)
        self.assertEqual(self.response.status_code, 200)
        list_template = [t.name for t in self.response.templates]
        assert 'announcement/create_announcement.html' in list_template
        assert 'announcement/form.html' in list_template
        assert 'core/sidenav_connected.html' in list_template

    def test_initial_form_data(self):
        ''' test the initial data , the form is prepopulated'''

        self.assertContains(self.response, 'Contrebassiste cherche groupe')
        self.assertContains(self.response, 'Montpellier')
        self.assertContains(self.response, 'Hérault')

    def test_valid_form(self):
        ''' test the valid form'''
        form = MusicianAnnouncementForm(self.data)
        self.assertTrue(form.is_valid)

    def test_invalid_form(self):
        ''' test blank field'''
        self.data['title'] = ""
        form = MusicianAnnouncementForm(self.data)
        self.assertEqual(form.errors['title'][0], 'This field is required.')

    def test_post_announcement(self):
        ''' with Factory request test the create ok a new ads'''

        # count before musician announcement
        before = MusicianAnnouncement.objects.count()
        request = self.factory.post(self.url, self.data)
        request.user = self.test_user

        # adding session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        # adding messages
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # test the view
        response = views.AnnouncementCreateView.as_view()(request)

        # test the success message
        for m in messages:
            message = str(m)
        self.assertEqual(message, ' Félicitations ! Votre annonce a été créée ! ')

        # test the redirection
        self.assertEqual(response.status_code, 302)

        # test the announcement is well created
        after = MusicianAnnouncement.objects.count()
        self.assertEqual(after, before + 1)

        # test if the request user is really the author
        a = MusicianAnnouncement.objects.get(content='blablabla')
        self.assertEqual(a.author, self.test_user)



class AnnouncementListTest(MyTestCase):
    ''' we test here all the management of announcement thought the list view'''

    def setUp(self):
        super(AnnouncementListTest, self).setUp()
        self.url = reverse('announcement:announcement_list')
        self.response = self.client.get(self.url)

    def test_list_views(self):

        self.assertEqual(self.login, True)
        self.assertEqual(self.response.status_code, 200)
        list_template = [t.name for t in self.response.templates]

        assert 'announcement/announcement_list.html' in list_template
        assert 'core/sidenav_connected.html' in list_template
        # print(self.response.content)
        # button to create announcement
        self.assertContains(self.response, 'Creer une annonce')
        # list of announcement
        self.assertContains(self.response, 'Mes annonces en ligne')
        self.assertContains(self.response, 'title1')
        self.assertContains(self.response, 'title2')
        self.assertContains(self.response, 'title3')
        # print(self.response.context['list of announcements'])


class AnnouncementManagementTest(MyTestCase):
    ''' we test the fact to archive and online announcement'''

    def test_archive_announcement(self):
        ''' with Factory request we test archive an announcement a1'''
        self.assertEqual(self.a1.is_active, True)

        url_archive = reverse ('announcement:archive', kwargs={'id': self.a1.id})
        data = {'signal': self.a1.id}
        request = self.factory.post(url_archive, data)
        request.user = self.test_user

        # adding session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        # adding messages
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # test the view
        response = views.archive_announcement(request)

        # test the success message
        for m in messages:
            message = str(m)
        self.assertEqual(message, "L'annonce a été archivée")
        # redirect to list_announcement
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/announcement/list_post/')

        # test if ads is well archived
        self.a1.refresh_from_db()
        self.assertEqual(self.a1.is_active, False)

    def test_online_announcement(self):
        ''' with Factory request we test archive an announcement a1'''
        self.a1.is_active = False
        self.a1.save()
        url_online = reverse ('announcement:online', kwargs={'id': self.a1.id})
        data = {'signal2': self.a1.id}
        request = self.factory.post(url_online, data)
        request.user = self.test_user

        # adding session
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()

        # adding messages
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

        # test the view
        response = views.online_announcement(request)

        # test the success message
        for m in messages:
            message = str(m)
        self.assertEqual(message, "L'annonce a été mise en ligne")
        # # redirect to list_announcement
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/announcement/list_post/')

        # test if ads is well archived
        self.a1.refresh_from_db()
        self.assertEqual(self.a1.is_active, True)


class AnnouncementUpdateTest(MyTestCase):
    ''' to test update view'''

    def setUp(self):
        super(AnnouncementUpdateTest, self).setUp()
        self.url = reverse('announcement:update_announcement', kwargs={"pk": self.a1.id})
        self.response = self.client.get(self.url)

    def test_announcement_update_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        list_template = [t.name for t in self.response.templates]
        assert 'announcement/update_announcement.html'in list_template
        assert 'announcement/form.html' in list_template
        assert 'core/sidenav_connected.html' in list_template
        self.assertContains(response, 'Coucou Toi!')

    def test_announcement_update_post(self):
        data = {'title' : 'Cherche machine à laver',
                'content' : 'Sur le bon coin'}
        response = self.client.post(self.url, data, follow=True)
        self.assertRedirects(response,
                             expected_url=reverse_lazy('announcement:announcement_list'),
                             status_code=302,
                             target_status_code=200
                             )
        # test if the title is well changed
        self.a1.refresh_from_db()
        self.assertEqual(self.a1.title, 'Cherche machine à laver')


class AnnouncementDetailTest(MyTestCase):
    ''' this view is public , we don't need log an user'''

    def test_detail_view(self):
        self.client.logout()
        url = reverse('announcement:detail_announcement', kwargs={"pk": self.a1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        list_template = [t.name for t in response.templates]
        assert 'announcement/announcement.html' in list_template
        assert 'announcement/answer.html' in list_template
        # assert 'core/sidenav_connected.html' in list_template
        self.assertContains(response, 'Pour répondre se connecter')
        self.assertContains(response, 'Coucou Toi!')
        self.client.login(username=self.email, password=self.password)
        response = self.client.get(url)
        self.assertNotContains(response, 'Pour répondre se connecter')
        self.assertContains(response, 'Répondre')


from django.test import TestCase, RequestFactory
from django.test.client import Client
from authentication.models import User
from core.views import accueil


class MyTestCase(TestCase):
    '''Here is a parent class with custom global setup'''
    def setUp(self):
        # web client
        self.client = Client()
        # our test user
        self.user = User.objects.create( email='test@hotmail.com',
                                              password = 'aqwz7418')

        self.factory = RequestFactory()

class AccueilTest(MyTestCase):
    ''' Test accueil view'''
    def test_accueil(self):
        request = self.factory.get('')
        response = accueil(request)
        self.assertEqual(response.status_code, 200)


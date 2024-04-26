from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse


# Create your tests here.
class BaseTestCase(APITestCase):
    login_data = {
        "username":"betty",
        "password":"betty@123"
    }

    data = {
        "available_seats": 18, 
        "destination":"JFK", 
        "depature_time":"2024-04-25T5:18:10Z"
    }

    fixtures = ['reserve/fixtures/users.json', 'reserve/fixtures/flights.json']

    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.login_response = self.client.post(
            self.login_url, 
            self.login_data, 
            format='json',
            )
        test_token = self.login_response.data['token']
        self.auth_header = 'Token {}'.format(test_token)
        self.data = self.data
class FlightViewTestCase(BaseTestCase):

    def test_api_gets_flight(self):
        url = reverse('flights')

        response = self.client.get(
            url, HTTP_AUTHORIZATION=self.auth_header, format='json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['flights'][0]['destination'],"New Jersey" )
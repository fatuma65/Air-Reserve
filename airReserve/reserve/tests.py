from django.test import TestCase
from rest_framework.test import APIClient, APITestCase
from django.urls import reverse
from rest_framework import status
from reserve.models import Booking, Flight

# Create your tests here.
class BaseTestClass(APITestCase):
    login_data = {
        "username":"cathy",
        "password":"Cathy@123"
    }
    data = {
        "depature_time": "2024-04-13 21:00:00+03",
        "destination": "New York",
        "available_seats":200
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
        self.auth_header = {"Authorization": 'Token {}'.format(test_token)}
class FlightViewTestCase(BaseTestClass):

    def test_api_gets_flight(self):
        url = reverse('flights')

        response = self.client.get(
            url, headers=self.auth_header, format='json'
        )

        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['flights'][0]['destination'],"Canada" )

class BookingTestCase(BaseTestClass):

    def test_api_creates_bookings(self):

        flight = Flight.objects.all()
        print('fights available',[f.id for f in flight])

        url = '/create/booking/5/'
        response = self.client.post(
            url,
            data={"seat_number":3},
            headers=self.auth_header,
            format='json'

        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'flight booked successfully')

class ListBookingsTestClass(BaseTestClass):

    def test_api_gets_bookings(self):

        flight = Flight.objects.all()
        print('listing bookings', [f.id for f in flight])

        url = '/create/booking/10/'
        url_param = '/bookings/'
        print(url_param)
        self.client.post(
            url, 
            data={"seat_number":7},
            headers = self.auth_header, 
            format='json'
        )
        response = self.client.get(
            url_param, 
            headers = self.auth_header, 
            format='json'
        )
        self.assertEqual(response.status_code, 200)

class CancelBookingTestCase(BaseTestClass):
    def test_api_cancels_bookings(self):

        flight = Flight.objects.all()
        print('fights available',[f.id for f in flight])

        flight = Booking.objects.all().values()
        print('canceling bookings', [f.id for f in flight])

        url_h = '/create/booking/6/'
        url_b = '/bookings/'
        url = '/cancel/2/'

        print(url_b)

        self.client.post(
            url_h, 
            data={"seat_number":7},
            headers = self.auth_header, 
            format='json'
        )

        self.client.get(
            url_b,
            headers=self.auth_header,
            format='json'
        )
        response = self.client.delete(
            url,
            headers=self.auth_header,
            format='json'
        )
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Your booking is deleted successfully')

    def test_case_booking_doesnt_exist(self):
        url_b = '/bookings/'
        url = '/cancel/'
        self.client.post(
            url_b,
            headers=self.auth_header,
            format='json'
        )
        response = self.client.delete(
            url,
            headers=self.auth_header,
            format='json'
        )
        self.assertEqual(response.status_code, 404)

class AdminCreatesFlights(BaseTestClass):

    def test_case_admin_creates_flighs(self):
        url = reverse('create_flights')
        response = self.client.post(
            url,
            headers=self.auth_header,
            data=self.data,
            format='json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['message'], 'Flight successfully created')
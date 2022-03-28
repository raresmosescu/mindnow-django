from django.test import TestCase
from django.urls import reverse
from app_dir.trip.models import Trip, City, Flight, Booking, UserTrip
from django.contrib.auth.models import User
from ..urls import urlpatterns
from django.contrib.auth.hashers import make_password

class TripViewTest(TestCase):
    
    def setUp(self):
        self.user = User(username='rares', password=make_password('rarespassword'))
        self.user.save()
        self.trip = Trip.create_trip('Trip Name', self.user)
        self.member = UserTrip.create_member(self.trip, 'rares', 'Rares Mosescu')
        self.city1 = City.create_city('Bucharest', self.trip)
        self.city2 = City.create_city('Brasov', self.trip)
        self.booking = Booking(
            location_name = 'asd',
            city = self.city2,
            check_in = '2022-09-13',
            check_out = '2022-09-15',
            cost = '33',
        )
        self.booking.save() 
        self.flight = Flight(
            airline_name = 'Blue Air',
            departure_date = '2022-09-13',
            arrival_date = '2022-09-13',
            departure_time = '10:30',
            arrival_time = '12:30',
            from_city = self.city1,
            to_city = self.city2,
            cost = '44',
        )
        self.flight.save()

        self.client.login(username='rares', password='rarespassword')
        


    def test_all_paths_status_200(self):
        responses = []
        
        # Auth
        responses.append(self.client.get(f'/login/'))
        responses.append(self.client.get(f'/register/'))

        # Trip
        responses.append(self.client.get(f'')) 
        responses.append(self.client.get(f'/trip/')) 
        responses.append(self.client.get(f'/trip/create/')) 
        responses.append(self.client.get(f'/trip/{self.trip.id}/edit/')) 
        Trip.create_trip('Trip Name', self.user) # create new trip to delete
        responses.append(self.client.get(f'/trip/{self.trip.id+1}/delete/', follow=True)) 

        # Member (UserTrip)
        responses.append(self.client.get(f'/trip/{self.trip.id}/member/{self.member.id}/')) 
        responses.append(self.client.get(f'/trip/{self.trip.id}/member/create/')) 
        responses.append(self.client.get(f'/trip/{self.trip.id}/member/{self.member.id}/edit/')) 
        m = UserTrip.create_member(self.trip, '', 'Adrian') # create new trip to delete
        responses.append(self.client.get(f'/trip/{self.trip.id}/member/{m.id}/delete/', follow=True))

        # City 
        responses.append(self.client.get(f'/trip/{self.trip.id}/city/{self.city2.id}/')) 
        # responses.append(self.client.get(f'/trip/{self.trip.id}/city/create')) 
        responses.append(self.client.get(f'/trip/{self.trip.id}/city/{self.city2.id}/edit/')) 
        c = City.create_city('Vaslui', self.trip) # create new trip to delete
        responses.append(self.client.get(f'/trip/{self.trip.id}/city/{c.id}/delete/', follow=True))

        # Booking
        responses.append(self.client.get(f'/trip/{self.trip.id}/city/{self.city2.id}/b/{self.booking.id}/')) 
        responses.append(self.client.get(f'/trip/{self.trip.id}/city/{self.city2.id}/b/create/')) 
        responses.append(self.client.get(f'/trip/{self.trip.id}/city/{self.city2.id}/b/{self.booking.id}/edit/'))
        b = Booking(
            location_name = 'asdas',
            city = self.city2,
            check_in = '2022-09-01',
            check_out = '2022-09-03',
            cost = '33',
        ) # create new trip to delete
        b.save()
        responses.append(self.client.get(f'/trip/{self.trip.id}/city/{self.city2.id}/b/{b.id}/delete/', follow=True)) 

        # Flight
        responses.append(self.client.get(f'/trip/{self.trip.id}/f/{self.flight.id}/')) 
        responses.append(self.client.get(f'/trip/{self.trip.id}/f/create/')) 
        responses.append(self.client.get(f'/trip/{self.trip.id}/f/{self.flight.id}/edit/')) 
        f = Flight(
            airline_name = 'Blue Air',
            departure_date = '2022-09-01',
            arrival_date = '2022-09-01',
            departure_time = '12:30',
            arrival_time = '13:30',
            from_city = self.city1,
            to_city = self.city2,
            cost = '55',
        ) # create new trip to delete
        f.save()
        responses.append(self.client.get(f'/trip/{self.trip.id}/f/{f.id}/delete/', follow=True))

        for idx, r in enumerate(responses):
            self.assertEqual(200, r.status_code, msg=r)


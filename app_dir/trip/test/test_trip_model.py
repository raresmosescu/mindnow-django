
from django.test import TestCase
from app_dir.trip.models import Trip, City, Flight, Booking, UserTrip
from django.contrib.auth.models import User
import os
from django.conf import settings

class UnitTest(TestCase):
    def setUp(self):
        self.user = User(username='rares', password='rarespassword')
        self.user.save()

    def test_trip_create_trip_function(self):
        """ Test Trip.create_trip function """
        trip_name = 'Trip to Romania'
        old_trip_count, old_member_count = Trip.objects.count(), UserTrip.objects.count()
        trip = Trip.create_trip(trip_name, self.user)
        new_trip_count, new_member_count = Trip.objects.count(), UserTrip.objects.count()
        self.assertNotEqual(old_trip_count, new_trip_count)
        self.assertNotEqual(old_member_count, new_member_count)

    def test_usertrip_create_member_function(self):
        """ Test if the UserTrip.create_member function creates a Member as expected. """
        trip = Trip.create_trip('Trip Name', self.user)
        trip, username, nickname = trip, 'rares', 'Rares Mosescu'
        old_count = UserTrip.objects.count()
        self.member = UserTrip.create_member(trip, username, nickname)
        new_count = UserTrip.objects.count()
        self.assertNotEqual(old_count, new_count)
        self.assertEqual(self.member.nickname, nickname)
        self.assertEqual(self.member.user.username, username)
        self.assertEqual(self.member.trip, trip)

    def test_usertrip_create_member_function(self):
        """ Test if the UserTrip.create_member function creates a Member as expected. """
        trip = Trip.create_trip('Trip Name', self.user)
        trip, username, nickname = trip, 'rares', 'Rares Mosescu'
        old_count = UserTrip.objects.count()
        self.member = UserTrip.create_member(trip, username, nickname)
        new_count = UserTrip.objects.count()
        self.assertNotEqual(old_count, new_count)
        self.assertEqual(self.member.nickname, nickname)
        self.assertEqual(self.member.user.username, username)
        self.assertEqual(self.member.trip, trip)
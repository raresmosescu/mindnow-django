from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db.models import Q



class Trip(models.Model):
    """Trip model    
    
    Fields: name, created_by
    """
    name = models.CharField(max_length=128)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)

    @property
    def trip_users(self):
        """
        Return the IDs of all users associated to this trip
        """
        return UserTrip.objects.filter(trip_id=self.id).values_list('user_id',flat=True)

    @property
    def trip_cities(self):
        """
        Return the IDs of all cities associated to this trip
        """
        return City.objects.filter(trip_id=self.id).values_list('id',flat=True)

    @property
    def trip_flights(self):
        """
        Return the ID of all flights associated to this trip
        """
        return Flight.objects.filter(Q(from_city_id__in=self.trip_cities)|Q(to_city_id__in=self.trip_cities)).values_list('id',flat=True)

    @property
    def trip_bookings(self):
        """
        Return the ID of all flights associated to this trip
        """
        return Booking.objects.filter(city_id__in=self.trip_cities).values_list('id',flat=True)

    @staticmethod
    def create_trip(name, user):
        """
        Create new trip & m2m relation
        """
        trip = Trip(name=name, created_by=user)
        trip.save()
        UserTrip(user=user, trip=trip, nickname=user.username).save()
        return trip
    
    def __str__(self):
        return self.name



class UserTrip(models.Model):
    """
    M2M model for User and Trip
    
    Fields: user, trip, nickname (trip specific nick name)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, null=False)
    nickname = models.CharField(max_length=60, blank=False)

    @staticmethod
    def user_trips(user_id):
        """
        Join user and trips tables related to user_id
        """
        return UserTrip.objects.filter(user=user_id).select_related('user', 'trip')

    @staticmethod
    def create_member(trip, username, nickname):
        """Create trip member

        Args:
            trip (Trip object): This is the trip the member will be added to
            username (str): Member User.username, if they have account
            nickname (str): Trip display name

        Returns:
            UserTrip: returns the created UserTrip object
        """
        if username:
            user = User.objects.get(username=username)
            member = UserTrip(user=user, trip=trip, nickname=nickname)
        else:
            member = UserTrip(trip=trip, nickname=nickname)

        member.save()
        return member
         


class City(models.Model):
    """ 
    Destinations for each Trip
    
    Fields: name, trip
    """
    name = models.CharField(max_length=60)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Cities"

    @staticmethod
    def create_city(name, trip):
        """
        Create new city in specific trip
        """
        city = City(name=name, trip=trip)
        city.save()
        return city



class Booking(models.Model):
    """ 
    Information about bookings for each City 

    Fields: location_name, city, check_in, check_out, cost
    """
    location_name = models.CharField(max_length=128)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    
    def __str__(self):
        return self.location_name



class Flight(models.Model):
    """ 
    Information about flights for each City 

    If it's a round trip, make the cost field 0.

    Fields: airline_name, departure_time, arrival_time, from_city, to_city, cost

    from_city - city from where they take the plane (the cost of the plane ticket will be linked to this city even if it's purchased in advance from the start of the trip)
    """
    
    airline_name = models.CharField(max_length=60)
    departure_date = models.DateField()
    arrival_date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    from_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='from_city')
    to_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='to_city')
    cost = models.DecimalField(decimal_places=2, max_digits=10) # Make this 0 if it's a round trip

    def __str__(self):
        return self.airline_name 


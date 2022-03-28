from rest_framework import serializers
from app_dir.trip.models import UserTrip, Trip, City, Flight, Booking
from app_dir.user.models import User
from app_dir.user.api.serializers import UserSerializer
from app_dir.trip.api.city.serializers import CitySerializer
from app_dir.trip.api.flight.serializers import FlightSerializer
from app_dir.trip.api.booking.serializers import BookingSerializer


class TripSerializer(serializers.ModelSerializer):
    """
    This is the serializer for creating a trip and/or 
    displaying the details of trips in the list of trips
    """
    created_by = UserSerializer(required=False)

    class Meta:
        model = Trip

        fields = [
            'id', 'created_at', 'updated_at','name','created_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        """
        Make sure to validate some of the fields before
        performing various opertions on them.
        """
        
        # Add current user as the owner of the trip unless specified otherwise
        if not attrs.get('created_by',None):
            attrs['created_by_id'] = self.context['request'].user.id

        return attrs

    def create(self, validated_data):
        trip = Trip.objects.create(**validated_data)
        user_trip = UserTrip.objects.create(
            trip=trip,
            user=self.context['request'].user,
            nickname=self.context['request'].user.first_name,
            )
        return trip

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


class TripDetailSerializer(serializers.ModelSerializer):
    """
    This is the serializer for displaying the details of 
    a particular trip. As such, it returns much more details
    than the TripSerializer.
    """

    users = serializers.SerializerMethodField()
    cities = serializers.SerializerMethodField()
    flights = serializers.SerializerMethodField()
    bookings = serializers.SerializerMethodField()
    created_by = UserSerializer()

    class Meta:
        model = Trip

        fields = [
            'id', 'created_at', 'updated_at', 'name',
            'users','cities','bookings','flights','created_by'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_users(self, obj: Trip):
        """
        Return all travelers in this trip by their nickname
        """
        #users = User.objects.filter(id__in=obj.trip_users)
        #return UserSerializer(users,many=True).data
        guests = UserTrip.objects.filter(trip_id=obj.id)
        return list(guests.values_list('nickname',flat=True))

    def get_cities(self, obj: Trip):
        cities = City.objects.filter(id__in=obj.trip_cities)
        return CitySerializer(cities,many=True).data

    def get_flights(self, obj: Trip):
        flights = Flight.objects.filter(id__in=obj.trip_flights)
        return FlightSerializer(flights,many=True).data

    def get_bookings(self, obj: Trip):
        bookings = Booking.objects.filter(id__in=obj.trip_bookings)
        return BookingSerializer(bookings,many=True).data


class UserTripSerializer(serializers.ModelSerializer):
    """
    This is the serializer to add accompanying travelers
    to a trip
    """
    
    class Meta:
        model = UserTrip

        fields = [
            'id', 'trip','nickname'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        user_trip = UserTrip.objects.create(**validated_data)
        return user_trip

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance
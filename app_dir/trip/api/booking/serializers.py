from rest_framework import serializers
from app_dir.trip.models import City, Booking, Trip
from app_dir.user.models import User
from app_dir.user.api.serializers import UserSerializer


class BookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Booking

        fields = [
            'id', 'location_name','city',
            'check_in','check_out','cost'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        booking = Booking.objects.create(**validated_data)
        return booking

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


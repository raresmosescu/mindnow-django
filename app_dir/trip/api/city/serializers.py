from rest_framework import serializers
from app_dir.trip.models import City
from app_dir.user.models import User
from app_dir.user.api.serializers import UserSerializer


class CitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = City

        fields = [
            'id', 'name','trip'
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        city = City.objects.create(**validated_data)
        return city

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance


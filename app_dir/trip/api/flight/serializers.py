from rest_framework import serializers
from app_dir.trip.models import Flight, City
from app_dir.trip.api.city.serializers import CitySerializer

class FlightSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Flight

        fields = [
            'id', 'airline_name','from_city','to_city','cost',
            'departure_time','departure_date','arrival_time','arrival_date',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        flight = Flight.objects.create(**validated_data)
        return flight

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        return instance

    def to_representation(self,instance):
        data = super().to_representation(instance)
        data['from_city'] = CitySerializer(instance.from_city,many=False).data
        data['to_city'] = CitySerializer(instance.to_city,many=False).data
        return data


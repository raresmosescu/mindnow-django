from django.contrib import admin
from app_dir.trip.models import Trip, City, Flight, Booking, UserTrip

# Register your models here.
models_list = [Trip, City, Flight, Booking, UserTrip]
admin.site.register(models_list)
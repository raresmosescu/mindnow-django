from wsgiref.util import request_uri
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app_dir.trip.models import Trip, UserTrip, City, Booking, Flight
from django.contrib.auth.decorators import login_required
from ..forms import TripForm, UserTripForm, BookingForm, FlightForm, CityForm 
import os

@login_required(login_url='/login')
def flight_details(request, trip_id, f_id):
    """
    Detailed info about a specific flight
    """
    trip = Trip.objects.get(id=trip_id)
    flight = Flight.objects.get(id=f_id)
    form = FlightForm(instance=flight)
    return render(request, 'flight_details.html', context={'trip':trip, 'flight': flight, 'form': form})


@login_required(login_url='/login')
def flight_create(request, trip_id):
    """
    Create flight FROM a specific city
    
    The city where the user lives (or starts the trip) should be used for the first flight in the trip
    """
    trip = Trip.objects.get(id=trip_id)
    form = FlightForm()

    # limit the form city selection to current trip cities
    available_cities = City.objects.filter(trip__id=trip.id)
    form.fields["from_city"].queryset =available_cities
    form.fields["to_city"].queryset = available_cities
    
    if request.method == "POST":
        form = FlightForm(data = request.POST)
        
        if form.is_valid():            
            form.save(commit=True)
            return redirect('trip_details', trip_id=trip.id)
    
    return render(request, 'flight_create.html', context={'trip':trip, 'form': form})


@login_required(login_url='/login')
def flight_edit(request, trip_id, f_id):
    """
    Edit existing destination (flight) for specific trip
    """
    trip = Trip.objects.get(id=trip_id)
    flight = Flight.objects.get(id=f_id)
    form = FlightForm(instance = flight)
    if request.method == "POST":
        form = FlightForm(data = request.POST, instance=flight)
        
        if form.is_valid():            
            form.save()
            return redirect('trip_details', trip_id=trip_id)
    return render(request, 'flight_create.html', context={'trip':trip, 'flight':flight, 'form': form}) 


@login_required(login_url='/login')
def flight_delete(request, trip_id, f_id):
    """
    Delete flight
    """
    Flight.objects.get(id=f_id).delete()
    return redirect('trip_details', trip_id=trip_id)
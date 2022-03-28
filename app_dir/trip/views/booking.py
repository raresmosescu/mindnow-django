from django.http import HttpResponse
from django.shortcuts import render, redirect
from app_dir.trip.models import Trip, UserTrip, City, Booking, Flight
from django.contrib.auth.decorators import login_required
from ..forms import TripForm, UserTripForm, BookingForm, FlightForm, CityForm 


@login_required(login_url='/login')
def booking_details(request, trip_id, city_id, b_id):
    """
    Detailed info about a specific booking
    """
    trip = Trip.objects.get(id=trip_id)
    city = City.objects.get(id=city_id)
    booking = Booking.objects.get(id=b_id)
    return render(request, 'booking_details.html', context={'trip':trip, 'city': city, 'booking': booking})


@login_required(login_url='/login')
def booking_create(request, trip_id, city_id):
    """
    Create booking for specific city
    """
    trip = Trip.objects.get(id=trip_id)
    city = City.objects.get(id=city_id)
    form = BookingForm()

    # limit the form city selection to current trip cities
    available_cities = City.objects.filter(trip__id=trip.id)
    form.fields["city"].queryset = available_cities.filter(id=city.id)

    if request.method == "POST":
        form = BookingForm(data = request.POST)
        
        if form.is_valid():            
            form.save(commit=True)
            return redirect('city_details', trip_id=trip.id, city_id=city.id)

    return render(request, 'booking_create.html', context={'trip':trip, 'city': city, 'form': form})

@login_required(login_url='/login')
def flight_create(request, trip_id, city_id):
    """
    Create flight FROM a specific city
    
    The city where the user lives (or starts the trip) should be used for the first flight in the trip
    """
    trip = Trip.objects.get(id=trip_id)
    city = City.objects.get(id=city_id)   
    form = FlightForm()

    # limit the form city selection to current trip cities
    available_cities = City.objects.filter(trip__id=trip.id)
    form.fields["from_city"].queryset = available_cities.filter(id=city.id)
    form.fields["to_city"].queryset = available_cities.exclude(id=city.id)
    
    if request.method == "POST":
        form = FlightForm(data = request.POST)
        
        if form.is_valid():            
            form.save(commit=True)
            return redirect('city_details', trip_id=trip.id, city_id=city.id)
    
    return render(request, 'flight_create.html', context={'trip':trip, 'city': city, 'form': form})


@login_required(login_url='/login')
def booking_edit(request, trip_id, city_id, b_id):
    """
    Edit existing destination (booking) for specific trip
    """
    trip = Trip.objects.get(id=trip_id)
    city = City.objects.get(id=city_id)   
    booking = Booking.objects.get(id=b_id)
    form = BookingForm(instance = booking)
    if request.method == "POST":
        form = BookingForm(data = request.POST, instance=booking)
        
        if form.is_valid():            
            form.save()
            return redirect('trip_details', trip_id=trip_id)
    return render(request, 'booking_create.html', context={'trip':trip, 'city':city, 'booking':booking, 'form': form}) 


@login_required(login_url='/login')
def booking_delete(request, trip_id, city_id, b_id):
    """
    Delete booking
    """
    Booking.objects.get(id=b_id).delete()
    return redirect('city_details', trip_id=trip_id, city_id=city_id) 
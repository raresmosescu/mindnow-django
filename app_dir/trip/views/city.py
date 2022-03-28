from django.shortcuts import render, redirect
from app_dir.trip.models import Trip, City, Booking, Flight
from django.contrib.auth.decorators import login_required
from ..forms import CityForm 

@login_required(login_url='/login')
def city_details(request, trip_id, city_id):
    """
    Detailed information about bookings & flights in a specific city
    """
    trip = Trip.objects.get(id=trip_id)
    city = City.objects.get(id=city_id)
    bookings = Booking.objects.filter(city_id=city_id)
    flights = Flight.objects.filter(from_city_id=city_id)
    # print(bookings, flights)
    return render(request, 'city_details.html', context={'trip':trip, 'city': city, 'bookings': bookings, 'flights': flights})

@login_required(login_url='/login')
def city_create(request, trip_id):
    """
    Create destination (city) for specific trip
    """
    trip = Trip.objects.get(id=trip_id)
    form = CityForm()
    if request.method == "POST":
        form = CityForm(data = request.POST)
        
        if form.is_valid():            
            # redirect to the redirect url (the URL parameter "next") or to home page
            city_name = form.cleaned_data['name']
            city = City.create_city(city_name, trip)
            return redirect('trip_details', trip_id=trip_id)
    return render(request, 'city_create.html', context={'trip':trip, 'form': form})

@login_required(login_url='/login')
def city_edit(request, trip_id, city_id):
    """
    Edit existing destination (city) for specific trip
    """
    trip = Trip.objects.get(id=trip_id)
    city = City.objects.get(id=city_id)
    form = CityForm(instance = city)
    if request.method == "POST":
        form = CityForm(data = request.POST)
        
        if form.is_valid():            
            city_name = form.cleaned_data['name']
            city.name = city_name
            city.save()
            return redirect('trip_details', trip_id=trip_id)
    return render(request, 'city_create.html', context={'trip':trip, 'city':city, 'form': form}) 


@login_required(login_url='/login')
def city_delete(request, trip_id, city_id):
    """
    Delete city
    """
    City.objects.get(id=city_id).delete()
    return redirect('trip_details', trip_id=trip_id)
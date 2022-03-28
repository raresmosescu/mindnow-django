from decimal import Decimal
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app_dir.trip.models import Trip, UserTrip, City, Booking, Flight
from django.contrib.auth.decorators import login_required
from ..forms import TripForm, UserTripForm, BookingForm, FlightForm, CityForm 
from django.db.models import Avg, Count, Min, Sum

@login_required(login_url='/login')
def trips(request):
    """
    Renders list of all trips the current user is part of
    """
    user_trips = UserTrip.user_trips(request.user.id)
    return render(request, 'trips.html', context={'usertrips': user_trips})

@login_required(login_url='/login')
def trip_details(request, trip_id):
    """
    Trip overview - costs, schedule, cities
    """
    trip = Trip.objects.get(id=trip_id)

    members = UserTrip.objects.filter(trip = trip)

    cities = City.objects.filter(trip_id=trip_id)

    # cities based on the plane schedule (more useful to show 
    # them this way because flights link destinations together)
    flights = Flight.objects.filter(from_city__trip__id=trip.id).order_by('departure_date', 'departure_time')
    
    if flights:
        flight_costs = flights.aggregate(total_costs=Sum('cost'))['total_costs']
    else: 
        flight_costs = 0


    bookings = Booking.objects.filter(city__in = cities)
    
    if bookings:
        booking_costs = bookings.aggregate(total_costs=Sum('cost'))['total_costs']
    else: 
        booking_costs = 0

    total_costs = Decimal(booking_costs) + Decimal(flight_costs)

    context = {
        'trip': trip, 
        'members': members,
        'cities': cities, 
        'flights': flights, 
        'flight_costs': flight_costs, 
        'bookings': bookings,
        'booking_costs': booking_costs,
        'total_costs': total_costs
    }

    return render(request, 'trip_details.html', context=context)


@login_required(login_url='/login')
def trip_create(request):
    """
    Create trip
    """
    form = TripForm()
    if request.method == "POST":
        form = TripForm(data = request.POST)
        
        if form.is_valid():            
            trip_name = form.cleaned_data['name']
            trip = Trip.create_trip(trip_name, request.user)
            return redirect('/')
    
    return render(request, 'trip_create.html', context={'form': form}) 


@login_required(login_url='/login')
def trip_edit(request, trip_id):
    """
    Edit trip
    """
    trip = Trip.objects.get(id=trip_id)
    form = TripForm(instance = trip)
    if request.method == "POST":
        form = TripForm(data = request.POST)
        
        if form.is_valid():            
            trip_name = form.cleaned_data['name']
            trip = Trip.create_trip(trip_name, request.user)
            return redirect('/')
    
    return render(request, 'trip_create.html', context={'form': form}) 


@login_required(login_url='/login')
def trip_delete(request, trip_id):
    """
    Delete trip
    """
    Trip.objects.get(id=trip_id).delete()
    return redirect('/')
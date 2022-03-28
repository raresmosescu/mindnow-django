from django.shortcuts import render, redirect
from app_dir.trip.models import Trip, City, Booking, Flight, UserTrip
from django.contrib.auth.decorators import login_required
from ..forms import UserTripForm 

@login_required(login_url='/login')
def member_details(request, trip_id, member_id):
    """
    Detailed information about a specific member
    """
    trip = Trip.objects.get(id=trip_id)
    member = UserTrip.objects.get(id=member_id)
    return render(request, 'member_details.html', context={'trip':trip, 'member': member})

@login_required(login_url='/login')
def member_create(request, trip_id):
    """
    Create trip member
    """
    trip = Trip.objects.get(id=trip_id)
    form = UserTripForm()

    if request.method == "POST":
        form = UserTripForm(data = request.POST)
        
        if form.is_valid():            
            # redirect to the redirect url (the URL parameter "next") or to home page
            username, nickname = form.cleaned_data['username'], form.cleaned_data['nickname']
            member = UserTrip.create_member(trip, username, nickname)
            return redirect('trip_details', trip_id=trip_id)
    return render(request, 'member_create.html', context={'trip':trip, 'form': form})

@login_required(login_url='/login')
def member_edit(request, trip_id, member_id):
    """
    Edit member(UserTrip)
    """
    trip = Trip.objects.get(id=trip_id)
    member = UserTrip.objects.get(id=member_id)
    form = UserTripForm(instance = member)
    # form.data['username'] = member.user.username

    if request.method == "POST":
        form = UserTripForm(data = request.POST)
        
        if form.is_valid():            
            username, nickname = form.cleaned_data['username'], form.cleaned_data['nickname']

            member.username = username
            member.nickname = nickname

            member.save()
            return redirect('trip_details', trip_id=trip_id)
    return render(request, 'member_create.html', context={'trip':trip, 'member':member, 'form': form}) 


@login_required(login_url='/login')
def member_delete(request, trip_id, member_id):
    """
    Delete member
    """
    UserTrip.objects.get(id=member_id).delete()
    return redirect('trip_details', trip_id=trip_id)
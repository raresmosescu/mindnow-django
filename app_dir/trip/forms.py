import re
from django import forms
from django.contrib.auth.models import User
from .models import Trip, UserTrip, City, Flight, Booking
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput


class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ('name',)


class UserTripForm(forms.ModelForm):
    username = forms.CharField(max_length=60, label='Username (optional - can edit trip)', required=False)

    class Meta:
        model = UserTrip
        fields = ('username', 'nickname')

    def clean_username(self):
        username = self.cleaned_data['username']
        if username and not User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" doesn\'t exist.' % username)
        return username


class CityForm(forms.ModelForm):

    class Meta:
        model = City
        fields = ('name',)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

        widgets = {
            'check_in': DatePickerInput,
            'check_out': DatePickerInput,
        }


class FlightForm(forms.ModelForm):

    class Meta:
        model = Flight
        fields = '__all__'

        widgets = {
            'departure_date': DatePickerInput,
            'arrival_date': DatePickerInput,
            'departure_time': TimePickerInput,
            'arrival_time': TimePickerInput,
        }

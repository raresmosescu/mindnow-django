from django.urls import path
from rest_framework import routers
from .trip.views import TripView
from .city.views import CityView
from .booking.views import BookingView
from .flight.views import FlightView

app_name = 'trips'

router = routers.DefaultRouter()
router.include_root_view = False
router.register('cities', CityView, basename='cities')
router.register('bookings', BookingView, basename='bookings')
router.register('flights', FlightView, basename='flights')
router.register('', TripView, basename='trips')

urlpatterns = router.urls + [
    #path('', ModuleListAPIView.as_view(), name='list'),
]

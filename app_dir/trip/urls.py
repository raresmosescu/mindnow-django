from django.urls import path
from .views.trip import *
from .views.city import *
from .views.booking import *
from .views.flight import *
from .views.member import *

urlpatterns = [

    # Trip paths
    path('', trips, name='index'),

    path('<int:trip_id>/', trip_details, name='trip_details'),

    path('create/', trip_create, name='trip_create'),

    path('<int:trip_id>/edit/', trip_edit, name='trip_edit'),

    path('<int:trip_id>/delete/', trip_delete, name='trip_delete'),



    # Member paths (UserTrip model)

    path('<int:trip_id>/member/<int:member_id>/', member_details, name='member_details'),

    path('<int:trip_id>/member/create/', member_create, name='member_create'),

    path('<int:trip_id>/member/<int:member_id>/edit/', member_edit, name='member_edit'),

    path('<int:trip_id>/member/<int:member_id>/delete/', member_delete, name='member_delete'),



    # City paths
    path('<int:trip_id>/city/<int:city_id>/', city_details, name='city_details'),

    path('<int:trip_id>/city/create/', city_create, name='city_create'),

    path('<int:trip_id>/city/<int:city_id>/edit/', city_edit, name='city_edit'),

    path('<int:trip_id>/city/<int:city_id>/delete/', city_delete, name='city_delete'),



    # Booking paths
    path('<int:trip_id>/city/<int:city_id>/b/<int:b_id>/', booking_details, name='booking_details'),

    path('<int:trip_id>/city/<int:city_id>/b/create/', booking_create, name='booking_create'),

    path('<int:trip_id>/city/<int:city_id>/b/<int:b_id>/edit/', booking_edit, name='booking_edit'),

    path('<int:trip_id>/city/<int:city_id>/b/<int:b_id>/delete/', booking_delete, name='booking_delete'),



    # Flight paths
    path('<int:trip_id>/f/<int:f_id>/', flight_details, name='flight_details'),

    path('<int:trip_id>/f/create/', flight_create, name='flight_create'),

    path('<int:trip_id>/f/<int:f_id>/edit/', flight_edit, name='flight_edit'),

    path('<int:trip_id>/f/<int:f_id>/delete/', flight_delete, name='flight_delete'),
]

from rest_framework import viewsets, exceptions, status
from rest_framework.decorators import action
from rest_framework.generics import (
  ListAPIView, CreateAPIView,
  RetrieveUpdateAPIView,
  RetrieveAPIView,
  DestroyAPIView
)
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from app_dir.trip.models import UserTrip, Trip
from app_dir.core.pagination import PostLimitOffsetPagination
from .permissions import TripOwnerPermission
from .serializers import TripSerializer, TripDetailSerializer, UserTripSerializer



class TripView(viewsets.ModelViewSet):
    # We can have different serializers with varying degree of details for different actions
    serializer_classes = {
        'list': TripSerializer,
        'retrieve': TripDetailSerializer 
    }
    permission_classes = [IsAuthenticated, TripOwnerPermission]
    pagination_class = PostLimitOffsetPagination
    http_method_names = ['get', 'post', 'put']

    def get_serializer_class(self):
        """
        Decide which serializer to use
        """
        return self.serializer_classes['list'] if self.action != 'retrieve' else self.serializer_classes['retrieve'] 


    def get_queryset(self):
        
        page_size = self.request.GET.get('page_size',10)
        pagination.PageNumberPagination.page_size = page_size

        if self.request.user.is_staff:
            return Trip.objects.all()
        else:
            user_trips = UserTrip.objects.filter(user_id=self.request.user.id)
            return Trip.objects.filter(id__in=user_trips.values_list('trip_id',flat=True)).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        """
        Creating a trip from the specified data, namely:
        - Name
        - Request user
        """

        serializer = self.get_serializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)

        trip = serializer.save()

        return Response(data={'message':'Trip is successfully created.','id':trip.id}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """
        Get the list of trips for the specified user
        """

        paginated_query = self.paginate_queryset(self.get_queryset())
        paginated_data = self.get_serializer(paginated_query, many=True).data
        
        return self.get_paginated_response(paginated_data)

    def retrieve(self, request, pk=None):
        """
        Retreive the details of a particular trip
        """
        try:
            trip = Trip.objects.get(id=pk)
        except Trip.DoesNotExist:
            raise exceptions.NotFound

        trip_data = self.get_serializer(trip).data

        
        return Response(data=trip_data)


    def update(self, request, *args, **kwargs):
        """
        Update the details of a particular trip
        """
        try:
            trip = Trip.objects.get(id=kwargs.pop('pk'))
        except Trip.DoesNotExist:
            raise exceptions.NotFound

        # validate and update data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=trip, validated_data=serializer.validated_data)
        
        return Response(data={'message': 'item successfully updated'})

    @action(detail=True, methods=['post'])
    def add_trip_guest(self, request, pk=None):
        """
        Add multiple accompanying guests/travelers to the trip
        by specifying the trip ID and their nicknames
        """
        
        serializer = UserTripSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)

        user_trip = serializer.save()

        return Response(data={'message':'Trip is successfully created.','id':user_trip.id}, status=status.HTTP_201_CREATED)
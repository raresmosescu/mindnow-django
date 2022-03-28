from rest_framework import viewsets, exceptions, status
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from app_dir.trip.models import UserTrip, Trip, City
from app_dir.core.pagination import PostLimitOffsetPagination
from .permissions import CityOwnerPermission
from .serializers import CitySerializer



class CityView(viewsets.ModelViewSet):
    # We can have different serializers with varying degree of details for different actions
    serializer_classes = {
        'list': CitySerializer,
        'retrieve': CitySerializer 
    }
    permission_classes = [IsAuthenticated] #CityOwnerPermission
    pagination_class = PostLimitOffsetPagination
    http_method_names = ['get', 'post', 'put','patch']

    def get_serializer_class(self):
        """
        Decide which serializer to use
        """
        return self.serializer_classes['list'] if self.action == 'list' else self.serializer_classes['retrieve'] 


    def get_queryset(self):
        
        page_size = self.request.GET.get('page_size',10)
        pagination.PageNumberPagination.page_size = page_size

        if self.request.user.is_staff:
            return City.objects.all()
        else:
            user_trips = UserTrip.objects.filter(user_id=self.request.user.id)
            return City.objects.filter(trip_id__in=user_trips.values_list('trip_id',flat=True))

    def create(self, request, *args, **kwargs):
        """
        Creating a trip from the specified data, namely:
        - Name
        - Request user
        """

        serializer = self.get_serializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)

        city = serializer.save()

        return Response(data={'message':'City is successfully created.','id':city.id}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        """
        Get the list of trips for the specified user
        """

        paginated_query = self.paginate_queryset(self.get_queryset())
        paginated_data = self.get_serializer(paginated_query, many=True).data
        
        return self.get_paginated_response(paginated_data)

    def retrieve(self, request, pk=None):
        try:
            city = City.objects.get(id=pk)
        except City.DoesNotExist:
            raise exceptions.NotFound
        
        return Response(data=self.get_serializer(city).data)


    def patch(self, request, *args, **kwargs):
        try:
            city = City.objects.get(id=kwargs.pop('pk'))
        except City.DoesNotExist:
            raise exceptions.NotFound

        # validate and update data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=city, validated_data=serializer.validated_data)
        
        return Response(data={'message': 'item successfully updated'})

from rest_framework.generics import (
    ListAPIView, CreateAPIView, RetrieveUpdateAPIView,
    RetrieveAPIView, DestroyAPIView
)
from django.db.models import Q
from rest_framework import pagination, exceptions
from rest_framework.permissions import (IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny)

from .serializers import UserSerializer, User
from ...core.pagination import PostLimitOffsetPagination


class UserListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = PostLimitOffsetPagination

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            queryset_list = User.objects.all()
        else:
            queryset_list = User.objects.filter(id=self.request.user.id)

        page_size = 'page_size'
        if self.request.GET.get(page_size):
            pagination.PageNumberPagination.page_size = self.request.GET.get(page_size)
        else:
            pagination.PageNumberPagination.page_size = 10
        
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(email__icontains=query) |
                Q(username__icontains=query)
            )

        return queryset_list.order_by('-id')


class UserCreateAPIView(CreateAPIView):
    """
    This API is used to signup users. Three fields are required:
    - Username
    - Password
    - Email
    """

    serializer_class = UserSerializer
    permission_classes = [AllowAny]     # TODO: We should add rate limit, captcha, etc. to reduce fake users.
    queryset = User.objects.none()


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer


class UpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        """
        Update user fields. As a measure of security,
        make sure the person who is updating the user is either
        - A staff member
        - Or the same person who has this user id
        """
        if not self.request.user.is_staff and self.request.user.id != self.kwargs['pk']:
            raise exceptions.PermissionDenied

        serializer.save(user=self.request.user)
        

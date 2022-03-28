from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from app_dir.trip.views.trip import trips
from app_dir.user.views import login_view, register_view, logout_view
from app_dir.views import api_docs

urlpatterns = [
    path('', trips),
    path('docs/', api_docs, name='api_docs'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path('trip/', include(('app_dir.trip.urls'))),
    # path('api-auth/', include('rest_framework.urls', namespace='rest')),
    # path('api-token-auth', obtain_jwt_token),
    # path('user/', include(('app_dir.user.urls', 'user'), namespace='user')),
    path('api/user/', include(('app_dir.user.api.urls', 'user_api'), namespace='user_api')),
    path('api/trips/', include(('app_dir.trip.api.urls', 'trips_api'), namespace='trips_api'))
]


from rest_framework import permissions

class BookingOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        return request.method in permissions.SAFE_METHODS + ('POST', 'PATCH')

    def has_object_permission(self, request, view, obj):
        # for the user that this object belongs to,
        # he/she should be able to view or delete it
    
        return request.user.id in obj.city.trip.trip_users or request.user.is_staff

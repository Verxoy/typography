from rest_framework import permissions



from .roles import is_site_administrator, is_site_staff





class IsSiteStaff(permissions.BasePermission):

    def has_permission(self, request, view):

        u = request.user

        return bool(u and u.is_authenticated and is_site_staff(u))





class IsSiteAdministrator(permissions.BasePermission):

    def has_permission(self, request, view):

        u = request.user

        return bool(u and u.is_authenticated and is_site_administrator(u))



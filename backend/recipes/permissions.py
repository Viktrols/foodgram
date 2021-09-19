from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and (
                request.user.is_superuser or obj.author == request.user
                or request.method == 'POST'):
            return True
        return request.method in permissions.SAFE_METHODS


# class AdminOrAuthorOrReadOnly(permissions.BasePermission):

#     def has_permission(self, request, view):
#         if request.method == 'POST':
#             return request.user.is_authenticated
#         return True

#     def has_object_permission(self, request, view, obj):
#         if (request.method in ['PUT', 'PATCH', 'DELETE']
#                 and not request.user.is_anonymous):
#             return (
#                     request.user == obj.author
#                     or request.user.is_superuser
#                     or request.user.is_admin()
#             )
#         return request.method in permissions.SAFE_METHODS
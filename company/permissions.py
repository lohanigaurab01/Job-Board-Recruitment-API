from rest_framework import permissions

class IsUserRecruiter(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role =='recruiter' 
    
    # def has_object_permission(self, request, view, obj):

    #     if request.method in permissions.SAFE_METHODS:
    #         return True

    #     return obj.owners.profile.role =='recruiter'

class IsUserOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role =='recruiter'
    
    
    def has_object_permission(self, request, view, obj):
        return obj.owners == request.user

    
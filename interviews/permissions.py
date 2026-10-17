from rest_framework.permissions import BasePermission


class IsRecuriter(BasePermission):
    message = "only the recuriter"
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role =='recruiter'

 
class IsRecuriterOrOwner(BasePermission):
    message = "only the recuiter can perform action to their application"
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role == 'recruiter'

    def has_object_permission(self, request, view, obj):
        return obj.application.job_posting.company == request.user.companys
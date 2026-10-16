from rest_framework import permissions

class IsCandidate(permissions.BasePermission):
    message = "Only candidates can apply for jobs."

    def has_permission(self, request, view):
    
        return request.user.is_authenticated and  request.user.profile.role=='candidate'


class IsRecruiterOrOwner(permissions.BasePermission):
    message = "only recuriter can change their own company job details"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.role =='recruiter'
    
    def has_object_permission(self, request, view, obj):
        return obj.job_posting.company == request.user.companys
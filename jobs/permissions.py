from rest_framework import permissions
from company.permissions import IsUserRecruiter,IsUserOwner

class IsRecuriter(IsUserRecruiter):
    message ="only recuriter"
    def has_permission(self, request, view):
        return super().has_permission(request, view)
    
    def has_object_permission(self, request, view, obj):
        return super().has_object_permission(request, view, obj)


class IsRecuritorOwner(IsUserOwner):
    message = "only recuritor owner "
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return obj.company.owners == request.user

from rest_framework import generics
from .models import Company
from .permissions import IsUserRecruiter,IsUserOwner
from .serializers import CompanySerializer
from rest_framework import permissions

class CompanyCreate(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method =="POST":
            permission_classes= [IsUserRecruiter]
        else:
            permission_classes =[permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        return serializer.save(owners= self.request.user)


class CompanyRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field= 'id'

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            permission_classes= [IsUserOwner]
        else:
            permission_classes =[permissions.AllowAny]

        return [permission() for permission in permission_classes]






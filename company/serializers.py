from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'description', 'website', 'location',)

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.method == 'POST':
            if Company.objects.filter(owners=request.user).exists():
                raise serializers.ValidationError(
                    {"detail": "You have already created a company. Each recruiter can only own one."}
                )
        return attrs

    
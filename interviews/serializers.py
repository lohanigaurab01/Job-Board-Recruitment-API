from rest_framework import serializers
from .models import Interview
from django.utils import timezone


class InterviewScheduleSerializer(serializers.ModelSerializer):
    scheduled_at = serializers.DateTimeField()
    class Meta:
        model = Interview
        fields = ('application', 'scheduled_at', 'interviewer', 'mode', 'notes', 'status')
        read_only_fields = ('application','interviewer','status')

    def validate(self, attrs):
        application = self.context.get('application')
        print(application)

        application_status = application.status

        if application_status!="interview":
            raise serializers.ValidationError({"status": "the application status must be interview "})

        status = attrs.get('status')


        if status in ['cancelled' , 'completed']:
            raise serializers.ValidationError({"status": "the status has been finalized"})

        time = attrs.get('scheduled_at')
        if time <=timezone.now():
            raise serializers.ValidationError({
                "scheduled_at": "time is greather than current time"
            })
        if application.interviews.exclude(status__in=['completed', 'cancelled']).exists():
            raise serializers.ValidationError({"status":
            "The previous interview must be completed before scheduling a new one."
        })


        return attrs


    def create(self, validated_data):
        try:
            interview = Interview.objects.create(**validated_data)
            return validated_data


        except Exception as e:
            raise serializers.ValidationError({"error": e})


class InterviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ('status', )

    def validate_status(self, value):
        if value in ['cancelled' , 'completed']:
            raise serializers.ValidationError( "the status has been finalized")

        status = self.instance.status
        if status in ['cancelled' , 'completed']:
            if value == 'scheduled':
                raise serializers.ValidationError("cannot be rolled back")

    def update(self, instance, validated_data):
        try:
            instance = super().update(instance, validated_data)
            return instance

        except Exception as e:
            raise serializers.ValidationError({"errors": e})
    
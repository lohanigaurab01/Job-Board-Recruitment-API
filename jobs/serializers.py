from rest_framework import serializers
from .models import JobPosting,ScreeningQuestion
from django.db import transaction
from django.contrib.auth.models import User

class ScreeningQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScreeningQuestion
        fields = ('id','question_text')


class JobSerilaizer(serializers.ModelSerializer):
    questions = ScreeningQuestionSerializer(many= True, required = False)

    class Meta:
        model = JobPosting
        fields = '__all__'
        read_only_fields =('company','created_at', )

    def validate(self, attrs):
        salary_min = attrs.get('salary_min')
        salary_max = attrs.get('salary_max')

        if salary_min and salary_max and salary_min > salary_max:
            raise serializers.ValidationError(
                {"salary_min": "Minimum salary cannot be greater than maximum salary."}
            )

        current_log = self.context.get('request')
        if current_log.user.companys is None:
                raise serializers.ValidationError({
                    "company_error": "The recruiter must be associated with a company before creating a job posting."
                })

        return attrs


    def create(self, validated_data):
        try:
            with transaction.atomic():
                question = validated_data.pop('questions')
                job =JobPosting.objects.create(**validated_data)
                if question:
                    for quest in question:
                        ScreeningQuestion.objects.create(job_posting=job, **quest)
                    
                return job


        except Exception as e:
            raise serializers.ValidationError({"errors":f'{e}'})


    def update(self, instance, validated_data):
        try:
            with transaction.atomic():
                questions = validated_data.pop('questions', None)
                instance = super().update(instance, validated_data)
                if questions:
                    for quest in questions:
                        ScreeningQuestion.objects.create(job_posting= instance, question_text= quest)
                return instance

        except Exception as e:
            raise serializers.ValidationError({"errors": f'{e}'})


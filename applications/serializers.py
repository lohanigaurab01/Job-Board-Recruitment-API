from rest_framework import serializers
from .models import Application, ApplicationAnswer
class ApplicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Application
        fields = ['id','job_posting','status','applied_at']
        read_only_fields = ('id', 'job_posting', 'applied_at')

    def validate_status(self, data):
        curr_status = self.instance.status
        request = self.context.get('request')

        if curr_status in ['hired', 'rejected', 'withdrawn']:
            raise serializers.ValidationError("the status has been finalized and cannot be changed")

        if data in ['interview'] and request.user.profile.role=='recruiter':
            if curr_status!="applied":
                raise serializers.ValidationError("only the applied status can get in interview")

        if data in ['offer'] and request.user.profile.role=='recruiter':
            if curr_status!="interview" :
                raise serializers.ValidationError("only the interview status can get offer")

        if data in ['hired'] and request.user.profile.role=='recruiter':
            if curr_status !="offer":
                raise serializers.ValidationError("only the offer status can get offer")

        if data in ['withdrawn'] and request.user.profile.role!='candidate':
            raise serializers.ValidationError("only the candidate can withdrawn ")

        if curr_status in ['interview', 'offer']:
            if data in ['applied']:
                raise serializers.ValidationError("the status cannot get backwards")

        if data in ['interview', 'offer', 'hired', 'rejected'] and request.user.profile.role =='candidate':
            raise serializers.ValidationError("the status can only change by recruiter")

        if curr_status == data:
            raise serializers.ValidationError("the status cannot be changed as previous data")
            
        return data



    def update(self, instance, validated_data):
        try:
            request = self.context.get('request')
            new_status = validated_data.get('status')
            if request.user.profile.role == 'candidate':  
                if new_status =="withdrawn":
                    instance = super().update(instance, validated_data)

            if request.user.profile.role=='recruiter':
                if new_status in ['interview', 'offer', 'hired', 'rejected']:
                    instance = super().update(instance, validated_data)

            return instance

    
        except Exception as e:
            raise serializers.ValidationError({"message":e})
            
    
class ApplicationPostSerializer(serializers.ModelSerializer):
    class ApplicationAnswerSerializer(serializers.ModelSerializer):
        class Meta:
            model = ApplicationAnswer
            fields = ('question', 'answer_text')
        
    answers = ApplicationAnswerSerializer(many = True)

    class Meta:
        model= Application
        fields = ('id','job_posting', 'candidate', 'resume', 'cover_letter', 'status', 'applied_at', 'updated_at', 'answers')
        read_only_fields = ('job_posting','candidate', 'status', 'resume')


    def validate(self, attr):
        jobs = self.context.get('job_posting')
        request= self.context.get('request')
        user = request.user

        

        existing_application = Application.objects.filter(job_posting= jobs, candidate= user)
   
        if existing_application.exists():
            raise serializers.ValidationError({"error":"Application already exists"})
        

        answer_data = attr.get('answers', [])
        if answer_data and jobs:
            qn_valid = set(jobs.questions.values_list('id',flat= True))
            for item in answer_data:
                qn = item.get('question')
                if qn.id not in qn_valid:
                    raise serializers.ValidationError({"answers": f"Question ID  does not belong to job posting {jobs.id}."})

        return attr

    def create(self, validated_data):
        try:
            answers = validated_data.pop('answers')
            application = Application.objects.create(**validated_data)
            if answers:
                for ans in answers:
                    applicationanswer = ApplicationAnswer.objects.create(application= application, question= ans["question"], answer_text = ans["answer_text"])
            return application

        except Exception as e:
            raise serializers.ValidationError({"error": e})


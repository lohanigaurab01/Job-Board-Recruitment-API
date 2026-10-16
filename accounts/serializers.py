from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth import authenticate

class UserRegisterSerializer(serializers.ModelSerializer):

    class ProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ('role',)
        
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)
    confirm_password = serializers.CharField(write_only = True)
    profile = ProfileSerializer()


    class Meta:
        model = User
        fields =('first_name', 'last_name', 'username', 'email','password', 'confirm_password','profile')

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if User.objects.filter(username= username).exists():
            raise serializers.ValidationError({"username":"username already exists"})

        if User.objects.filter(email = email).exists():
            raise serializers.ValidationError({"email":"email already exists"})
        
        try:
            temp_user = User(first_name=first_name, last_name=last_name, username=username)
            validate_password(password, temp_user)

        except DjangoValidationError as e:
            raise serializers.ValidationError(e)

        if password !=confirm_password:
            raise serializers.ValidationError("both password should match")

        return data


    def create(self, validated_data):
        profile = validated_data.pop('profile')
        validated_data.pop('confirm_password', None)

        user = User.objects.create_user(**validated_data)

        if profile:
            Profile.objects.create(user= user, **profile)

        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username = data.get('username'), password = data.get('password'))
        if user is None:
            raise serializers.ValidationError({"errors":"username or password is incorrect"})

        data["user"]=user
        return data

    
    

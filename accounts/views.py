from django.shortcuts import render
from rest_framework import generics,status
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer,UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny,IsAuthenticated

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

class LoginView(APIView):
    permission_classes=[AllowAny]
    authentication_classes=[]

    def post(self, request):
        serializer = UserLoginSerializer(data =request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user:
            refresh =RefreshToken.for_user(user)
            response = Response({
                "message":"you have been sucessfully logged in",
            }, status=status.HTTP_200_OK)

            response.set_cookie(
            key='access_token',
            value=str(refresh.access_token),
            httponly=True,
            secure=False,
            samesite='Lax'
            )

            response.set_cookie(
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite='Lax'
            )
            return response

class UserLogout(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        refreshtoken = request.COOKIES.get('refresh_token')
        try:
            token = RefreshToken(refreshtoken)
            token.blacklist()
        except Exception as e:
            return Response({"error":"token in validated"})
        
        response = Response({"message":"Sucessfully logged out"}, status=status.HTTP_200_OK)
        response.delete_cookie('access_token', samesite='Lax')
        response.delete_cookie('refresh_token', samesite='Lax')
        return response
        


    
class MyRefreshView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request):
        old_token = request.COOKIES.get('refresh_token')

        
        if old_token:
            try:
                token = RefreshToken(old_token)
                user_id = token['user_id']
                user = User(id= user_id)
                refresh_token = RefreshToken.for_user(user)


                response = Response({
                    "message": "refresh generated",
                }, status=status.HTTP_200_OK)
                
                response.set_cookie(
                    key='access_token',
                    value=str(refresh_token.access_token), 
                    httponly=True,
                    secure=False,
                    samesite='Lax'
                )
                
                response.set_cookie(
                    key='refresh_token',
                    value=str(refresh_token),
                    httponly=True,
                    secure=False,            
                    samesite='Lax'
                )
                token.blacklist()
                return response
                
            except Exception as e:
                response = Response({"error": "Invalid or expired refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
                response.delete_cookie('access_token',samesite='Lax')
                response.delete_cookie('refresh_token',samesite='Lax')
                return response

        
        return Response({"error": "Refresh token missing"}, status=status.HTTP_400_BAD_REQUEST)



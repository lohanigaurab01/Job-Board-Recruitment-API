from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class JWTTokenAuthenticate(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if token is None:
            return None
        try:
            validated_token = self.get_validated_token(token)
            user = self.get_user(validated_token)
            return user, validated_token

        except AuthenticationFailed as e:
            raise AuthenticationFailed({"error":f"{e}"})

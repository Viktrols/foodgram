from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TokenSerializer

User = get_user_model()


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created= Token.objects.get_or_create(user=user)
        return Response(
            {'auth_token': str(token)},
            status=status.HTTP_200_OK
        )


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, status, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Follow
from .serializers import TokenSerializer, FollowSerializer, ShowFollowSerializer, UserSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from foodgram.pagination import CustomPageNumberPaginator


User = get_user_model()


class UsersListApiView(ListModelMixin, GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPageNumberPaginator
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


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


class FollowApiView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def get(self, request, id):
        data = {'user': request.user.id, 'following':id}
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        data = {'user': request.user.id, 'following': id}
        user = request.user
        following = get_object_or_404(Follow, following__id=id)
        serializer = FollowSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        Follow.objects.get(user=user, following=following).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListFollowViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ShowFollowSerializer
    pagination_class = CustomPageNumberPaginator

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)

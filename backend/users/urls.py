from django.urls import path, include
from users.views import (FollowApiView, Login, Logout,
                         ListFollowViewSet, UsersListApiView)

urlpatterns = [
    path('users/<int:id>/subscribe/', FollowApiView.as_view(),
         name='subscribe'),
    path('users/subscriptions/', ListFollowViewSet.as_view(),
         name='subscription'),
    path('users/', UsersListApiView.as_view(), name='user_list'),
    path('', include('djoser.urls')),
    path('auth/token/login/', Login.as_view()),
    path('auth/token/logout/', Logout.as_view()),
]

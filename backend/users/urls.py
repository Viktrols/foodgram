from django.urls import path, include
from users.views import Login, Logout

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/token/login/', Login.as_view()),
    path('auth/token/logout/', Logout.as_view())
]
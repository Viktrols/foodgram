from django.contrib import admin
from django.urls import path, include


api_patterns = [
    path('', include('users.urls')),
    path('', include('recipes.urls')),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_patterns)),
]

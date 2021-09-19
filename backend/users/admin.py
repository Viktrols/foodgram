from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import Follow


User = get_user_model()


class UserAdmin(DjangoUserAdmin):
    list_filter = ['email', 'username']


admin.site.register(User, DjangoUserAdmin)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'following')

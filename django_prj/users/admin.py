from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile


@admin.register(Profile)
class UserAdmin(admin.ModelAdmin):
    list_display = ['user']

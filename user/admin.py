from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ("username", "first_name", "last_name", "email", "role",)
    search_fields = ("first_name", "last_name", "username",)
    list_filter = ("role",)

from django.contrib import admin
from django.contrib.auth import get_user_model
from application import models


@admin.register(get_user_model())
class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'is_active', 'is_staff',)
    search_fields = ('first_name',)
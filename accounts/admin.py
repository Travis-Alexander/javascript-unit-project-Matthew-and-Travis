from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'wins', 'losses']
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('wins', 'losses')}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('wins', 'losses')}),)

admin.site.register(CustomUser, CustomUserAdmin)

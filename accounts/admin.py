from django.contrib import admin
from rest_framework_simplejwt.token_blacklist import models
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin
from .models import *
from django.contrib.auth.admin import UserAdmin
from accounts.forms import *
from rest_framework_simplejwt import token_blacklist
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):    
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email','username']



class NewOutstandingTokenAdmin(OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True
class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
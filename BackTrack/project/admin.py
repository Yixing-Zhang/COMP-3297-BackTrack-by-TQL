from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import BackTrackUserCreationForm, BackTrackUserChangeForm


class BackTrackUserAdmin(UserAdmin):
    add_form = BackTrackUserCreationForm
    form = BackTrackUserChangeForm
    model = BackTrackUser
    list_display = ['username', 'email', 'is_staff', ]
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('project',)}),)


# Register your models here.
admin.site.register(Project)
admin.site.register(BackTrackUser, BackTrackUserAdmin)

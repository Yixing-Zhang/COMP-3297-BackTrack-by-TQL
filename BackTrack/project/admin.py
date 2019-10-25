from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Owner)
admin.site.register(Manager)
admin.site.register(Project)
admin.site.register(Developer)
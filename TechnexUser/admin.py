from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin
# from django.contrib.admin.options import ModelAdmin
from TechnexUser.models import *

admin.site.register(TechProfile)
admin.site.register(College)

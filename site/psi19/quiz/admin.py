from django.contrib import admin

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from quiz.models import User
# Register your models here.

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Question)
admin.site.register(Category)

admin.site.register(Game)
admin.site.register(Friendship)

admin.site.register(User)


from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Question)
admin.site.register(Category)

admin.site.register(Game)
admin.site.register(Friendship)
from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Question)
admin.site.register(Category_movies)
admin.site.register(Category_geography)
admin.site.register(Category_music)
admin.site.register(Category_history)
admin.site.register(Category_sports)

admin.site.register(Game)
admin.site.register(Senior_user)
admin.site.register(Friendship)
admin.site.register(User_profile)
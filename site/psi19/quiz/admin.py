from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from quiz.models import User
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *

# Register your models here.

#fixes user being created from admin page, without password hashing
class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm

    fieldsets = (
        ('Login data', {'fields': ('username','email', 'password')}),
        ('Personal data', {'fields':('first_name', 'last_name', 'age')}),
        ('Account data', {'fields':('level', 'picture', 'ranking')})
        )
    add_fieldsets = (
        ('Login data', {'fields': ('username','email', 'password')}),
        ('Personal data', {'fields':('first_name', 'last_name', 'age')}),
        )

    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)

admin.site.register(Question)
admin.site.register(Category)

admin.site.register(Game)
admin.site.register(Friendship)





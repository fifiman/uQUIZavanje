from django import forms
from quiz.models import *
from django.contrib.auth.forms import *
from django.contrib.auth import get_user_model

User = get_user_model()

class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['question', 'answer_one','answer_two','answer_three','answer_four','correct','category']

class SignUpForm(UserCreationForm):
    
    class Meta:
        model =  User
        fields = ('username', 'first_name', 'last_name', 'email', 'age')


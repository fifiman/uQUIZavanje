from django import forms
from quiz.models import *
from django.contrib.auth.forms import *



class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['question', 'answer_one','answer_two','answer_three','answer_four','correct','category']

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label='Name')
    last_name = forms.CharField(max_length=30, required=False, label='Last name')
    email = forms.EmailField(max_length=254, label='Email'  )
    age = forms.IntegerField()

class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'age')


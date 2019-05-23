from django import forms
from quiz.models import *


class QuestionForm(forms.ModelForm):
    
    class Meta:
        model = Question
        fields = ['question', 'answer_one','answer_two','answer_three','answer_four','correct','category']

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def home(request):
    template = loader.get_template('quiz/home.html')

    # Fill with context.
    context = {

    }

    return HttpResponse(template.render(context, request))




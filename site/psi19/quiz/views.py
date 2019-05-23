from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader


def home(request):
    template = loader.get_template('quiz/home.html')

    # Fill with context.
    context = {

    }

    return HttpResponse(template.render(context, request))

def signup(request):
    message = None

    # If POST request we trying to create new user.
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')

        message = 'BAD SIGNUP'

    # If GET or bad form we should return
    # the form again to the user.
    template = loader.get_template('quiz/signup.html')

    # Fill with form context.
    context = {
        'form': UserCreationForm()
    }

    if message is not None:
        context['message'] = message

    return HttpResponse(template.render(context, request))

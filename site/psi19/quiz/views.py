from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from quiz.models import *

def home(request):
    template = loader.get_template('quiz/home.html')

    # Fill with context.
    context = {

    }

    return HttpResponse(template.render(context, request))

#searches for 10 best players overall
def global_rank_list(request):
    template = loader.get_template('quiz/rank_list.html')

    context = {
        'top_10_users': User_profile.get_global_top_10(),
    }    

    return HttpResponse(template.render(context, request))

"""
def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        books = Book.objects.filter(title__icontains=q)
        return render(request, 'books/search_results.html',
                      {'books': books, 'query': q})
    else:
        return HttpResponse('Please submit a search term.')
"""

#search by username
def search(request):

    user = None

    if 'searched_name' in request.GET and request.GET['searched_name']:
        searched_name = request.GET['searched_name']
        user = User.objects.filter(username = searched_name)[0]

    already_friends = Friendship.already_friends(user, request.user)
    me = (user == request.user)

    return render(request, 'quiz/search_results.html', {'found' : user, 'already_friends': already_friends, 'me' : me})
    
def follow(request):    

    if 'username' in request.GET and request.GET['username']:
        recieved_username = request.GET['username']
    
    user1 = User.objects.filter(username=recieved_username)[0]

    if user1 != request.user:
        Friendship.follow(request.user, user1)
   

    return redirect('/home')

def unfollow(request):    

    if 'username' in request.GET and request.GET['username']:
        recieved_username = request.GET['username']
    
    user1 = User.objects.filter(username=recieved_username)[0]

    if user1 != request.user:
        Friendship.unfollow(request.user, user1)
   

    return redirect('/home')


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

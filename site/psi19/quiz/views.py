from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from quiz.models import *
from quiz.forms import *

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


def submit_a_question(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = QuestionForm(request.POST)
        # check whether it's valid:
        # print('DRUGI POZIV')
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            
            q = request.POST['question']
            a1 = request.POST['answer_one']
            a2 = request.POST['answer_two']
            a3 = request.POST['answer_three']
            a4 = request.POST['answer_four']
            c = request.POST['correct']
            cat = Category.objects.filter(id = request.POST['category'])[0]

            Question.submit_a_question(q,a1,a2,a3,a4,c,cat)
            return redirect('/home')

    # if a GET (or any other method) we'll create a blank form
    else:
        print('PRVI POZIV')
        form = QuestionForm()

    return render(request, 'quiz/add_question.html', {'form': form})


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

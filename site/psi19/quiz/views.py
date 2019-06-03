from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from quiz.models import *
from quiz.forms import *
from django.views import generic
from django.views.generic import UpdateView
from django.http import Http404



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
        form = SignUpForm(request.POST)

        if form.is_valid():
            #form.save()
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            name = form.cleaned_data.get('first_name')
            last = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            agef = form.cleaned_data.get('age')
            
            new_user = User.objects.create_user(username,email,raw_password)
            new_user.first_name = name
            new_user.last_name = last
            new_user.age = agef
            new_user.save()

            print(new_user.id)

            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')

        message = form.errors

    # If GET or bad form we should return
    # the form again to the user.
    template = loader.get_template('quiz/signup.html')

    # Fill with form context.
    context = {
        'form': SignUpForm()
    }

    if message is not None:
        context['message'] = message

    return HttpResponse(template.render(context, request))

#searches for 10 best players overall
def global_rank_list(request):
    template = loader.get_template('quiz/rank_list.html')

    context = {
        'top_10_friends': Friendship.top_10_friends(request.user),
        'top_10_users': User.get_global_top_10(),
    }   

    print (User.get_global_top_10()) 

    return HttpResponse(template.render(context, request))


# search by username
def search(request):

    users = []

    if 'searched_name' in request.GET and request.GET['searched_name']:
        searched_name = request.GET['searched_name']
        users = User.objects.filter(username__contains = searched_name)

    ret = []

    for user in users:
        
        # cannot check already friends if im already logged in
        if(request.user.is_authenticated):
            already_friends = Friendship.already_friends(user, request.user)
            request_sent = Friendship.request_sent(request.user, user)
            request_recieved = Friendship.request_sent(user, request.user)
        else:
            already_friends = False
            request_sent = False
            request_recieved = False
        
        me = (user == request.user)
        
        if(not me):
            ret.append({
                'user' : user,
                'already_friends' : already_friends,
                'request_sent' : request_sent,
                'request_recieved' : request_recieved
            })

    return render(request, 'quiz/search_results.html', {'found' : ret})

# friendship related methods

# secured    
def send_request(request, value):    

    if request.user.is_authenticated:    
        if 'username' in request.GET and request.GET['username']:
            recieved_username = request.GET['username']
        
        user1 = User.objects.filter(username=recieved_username)[0]

        if user1 != request.user:
            Friendship.send_request(request.user, user1)
    
        return redirect('/friends_page/'+value)
    return redirect('/home')

# secured
def cancel_request(request, value):
    if request.user.is_authenticated:
        if 'username' in request.GET and request.GET['username']:
            recieved_username = request.GET['username']
        
        user1 = User.objects.get(username=recieved_username)

        if user1 != request.user:
            Friendship.cancel_request(request.user, user1)
    
        return redirect('/friends_page/'+value)
    return redirect('/home')

#secured
def confirm_request(request, value):    

    if request.user.is_authenticated:    
        if 'username' in request.GET and request.GET['username']:
            recieved_username = request.GET['username']
        
        user1 = User.objects.get(username=recieved_username)

        if user1 != request.user:
            Friendship.accept_request(request.user, user1)
        
        return redirect('/friends_page/'+value)
    return redirect('/home')

# secured
def deny_request(request, value):    

    if request.user.is_authenticated:
        if 'username' in request.GET and request.GET['username']:
            recieved_username = request.GET['username']
        
        user1 = User.objects.get(username=recieved_username)

        if user1 != request.user:
            Friendship.deny_request(request.user, user1)
    
        return redirect('/friends_page/'+value)
    return ('/home')
# secured
def unfriend(request, value):    
    
    if request.user.is_authenticated:
        if 'username' in request.GET and request.GET['username']:
            recieved_username = request.GET['username']
        
        user1 = User.objects.filter(username=recieved_username)[0]

        if user1 != request.user:
            Friendship.unfriend(request.user, user1)

        return redirect('/friends_page/'+value)
    
    return redirect('/home')
# friendship related methods done

# Question submission methods : SENIOR + only - 

# secured
def submit_a_question(request):
    user = request.user
    message = ""
    if user.is_authenticated:
        if user.is_senior() or user.is_moderator or user.is_superuser:
            # if this is a POST request we need to process the form data
            if request.method == 'POST':
                # create a form instance and populate it with data from the request:
                form = QuestionForm(request.POST)
                # check whether it's valid:
   
                if form.is_valid():
                    # process the data in form.cleaned_data as required
                    # ...
                    # redirect to a new URL:
                    q = form.cleaned_data.get('question')
                    q = request.POST['question']
                    a1 = form.cleaned_data.get('answer_one')
                    a2 = form.cleaned_data.get('answer_two')
                    a3 = form.cleaned_data.get('answer_three')
                    a4 = form.cleaned_data.get('answer_four')
                    c = form.cleaned_data.get('correct')
                    cat = Category.objects.filter(id = request.POST['category'])[0]

                    if(c > 4 or c < 0):
                        message = "Odgovor je van opsega"
                    else:
                        if (a1 == a2 or a1 == a3 or a1 == a4 or a2 == a3 or a2 == a4 or a3 == a4):
                            message = "Neki od odgovora su isti"
                        else:
                            # privileged_submit unapred potvrdjuje pitanje, jer nema smisla admin i moderator
                            if(user.is_moderator or user.is_superuser):
                                Question.privileged_submit_a_question(q,a1,a2,a3,a4,c,cat)
                            else:    
                                Question.submit_a_question(q,a1,a2,a3,a4,c,cat)
                            
                            # ako je izvrsen uspesan unos renderuj novu, praznu formu
                            form = QuestionForm()

            # if a GET (or any other method) we'll create a blank form
            else:
                form = QuestionForm()

            return render(request, 'quiz/add_question.html', {'form': form, 'message' : message})

    return redirect('/home')        

# secured
def needs_validation(request):
    
    user = request.user

    if user.is_authenticated:
        if user.is_moderator or user.is_superuser:
            template = loader.get_template('quiz/questions_that_need_validation.html')
            questions = []
            questions =  Question.get_all_not_validated()
            context = {
                'questions': questions,
            }   

            return HttpResponse(template.render(context, request))

    return redirect('\home')

# secured
def approve_question(request):
    
    user = request.user

    if user.is_authenticated:
        if user.is_superuser or user.is_moderator:
            recieved_operation = request.GET['operation']
            recieved_id = request.GET['id']

            if recieved_operation == "ok":
                Question.approve_question(recieved_id)
            else:
                Question.delete_question(recieved_id)

    return redirect('/needs_validation')

def admin_question_overview(request):
    user = request.user

    if user.is_superuser:
        questions = Question.get_all_questions()
        context = {
            'questions' : questions
        }
        
        return render(request, 'quiz/list_all_questions.html', context)

    return redirect('/home')

def admin_remove_question(request):
    
    user = request.user

    if user.is_authenticated:
        if user.is_superuser:
            recieved_id = request.GET['id']
         
            Question.delete_question(recieved_id)

            questions = Question.get_all_questions()
            context = {
                'questions' : questions
            }

        #return render(request, 'quiz/list_all_questions.html', context)
        return redirect('/admin_question_overview')
    return redirect('/home')

# Question submission methods done

# moderator related views

# secured
def moderator_candidates(request):

    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            template = loader.get_template('quiz/approve_moderator.html')
            moderators = []
            moderators = User.get_moderator_candidates()
            context = {
                'moderators': moderators,
            }

            return HttpResponse(template.render(context, request))
    
    return redirect('/home')

# secured
def approve_moderator(request):
    
    user = request.user

    if user.is_authenticated:
        if user.is_superuser:
            recieved_operation = request.GET['operation_mod']
            
            username = request.GET['username_mod']

            if recieved_operation == "ok":
                User.approve_moderator(username)
            else:
                User.delete_moderator(username)

            return redirect('/moderator_candidates/')

    return redirect('/home')

# secured    
def submit_wants_moderator(request):
    user = request.user

    # iz nekog razloga mi ne radi lazy eval tako da if u ifu
    if user.is_authenticated:
        if user.is_senior() and not user.is_moderator:
            User.set_wants_moderator(user.username)

    return redirect('/home')    
    
# secured
def my_profile(request, value):
    user = User.get_by_id(value)
    if request.user.is_authenticated:
    
        template = loader.get_template('quiz/my_profile.html')
        lvl = user.level

        print(lvl)

        wins = Game.number_of_wins(user)
        played = Game.number_of_games_played(user)
        
        if played != 0:
            percentage = (float)(wins/played)
        else:
            percentage = 0

        number_of_friends = Friendship.count_my_friends(user)
        friends = Friendship.get_random_four_freinds(user)
        senior = user.is_senior()
        wants_moderator = user.wants_moderator

        trophies = []
        trophies.append({'name': "New user", 'src':"quiz/new_user.jpg"})
        
        if wins>=10:
            trophies.append({'name': "10 wins", 'src': "quiz/10win.jpg"})
        if wins>=50:
            trophies.append({'name': "50 wins", 'src': "quiz/50win.jpg"})
        if wins>=100:
            trophies.append({'name': "100 wins", 'src': "quiz/100win.jpg"})
        if lvl>=5:
            trophies.append({'name': "Level 5+", 'src': "quiz/lvl5.jpg"})
        if lvl>=10:
            trophies.append({'name': "Level 10+", 'src': "quiz/lvl10.jpg"})  
        if lvl>=20:
            trophies.append({'name': "Level 20+", 'src': "quiz/lvl20.jpg"})  
        if user.is_moderator:
            trophies.append({'name': "Moderator", 'src': "quiz/moderator.jpg"})
        if user.is_senior():
            trophies.append({'name': "Senior", 'src': "quiz/senior_user.jpg"})               
        
        context = {
            'curUser': user,
            'wins': wins,
            'played': played,
            'percentage': percentage,
            'number_of_friends': number_of_friends,
            'trophies': trophies,
            'friends' : friends,
            'senior' : senior,
            'wants_moderator' : wants_moderator,
        }
        return HttpResponse(template.render(context, request))
    else: 
        return redirect('/home')
    
# secured
def trophy_page(request, value):
    if request.user.is_authenticated:
        user = User.get_by_id(value)
        template = loader.get_template('quiz/trophy_page.html')
        lvl = user.level
        wins = Game.number_of_wins(user)
        played = Game.number_of_games_played(user)
        if played != 0:
            percentage = (float)(wins/played)
        else: 
            percentage = 0
        senior = lvl>=10
        moderator = user.moderator()
        #friends = Friendship.count_my_friends(request.user.id)
        context = {
                'curUser': user,
                'wins10': wins>=10,
                'wins50': wins>=50,
                'wins100': wins>=100,
                'senior': senior,
                'moderator': moderator,
                'level5' : lvl>=5,
                'level10' : lvl>=10,
                'level20' : lvl>=20,
            }
        return HttpResponse(template.render(context, request))
    else: 
        return redirect('/home')

# secured
def friends_page(request, value):
    if request.user.is_authenticated:
        user = User.get_by_id(value)
        template = loader.get_template('quiz/friends_page.html')
        friends = Friendship.get_friends(user)
        recieved = Friendship.get_recieved_friend_requests(user)
        sent = Friendship.get_sent_friend_requests(user)
        statusFriend = []
        for friend in friends:
            if Friendship.already_friends(friend["second_friend_id"],request.user.id): 
                statusFriend.append([friend,1])
            elif Friendship.request_sent(request.user.id,friend["second_friend_id"]): 
                statusFriend.append([friend,2])
            elif Friendship.request_sent(friend["second_friend_id"],request.user.id): 
                statusFriend.append([friend,3])
            else: 
                statusFriend.append([friend,4])
        context = {
                'curUser': user,
                'friends': statusFriend,
                'recieved': recieved,
                'sent': sent,
            }
        return HttpResponse(template.render(context, request))
    else: 
        return redirect('/home')        

def games_overview(request, value):
    if request.user.is_authenticated:
        user = User.get_by_id(value)
        template = loader.get_template('quiz/games_overview.html')
        games = Game.get_all_games(user)
        context = {
                'curUser': user,
                'games': games,
            }
        return HttpResponse(template.render(context, request))
    else: 
        return redirect('/home')

def edit_question(request, pk):
    user = request.user
    question = Question.get_by_id(pk)
    form = QuestionForm(request.POST or None, instance=question)
    message = ""
    if user.is_authenticated:
        if user.is_senior() or user.is_moderator or user.is_superuser:
            if request.method == 'POST':
                if form.is_valid():
                    q = form.cleaned_data.get('question')
                    q = request.POST['question']
                    a1 = form.cleaned_data.get('answer_one')
                    a2 = form.cleaned_data.get('answer_two')
                    a3 = form.cleaned_data.get('answer_three')
                    a4 = form.cleaned_data.get('answer_four')
                    c = form.cleaned_data.get('correct')
                    cat = Category.objects.filter(id = request.POST['category'])[0]

                    if(c > 4 or c < 0):
                        message = "Odgovor je van opsega"
                    else:
                        if (a1 == a2 or a1 == a3 or a1 == a4 or a2 == a3 or a2 == a4 or a3 == a4):
                            message = "Neki od odgovora su isti"
                        else:
                            form.save()
                    
                return redirect('/admin_question_overview')
            return render(request, 'quiz/edit_question.html', {'form': form, 'message': message, 'qid': question.id}) 
    return redirect('/home')    
# secured
def change_avatar(request):

    user = request.user

    # slika moze da se menja samo ako je user ulogovan
    if(user.is_authenticated and 'avatar_option' in request.GET):
        recieved_avatar = request.GET['avatar_option']
        
        User.update_image(user.username, recieved_avatar)

        # TODO change to my_profile
        return redirect('/my_profile')

    # if not logged in just redirect to home    
    return redirect('/home')

# secured
def choose_avatar(request):
    user = request.user
    if(user.is_authenticated):
        template = loader.get_template('quiz/choose_avatar.html')

        context = {
            
        }   

        return HttpResponse(template.render(context, request))
    
    return redirect('\home')

        

def report_form(request):

    user = request.user

    if (user.is_authenticated):
        template = loader.get_template('quiz/report_form.html')
        reported = request.POST['reported']

        context = {
            'reported': reported,
        }

        return HttpResponse(template.render(context, request))

    return home(request)


def report_form_submit(request):

    user = request.user

    if (user.is_authenticated):

        reported_username = request.POST['reported']
        reported = User.objects.filter(username = reported_username)[0]

        report_text = request.POST['report_text']

        Report.add_report(user, reported, report_text)

    return home(request)


def report_list(request):

    user = request.user

    if (user.is_authenticated):

        template = loader.get_template('quiz/report_list.html')
        reports = Report.list_valid_reports()

        context = {
            'reports': reports,
        }

        return HttpResponse(template.render(context, request))

    return home(request)


def approve_report(request):
    user = request.user

    if user.is_authenticated:
        if user.is_superuser:
            operation = request.POST['operation']

            id = request.POST['id']

            if operation == "ok":
                Report.approve_report(id)
            else:
                Report.deny_report(id)

            return redirect('/report_list/')

    return redirect('/home/')



def create_game(request):

    template = loader.get_template('quiz/create_game.html')

    context = {

    }

    return HttpResponse(template.render(context, request))


def game(request):

    template = loader.get_template('quiz/game.html')

    context = {

    }

    return HttpResponse(template.render(context, request))

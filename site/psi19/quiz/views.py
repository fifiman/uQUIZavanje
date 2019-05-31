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
def send_request(request):    

    if request.user.is_authenticated:    
        if 'username' in request.GET and request.GET['username']:
            recieved_username = request.GET['username']
        
        user1 = User.objects.filter(username=recieved_username)[0]

        if user1 != request.user:
            Friendship.send_request(request.user, user1)
    
        return redirect('/friends_page')
    return redirect('/home')

# secured
def cancel_request(request):
    if request.user.is_authenticated:
        if 'username' in request.GET and request.GET['username']:
            recieved_username = request.GET['username']
        
        user1 = User.objects.get(username=recieved_username)

        if user1 != request.user:
            Friendship.cancel_request(request.user, user1)
    
        return redirect('/friends_page')
    return redirect('/home')

#secured
def confirm_request(request):    

    if request.user.is_authenticated:    
        if 'username' in request.GET and request.GET['username']:
            recieved_username = request.GET['username']
        
        user1 = User.objects.get(username=recieved_username)

        if user1 != request.user:
            Friendship.accept_request(request.user, user1)
        
        return redirect('/friends_page')
    return redirect('/home')

# secured
def deny_request(request):    

    if request.user.is_authenticated:
        if 'username' in request.GET and request.GET['username']:
            recieved_username = request.GET['username']
        
        user1 = User.objects.get(username=recieved_username)

        if user1 != request.user:
            Friendship.deny_request(request.user, user1)
    
        return redirect('/friends_page')
    return ('/home')
# secured
def unfriend(request):    
    
    if request.user.is_authenticated:
        if 'username' in request.GET and request.GET['username']:
            recieved_username = request.GET['username']
        
        user1 = User.objects.filter(username=recieved_username)[0]

        if user1 != request.user:
            Friendship.unfriend(request.user, user1)

        return redirect('/friends_page')
    
    return redirect('/home')
# friendship related methods done

# Question submission methods : SENIOR + only - 

# secured
def submit_a_question(request):
    user = request.user

    if user.is_authenticated:
        if user.is_senior() or user.is_moderator or user.is_superuser:
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
                form = QuestionForm()

            return render(request, 'quiz/add_question.html', {'form': form})

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

    return redirect('/my_profile')    
    
# secured
def my_profile(request):
    user = request.user
    if request.user.is_authenticated:
    
        template = loader.get_template('quiz/my_profile.html')
        lvl = user.level

        print(lvl)

        wins = Game.number_of_wins(request.user)
        played = Game.number_of_games_played(request.user)
        
        if played != 0:
            percentage = (float)(wins/played)
        else:
            percentage = 0

        number_of_friends = Friendship.count_my_friends(request.user)
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
        if lvl>=20:
            trophies.append({'name': "Level 20+", 'src': "quiz/lvl20.jpg"})  
        if user.is_moderator:
            trophies.append({'name': "Moderator", 'src': "quiz/moderator.jpg"})
        if user.is_senior():
            trophies.append({'name': "Senior", 'src': "quiz/senior_user.jpg"})               
        
        print(wants_moderator)

        context = {
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
def trophy_page(request):
    if request.user.is_authenticated:
        user = request.user
        template = loader.get_template('quiz/trophy_page.html')
        lvl = user.level
        wins = Game.number_of_wins(request.user)
        played = Game.number_of_games_played(request.user)
        if played != 0:
            percentage = (float)(wins/played)
        else: 
            percentage = 0
        senior = lvl>=10
        moderator = user.moderator()
        #friends = Friendship.count_my_friends(request.user.id)
        context = {
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
def friends_page(request):
    if request.user.is_authenticated:
        user = request.user
        template = loader.get_template('quiz/friends_page.html')
        friends = Friendship.get_friends(user)
        recieved = Friendship.get_recieved_friend_requests(user)
        sent = Friendship.get_sent_friend_requests(user)

        print(recieved  )

        context = {
                'friends': friends,
                'recieved': recieved,
                'sent': sent,
            }
        return HttpResponse(template.render(context, request))
    else: 
        return redirect('/home')        

class EditQuestion(UpdateView): 
    model = Question
    form_class = AdminQuestionForm
    template_name = "quiz/question_update_form.html"

    def get_success_url(self, *args, **kwargs):
        return reverse('quiz:home')

    def get_object(self, queryset=None):
    
        user = self.request.user
        question = super(EditQuestion, self).get_object(queryset)
        
        if not user.is_authenticated:
            raise Http404("You are not allowed here")
        else:
            if not user.is_superuser and not user.is_moderator:
                raise Http404("You are not allowed here")
        return question

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

        



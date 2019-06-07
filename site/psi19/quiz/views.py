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
import math

'''
Zbog strukture koda koju zahteva Django, umesto klasa u ovom projektu postoji jedan veliki views.py fajl i jedan veliki models.py fajl.
Ovi fajlovi enkapsuliraju najveci deo onoga sto u nekom drugom okruzenju predstavljaju modeli i kontroleri
S obzirom na monolitnost samih fajlova, nije moguce odrediti dve osobe odgovorne za svaki fajl, jer su im svi clanovi tima znacajno doprineli   
'''
'''
Home metoda koja vraca glavnu stranicu aplikacije
@param Request request
@return HttpResponse
'''
def home(request):
    template = loader.get_template('quiz/home.html')

    # Fill with context.        
    context = {}

    return HttpResponse(template.render(context, request))
'''
Metoda koja se poziva prilikom kreiranja nove partije, i kao argument uzima kategoriju pitanja za tu partiju
@param Request request, Category category
@return HttpResponse
'''
def quickgame(request, category):
    """
    Create a quick game.
    """

    categories = []
    categories.append(category)

    questions = Question.get_questions_from_categories(categories)
    '''
    if category == 'all':
        questions = Question.get_questions_from_categories()
    else: 
        category = Category.objects.get(name=category)
        questions = Question.objects.filter(category=category)[:10]
    '''
    if len(questions) == 0:
        return HttpResponse('No question in current category.')

    # Create game and add all questions.
    new_game = Game.objects.create()
    
    for question in questions:
        new_game.add_question(question)
    
    new_game.save()

    # Redirect to view with game id.
    return redirect('/game/' + str(new_game.id))
'''
Metoda koja realizuje logiku igre, u zavisnosti od stanja partije poslace korisnika u cekaonicu, na sledece pitanje ili na ekran za kraj igre
Prima argument game_id koji upucuje na partiju kreiranu u metodu quickgame
@param Request request, Int game_id
@return HttpResponse
'''
def game(request, game_id):    
    # Fetch game from DB.
    if not Game.objects.filter(id=game_id).exists():
        return HttpResponse('Game does not exist.')

    game = Game.objects.get(id=game_id)

    # Game over.
    if game.game_state == Game.GAME_OVER:
        template = loader.get_template('quiz/game_end_stats.html')
        max_pts = max([game.player_one_pts, game.player_two_pts, game.player_three_pts, game.player_four_pts])
        if game.num_players == 1:
            multiplier = 0
        elif game.num_players == 2:
            multiplier = 1
        elif game.num_players == 3:
            multiplier = 2
        elif game.num_players == 4:
            multiplier = 3
        
        #player one wins, update rankings
        if game.player_one_pts==max_pts:
            game.winner = game.player_one
            if game.player_one.is_senior():
                game.player_one.ranking+=20
            if game.player_two is not None:
                if game.player_two.is_senior():
                    game.player_two.ranking-=20
            if game.player_three is not None:
                if game.player_three.is_senior():
                    game.player_three.ranking-=20
            if game.player_four is not None:
                if game.player_four.is_senior():
                    game.player_four.ranking-=20
        
        #player two wins, update rankings
        if game.player_two_pts==max_pts:
            game.winner = game.player_two
            if game.player_two.is_senior():
                game.player_one.ranking+=20
            if game.player_one is not None:
                if game.player_one.is_senior():
                    game.player_one.ranking-=20
            if game.player_three is not None:
                if game.player_three.is_senior():
                    game.player_three.ranking-=20
            if game.player_four is not None:
                if game.player_four.is_senior():
                    game.player_four.ranking-=20
        
        #player three wins, update rankings
        if game.player_three_pts==max_pts:
            game.winner = game.player_three
            if game.player_three.is_senior():
                game.player_three.ranking+=20
            if game.player_two is not None:
                if game.player_two.is_senior():
                    game.player_two.ranking-=20
            if game.player_one is not None:
                if game.player_one.is_senior():
                    game.player_one.ranking-=20
            if game.player_four is not None:
                if game.player_four.is_senior():
                    game.player_four.ranking-=20
        
        #player four wins, update rankings
        if game.player_four_pts==max_pts:
            game.winner = game.player_four
            if game.player_four.is_senior():
                game.player_four.ranking+=20
            if game.player_two is not None:
                if game.player_two.is_senior():
                    game.player_two.ranking-=20
            if game.player_three is not None:
                if game.player_three.is_senior():
                    game.player_three.ranking-=20
            if game.player_one is not None:
                if game.player_one.is_senior():
                    game.player_one.ranking-=20
        
        #make sure no one has a negative ranking
        if game.player_one.ranking<0:
            game.player_one.ranking = 0
        
        #add points to experience and calculate new levels  
        game.player_one.exp+=int((game.player_one_pts/10))*multiplier
        game.player_one.level = math.floor(game.player_one.exp/200)+1
        
        #
        if game.player_two is not None:
            if game.player_two.ranking<0:
                game.player_two.ranking = 0
            game.player_two.exp+=int((game.player_two_pts/10))*multiplier
            game.player_two.level = math.floor(game.player_two.exp/200)+1
        if game.player_three is not None:
            if game.player_three.ranking<0:
                game.player_three.ranking = 0
            game.player_three.exp+=int((game.player_three_pts/10))*multiplier
            game.player_three.level = math.floor(game.player_four.exp/200)+1
        if game.player_four is not None:
            if game.player_four.ranking<0:
                game.player_four.ranking = 0 
            game.player_four.exp+=int((game.player_four_pts/10))*multiplier
            game.player_four.level = math.floor(game.player_four.exp/200)+1
 
        # save changes to plate
        game.player_one.save()
        if game.player_two is not None:
            game.player_two.save()
        if game.player_three is not None:
            game.player_three.save()
        if game.player_four is not None:
            game.player_four.save()

        game.save()
        
        context = {
            "game": game,
            "questions": Game.get_questions_for_game(game),
            "p1exp": int((game.player_one_pts/10))*multiplier,
            "p2exp": int((game.player_two_pts/10))*multiplier,
            "p3exp": int((game.player_three_pts/10))*multiplier,
            "p4exp": int((game.player_four_pts/10))*multiplier,
            "winner": game.num_players>1,
        }
        return HttpResponse(template.render(context,request))

    if game.user_part_of_game(request.user):
        if game.game_state == Game.GAME_IN_PLAY:
            return game_question(request, game)
        
        # Send to waiting room.
        return waiting_room(request, game_id)

    # Game is in-play, can't join.
    # We can maybe change this later.
    if game.game_state == Game.GAME_IN_PLAY:
        return HttpResponse('Game is in play, cannot join now.')

    # Try to join.
    join_status = game.join_game(request.user)

    if join_status == False:
        return HttpResponse("Can't join, too many players in room.")

    return waiting_room(request, game_id)
'''
Metoda koju poziva game ukoliko partija nije pocela, vraca waiting_room.html
Prima argument game_id koji upucuje na partiju kreiranu u metodu quickgame
@param Request request, Int game_id
@return HttpResponse
'''
def waiting_room(request, game_id):
    # Send to waiting room.
    template = loader.get_template('quiz/game_waiting_room.html')
    
    friends_all = []
    friends_not_in_game = []
    
    if request.user.is_authenticated:
        friends_all = Friendship.get_friends(request.user)
        
        '''
        for friend in friends_all:
            print(friend)

            if(not Game.is_in_game(friend['second_friend_id'])):
                friends_not_in_game.append(friend)
        '''
    
    context = {
        'game_id':      game_id,
        #'friends':      friends_not_in_game
        'friends':      friends_all
    }

    return HttpResponse(template.render(context, request))
'''
Metoda koju poziva game ukoliko je partija u toku i korisnik je u partiji, vraca game_question.html
Prima argument game koji upucuje na partiju kreiranu u metodu quickgame
@param Request request, Game game
@return HttpResponse
'''
def game_question(request, game):

    # Return info to the current question.
    current_question = game.get_current_question()

    context = {
        'game_id':      game.id,
        'user_id':      request.user.id,
        'question':     current_question,
        'game':         game,
    }

    template = loader.get_template('quiz/game_question.html')
    return HttpResponse(template.render(context, request))
'''
Metoda za stvaranje novog korisnika, ukoliko je pozvana prvi put (klikom na dugme) vraca signup.html
Ukoliko je pozvana post metodom, radi provere parametara i ispisuje gresku odnosno stvara novog korisnika u bazi
@param Request request
@return HttpResponse
'''
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
'''
Metoda koja puni i vraca stranicu rank_list.html sa 10 najbolje rankiranih igraca i prijatelja
@param Request request
@return HttpResponse
'''
#searches for 10 best players overall
def global_rank_list(request):
    template = loader.get_template('quiz/rank_list.html')

    context = {
        'top_10_friends': Friendship.top_10_friends(request.user),
        'top_10_users': User.get_global_top_10(),
    }   

    print (User.get_global_top_10()) 

    return HttpResponse(template.render(context, request))

'''
Metoda koja puni i vraca stranicu search_results rezultatima pretrage korisnika po unetoj reci
@param Request request
@return HttpResponse
'''
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
'''
Metoda koja sadrzi logiku slanja zahteva za prijateljstvo
Value argument sluzi da bi se razlikovao korisnik u sesiji i korisnik ciji profil posecujemo, a na koji treba da nas vrati ova metoda
@param Request request, Int value
@return HttpResponse
'''
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
'''
Metoda koja sadrzi logiku ponistavanja zahteva za prijateljstvo
Value argument sluzi da bi se razlikovao korisnik u sesiji i korisnik ciji profil posecujemo, a na koji treba da nas vrati ova metoda
@param Request request, Int value
@return HttpResponse
'''
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
'''
Metoda koja sadrzi logiku prihvatanja zahteva za prijateljstvo
Value argument sluzi da bi se razlikovao korisnik u sesiji i korisnik ciji profil posecujemo, a na koji treba da nas vrati ova metoda
@param Request request, Int value
@return HttpResponse
'''
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
'''
Metoda koja sadrzi logiku odbijanja zahteva za prijateljstvo
Value argument sluzi da bi se razlikovao korisnik u sesiji i korisnik ciji profil posecujemo, a na koji treba da nas vrati ova metoda
@param Request request, Int value
@return HttpResponse
'''
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
'''
Metoda koja sadrzi logiku brisanja prijatelja
Value argument sluzi da bi se razlikovao korisnik u sesiji i korisnik ciji profil posecujemo, a na koji treba da nas vrati ova metoda
@param Request request, Int value
@return HttpResponse
'''
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
'''
Metoda koja vraca formu za dodavanje prijatelja ukoliko je korisnik sa odgovarajucim privilegijama
@param Request request
@return HttpResponse
'''
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
'''
Metoda koja vraca stranicu za prihvatanje predlozenih pitanja za moderatora
@param Request request
@return HttpResponse
'''
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
'''
Metoda koja sadrzi logiku prihvatanja predlozenih pitanja za moderatora
@param Request request
@return HttpResponse
'''
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
'''
Metoda koja vraca pregled svih pitanja za administratora
@param Request request
@return HttpResponse
'''
def admin_question_overview(request):
    user = request.user

    if user.is_superuser:
        questions = Question.get_all_questions()
        context = {
            'questions' : questions
        }
        
        return render(request, 'quiz/list_all_questions.html', context)

    return redirect('/home')
'''
Metoda koja sadrzi logiku brisanja pitanja za administratora
@param Request request
@return HttpResponse
'''
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
'''
Metoda koja vraca prikaz kandidata za moderatorsku poziciju
@param Request request
@return HttpResponse
'''
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
'''
Metoda koja sadrzi logiku prihvatanja ili odbijanja kandidata za moderatorsku poziciju
@param Request request
@return HttpResponse
'''
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
'''
Metoda koja sadrzi logiku slanja zahteva za moderatorstvo
@param Request request
@return HttpResponse
'''
# secured    
def submit_wants_moderator(request):
    user = request.user

    # iz nekog razloga mi ne radi lazy eval tako da if u ifu
    if user.is_authenticated:
        if user.is_senior() and not user.is_moderator:
            User.set_wants_moderator(user.username)

    return redirect('/home')    
'''
Metoda koja sadrzi puni i vraca stranicu my_profile.html
Parametar value sluzi da razlikujemo korisnika iz sesije i korisnika ciji profil posecujemo
@param Request request, Int value
@return HttpResponse
'''
# secured
def my_profile(request, value):
    user = User.get_by_id(value)
    if request.user.is_authenticated:
    
        template = loader.get_template('quiz/my_profile.html')
        lvl = user.level

        wins = Game.number_of_wins(user)
        played = Game.number_of_games_played(user)
        
        if played != 0:
            percentage = float("{0:.2f}".format(((float)(wins/played) * 100)))
        else:
            percentage = 0

        number_of_friends = Friendship.count_my_friends(user)
        friends = Friendship.get_random_four_freinds(user)
        senior = user.is_senior()
        
        # bool for apply for moderator button
        wants_moderator = user.wants_moderator
        moderator = user.is_moderator
        show_apply_for_moderator = not wants_moderator and senior and not moderator 

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
            'show_apply_for_moderator' : show_apply_for_moderator,
        }

        return HttpResponse(template.render(context, request))
    else: 
        return redirect('/home')
'''
Metoda koja sadrzi puni i vraca stranicu trophy_page.html
Parametar value sluzi da razlikujemo korisnika iz sesije i korisnika ciji profil posecujemo
@param Request request, Int value
@return HttpResponse
'''   
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
'''
Metoda koja sadrzi puni i vraca stranicu friends_page.html
Parametar value sluzi da razlikujemo korisnika iz sesije i korisnika ciji profil posecujemo
@param Request request, Int value
@return HttpResponse
'''   
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
'''
Metoda koja sadrzi puni i vraca stranicu games_overview.html
Parametar value sluzi da razlikujemo korisnika iz sesije i korisnika ciji profil posecujemo
@param Request request, Int value
@return HttpResponse
'''   
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
'''
Metoda koja vraca stranicu za izmenu pitanja (ukoliko je pozvana prvi put) ili radi neophodne provere i azurira pitanje ako je pozvana post metodom
Parametar pk sluzi da pristupimo pitanju koje menjamo
@param Request request, Int pk
@return HttpResponse
''' 
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
'''
Metoda koja sadrzi logiku za izmenu avatara
@param Request request
@return HttpResponse
'''     
# secured
def change_avatar(request):

    user = request.user

    # slika moze da se menja samo ako je user ulogovan
    if(user.is_authenticated and 'avatar_option' in request.GET):
        recieved_avatar = request.GET['avatar_option']
        
        User.update_image(user.username, recieved_avatar)

        # TODO change to my_profile
        return redirect("/my_profile/"+str(request.user.id))

    # if not logged in just redirect to home    
    return redirect('/home')
'''
Metoda koja vraca stranicu za izbor avatara
@param Request request
@return HttpResponse
'''  
# secured
def choose_avatar(request):
    user = request.user
    if(user.is_authenticated):
        template = loader.get_template('quiz/choose_avatar.html')

        context = {
            
        }   

        return HttpResponse(template.render(context, request))
    
    return redirect('\home')
'''
Metoda koja vraca stranicu za podnosenje zahteva za blokiranje korisnika
@param Request request
@return HttpResponse
'''  
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

'''
Metoda koja sadrzi logiku podnosenja zahteva za blokiranje korisnika
@param Request request
@return HttpResponse
''' 
def report_form_submit(request):

    user = request.user

    if (user.is_authenticated):

        reported_username = request.POST['reported']
        reported = User.objects.filter(username = reported_username)[0]

        report_text = request.POST['report_text']

        Report.add_report(user, reported, report_text)

    return home(request)

'''
Metoda koja vraca prikaz zahteva za blokiranje korisnika
@param Request request
@return HttpResponse
''' 
def report_list(request):

    user = request.user

    if (user.is_superuser):

        template = loader.get_template('quiz/report_list.html')
        reports = Report.list_valid_reports()

        context = {
            'reports': reports,
        }

        return HttpResponse(template.render(context, request))

    return home(request)

'''
Metoda koja sadrzi logiku za odobravanje ili brisanje zahteva za blokiranje korisnika
@param Request request
@return HttpResponse
''' 
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

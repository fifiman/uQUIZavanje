from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import random


class User(AbstractUser):
    
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    age = models.IntegerField(null = True)
    #equivalent to banned
    is_active = models.BooleanField(default=True)
    is_moderator = models.BooleanField(default=False)
    wants_moderator = models.BooleanField(default = False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField( max_length=50)
    level = models.IntegerField(default = 0)
    exp = models.IntegerField(default = 0)
    picture = models.TextField(default = "quiz/default_avatar.jpg", max_length = 50, blank = True, null = True)
    ranking = models.IntegerField(default = -1)

    def __str__(self):
        temp = str(self.username) + " Level: " + str(self.level)
        if self.level >= 10:
            temp = temp + " Rating: " + str(self.ranking) 

        return temp
        
    def moderator(self):
        return self.is_moderator

    def is_senior(self):    
        return self.level >= 10

    def get_level(self):
        return self.level

    def get_ranking(self):
        return self.ranking

    def get_age(self):
        return self.age

    # gets 10 best players overall
    def get_global_top_10():
        return User.objects.filter(level__gte = 10, is_active=true).order_by('-ranking')[:10]
    
    def get_by_id(id_val):
        return User.objects.filter(id=id_val).first()

    # returns all users who are not banned
    def get_active_users():
        return User.objects.filter(is_active = True)

    #returns all users who want to be modeators, and are eligible for the role
    def get_moderator_candidates():
        return User.objects.filter(wants_moderator = True, is_moderator = False, level__gte = 10)    

    def set_wants_moderator(username):
        User.objects.filter(username = username).update(wants_moderator = True)

    def approve_moderator(username):
        User.objects.filter(username = username).update(wants_moderator = False, is_moderator = True)
        
    def delete_moderator(username):
        User.objects.filter(username = username).update(wants_moderator = False, is_moderator = False)

    # sets path for a chosen image
    def update_image(username, pic):
        User.objects.filter(username = username).update(picture = pic)

    def is_over_level_five(self):
        if(self.level >= 5):
            return True
        else:
            return False

    def is_over_level_ten(self):
        if(self.level >= 10):
            return True
        else:
            return False

    def is_over_level_twenty(self):
        if(self.level >= 20):
            return True
        else:
            return False

    def has_more_than_five_wins(self):
        count = Game.number_of_wins()

        if count > 5:
            return True
        else:
            return False    

    def has_more_than_fifty_wins(self):
        count = Game.number_of_wins()

        if count > 50:
            return True
        else:
            return False    

    def has_more_than_hundred_wins(self):
        count = Game.number_of_wins()

        if count > 100:
            return True
        else:
            return False    

            

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']




# Connects two users, and allows them to see eachothers profiles, and play with eachother
class Friendship(models.Model):
    first_friend_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_f1', on_delete=models.DO_NOTHING)
    second_friend_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_f2', on_delete=models.DO_NOTHING)
    accepted = models.BooleanField(default = False)

    def __str__(self):
        return str(self.first_friend_id) + " " + str(self.second_friend_id)

    # checks if users are already friends
    def already_friends(user1, user2):

        count1 = Friendship.objects.filter(first_friend_id = user1, second_friend_id = user2).count()
        count2 = Friendship.objects.filter(first_friend_id = user2, second_friend_id = user1).count()

        # nece se desiti da su obojca poslala zahteve za prijateljstvo !    
        if (count1 + count2) > 1:
            return True
        else:
            return False    

    # ako zahtev postoji **** request_recieved(user1, user2) <=> request_sent(user2, user1) ****
    def request_sent(user1, user2):
        count = Friendship.objects.filter(first_friend_id = user1, second_friend_id = user2).count()

        if count > 0:
            return True
        else:
            return False

    # salje se zahtev za prijateljstvo, u bazu ubacujemo nepotvrdjeno prijateljstvo, ako zahtev vec nije napravljen
    def send_request(user1, user2):
        count = Friendship.objects.filter(first_friend_id = user1,second_friend_id = user2).count()
            
        if(user1 != user2 and count == 0):
            friendship = Friendship.objects.create(first_friend_id = user1,second_friend_id = user2)
            friendship.save()


    # poziva se samo ako zahtev vec nije prihvacen, potvrdjujem zahtev, i dodajem prijateljstvo u drugom pravcu
    def accept_request(user1, user2):
        f = Friendship.objects.filter(second_friend_id = user1, first_friend_id = user2)
        
        count = f.count()

        if count > 0:
            accepted = f[0].accepted    
            if(user1 != user2 and not accepted):
                # ne znam sto sam morao ponovo da dohvatam, ali drugacije nije htelo
                fr = Friendship.objects.get(second_friend_id = user1, first_friend_id = user2)
                fr.accepted = True
                fr.save()

                print(f[0].accepted)

                friendship = Friendship.objects.create(first_friend_id = user1,second_friend_id = user2, accepted = True)
                friendship.save()

    def deny_request(user1, user2):
        f = Friendship.objects.filter(second_friend_id = user1, first_friend_id = user2)
        
        count = f.count()

        if count > 0:
            accepted = f[0].accepted    
            if(user1 != user2 and not accepted):
                # ne znam sto sam morao ponovo da dohvatam, ali drugacije nije htelo
                fr = Friendship.objects.get(second_friend_id = user1, first_friend_id = user2)
                fr.delete()

    # current user wants to cancel his request, should be called only if the request isnt already confirmed
    def cancel_request(user1, user2): 
        friendship = Friendship.objects.get(first_friend_id = user1,second_friend_id = user2)
        accepted = friendship.accepted
        
        if(user1 != user2 and not accepted):
            friendship.delete()     

    # ako je prijateljstvo postojalo, obrisi ga 
    def unfriend(user1, user2):
        friendship = Friendship.objects.filter(first_friend_id = user1,second_friend_id = user2)
        count = friendship.count()
        
        if(count > 0):
            accepted = friendship[0].accepted    
            
            if(accepted):
                friendship.delete()          

                friendship1 = Friendship.objects.get(first_friend_id = user2,second_friend_id = user1)
                friendship1.delete()          
    

    #needs testing, return 10 friends with best scores
    def top_10_friends(user):
        friends =  Friendship.objects.filter(first_friend_id = user.id, accepted = True)
        friendsLvl = friends.filter(second_friend_id__level__gte = 10)
        friendsLvlId = friendsLvl.values_list('second_friend_id')
        users = User.objects.filter(id__in = friendsLvlId)
        return users.order_by('-ranking')[:10]

    
    # returns list of friends 
    def get_friends(user):
        return Friendship.objects.filter(first_friend_id = user, accepted = True).select_related('second_friend_id').values('second_friend_id', 'accepted', 'second_friend_id__username', 'second_friend_id__picture', 'second_friend_id__ranking')  

    def get_random_four_freinds(user):
        return Friendship.objects.filter(first_friend_id = user, accepted = True).select_related('second_friend_id').values('second_friend_id', 'accepted', 'second_friend_id__username', 'second_friend_id__picture', 'second_friend_id__ranking').order_by('?')[:4] 

    # gets all friend request that the user has sent    
    def get_sent_friend_requests(user):
        return Friendship.objects.filter(first_friend_id = user, accepted = False).select_related('second_friend_id').values('second_friend_id', 'second_friend_id__username', 'second_friend_id__picture', 'second_friend_id__ranking')  

    # gets all friend requests that a user has recieved
    def get_recieved_friend_requests(user):
        return Friendship.objects.filter(second_friend_id = user, accepted = False).select_related('first_friend_id').values('first_friend_id', 'first_friend_id__username', 'first_friend_id__picture', 'first_friend_id__ranking')  

    # counts how many friends user user has
    def count_my_friends(user):
        return Friendship.objects.filter(first_friend_id = user, accepted = True).count()    

#class containing all game relevant data
class Game(models.Model):
    # Game constants.
    MAX_PLAYERS = 4
    NUM_ANSWERS = 4

    GAME_NOT_STARTED    = 0
    GAME_IN_PLAY        = 1
    GAME_OVER           = 2

    player_one = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = '%(class)s_p1', on_delete=models.DO_NOTHING, null=True)
    player_two = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_p2',on_delete=models.DO_NOTHING, null=True)
    player_three = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_p3', on_delete=models.DO_NOTHING, null=True)
    player_four = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_p4', on_delete=models.DO_NOTHING, null=True)
    
    player_one_pts = models.IntegerField(default=0)
    player_two_pts = models.IntegerField(default=0)
    player_three_pts = models.IntegerField(default=0)
    player_four_pts = models.IntegerField(default=0)

    # Current game state.
    game_state      = models.IntegerField(default=0)

    # Number of question in the game.
    num_questions   = models.IntegerField(default=0)

    # Current question index we are, -1 for not started yet.
    cur_question    = models.IntegerField(default=-1)

    # Number of players in the room.
    num_players     = models.IntegerField(default=0)

    # Number of players that have answered the current question.
    num_answers     = models.IntegerField(default=0)

    winner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_win', on_delete=models.DO_NOTHING, blank = True, null = True)

    def add_question(self, question):
        GameQuestions.objects.create(game=self, index=self.num_questions, question=question)
        
        self.num_questions += 1
        self.save()

    def get_questions_for_game(self):
        return GameQuestions.objects.filter(game = self)

    def start_game(self):
        """
        Start the game if possible, otherwise return an Exception.
        """
        if self.cur_question != -1:
            raise Exception('Game has already been started.')
        
        if self.num_players == 0:
            raise Exception('No players inside game, nothing to start.')
        
        if self.num_questions == 0:
            raise Exception("Can't start game if there are no questions.")

        self.game_state     = Game.GAME_IN_PLAY
        self.cur_question   = 0

        print ('Game has started')

        self.save()

        return True

    def user_part_of_game(self, user):
        all_players = [self.player_one, self.player_two,
                       self.player_three, self.player_four]

        return user in all_players

    def join_game(self, user):
        """
        Attempt to join the game.

        Returns True/False if joining is possible.
        """
        # Check max number of players already.
        if self.num_players >= Game.MAX_PLAYERS:
            print('Max number of players reached.')
            return False
        print('USER' + str(user))
        # TODO: Check if is invite only game and only add
        # user if they are invited.

        # Check that user is part of the game already.
        if self.user_part_of_game(user):
            print ('User is already part of the game.')
            return True

        # All good, add the user to the game.
        self.num_players += 1

        if self.player_one is None:
            self.player_one = user
        elif self.player_two is None:
            self.player_two = user
        elif self.player_three is None:
            self.player_three = user
        elif self.player_four is None:
            self.player_four = user
        else:
            raise Exception('BAAAAD')

        self.save()
        return True

    def leave_game(self, user):
        if self.num_players == 0:
            print ('Cannot leave empty room')
            return False

        if self.player_one == user:
            self.player_one = None
        elif self.player_two == user:
            self.player_two = None
        elif self.player_three == user:
            self.player_three = None
        elif self.player_four == user:
            self.player_four = None
        else:
            print ('Player is not in game to leave')
            return False

        self.num_players -= 1
        self.save()

        return True

    def answer(self, user, answer_ind, msPassed):
        print("Usao u answer za"+user.username)
        # Check all input parameters.
        all_players = [self.player_one, self.player_two,
                       self.player_three, self.player_four]

        # Check if we are in a game state to answer a question.
        if self.game_state != Game.GAME_IN_PLAY:
            raise Exception('Cannot answer question in current state.')

        # Check if user is part of the game.
        if user not in all_players:
            raise Exception('Player is not part of the current game.')

        user_ind = all_players.index(user)

        # Fetch question from database, it should exist.
        question = GameQuestions.objects.get(game=self, index=self.cur_question).question

        # Check that the user has not answered before.
        if GameAnswers.objects.filter(game=self, user=user, question_index=self.cur_question).exists():
           print('User has already answered this question')
           return

        # Create answer in database.
        is_correct = question.correct == (answer_ind + 1)

        GameAnswers.objects.create(game=self, user=user, question_index=self.cur_question,
                                   answer_index=answer_ind, correct=is_correct)

        self.num_answers += 1

        question_changed = False
        time_bonus = int((5000 - msPassed)/100)

        if time_bonus<0:
            time_bonus=0

        if is_correct:
            if user == self.player_one:
                self.player_one_pts+=50
                self.player_one_pts+=time_bonus
                quest =  GameQuestions.objects.get(game=self, index=self.cur_question)
                quest.p1_pts = 50+time_bonus
                quest.save()
                print("dodao sam poene useru"+user.username)

            if user == self.player_two:
                self.player_two_pts+=50
                self.player_two_pts+=time_bonus
                quest =  GameQuestions.objects.get(game=self, index=self.cur_question)
                quest.p2_pts = 50+time_bonus
                quest.save()
                print("dodao sam poene useru"+user.username)

            if user == self.player_three:
                self.player_three_pts+=50
                self.player_three_pts+=time_bonus
                quest =  GameQuestions.objects.get(game=self, index=self.cur_question)
                quest.p3_pts = 50+time_bonus
                quest.save()
                print("dodao sam poene useru"+user.username)

            if user == self.player_four:
                self.player_four_pts+=50
                self.player_four_pts+=time_bonus
                quest =  GameQuestions.objects.get(game=self, index=self.cur_question)
                quest.p4_pts = 50+time_bonus
                quest.save()
                print("dodao sam poene useru"+user.username)
            
        # Move on to next question if we have to.
        if self.num_answers == self.num_players:
            self.cur_question += 1
            self.num_answers = 0
            question_changed = True

        # Check if the game is over.
        if self.cur_question == self.num_questions:
            question_changed = True
            # Game over.
            self.game_state = Game.GAME_OVER
            # Calculate points and winner.
        
        self.save()

        return is_correct, question_changed

    # racuna broj partija koje je pobedio korisnik user
    def number_of_wins(user):
        return Game.objects.filter(winner = user).count()

    # racuna broj partija koje je odigrao korisnik user
    def number_of_games_played(user):
        p1 = Game.objects.filter(player_one = user).count()
        p2 = Game.objects.filter(player_two = user).count()
        p3 = Game.objects.filter(player_three = user).count()
        p4 = Game.objects.filter(player_four = user).count()

        result = p1+p2+p3+p4

        return result

    def get_state(self):
        state =  {
            'game_state':       self.game_state,
            'cur_question':     self.cur_question,
            'num_players':      self.num_players,
            'num_answers':      self.num_answers,
            'player_names':     [],
        }

        # Add player names to state.
        all_players = [self.player_one, self.player_two,
                       self.player_three, self.player_four]
        
        for player in all_players:
            state['player_names'].append(player.username if player is not None else '')

        return state

    def get_current_question(self):
        if self.game_state != Game.GAME_IN_PLAY:
            raise Exception('Game not in play, cannot get current question.')
        
        current_question = GameQuestions.objects.get(game=self, index=self.cur_question).question
        return current_question

    def __str__(self):
        return str(self.get_state())

    def get_all_games(user):
        return Game.objects.filter(player_one = user) | Game.objects.filter(player_two = user) | Game.objects.filter(player_three = user) | Game.objects.filter(player_four = user)

#categorie id's and their names 
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

# class containing all question relevant data
# when inserting questions notice thet there is category General Knowledge 
# so when you dont know in which category to put your question, put it there
class Question(models.Model):
    question = models.TextField(max_length = 100)
    is_valid = models.BooleanField(default = False)
    answer_one = models.TextField(max_length = 20)
    answer_two = models.TextField(max_length = 20)
    answer_three = models.TextField(max_length = 20)
    answer_four = models.TextField(max_length = 20)
    correct = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Question:" + self.question + " Answers: " + self.answer_one + " " + self.answer_two + " " + self.answer_three + " " + self.answer_four

    def get_by_id(id_val):
        return Question.objects.filter(id=id_val).first()        

    def get_all_questions():
        return Question.objects.all()

    #NOTE Dodaj proveru da su svi odgovori razliciti
    def submit_a_question(question_in, answer_one_in, answer_two_in, answer_three_in, answer_four_in, correct_in, category_in):
        
        new_question = Question.objects.create(question = question_in, answer_one = answer_two_in,answer_two = answer_two_in, answer_three=answer_three_in, answer_four=answer_four_in, correct=correct_in, category=category_in)
        new_question.save()

    # nema smisla da admin i moderator potvrdjuju pitanja koja su dodali
    def privileged_submit_a_question(question_in, answer_one_in, answer_two_in, answer_three_in, answer_four_in, correct_in, category_in):
        new_question = Question.objects.create(question = question_in, answer_one = answer_one_in,answer_two = answer_two_in, answer_three=answer_three_in, answer_four=answer_four_in, correct=correct_in, category=category_in, is_valid = True)
        new_question.save()
 

    # returns all questions that needs validating
    def get_all_not_validated():
        return Question.objects.filter(is_valid = False)

    #query the db for speceific questions
    #def get_question_from_category(category, number_of_questions):

    def approve_question(question_id):
        Question.objects.filter(id = question_id).update(is_valid = True)

    def delete_question(question_id):
        Question.objects.filter(id = question_id).delete()

    # ako se prosledi prazan niz dohvata dohvata random 10 pitanja iz baze
    def get_questions_from_categories(categories):
        
        ret_q_set = Question.objects.none()
        # ako nema odabranih kategorija
        if(not categories):
            ret_q_set = Question.objects.all().order_by('?')[:10]
        else:
            # dohvati pitanja iz svih prosledjenih kategorija i skupi ih u jedan q_set
            for i in range(0,len(categories)):
                q_set = Question.objects.filter(category = categories[i]).order_by('?')[:10]    
                ret_q_set = ret_q_set | q_set

            # izmesaj q_set i uzmi 10 sa vrha
            ret_q_set.order_by('?')[:10]

        return ret_q_set

    # empty db, and add default questions
    def reset_to_default():

        # clear all game question data
        GameQuestions.objects.all().delete()

        # clear all game answer data
        GameAnswers.objects.all().delete()

        # clear all the data from the table
        Question.objects.all().delete()

        # clear all the data from categories table
        Category.objects.all().delete()

        # clear all games data
        Game.objects.all().delete()


        # create a category and create, and fill the database 
        sport = Category.objects.create(name = "Sport")
        sport.save()

        new_question = Question.objects.create(question = 'Koje godine je rodjen Leo Messi?', answer_one = '1987',answer_two = '1990', answer_three = '1986', answer_four='1988', correct = 1, category= sport, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koje godine su se spojile NBA i ABA(American Basketball Association)?', answer_one = '1966',answer_two = '1976', answer_three = '1986', answer_four='1996', correct = 2, category = sport, is_valid = True)
        new_question.save()
 
        new_question = Question.objects.create(question = 'Koja reprezentacija je osvojila prvo svetsko prvenstvo u fudbalu?', answer_one = 'Brazil',answer_two = 'Argentina', answer_three = 'Urugvaj', answer_four='Paragvaj', correct = 3, category = sport, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koji NBA tim ima najvise sampionskih titula?', answer_one = 'Boston Celtics',answer_two = 'LA Lakers', answer_three = 'Golden State Warriors', answer_four='Milwaukee Bucks', correct = 1, category = sport, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'U kom timu je Kristijano Ronaldo zapoceo svoju profesionalnu karijeru?', answer_one = 'Real Madrid',answer_two = 'Mancester junajted', answer_three = 'Sporting', answer_four='Porto', correct = 3, category = sport, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koliko ukupno olimpijskih medalja ima Majkl Felps?', answer_one = '30',answer_two = '28', answer_three = '26', answer_four='24', correct = 2, category = sport, is_valid = True)
        new_question.save()
        
        new_question = Question.objects.create(question = 'Koji tim ima najvise osvojenih titula u Premier ligi(od njenog osnivanja 1992)?', answer_one = 'Liverpul', answer_two = 'Celsi', answer_three = 'Mancester junajted', answer_four='Arsenal', correct = 3, category = sport, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koji je jedini tim u Premier ligi koji je imao savrsenu sezonu(sezonu bez poraza)?', answer_one = 'Liverpul',answer_two = 'Arsenal', answer_three = 'Mancester junajted', answer_four='Mancester siti', correct = 2, category = sport, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Kako se zove covek koji je izmislio kosarku?', answer_one = 'Dzejms Nejsmit',answer_two = 'Dzejms Harden', answer_three = 'Dzejms Lebron', answer_four='Dzejms Bond', correct = 1, category = sport, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koje godine je FK Partizan igrao finale Lige Sampiona?', answer_one = '1946',answer_two = '1956', answer_three = '1966', answer_four='Nikad', correct = 3, category = sport, is_valid = True)
        new_question.save()

        # create a category and create, and fill the database 
        music = Category.objects.create(name = "Music")
        music.save()

        new_question = Question.objects.create(question = 'Koji Jamajcanski reper je 1995 izdao pesmu "Bombastic"?', answer_one = 'Shaggy',answer_two = 'Sean Paul', answer_three = 'Shuggy', answer_four='Shrek th rapper', correct = 1, category= music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Dopunite naslov pesme grupe U2: "Hold me, Thrill Me, Kiss me ..."', answer_one = 'Feel me',answer_two = 'Beat me', answer_three = 'Kill me', answer_four='Miss me', correct = 3, category = music, is_valid = True)
        new_question.save()
 
        new_question = Question.objects.create(question = 'Koje godine su Bitlsi (The Beatles) izdali pesmu "Hey Jude"?', answer_one = '1963',answer_two = '1964', answer_three = '1966', answer_four='1968', correct = 4, category = music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koji Svedski DJ je 2004te izdao pesmu "Call on me"?', answer_one = 'Avicii',answer_two = 'Sweedish House Mafia', answer_three = 'Eric Prydz', answer_four='Tiesto', correct = 3, category = music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Tekst  "Since you\'ve gone I\'ve been lost without a trace /I dream at night I can only see your face" je deo koje Stingove pesme?', answer_one = 'Every breath you take',answer_two = 'Shape of my heart', answer_three = 'Desert rose', answer_four='Englishman in New York', correct = 1, category = music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Tekst "They told him don\'t you ever come around here / Don\'t want to see your face, you better disappear" je deo koje Majkl Dzeksonove pesme?', answer_one = 'Bad',answer_two = 'They don\'t care about us', answer_three = 'Beat it', answer_four='Smooth criminal', correct = 3, category = music, is_valid = True)
        new_question.save()
        
        new_question = Question.objects.create(question = 'Koje godine je preminuo reper Mac Miller?', answer_one = '1998', answer_two = '2008', answer_three = '2017', answer_four='2018', correct = 4, category = music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koje godine je grupa Queen izdala pesmu "Bohemian rhapsody"?', answer_one = '1974',answer_two = '1975', answer_three = '1976', answer_four='1977', correct = 2, category = music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koje godine je rodjen reper Snoop Dogg?', answer_one = '1967',answer_two = '1971', answer_three = '1974', answer_four='1973', correct = 2, category = music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Gde se nalazi Rock\'n\'roll kuca slavnih?', answer_one = 'Springfild',answer_two = 'Nju Jork', answer_three = 'Klivland', answer_four='Hjuston', correct = 3, category = music, is_valid = True)
        new_question.save()

        # create a category and create, and fill the database 
        music = Category.objects.create(name = "Music")
        music.save()

        new_question = Question.objects.create(question = 'Koji Jamajcanski reper je 1995 izdao pesmu "Bombastic"?', answer_one = 'Shaggy',answer_two = 'Sean Paul', answer_three = 'Shuggy', answer_four='Shrek th rapper', correct = 1, category= music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Dopunite naslov pesme grupe U2: "Hold me, Thrill Me, Kiss me ..."', answer_one = 'Feel me',answer_two = 'Beat me', answer_three = 'Kill me', answer_four='Miss me', correct = 3, category = music, is_valid = True)
        new_question.save()
 
        new_question = Question.objects.create(question = 'Koje godine su Bitlsi (The Beatles) izdali pesmu "Hey Jude"?', answer_one = '1963',answer_two = '1964', answer_three = '1966', answer_four='1968', correct = 4, category = music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koji Svedski DJ je 2004te izdao pesmu "Call on me"?', answer_one = 'Avicii',answer_two = 'Sweedish House Mafia', answer_three = 'Eric Prydz', answer_four='Tiesto', correct = 3, category = music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Tekst  "Since you\'ve gone I\'ve been lost without a trace /I dream at night I can only see your face" je deo koje Stingove pesme?', answer_one = 'Every breath you take',answer_two = 'Shape of my heart', answer_three = 'Desert rose', answer_four='Englishman in New York', correct = 1, category = music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Tekst "They told him don\'t you ever come around here / Don\'t want to see your face, you better disappear" je deo koje Majkl Dzeksonove pesme?', answer_one = 'Bad',answer_two = 'They don\'t care about us', answer_three = 'Beat it', answer_four='Smooth criminal', correct = 3, category = music, is_valid = True)
        new_question.save()
        
        new_question = Question.objects.create(question = 'Koje godine je preminuo reper Mac Miller?', answer_one = '1998', answer_two = '2008', answer_three = '2017', answer_four='2018', correct = 4, category = music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koje godine je grupa Queen izdala pesmu "Bohemian rhapsody"?', answer_one = '1974',answer_two = '1975', answer_three = '1976', answer_four='1977', correct = 2, category = music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koje godine je rodjen reper Snoop Dogg?', answer_one = '1967',answer_two = '1971', answer_three = '1974', answer_four='1973', correct = 2, category = music, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Gde se nalazi Rock\'n\'roll kuca slavnih?', answer_one = 'Springfild',answer_two = 'Nju Jork', answer_three = 'Klivland', answer_four='Hjuston', correct = 3, category = music, is_valid = True)
        new_question.save()
        
        # create a category and create, and fill the database 
        geography = Category.objects.create(name = "Geography")
        geography.save()

        new_question = Question.objects.create(question = 'Koji je najseverniji glavni grad na svet?', answer_one = 'Otava',answer_two = 'Rejkjavik', answer_three = 'Ulanbator', answer_four='Helsinki', correct = 1, category= geography, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koja od ovih drzava ima tri glavna grada?', answer_one = 'Juznoafricka republika',answer_two = 'Holandija', answer_three = 'Izrael', answer_four='Bolivia', correct = 1, category = geography, is_valid = True)
        new_question.save()
 
        new_question = Question.objects.create(question = 'Koji je drugi po povrsini najveci kontinent na svetu?', answer_one = 'Afrika',answer_two = 'Severna Amerika', answer_three = 'Juzna Amerika', answer_four='Evvropa', correct = 1, category = geography, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koja zemlja ima najduzu obalu na svetu?', answer_one = 'Australia',answer_two = 'Kanada', answer_three = 'Indonezija', answer_four='Grcka', correct = 2, category = geography, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Kako se zove glavni grad Jordan-a?', answer_one = 'Abu dabi(Abu Dhabi)',answer_two = 'Kito(Quito)', answer_three = 'Aman(Amman)', answer_four='Dakar(Dakar)', correct = 3, category = geography, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Kako se zove glavni grad Gane', answer_one = 'Beirut(Beirut)',answer_two = 'Manila(Manilla)', answer_three = 'Akra(Accra)', answer_four='Kinsasa(Kinshasa)', correct = 3, category = geography, is_valid = True)
        new_question.save()
        
        new_question = Question.objects.create(question = 'Kako se zove glavni grad Nigerije?', answer_one = 'Gitega(Gitega)', answer_two = 'Harare(Harare)', answer_three = 'Abudza(Abuja)', answer_four='Aman(Amman)', correct = 3, category = geography, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koji je bio glavni grad Obale slonovace od 1933 do 1983 godine?', answer_one = 'Daloa',answer_two = 'Kumasi', answer_three = 'Abidjan', answer_four='San Pedro', correct = 3, category = geography, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koji je bio glavni grad Zapadne Nemacke od 1949 do 1990', answer_one = 'Zapadni Berlin',answer_two = 'Bon', answer_three = 'Stutgart', answer_four='Bremen', correct = 3, category = geography, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koji je bio glavni grad Kine od 1945 do 1949?', answer_one = 'Nanking',answer_two = 'Chang\'an', answer_three = 'Kaifeng', answer_four='Hangzhou', correct = 1, category = geography, is_valid = True)
        new_question.save()
        

        # NOTE dovrsiti popunjavanje za istoriju
        # create a category and create, and fill the database 
        history = Category.objects.create(name = "History")
        history.save()

        new_question = Question.objects.create(question = 'Koja istorijska licnost je zivela od 1758 do 1794?', answer_one = 'Fernando Magelan',answer_two = 'Maksimilijan Robespijer', answer_three = 'Frencis Bejkon', answer_four='Napoleon', correct = 1, category= history, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Kako se zove Portugalski istrazivac koji je poznat kao prvi Evropljanin koji je doplovio do Indije kroz Rt Dobre Nade?', answer_one = 'Amerigo Vespuci',answer_two = 'Vasko Da Gama', answer_three = 'Francisko Pizaro', answer_four='Bartolomeo Dijaz', correct = 2, category = history, is_valid = True)
        new_question.save()
 
        new_question = Question.objects.create(question = 'Kako se zove prvi istrazivac koji je tvrdio da Kolumbo nije doplovio do istocne Azije, vec do novog(do tada nepoznatog) sveta?', answer_one = 'Amerigo Vespuci',answer_two = 'Marko Polo', answer_three = 'Bartolomeo Dijaz', answer_four='Francisko Pizaro', correct = 1, category = history, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'U kom gradu je izvrsen atentat na Abrahama Linkolna?', answer_one = 'Vasington DC',answer_two = 'Nju Jork', answer_three = 'Atlanta', answer_four='Ricmond', correct = 2, category = history, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'U kom gradu je izvrsen atentat na Dzona F. Kenedija?', answer_one = 'Nju Jork',answer_two = 'Nju Orleans', answer_three = 'Dalas', answer_four='Vasington DC', correct = 3, category = history, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = '', answer_one = 'Beirut(Beirut)',answer_two = 'Manila(Manilla)', answer_three = 'Akra(Accra)', answer_four='Kinsasa(Kinshasa)', correct = 3, category = history, is_valid = True)
        new_question.save()
        
        new_question = Question.objects.create(question = 'Kako se zove glavni grad Nigerije?', answer_one = 'Gitega(Gitega)', answer_two = 'Harare(Harare)', answer_three = 'Abudza(Abuja)', answer_four='Aman(Amman)', correct = 3, category = history, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koji je bio glavni grad Obale slonovace od 1933 do 1983 godine?', answer_one = 'Daloa',answer_two = 'Kumasi', answer_three = 'Abidjan', answer_four='San Pedro', correct = 3, category = history, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koji je bio glavni grad Zapadne Nemacke od 1949 do 1990', answer_one = 'Zapadni Berlin',answer_two = 'Bon', answer_three = 'Stutgart', answer_four='Bremen', correct = 3, category = history, is_valid = True)
        new_question.save()

        new_question = Question.objects.create(question = 'Koji je bio glavni grad Kine od 1945 do 1949?', answer_one = 'Nanking',answer_two = 'Chang\'an', answer_three = 'Kaifeng', answer_four='Hangzhou', correct = 1, category = history, is_valid = True)
        new_question.save()

        
class GameQuestions(models.Model):
    """
    Table that contains all the questions for 
    a certain game.
    """
    class Meta:
        unique_together = (('game', 'index'),)

    game       = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    index      = models.IntegerField()
    question   = models.ForeignKey(Question, on_delete=models.DO_NOTHING)
    p1_pts = models.IntegerField(default=0)
    p2_pts = models.IntegerField(default=0)
    p3_pts = models.IntegerField(default=0)
    p4_pts = models.IntegerField(default=0)

    def __str__(self):
        return '{}, {}, {}'.format(self.game, self.index, self.question)

class GameAnswers(models.Model):
    """
    Table that contains the users answers for each question
    in a game.
    """
    class Meta:
        unique_together = (('game', 'user', 'question_index'),)

    game           = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    question_index = models.IntegerField()

    # Answer information, not required.
    answer_index   = models.IntegerField()
    correct        = models.BooleanField()
class Report(models.Model):
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_f1', on_delete=models.DO_NOTHING)
    reported = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_f2', on_delete=models.DO_NOTHING)
    report_text = models.TextField(max_length = 200)    


    def __str__(self):  
        return "Reporter : " + str(self.reporter) + " Reported :" + str(self.reported) + " beceause of :" + str(self.report_text)

    def add_report(reporter, reported, text):
        report = Report.objects.create(reporter = reporter, reported = reported, report_text = text)
        report.save()


    # report is valid if reported is still active - 
    # if admin decides that report is not valid, it will be removed, 
    # and if he decides otherwise user will not be active anymore
    def list_valid_reports():    
        return Report.objects.filter(reported__is_active = True)

    def deny_report(report_id):
        Report.objects.filter(id = report_id).delete()

    def approve_report(report_id):
        reported = Report.objects.filter(id = report_id).values('reported')[0]
        rep_id = reported['reported']
        User.objects.filter(id = rep_id).update(is_active = False)    

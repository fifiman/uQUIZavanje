from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse
from django.db.models import Q


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
    picture = models.TextField(default = " ", max_length = 50, blank = True, null = True)
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

    # gets 10 best players overall
    def get_global_top_10():
        #return User.objects.raw("SELECT * FROM quiz_User WHERE level >= 10 ORDER BY ranking desc")[:10]
        return User.objects.filter(level >= 10).order_by(ranking)[:10]
    
    #returns all users who want to be modeators, and are eligible for the role
    def get_moderator_candidates():
        return User.objects.filter(wants_moderator = True, is_moderator = False, level >= 10)    

    # returns all users who are not banned
    def get_acitive_users():
        return User.objects.filter(is_active = True)


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
        return Friendship.objects.filter(first_firend_id = user).filter(second_friend_id__level>=10).order_by(second_friend_id__ranking)[:10]

    
    # should return list of friends ordered by username
    def get_friends(user):
        return Friendship.objects.filter(first_friend_id = user).order_by(second_friend_id__username)    
        
    # gets all friend request that the user has sent    
    def get_sent_friend_requests(user):
        return Friendship.objects.filter(first_friend_id = user, accepted = False)

    # gets all friend requests that a user has recieved
    def get_recieved_friend_requests(user):
        return Friendship.objects.filter(second_friend_id = user, accepted = False)    


#class containing all game relevant data
class Game(models.Model):
    player_one = models.ForeignKey(settings.AUTH_USER_MODEL,related_name = '%(class)s_p1', on_delete=models.DO_NOTHING)
    player_two = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_p2',on_delete=models.DO_NOTHING)
    player_three = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_p3', on_delete=models.DO_NOTHING)
    player_four = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_p4', on_delete=models.DO_NOTHING)
    
    player_one_pts = models.IntegerField()
    player_two_pts = models.IntegerField()
    player_three_pts = models.IntegerField()
    player_four_pts = models.IntegerField()

    winner = models.IntegerField()
    '''
    def number_of_wins(user):
        return Game.objects.filter()
    def number_of_games_played():
    '''


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


    #NOTE Dodaj proveru da su svi odgovori razliciti
    def submit_a_question(question_in, answer_one_in, answer_two_in, answer_three_in, answer_four_in, correct_in, category_in):
        new_question = Question.objects.create(question = question_in, answer_one = answer_two_in,answer_two = answer_two_in, answer_three=answer_three_in, answer_four=answer_four_in, correct=correct_in, category=category_in)
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
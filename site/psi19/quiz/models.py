from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField( max_length=50)
    age = models.IntegerField(default = 0, blank = True, null = True)
    level = models.IntegerField(default = 0)
    picture = models.TextField(default = " ", max_length = 50, blank = True, null = True)
    banned = models.TextField(default = "", max_length = 50, blank = True, null = True)
    is_moderator = models.BooleanField(default = False)
    ranking = models.IntegerField(default = -1)

    def __str__(self):
        temp = str(self.user) + " Level: " + str(self.level)
        if self.level >= 10:
            temp = temp + " Rating: " + str(self.ranking) 

        return temp

    def is_moderator(self):
        return self.is_moderator

    def is_senior(self):    
        return self.level >= 10
    
    def get_global_top_10():
        return User.objects.raw("SELECT * FROM quiz_User WHERE level > 10 ORDER BY ranking desc")[:10]




# Connects two users, and allows them to see eachothers profiles, and play with eachother
class Friendship(models.Model):
    first_friend_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_f1', on_delete=models.DO_NOTHING)
    second_friend_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name = '%(class)s_f2', on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.first_friend_id) + " " + str(self.second_friend_id)

    def already_friends(user1, user2):

        count1 = Friendship.objects.filter(first_friend_id = user1, second_friend_id = user2).count()
        count2 = Friendship.objects.filter(first_friend_id = user2, second_friend_id = user1).count()

        if (count1 + count2) > 0:
            return True
        else:
            return False    

    def follow(user1, user2):
        if(user1 != user2):
            friendship = Friendship.objects.create(first_friend_id = user1,second_friend_id = user2)
            friendship.save()

    def unfollow(user1, user2):
        if(user1 != user2):
            friendship = Friendship.objects.filter(first_friend_id = user1,second_friend_id = user2)[0]
            friendship.delete()          

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
    category = models.OneToOneField(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Question:" + self.question + " Answers: " + self.answer_one + " " + self.answer_two + " " + self.answer_three + " " + self.answer_four

    def submit_a_question(question_in, answer_one_in, answer_two_in, answer_three_in, answer_four_in, correct_in, category_in):
        new_question = Question.objects.create(question = question_in, answer_one = answer_two_in,answer_two = answer_two_in, answer_three=answer_three_in, answer_four=answer_four_in, correct=correct_in, category=category_in)
        new_question.save()
        
    #query the db for speceific questions
    #def get_question_from_category(category, number_of_questions):


    
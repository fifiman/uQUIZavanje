from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Django's user already has
# username
# email
# first name
# last name
# staff status
# User profile will contain everything else
# and have 1-1 relationship with user
class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    level = models.IntegerField()
    picture = models.TextField(max_length = 50)
    banned = models.TextField(max_length = 50)

# User whose level is above 10
class Senior_user(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    is_moderator = models.BooleanField(default = False)
    ranking = models.IntegerField()

    def __str__(self):
        return str(self.user) + str(self.ranking)

    def get_global_top_10():
        return Senior_user.objects.order_by('ranking')[:10]


# IMPORTANT - table admin is unnecessary because of the staff member part of user
# TODO - check out if staff members helps with is_moderator

# Connects two users, and allows them to see eachothers profiles, and play with eachother
class Friendship(models.Model):
    first_friend_id = models.ForeignKey(User, related_name = '%(class)s_f1', on_delete=models.DO_NOTHING)
    second_friend_id = models.ForeignKey(User, related_name = '%(class)s_f2', on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.first_friend_id + " " + self.second_friend_id

#class containing all game relevant data
class Game(models.Model):
    player_one = models.ForeignKey(User,related_name = '%(class)s_p1', on_delete=models.DO_NOTHING)
    player_two = models.ForeignKey(User, related_name = '%(class)s_p2',on_delete=models.DO_NOTHING)
    player_three = models.ForeignKey(User, related_name = '%(class)s_p3', on_delete=models.DO_NOTHING)
    player_four = models.ForeignKey(User, related_name = '%(class)s_p4', on_delete=models.DO_NOTHING)
    
    player_one_pts = models.IntegerField()
    player_two_pts = models.IntegerField()
    player_three_pts = models.IntegerField()
    player_four_pts = models.IntegerField()

    winner = models.IntegerField()

#class containing all question relevant data
class Question(models.Model):
    question = models.TextField(max_length = 100)
    is_valid = models.BooleanField(default = False)
    answer_one = models.TextField(max_length = 100)
    answer_two = models.TextField(max_length = 100)
    answer_three = models.TextField(max_length = 100)
    answer_four = models.TextField(max_length = 100)
    correct = models.IntegerField()

    def __str__(self):
        return "Question:" + self.question + " Answers: " + self.answer_one + " " + self.answer_two + " " + self.answer_three + " " + self.answer_four

class Category_sports(models.Model):
    id_global = models.OneToOneField(Question, on_delete=models.CASCADE) 
    
class Category_history(models.Model):
    id_global = models.OneToOneField(Question, on_delete=models.CASCADE) 

class Category_geography(models.Model):
    id_global = models.OneToOneField(Question, on_delete=models.CASCADE) 

class Category_music(models.Model):
    id_global = models.OneToOneField(Question, on_delete=models.CASCADE) 
                
class Category_movies(models.Model):
    id_global = models.OneToOneField(Question, on_delete=models.CASCADE) 
    
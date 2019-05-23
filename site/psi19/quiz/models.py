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
    picture = models.TextField(max_length = 50, blank = True, null = True)
    banned = models.TextField(max_length = 50, blank = True, null = True)
    is_moderator = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)
    ranking = models.IntegerField(default = -1)

    def __str__(self):
        temp = str(self.user) + " Level: " + str(self.level)
        if self.level >= 10:
            temp = temp + " Rating: " + str(self.ranking) 

        return temp


    def get_global_top_10():
        return User_profile.objects.raw("SELECT * FROM quiz_User_profile WHERE level > 10 ORDER BY ranking desc")[:10]




# IMPORTANT - table admin is unnecessary because of the staff member part of user
# TODO - check out if staff members helps with is_moderator

# Connects two users, and allows them to see eachothers profiles, and play with eachother
class Friendship(models.Model):
    first_friend_id = models.ForeignKey(User, related_name = '%(class)s_f1', on_delete=models.DO_NOTHING)
    #idk why ...
    second_friend_id = models.ForeignKey(User, related_name = '%(class)s_f2', on_delete=models.DO_NOTHING, default = -1)


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
    answer_one = models.TextField(max_length = 100)
    answer_two = models.TextField(max_length = 100)
    answer_three = models.TextField(max_length = 100)
    answer_four = models.TextField(max_length = 100)
    correct = models.IntegerField()
    category = models.OneToOneField(Category, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Question:" + self.question + " Answers: " + self.answer_one + " " + self.answer_two + " " + self.answer_three + " " + self.answer_four

    #query the db for speceific questions
    #def get_question_from_category(category, number_of_questions):


    
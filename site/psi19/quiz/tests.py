from django.test import TestCase
from quiz.models import *
from django.conf import settings

# Create your tests here.
class EngineTestCase(TestCase):
    # Class constants
    CUR_USER = 1
    USER_PREFIX = 'user_'
    EMAIL_POSTFIX = '@nenad.com'

    def create_random_user():
        # Get user id.
        id = EngineTestCase.CUR_USER
        EngineTestCase.CUR_USER += 1

        # Create needed user info.
        username = EngineTestCase.USER_PREFIX + str(id)
        email = str(id) + EngineTestCase.EMAIL_POSTFIX

        return User.objects.create(username=username, email=email)

    def create_random_question(category):
        return Question.objects.create(question='What is correct?', is_valid=True,
                                       answer_one='Ans 1', answer_two='Ans 2', 
                                       answer_three='Ans 3', answer_four='Ans 4',
                                       correct=0, category=category)

    def setUp(self):
        """
        Do some setting up maybe.
        """
        self.user1 = EngineTestCase.create_random_user()
        self.user2 = EngineTestCase.create_random_user()
        self.user3 = EngineTestCase.create_random_user()
        self.user4 = EngineTestCase.create_random_user()

        self.category1 = Category.objects.create(name='Category #1')

        self.question_1 = EngineTestCase.create_random_question(self.category1)
        self.question_2 = EngineTestCase.create_random_question(self.category1)
        self.question_3 = EngineTestCase.create_random_question(self.category1)
        self.question_4 = EngineTestCase.create_random_question(self.category1)

        self.game = Game.objects.create()

        # Add question to game.
        GameQuestions.objects.create(game=self.game, index=0, question=self.question_1)
        GameQuestions.objects.create(game=self.game, index=1, question=self.question_2)
        GameQuestions.objects.create(game=self.game, index=2, question=self.question_3)
        GameQuestions.objects.create(game=self.game, index=3, question=self.question_4)

    def test_start_game_no_players(self):
        """
        Start game with no players, raises Exception.
        """
        self.assertRaises(Exception, self.game.start_game)

    def test_too_many_players_join(self):
        """
        Join the same player multiple times.
        """
        self.game.join_game(self.user1)
        self.game.join_game(self.user2)
        self.game.join_game(self.user3)
        self.game.join_game(self.user4)

        self.assertRaises(Exception, self.game.join_game, self.user1)

    def test_blah(self):
        self.assertEqual(True, True)

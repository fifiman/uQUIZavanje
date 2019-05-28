

class Engine:
    """
    Game engine for quiz.

    Contains all logic to serve clients/players in a synchronous fashion.
    """

    # Class constats.
    NUM_ANSWERS = 4     # Num of answers per question.
    MAX_PLAYERS = 4     # Maximum number of players.

    # Game states encoded as integers.
    GAME_NOT_STARTED    = 0
    GAME_IN_PLAY        = 1
    GAME_OVER           = 2


    def __init__(self, questions, answers, answer_texts):
        self.questions = questions          # List of questions in text format.
        self.answers   = answers            # ID of correct answer for each question.
        self.answer_texts = answer_texts    # Text of each answer in Nx4 matrix format.

        self.num_questions = len(self.questions)

        # User answers will be stored as a matrix.
        # This will be initialized once the game starts and
        # the number of players are known.
        self.players_answers = None

        # Game state information.
        self.cur_question = -1  # Current question we are at, -1 means we have not begun.
        self.num_players = 0    # Number of players in the room.
        self.num_answers = 0    # Number of players that have answered the current question.
        self.winner_id   = -1   # Player id of that player that won.

        self.game_state = Engine.GAME_NOT_STARTED

    def start_game(self):
        if self.cur_question != -1:
            raise Exception('Game has already been started.')
        
        if self.num_players == 0:
            raise Exception('No players inside game, nothing to start.')

        # Start the game.
        self.game_state = Engine.GAME_IN_PLAY

        self.cur_question = 0
        self.players_answers = [[-1 for _ in range(self.num_players)] for _ in range(self.num_questions)]

        print ('Game has started.')

    def answer(self, player_id, question_id, answer_index):
        # Check all input parameters.
        if player_id < 0 or player_id >= self.num_players:
            raise Exception('Player id is out of range for the current room: {}.'.format(player_id))

        if question_id < 0 or question_id >= self.num_questions:
            raise Exception('Question id is out of range for the current room: {}.'.format(question_id))

        if answer_index < 0 or answer_index >= Engine.NUM_ANSWERS:
            raise Exception('Answer id is out of range for the current room: {}.'.format(answer_index))

        # Check that the game has not started.
        if self.game_state == Engine.GAME_NOT_STARTED:
            raise Exception('Cannot answer question before the game has started.')
        
        # Check that the game has ended.
        if self.game_state == Engine.GAME_OVER:
            raise Exception('Cannot answer once game is over.')

        # Check if user is not trying to answer the current question.
        if self.cur_question != question_id:
            raise Exception('Cannot answer question that is not the current question.')

        # Check that the user has not answered already.
        has_answered_before = (self.players_answers[question_id][player_id] != -1)

        if has_answered_before:
            return Exception('User has already answered question before.')

        # Otherwise save answer and return whether the answer is correct.
        self.players_answers[question_id][player_id] = answer_index

        # Move on to next question if all players have answered the current question.
        self._update_current_question()

        return answer_index == self.answers[question_id]

    def _update_current_question(self):
        all_players_answered = True  # Assume true until a negative is found.

        for player_id in range(self.num_players):
            if self.players_answers[self.cur_question][player_id] == -1:
                all_players_answered = False

        if all_players_answered:
            self.cur_question += 1
        
        # Check whether all questions have been exhausted.
        if self.cur_question == self.num_questions:
            self.game_state = Engine.GAME_OVER

    def get_state(self):
        """
        Return game state as a JSON string.
        State consists of whether the game has started, in-play, or game over. With
        extra information for each of those.
        """

        base_state = {
            'game_state'        : self.game_state,
            'num_players'       : self.num_players,
        }

        if self.game_state == Engine.GAME_NOT_STARTED:
            cur_state = {}
        elif self.game_state == Engine.GAME_IN_PLAY:
            cur_state = {
                'question_id'       : self.cur_question,
                'question_text'     : self.questions[self.cur_question],
                'answers_text'      : self.answer_texts[self.cur_question],
            }
        elif self.game_state == Engine.GAME_OVER:
            cur_state = {
                'winner_id'         : self.winner_id
            }

        # Merge both state dicts into one and return.
        state = {**base_state, **cur_state}
        return state

    def join_game(self):
        """
        Player requests to join the game.
        They will be rejected if the game has started or exceeds the maximum number of players.

        Returns:
            Boolean representing whether the player successfully joined or not.
        """

        can_join = (self.game_state == Engine.GAME_NOT_STARTED) and (self.num_players < Engine.MAX_PLAYERS)

        if can_join:
            new_player_id = self.num_players
            self.num_players += 1

            return new_player_id
        else:
            return None

if __name__ == '__main__':

    questions = ['Which year is the oldest?', 'Which year is the youngest?']
    answers = [3, 0]
    answer_texts = [['1', '2', '3', '4'], ['1', '2', '3', '4']]

    game = Engine(questions, answers, answer_texts)

    # Players join.
    p1_id = game.join_game()
    p2_id = game.join_game()

    # Start game.
    game.start_game()

    # Answer first round of questions.
    print (game.answer(p1_id, 0, 0))        # Wrong answer.
    print (game.answer(p2_id, 0, 3))        # Correct answer.

    # Answer second round of question.
    print (game.answer(p1_id, 1, 1))        # Wrong answer.
    print (game.answer(p2_id, 1, 2))        # Wrong answer.

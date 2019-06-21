from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings

from .models import Game, User


class GameConsumer(AsyncJsonWebsocketConsumer):
    """
    Consumer through which client connects to game engine. 
    """

    async def connect(self):
        # Validate user somehow.
        '''
            Vrsi konekciju
            
            @param GameConsumer self
            
            @return void
        '''
        
        self.game_id = str(self.scope['url_route']['kwargs']['game_id']).strip()
        self.user    = self.scope['user']

        print ('User:', self.user, ',Entered game:', self.game_id)

        await self.accept()

        # Add this connection to the group.
        await self.channel_layer.group_add(
            self.game_id,
            self.channel_name,
        )

        # Send game state after a user joins.
        await self.send_state_to_group()
    
    async def send_state_to_group(self):
        '''
            Get game state.
            
            @param GameConsumer self
            
            @return void
        '''
        game = await get_game_or_error(int(self.game_id))
        game_state = game.get_state()

        await self.channel_layer.group_send(
            self.game_id,
            {
                'type':     'game.sendstate',
                'state':    game_state
            }
        )

    async def force_refresh_to_group(self):
        await self.channel_layer.group_send(
            self.game_id,
            {
                'type':     'force.reload'
            }
        )
    
    async def group_send_next_question(self, question):
        '''
            Salje sledece pitanje
            
            @param GameConsumer self, Question question
            
            @return void
        '''
        
        await self.channel_layer.group_send(
            self.game_id,
            {
                'type':     'send.nextquestion',
                'question': question.question,
                'answers': [
                    question.answer_one,
                    question.answer_two,
                    question.answer_three,
                    question.answer_four,
                ],
                'correct_ind': question.correct
            }
        )

    async def receive_json(self, content):
        
        '''
            Metoda za prijem poruka
            
            
            @param GameConsumer self, JSON content
            
            @return void
        '''
        print (content)

        command = content.get('command', None)

        try:
            if command == "start_game":
                # Make them join the room
                game = await get_game_or_error(int(self.game_id))

                start_game_status = game.start_game()
                assert start_game_status == True    # Throw exception if cannot start the game.

                # Send game state after a user joins.
                await self.send_state_to_group()
            elif command == 'answer':
                answer_ind = content['answer_ind']
                user_id    = content['user_id']
                msPassed   = content['msPassed']
                game = await get_game_or_error(int(self.game_id))
                user = await get_user_or_error(int(user_id))

                is_correct, state_changed = game.answer(user, answer_ind, msPassed)

                if state_changed:
                    if game.game_state != Game.GAME_OVER:
                        question = await get_games_current_question(game)
                        await self.group_send_next_question(question)
                    else:
                        await self.force_refresh_to_group()

        except Exception as e:
            # Catch any errors and send it back
            await self.send_json({
                'error':    str(e)
            })

    async def disconnect(self, close_code):
        '''
        
            Poziva se pri prekidu konekcije
            
            @param GameConsumer self, Question question
            
            @return void
        '''
        
        
        await self.channel_layer.group_discard(
            self.game_id,
            self.channel_name,
        )

        # Remove user from game.
        game = await get_game_or_error(int(self.game_id))
        if game.game_state == 0:
            game.leave_game(self.user)

        # Send state to other users.
        await self.send_state_to_group()

        await self.close()

    ###     Group handlers      ###
    async def game_sendstate(self, event):
        """
        Sending state to user.
        """
        await self.send_json(
            {
                'msg_type':     settings.MSG_TYPE_UPDATE_STATE,
                'state':        event['state']
            },
        )
    
    async def send_nextquestion(self, event):
        """

        """
        # Add message type to event and send that.
        event['msg_type'] = settings.MSG_TYPE_NEXT_QUESTION,
        await self.send_json(event)
    
    async def force_reload(self, event):
        """
        Send to all users to reload page.
        """
        await self.send_json(
            {
                'msg_type':     settings.MSG_TYPE_FORCE_REFRESH,
            },
        )

@database_sync_to_async
def get_game_or_error(game_id):
    '''
        Dohvata partiju iz baze
        
        @param game_id
        
        @return Game
            
    '''
    try:
        game = Game.objects.get(id=game_id)
        return game
    except Game.DoesNotExist:
        raise Exception("BAAD, game does not exist.")

@database_sync_to_async
def get_user_or_error(user_id):
    
    '''
    
        Dohvata korisnika iz baze
        
        @param user_od
        
        @return User
    '''
    
    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        raise Exception("BAAD, user does not exist.")

@database_sync_to_async
def get_games_current_question(game):
    '''
        Dohvata trenutno pitanje iz baze
        
        @param game
        
        @return Question
    '''
    return game.get_current_question()

class UserConsumer(AsyncJsonWebsocketConsumer):
    """
    Consumer through which clients connect with eachother. 
    """

    async def connect(self):
        # on connection we get users id and add him to his group 
        '''
            Vrsi konekciju
            
            @param UserConsumer self
            
            @return void
        '''
        
        self.user_id = str(self.scope['url_route']['kwargs']['user_id']).strip()

        await self.accept()
        
        print(self.user_id)

        # Add this connection to the group.
        await self.channel_layer.group_add(
            self.user_id,
            self.channel_name,
        )
        # after user connects might update his status later, for now nothin'
        # await self.send_state_to_group()
        # send state to friends or sth like that 
    
    async def receive_json(self, content):
        '''
            Metoda za prijem poruka
            
            
            @param UserConsumer self, JSON content
            
            @return void
        '''
        
        command = content.get('command', None)

        try:
            if command == "join_my_game":
                
                # id of the recipient
                id_to = content.get('id')
                # id of the game sender wants you to join
                game_id = content.get('game_id')
                # username of the player who sends the invite
                sender = content.get('sender')

                # Send the request to the group with userid
                await self.channel_layer.group_send(
                    str(id_to),
                    {
                        'type'    : 'notify',
                        'game_id' : game_id,
                        'sender'  : sender,  
                    }
                )
                
        except Exception as e:
            # Catch any errors and send it back
            await self.send_json({
                'error':    str(e)
            })

    async def disconnect(self, close_code):
        '''
        Poziva se pri prekidu konekcije
        
        @parmas UserConsumer self
        
        @ return void
        '''
        await self.channel_layer.group_discard(
            self.user_id,
            self.channel_name,
        )

        await self.close()

    async def notify(self, event):        
        # send json message to the recipient, inviting him to game_id
        '''
        Salje primaocu notifikaciju
        
        @parmas UserConsumer self, Event event
        @ return void
        '''
        await self.send_json(
            {
                'game_id'  :    event["game_id"],
                'username' :    event['sender'],
            },
        ) 

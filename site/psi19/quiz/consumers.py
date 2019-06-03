from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings

from .models import Game


class GameConsumer(AsyncJsonWebsocketConsumer):
    """
    Consumer through which client connects to game engine. 
    """

    async def connect(self):
        # Validate user somehow.

        self.game_id = str(self.scope['url_route']['kwargs']['game_id']).strip()
        print ([self.game_id])
        print (self.game_id)
        await self.accept()

        # Add this connection to the group.
        await self.channel_layer.group_add(
            self.game_id,
            self.channel_name,
        )

        # Send game state after a user joins.
        await self.send_state_to_group()
    
    async def send_state_to_group(self):
        # Get game state.
        game = await get_game_or_error(int(self.game_id))
        print (game)
        game_state = game.get_state()

        await self.channel_layer.group_send(
            self.game_id,
            {
                'type':     'game.getstate',
                'state':    game_state
            }
        )


    async def receive_json(self, content):
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
                
                game = await get_game_or_error(int(self.game_id))

        except Exception as e:
            # Catch any errors and send it back
            await self.send_json({
                'error':    str(e)
            })

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.game_id,
            self.channel_name,
        )

        await self.close()

    ###     Group handlers      ###
    async def game_getstate(self, event):
        """
        Sending state to user.
        """
        await self.send_json(
            {
                'msg_type':     settings.MSG_TYPE_UPDATE_STATE,
                'state':        event['state']
            },
        )


@database_sync_to_async
def get_game_or_error(game_id):
    try:
        game = Game.objects.get(id=game_id)
        return game
    except Game.DoesNotExist:
        raise Exception("BAAD, game does not exist.")

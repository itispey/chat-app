from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Chat, Message, User
import json


class JoinAndLeave(WebsocketConsumer):
    def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['id']
        self.room_group_name = f'chat_{self.room_id}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_id = self.scope['user'].id

        user = User.objects.get(id=user_id)
        chat = Chat.objects.get(id=self.room_id)

        db_insert = Message(sender=user, content=message, chat=chat)
        db_insert.save()

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {'type': 'chat_message', 'message': f'{user.username}: {message}'}
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps({'message': message}))

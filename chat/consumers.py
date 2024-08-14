from channels.generic.websocket import SyncConsumer,AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .models import Chat,Group

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('Websocket Connected....', event)
        print('Channel layer....', self.channel_layer)
        print('Channel name....', self.channel_name)

        # print('Group name',self.scope['url_route']['kwargs']['groupkaname'])
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']

        async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print('Message Received....', event['text'])
        data = json.loads(event['text'])

        group = Group.objects.get(name = self.group_name)

        chat = Chat(
            content = data['msg'],
            group = group
        )
        chat.save()
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "chat.message",
                "message": event['text'],
            },
        )

    def chat_message(self, event):
        print('Event...',event)
        self.send({
            'type':'websocket.send',
            'text': event['message']
        })
        
        
    def websocket_disconnect(self, event):
        print('Websocket Disconnected....', event)
        print('Channel layer....', self.channel_layer)
        print('Channel name....', self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
        raise StopConsumer()

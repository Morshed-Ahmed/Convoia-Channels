# from channels.generic.websocket import SyncConsumer,AsyncConsumer
# from channels.exceptions import StopConsumer
# from asgiref.sync import async_to_sync
# import json
# from .models import Chat,Group

# class MySyncConsumer(SyncConsumer):
#     def websocket_connect(self, event):
#         print('Websocket Connected....', event)
#         print('Channel layer....', self.channel_layer)
#         print('Channel name....', self.channel_name)

#         # print('Group name',self.scope['url_route']['kwargs']['groupkaname'])
#         self.group_name = self.scope['url_route']['kwargs']['groupkaname']

#         async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
#         self.send({
#             'type': 'websocket.accept'
#         })

#     def websocket_receive(self, event):
#         print('Message Received....', event['text'])
#         data = json.loads(event['text'])

#         group = Group.objects.get(name = self.group_name)
#         if self.scope['user'].is_authenticated:
#             chat = Chat(
#                 content = data['msg'],
#                 username = self.scope['user'],
#                 group = group
#             )
#             chat.save()
#             # print('kk',chat.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
#             data['username'] = self.scope['user'].username
#             data['timestamp'] = chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')
#             async_to_sync(self.channel_layer.group_send)(
#                 self.group_name,
#                 {
#                     "type": "chat.message",
#                     "message": json.dumps(data)
#                 },
#             )
#         else:
#             self.send({
#                     'type':'websocket.send',
#                     'text': json.dumps({'msg':'Login Required'})
#             })

#     def chat_message(self, event):
#         print('Event...',event)
#         self.send({
#             'type':'websocket.send',
#             'text': event['message']
#         })
        
        
#     def websocket_disconnect(self, event):
#         print('Websocket Disconnected....', event)
#         print('Channel layer....', self.channel_layer)
#         print('Channel name....', self.channel_name)
#         async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
#         raise StopConsumer()



from channels.generic.websocket import SyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .models import Chat, Group

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print('Websocket Connected....', event)
        print('Channel layer....', self.channel_layer)
        print('Channel name....', self.channel_name)

        # Group name from URL
        self.group_name = self.scope['url_route']['kwargs']['groupkaname']

        # Add this channel to the group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name, 
            self.channel_name
        )
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print('Message Received....', event['text'])
        data = json.loads(event['text'])

        # Check if the incoming data is a message
        if 'msg' in data:
            group = Group.objects.get(name=self.group_name)
            if self.scope['user'].is_authenticated:
                chat = Chat(
                    content=data['msg'],
                    username=self.scope['user'],
                    group=group
                )
                chat.save()
                data['username'] = self.scope['user'].username
                data['timestamp'] = chat.timestamp.strftime('%Y-%m-%d %H:%M:%S')
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        "type": "chat.message",
                        "message": json.dumps(data)
                    },
                )
            else:
                self.send({
                    'type': 'websocket.send',
                    'text': json.dumps({'msg': 'Login Required'})
                })
        elif 'typing' in data:
            # Handle typing indicator
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "chat.typing",
                    "username": self.scope['user'].username,
                    "typing": data['typing']
                },
            )

    def chat_message(self, event):
        print('Event...', event)
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    def chat_typing(self, event):
        print('Typing Event...', event)
        self.send({
            'type': 'websocket.send',
            'text': json.dumps({
                'username': event['username'],
                'typing': event['typing']
            })
        })

    def websocket_disconnect(self, event):
        print('Websocket Disconnected....', event)
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, 
            self.channel_name
        )
        raise StopConsumer()

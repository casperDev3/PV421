import json
from channels.generic.websocket import AsyncWebsocketConsumer

room_state = {
    "color": "#ffffff",
    "counter": 0
}


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # name of the room/group
        self.group_name = 'global_notifications'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type_notification': event['type_notification'],
            'message': event['message'],
            'sender': str(event['sender'])
        }))


class InteractiveConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'interactive_room'
        # self.user_id = self.user_id = self.scope['url_route']['kwargs'].get('user_id', 'anon')
        # print(self.user_id)

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        await self.send(text_data=json.dumps({
            "type": "sync",
            "state": room_state
        }))
        print("Клієнт підключився до інтерактивної кімнати!")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        print("Клієнт відключився від інтерактивної кімнати!")

    async def receive(self, text_data=None, bytes_data=None):
        global room_state
        data = json.loads(text_data)
        command = data.get("command")

        if command == "change_color":
            new_color = data.get("color")
            room_state["color"] = new_color
        elif command == "increment":
            room_state["counter"] += 1
        elif command == "reset":
            room_state["counter"] = 0

        print(room_state["counter"])
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "broadcast_state",
                "state": room_state
            }
        )
    async def broadcast_state(self,  event):
        await self.send(text_data=json.dumps({
            "type": "update",
            "state": event["state"]
        }))

class MassMailerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'mass_mailer'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_mass_mail_update(self, event):
        print(event['message'])
        # await self.send(text_data=json.dumps({
        #     'status': event['status'],
        #     'progress': event['progress'],
        #     'message': event['message']
        # }))
# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils import timezone
from .models import Message
from authentication.models import CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.receiver = await self.get_receiver_user(self.room_name)
        # group for the two users
        self.room_group_name = f"chat_{'_'.join(sorted([self.user.username, self.receiver.username]))}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # increment connection count -> mark user online if first connection
        await self.increment_connections(self.user)

        # broadcast presence update
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "presence_update",
                "username": self.user.username,
                "status": "online"
            }
        )

        # mark messages from the other user as seen (receiver's unread messages become seen)
        # and notify sender(s)
        updated = await self.mark_messages_as_seen(self.receiver, self.user)
        if updated:
            await self.channel_layer.group_send(
                self.room_group_name,
                {"type": "message_seen", "seen_by": self.user.username}
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # decrement connection count -> mark offline when zero
        await self.decrement_connections(self.user)

        # broadcast presence update (include last_seen so UI can show it)
        last_seen = timezone.localtime(timezone.now()).strftime("%I:%M %p")
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "presence_update",
                "username": self.user.username,
                "status": "offline",
                "last_seen": last_seen
            }
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        # If frontend tells us messages are seen
        if data.get("type") == "seen":
            updated = await self.mark_messages_as_seen(self.receiver, self.user)
            if updated:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"type": "message_seen", "seen_by": self.user.username}
                )
            return

        # Normal message send
        message_text = data.get("message", "").strip()
        if not message_text:
            return

        sender = self.user
        receiver = self.receiver

        msg = await self.save_message(sender, receiver, message_text)

        # If receiver currently has connections > 0, mark delivered immediately
        is_receiver_online = await self.get_connections_count(receiver) > 0
        if is_receiver_online:
            await self.mark_delivered_messages(sender, receiver)

        # Broadcast the new message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "sender": sender.username,
                "receiver": receiver.username,
                "message": msg.content,
                "timestamp": timezone.localtime(msg.timestamp).strftime("%I:%M %p"),
                "is_seen": False,
                "is_delivered": is_receiver_online
            }
        )

    # Event handlers sent to clients
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"type": "chat_message", **event}))

    async def message_seen(self, event):
        await self.send(text_data=json.dumps({"type": "message_seen", "seen_by": event.get("seen_by")}))

    async def presence_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "user_status",
            "username": event.get("username"),
            "status": event.get("status"),
            "last_seen": event.get("last_seen", None)
        }))

    # --- DB helpers (sync_to_async) ---
    @sync_to_async
    def get_receiver_user(self, username):
        return CustomUser.objects.get(username=username)

    @sync_to_async
    def save_message(self, sender, receiver, content):
        return Message.objects.create(sender=sender, receiver=receiver, content=content)

    @sync_to_async
    def mark_messages_as_seen(self, sender, receiver):
        qs = Message.objects.filter(sender=sender, receiver=receiver, is_seen=False)
        changed = qs.exists()
        if changed:
            qs.update(is_seen=True, is_delivered=True)
        return changed

    @sync_to_async
    def mark_delivered_messages(self, sender, receiver):
        Message.objects.filter(sender=sender, receiver=receiver, is_delivered=False).update(is_delivered=True)

    # connection counting helpers
    @sync_to_async
    def increment_connections(self, user):
        # increase connections, set is_online True
        user.connections = (user.connections or 0) + 1
        user.is_online = True
        user.save(update_fields=["connections", "is_online"])

    @sync_to_async
    def decrement_connections(self, user):
        # reduce connections; if zero -> offline + last_seen
        user.connections = max((user.connections or 0) - 1, 0)
        if user.connections == 0:
            user.is_online = False
            user.last_seen = timezone.now()
            user.save(update_fields=["connections", "is_online", "last_seen"])
        else:
            user.save(update_fields=["connections"])
    
    @sync_to_async
    def get_connections_count(self, user):
        return user.connections or 0

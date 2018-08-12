from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserCustomized(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos', blank=True)


class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')


class ConversationReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    reply_message = models.TextField()
    time_send = models.DateTimeField(auto_now_add=True)


class RoomChat(models.Model):
    name = models.CharField(max_length=255)
    time_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class LoggedInRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_chat = models.ForeignKey(RoomChat, on_delete=models.CASCADE)


class RoomChatReply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_chat = models.ForeignKey(RoomChat, on_delete=models.CASCADE)
    reply_message = models.TextField()
    time_send = models.DateTimeField(auto_now_add=True)
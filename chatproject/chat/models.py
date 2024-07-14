from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    members = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        return f"Chat {self.id} with {[user.phone_number for user in self.members.all()]}"


class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender.phone_number}"

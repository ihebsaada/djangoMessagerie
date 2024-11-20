# your_app/models/conversation.py
from django.db import models
from .user import User

class Conversation(models.Model):
    users = models.ManyToManyField(User)  # Many-to-many relationship with User
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Conversation between {', '.join([User.username for User in self.users.all()])}"

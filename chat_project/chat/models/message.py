from django.db import models
from .conversation import Conversation
from .user import Client

class Message(models.Model):
    sender = models.ForeignKey(Client, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}:{self.content}"
    
    class Meta:
        ordering=['-timestamp']

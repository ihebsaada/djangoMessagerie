from django.contrib import admin
from .models.conversation import Conversation
from .models.message import Message
from .models.user import Client

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name']
    search_fields = ['username', 'email']

admin.site.register(Client, CustomUserAdmin)
admin.site.register(Message)
admin.site.register(Conversation)
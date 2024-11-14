from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from chat.models.user import Client

@api_view(['POST'])
def signup_view(request):
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    username = request.data['username']
    email = request.data['email']
    password = request.data['password']
    user = Client.objects.create_user(
        first_name=first_name, 
        last_name=last_name,
        username=username, 
        email=email,
        password=password 
        )
    token, _ = Token.objects.get_or_create(user=Client)
    return JsonResponse({'token': token.key})
class Meta:
        app_label = 'chat'  # This moves the model under the "CHAT" section
        verbose_name = 'User'
        verbose_name_plural = 'Users'
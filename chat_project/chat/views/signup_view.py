from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from chat.models import User
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def signup_view(request):
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    logger.info(f"Received signup data: {first_name}, {last_name}, {username}, {email}")

    # Check for existing username to avoid duplicates
    if User.objects.filter(username=username).exists():
        logger.warning(f"Username {username} already exists.")
        return JsonResponse({'error': 'Username already exists.'}, status=400)

    try:
        # Create the new user instance
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password
        )
        logger.info(f"User {username} created successfully.")

        # badlt f hthom
        token, _ = Token.objects.get_or_create(user=user)

        return JsonResponse({'token': token.key})

    except Exception as e:
        logger.error(f"Error during user creation: {str(e)}")
        return JsonResponse({'error': 'Something went wrong, please try again.'}, status=500)
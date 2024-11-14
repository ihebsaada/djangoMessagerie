from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chat.models import Message, Conversation
from chat.models import User

@api_view(['POST'])
def message_view(request):
    sender = request.User
    content = request.data.get("content")
    receiver_id = request.data.get("receiver_id")  # Assuming receiver ID is sent for new conversations
    conversation_id = request.data.get("conversation_id")

    # Check that content and either conversation_id or receiver_id are provided
    if not content or not (conversation_id or receiver_id):
        return Response({"error": "Content and either conversation ID or receiver ID are required."}, 
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        # Try to get an existing conversation
        if conversation_id:
            conversation = Conversation.objects.get(id=conversation_id)
        else:
            # Create a new conversation if it doesn't exist
            receiver = User.objects.get(id=receiver_id)
            conversation, created = Conversation.objects.get_or_create(
                users__in=[sender, receiver],
                defaults={'users': [sender, receiver]}
            )

        # Create the message
        message = Message.objects.create(sender=sender, content=content, conversation=conversation)
        return Response({"message": "Message sent successfully!"}, status=status.HTTP_201_CREATED)

    except User.DoesNotExist:
        return Response({"error": "Receiver not found."}, status=status.HTTP_404_NOT_FOUND)
    except Conversation.DoesNotExist:
        return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

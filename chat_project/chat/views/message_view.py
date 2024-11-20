from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from chat.models import Message, Conversation
from chat.models.user import User
from rest_framework import serializers

# Serializer to format the message data
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']  # Adjust the fields as necessary



@api_view(['POST'])
def message_view(request):
    sender_id = request.data.get("sender")  # Get sender ID from request data
    content = request.data.get("content")
    receiver_id = request.data.get("receiver_id")  # Assuming receiver ID is sent for new conversations
    conversation_id = request.data.get("conversation_id")

    # Check that content and either conversation_id or receiver_id are provided
    if not content or not (conversation_id or receiver_id):
        return Response({"error": "Content and either conversation ID or receiver ID are required."}, 
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        # Try to get the sender user from the database based on sender_id
        sender = User.objects.get(id=sender_id)

        # Try to get an existing conversation
        if conversation_id:
            conversation = Conversation.objects.get(id=conversation_id)
        else:
            # Create a new conversation if it doesn't exist
            receiver = User.objects.get(id=receiver_id)
            conversation = Conversation.objects.create()  # Create conversation without users

            # Assign the users to the conversation using set() method
            conversation.users.set([sender, receiver])
            conversation.save()  # Don't forget to save after setting users

        # Create the message
        message = Message.objects.create(sender=sender, content=content, conversation=conversation)
        return Response({"message": "Message sent successfully!"}, status=status.HTTP_201_CREATED)

    except User.DoesNotExist:
        return Response({"error": "Sender or receiver not found."}, status=status.HTTP_404_NOT_FOUND)
    except Conversation.DoesNotExist:
        return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_messages_by_conversation(request):
    conversation_id = request.query_params.get('conversation_id')

    # Validate that conversation_id is provided
    if not conversation_id:
        return Response({"error": "conversation_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Get the conversation based on the provided conversation_id
        conversation = Conversation.objects.get(id=conversation_id)

        # Retrieve all messages for the conversation
        messages = Message.objects.filter(conversation=conversation)

        # Serialize the messages
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Conversation.DoesNotExist:
        return Response({"error": "Conversation not found."}, status=status.HTTP_404_NOT_FOUND)

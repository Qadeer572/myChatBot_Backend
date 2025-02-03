from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
import os
import json
# Create your views here.

FILENAME = "chat_history.json"




def user_profile(request):
    return HttpResponse("welcome to the user Page")


@api_view(['POST'])
def register_user(request):
    data = request.data  # Get data from request

    username = data.get('name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    print('username :', username)
    print('email :', email)
    print('password :', password)
    print('confirm_password :', confirm_password)

    # Check if password and confirm password match
    if password != confirm_password:
        return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if user already exists
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    # Create user
    user = User.objects.create_user(username=username, email=email, password=password)

    user.save()

    return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)



            
@api_view(['POST'])
def login_user(request):
    data = request.data  # Get data from request

    email = data.get('email')
    password = data.get('password')

    # Check if email is provided
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Try to get the user based on the email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Authenticate the user using username and password
    user = authenticate(request, username=user.username, password=password)

    c_user=User.objects.filter(email=email)
    
    # If authentication fails
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    # Authentication successful
 
    return Response({'email': email}, status=status.HTTP_200_OK)







def load_chat_data():
    """Load existing chat data from the JSON file."""
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}



def save_chat_history(user_id, user_message, bot_response):
    """Save chat history for a user in a single JSON file."""
    chat_data = load_chat_data()
    
    # Ensure the user has an entry in the chat data
    if user_id not in chat_data:
        chat_data[user_id] = []
    
    # Append the new chat message
    chat_data[user_id].append({"user": user_message, "bot": bot_response})

    # Write updated data back to the file
    with open(FILENAME, "w") as file:
        json.dump(chat_data, file, indent=4)
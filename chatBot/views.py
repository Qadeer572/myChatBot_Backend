from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import google.generativeai as genai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import os


FILENAME = "chat_history.json"

API_KEY = "AIzaSyA2qPG4deKcarcXDOXY1dPJ-oI9JNjH4wA"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini")



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
def chat(request):
    data=request.data
    user_message=data.get('message')
    email=data.get('email')
    
     

    if user_message:
        response = model.generate_content(user_message)
        if email is None:
            print("No History stored for user")
        else:    
            save_chat_history(email, user_message, response.text)
        return Response({"chatResponse": response.text}, status=status.HTTP_201_CREATED)
    else :
        return Response({"chatResponse": "I didn't get your message. Please try again."}, status=status.HTTP_400_BAD_REQUEST)
         



def load_chat_data():
    """Load chat data from JSON file."""
    try:
        with open(FILENAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_chat_history(email, user_message, bot_response):
    """Save chat history for a user using their email as the identifier."""
    chat_data = load_chat_data()

    # Ensure the user (email) has an entry in the chat data
    if email not in chat_data:
        chat_data[email] = []
    
    # Append the new chat message
    chat_data[email].append({"user": user_message, "bot": bot_response})
    
    # Write updated data back to the file
    with open(FILENAME, "w") as file:
        json.dump(chat_data, file, indent=4)


@api_view(["POST"])
def get_chat_history(request):
    """Retrieve chat history for a specific user by email."""
    email = request.data.get("email")  # Retrieve email from the POST data
    
    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)
    
    chat_data = load_chat_data()
    chat_history = chat_data.get(email, [])
     
    return JsonResponse({"email": email, "history": chat_history})        



@api_view(["POST"])
def delete_chat_history(request):
    email = request.data.get("email")

    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)
    
    chat_data = load_chat_data()
    if email in chat_data:
        del chat_data[email]
        with open(FILENAME, "w") as file:
            json.dump(chat_data, file, indent=4)
        return JsonResponse({"message": "Chat history deleted successfully"})
    else:
        return JsonResponse({"error": "Email not found"}, status=404)
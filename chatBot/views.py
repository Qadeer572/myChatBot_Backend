from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import google.generativeai as genai
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


API_KEY = "AIzaSyDnODAc5ZxH8t-xRme8Zm6LqLGI8n1fkCM"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-pro")


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


    if user_message:
        response = model.generate_content(user_message)
        return Response({"chatResponse": response.text}, status=status.HTTP_201_CREATED)
    else :
        return Response({"chatResponse": "I didn't get your message. Please try again."}, status=status.HTTP_400_BAD_REQUEST)
         
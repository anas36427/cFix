from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from .models import User

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        data['password'] = make_password(data['password'])
        User(**data).save()
        return Response({"message": "User registered successfully"}, status=201)

class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = User.objects(email=data['email']).first()
        if user and check_password(data['password'], user.password):
            return Response({"message": "Login successful"}, status=200)
        return Response({"error": "Invalid credentials"}, status=401)

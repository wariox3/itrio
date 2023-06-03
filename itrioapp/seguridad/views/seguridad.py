from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from seguridad.serializers import UserSerializer, UserListSerializer, UserDetalleSerializer, CustomTokenObtainPairSerializer, CustomUserSerializer, VerificacionSerializer
from django.shortcuts import get_object_or_404
from seguridad.models import User, Verificacion
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from datetime import datetime, timedelta
from decouple import config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import secrets
    
class Login(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:
            login_serializer = self.serializer_class(data=request.data)
            if login_serializer.is_valid():
                user_serializer = CustomUserSerializer(user)
                return Response({
                    'token': login_serializer.validated_data.get('access'),
                    'refresh-token': login_serializer.validated_data.get('refresh'),
                    'user':user_serializer.data
                }, status=status.HTTP_200_OK)
            return Response({'error':'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'Contraseña o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)        
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from seguridad.serializers import UserSerializer, UserUpdateSerializer, UserListSerializer, UserDetalleSerializer
from django.shortcuts import get_object_or_404
from seguridad.models import User
from .verificacion import VerificacionNuevo

class UsuarioViewSet(GenericViewSet, UpdateModelMixin):
    model = User
    queryset = None
    serializer_class = UserSerializer
    detalle_serializer_class = UserDetalleSerializer
    
    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def list(self, request):        
        queryset = User.objects.all()
        serializer_class = UserListSerializer(queryset, many=True)
        return Response(serializer_class.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user = user_serializer.save()
            #Enviar verificacion (metodo)
            request.data['username'] = user.username
            request.data['accion'] = 'registro'
            verificacionAPIView = VerificacionNuevo()
            verificacionAPIView.post(request)
            return Response({'usuario': user_serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'mensaje':'Errores en el registro del usuario', 'codigo':2, 'validaciones': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = self.detalle_serializer_class(user)
        return Response(user_serializer.data)

    def update(self, request, pk=None):
        user = self.get_object(pk)
        user_serializer = UserUpdateSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'actualizacion': True, 'usuario': user_serializer.data}, status=status.HTTP_201_CREATED)            
        return Response({'mensaje':'Errores en la actualizacion del usuario', 'codigo':10, 'validaciones': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ClaveCambiar(APIView):

    def post(self, request):    
        codigoUsuario = request.data.get('id')
        clave = request.data.get('password')
        usuario = User.objects.get(id = codigoUsuario)
        usuario.set_password(clave)
        usuario.save()
        return Response({'cambio': True}, status=status.HTTP_200_OK)
from django.shortcuts import render
from rest_framework import viewsets, response, status
from users.serializers import UserSerializer, UserListSerializer

class UsuarioViewSet(viewsets.GenericViewSet):
    queryset = None
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.serializer_class.Meta.model.objects.all().values('id', 'username', 'email', 'codigo_cliente_fk', 'dominio')
        return self.queryset

    def list(self, request):
        users = self.get_queryset()
        users_serializer = self.list_serializer_class(users, many=True)
        return response.Response(users_serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return response.Response({'message':'Usuario registrado'}, status=status.HTTP_201_CREATED)
        return response.Response({'message:':'Errores en el registro', 'errors': user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


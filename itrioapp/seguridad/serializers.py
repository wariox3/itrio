from rest_framework import serializers
from seguridad.models import User, Verificacion
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Serializers define the API representation.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.email = user.username;
        user.is_active = False;
        user.dominio = "app.muupservicios.online";
        user.set_password(validated_data['password'])    
        user.save()
        return user

class UserUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'last_name']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'dominio', 'codigo_cliente_fk', 'name', 'last_name']
    
        
class UserDetalleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'dominio', 'name', 'last_name']  

class VerificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verificacion
        fields = ['id', 'codigo_usuario_fk', 'token', 'estado_usado', 'vence', 'accion']                 
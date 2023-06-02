from rest_framework import serializers
from users.models import User, Verificacion
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

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    
    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'codigo_cliente_fk': instance['codigo_cliente_fk'],
            'dominio': instance['dominio']
        }
    
class UserDetalleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'dominio']  

class VerificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verificacion
        fields = ['id', 'codigo_usuario_fk', 'token', 'estado_usado', 'vence', 'accion']                 
from rest_framework import serializers
from users.models import User

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.email = user.username;
        user.dominio = "app.muupservicios.online";
        user.set_password(validated_data['password'])    
        user.save()
        return User

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
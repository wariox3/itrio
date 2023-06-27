from rest_framework import serializers
from seguridad.models import User, Verificacion, UsuarioEmpresa
from inquilino.models import Empresa
from inquilino.serializers import EmpresaSerializer
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
        user.dominio = "muupservicios.online";
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
        fields = ['id', 'username', 'email', 'dominio', 'name', 'last_name']    
        
class UserDetalleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'dominio', 'name', 'last_name']  

class VerificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verificacion
        fields = ['id', 'codigo_usuario_fk', 'token', 'estado_usado', 'vence', 'accion']      

class UsuarioEmpresaSerializador(serializers.HyperlinkedModelSerializer):
    # se renderiza por to_representation
    #usuario = UserListSerializer()
    # se renderiza por to_representation
    #empresa = .StringRelatserializersedField()
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())
    class Meta:
        model = UsuarioEmpresa
        fields = ['usuario', 'empresa']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'usuario_id': instance.usuario_id,
            'empresa_id': instance.empresa_id,
            'subdominio': instance.empresa.schema_name,
            'nombre': instance.empresa.nombre,
            'imagen': instance.empresa.imagen
        }
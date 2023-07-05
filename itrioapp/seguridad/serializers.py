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
        fields = ['id', 'username', 'nombre_corto']

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.correo = user.username;
        user.is_active = False;
        user.dominio = "muupservicios.online";
        user.set_password(validated_data['password'])    
        user.save()
        return user

class UserUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['nombre_corto', 'nombre', 'apellido', 'telefono']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'correo', 'dominio', 'nombre_corto', 'nombre', 'apellido', 'telefono']    
        
class UserDetalleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'dominio', 'nombre_corto', 'nombre', 'apellido', 'correo', 'telefono']  

class VerificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verificacion
        fields = ['id', 'token', 'estado_usado', 'vence', 'accion', 'usuario_id', 'empresa_id', 'usuario_invitado_username']      

class UsuarioEmpresaSerializador(serializers.HyperlinkedModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())
    class Meta:
        model = UsuarioEmpresa
        fields = ['usuario', 'empresa', 'rol']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'usuario_id': instance.usuario_id,
            'empresa_id': instance.empresa_id,
            'rol': instance.rol,
            'subdominio': instance.empresa.schema_name,
            'nombre': instance.empresa.nombre,
            'imagen': instance.empresa.imagen
        }
    
class UsuarioEmpresaConsultaEmpresaSerializador(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = UsuarioEmpresa
        fields = ['id', 'usuario']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'empresa_id': instance.empresa_id,
            'usuario_id': instance.usuario_id,            
            'rol': instance.rol,
            'username': instance.usuario.username
        }        
from rest_framework import serializers
from seguridad.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from decouple import config

# Serializers define the API representation.
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
    
    def create(self, validated_data):
        user = User(**validated_data)
        user.correo = user.username
        arrCadena = user.username.split("@")
        user.nombre_corto = arrCadena[0]
        user.is_active = True
        user.dominio = f"{config('DOMINIO_BACKEND')}"
        user.imagen = f"itrio/usuario_defecto.jpg"
        user.set_password(validated_data['password'])    
        user.save()
        return user

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'username': instance.username,
            'correo': instance.correo,
            'dominio': instance.dominio,
            'nombre_corto': instance.nombre_corto,
            'numero_identificacion' : instance.numero_identificacion,
            'nombre': instance.nombre,
            'apellido': instance.apellido,
            'telefono': instance.telefono,
            'idioma': instance.idioma,
            'vr_saldo': instance.vr_saldo,
            'vr_credito': instance.vr_credito,
            'vr_abono': instance.vr_abono,
            'cargo' : instance.cargo,
            'imagen': f"https://{config('DO_BUCKET')}.{config('DO_REGION')}.digitaloceanspaces.com/{instance.imagen}",
            'fecha_limite_pago': instance.fecha_limite_pago,
            'fecha_creacion': instance.fecha_creacion,
            'verificado': instance.verificado,
            'es_socio': instance.es_socio,
            'socio_id': instance.socio_id,
            'is_active': instance.is_active
        }

class UserUpdateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['nombre_corto', 'nombre', 'apellido', 'telefono', 'idioma', 'numero_identificacion', 'cargo']    
      
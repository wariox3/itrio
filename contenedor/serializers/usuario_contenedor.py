from rest_framework import serializers
from contenedor.models import Contenedor, UsuarioContenedor
from seguridad.models import User
from datetime import datetime
from decouple import config

class UsuarioContenedorSerializador(serializers.HyperlinkedModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    contenedor = serializers.PrimaryKeyRelatedField(queryset=Contenedor.objects.all())
    class Meta:
        model = UsuarioContenedor
        fields = ['usuario', 'contenedor', 'rol']
    
    def to_representation(self, instance):
        plan = instance.contenedor.plan
        planNombre = None
        usuariosBase = None
        if plan:
            planNombre = plan.nombre
            usuariosBase = plan.usuarios_base
        acceso_restringido = False
        if instance.contenedor:
            if instance.contenedor.usuario:
                usuario = instance.contenedor.usuario
                if usuario.vr_saldo > 0 and datetime.now().date() > usuario.fecha_limite_pago:
                    acceso_restringido = True            
        return {
            'id': instance.id,
            'usuario_id': instance.usuario_id,
            'contenedor_id': instance.contenedor_id,
            'rol': instance.rol,
            'subdominio': instance.contenedor.schema_name,
            'nombre': instance.contenedor.nombre,
            'imagen': f"https://{config('DO_BUCKET')}.{config('DO_REGION')}.digitaloceanspaces.com/{instance.contenedor.imagen}",
            'usuarios': instance.contenedor.usuarios,
            'usuarios_base': usuariosBase,
            'plan_id': instance.contenedor.plan_id,
            'plan_nombre': planNombre,
            'reddoc': instance.contenedor.reddoc,
            'ruteo': instance.contenedor.ruteo,
            'acceso_restringido': acceso_restringido
        }
    
class UsuarioContenedorConsultaContenedorSerializador(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = UsuarioContenedor
        fields = ['id', 'usuario']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'contenedor_id': instance.contenedor_id,
            'usuario_id': instance.usuario_id,            
            'rol': instance.rol,
            'username': instance.usuario.username
        }  
from rest_framework import serializers
from contenedor.models import Contenedor, UsuarioContenedor
from seguridad.models import User

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
        return {
            'id': instance.id,
            'usuario_id': instance.usuario_id,
            'contenedor_id': instance.contenedor_id,
            'rol': instance.rol,
            'subdominio': instance.contenedor.schema_name,
            'nombre': instance.contenedor.nombre,
            'imagen': f"https://semantica.sfo3.digitaloceanspaces.com/{instance.contenedor.imagen}",
            'usuarios': instance.contenedor.usuarios,
            'usuarios_base': usuariosBase,
            'plan_id': instance.contenedor.plan_id,
            'plan_nombre': planNombre,
            'reddoc': instance.contenedor.reddoc,
            'ruteo': instance.contenedor.ruteo
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
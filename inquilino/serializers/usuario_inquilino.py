from rest_framework import serializers
from inquilino.models import Inquilino, UsuarioInquilino
from seguridad.models import User

class UsuarioInquilinoSerializador(serializers.HyperlinkedModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    inquilino = serializers.PrimaryKeyRelatedField(queryset=Inquilino.objects.all())
    class Meta:
        model = UsuarioInquilino
        fields = ['usuario', 'inquilino', 'rol']
    
    def to_representation(self, instance):
        plan = instance.inquilino.plan
        planNombre = None
        usuariosBase = None
        if plan:
            planNombre = plan.nombre
            usuariosBase = plan.usuarios_base
        return {
            'id': instance.id,
            'usuario_id': instance.usuario_id,
            'inquilino_id': instance.inquilino_id,
            'rol': instance.rol,
            'subdominio': instance.inquilino.schema_name,
            'nombre': instance.inquilino.nombre,
            'imagen': f"https://itrio.fra1.digitaloceanspaces.com/{instance.inquilino.imagen}",
            'usuarios': instance.inquilino.usuarios,
            'usuarios_base': usuariosBase,
            'plan_id': instance.inquilino.plan_id,
            'plan_nombre': planNombre            
        }
    
class UsuarioInquilinoConsultaInquilinoSerializador(serializers.ModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = UsuarioInquilino
        fields = ['id', 'usuario']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'inquilino_id': instance.inquilino_id,
            'usuario_id': instance.usuario_id,            
            'rol': instance.rol,
            'username': instance.usuario.username
        }  
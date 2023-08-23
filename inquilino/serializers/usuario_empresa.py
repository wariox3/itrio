from rest_framework import serializers
from inquilino.models import Empresa, UsuarioEmpresa
from seguridad.models import User

class UsuarioEmpresaSerializador(serializers.HyperlinkedModelSerializer):
    usuario = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    empresa = serializers.PrimaryKeyRelatedField(queryset=Empresa.objects.all())
    class Meta:
        model = UsuarioEmpresa
        fields = ['usuario', 'empresa', 'rol']
    
    def to_representation(self, instance):
        plan = instance.empresa.plan
        planNombre = None
        usuariosBase = None
        if plan:
            planNombre = plan.nombre
            usuariosBase = plan.usuarios_base
        return {
            'id': instance.id,
            'usuario_id': instance.usuario_id,
            'empresa_id': instance.empresa_id,
            'rol': instance.rol,
            'subdominio': instance.empresa.schema_name,
            'nombre': instance.empresa.nombre,
            'imagen': f"https://itrio.fra1.digitaloceanspaces.com/{instance.empresa.imagen}",
            'usuarios': instance.empresa.usuarios,
            'usuarios_base': usuariosBase,
            'plan_id': instance.empresa.plan_id,
            'plan_nombre': planNombre            
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
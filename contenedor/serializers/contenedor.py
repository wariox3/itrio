from rest_framework import serializers
from contenedor.models import Contenedor, CtnPlan
from decouple import config

class ContenedorSerializador(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=CtnPlan.objects.all())
    class Meta:
        model = Contenedor
        fields = ['id', 'schema_name']
    
    def to_representation(self, instance):
        region = config('DO_REGION')
        bucket = config('DO_BUCKET')
        plan = instance.plan
        plan_usuarios_base = None
        plan_limite_usuarios = None
        plan_nombre = None
        if plan:
            plan_usuarios_base = plan.usuarios_base
            plan_limite_usuarios = plan.limite_usuarios
            plan_nombre = plan.nombre
        return {
            'id': instance.id,            
            'subdominio': instance.schema_name,
            'nombre': instance.nombre,
            'plan_id': instance.plan_id,
            'plan_usuarios_base': plan_usuarios_base,
            'plan_limite_usuarios': plan_limite_usuarios,
            'plan_nombre':  plan_nombre,
            'imagen': f"https://{bucket}.{region}.digitaloceanspaces.com/{instance.imagen}",
            'reddoc': instance.reddoc,
            'ruteo': instance.ruteo
        } 
    
class ContenedorActualizarSerializador(serializers.HyperlinkedModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=CtnPlan.objects.all())
    class Meta:
        model = Contenedor
        fields = ['nombre', 'plan']         
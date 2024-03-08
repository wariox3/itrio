from rest_framework import serializers
from contenedor.models import Contenedor, Plan
from decouple import config

class ContenedorSerializador(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())
    class Meta:
        model = Contenedor
        fields = ['id', 'schema_name']
    
    def to_representation(self, instance):
        region = config('DO_REGION')
        bucket = config('DO_BUCKET')
        return {
            'id': instance.id,            
            'subdominio': instance.schema_name,
            'nombre': instance.nombre,
            'plan_id': instance.plan_id,
            'plan_usuarios_base': instance.plan.usuarios_base,
            'plan_limite_usuarios': instance.plan.limite_usuarios,
            'plan_nombre':  instance.plan.nombre,
            'imagen': f"https://{bucket}.{region}.digitaloceanspaces.com/itrio/{instance.imagen}"
        } 
    
class ContenedorActualizarSerializador(serializers.HyperlinkedModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())
    class Meta:
        model = Contenedor
        fields = ['nombre', 'plan']         
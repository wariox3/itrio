from rest_framework import serializers
from contenedor.models import Contenedor, Plan

class ContenedorSerializador(serializers.ModelSerializer):
    class Meta:
        model = Contenedor
        fields = ['id', 'schema_name']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'subdominio': instance.schema_name,
            'nombre': instance.nombre,
            'plan_id': instance.plan_id,
            'imagen': f"https://itrio.fra1.digitaloceanspaces.com/{instance.imagen}"
        } 
    
class ContenedorActualizarSerializador(serializers.HyperlinkedModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all())
    class Meta:
        model = Contenedor
        fields = ['nombre', 'plan']         
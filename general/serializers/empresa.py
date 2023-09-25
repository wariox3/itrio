from general.models.empresa import Empresa, Ciudad, Identificacion, Regimen, TipoPersona
from rest_framework import serializers

class EmpresaSerializador(serializers.HyperlinkedModelSerializer):
    identificacion = serializers.PrimaryKeyRelatedField(queryset=Identificacion.objects.all())
    ciudad = serializers.PrimaryKeyRelatedField(queryset=Ciudad.objects.all())    
    tipo_persona = serializers.PrimaryKeyRelatedField(queryset=TipoPersona.objects.all())
    regimen = serializers.PrimaryKeyRelatedField(queryset=Regimen.objects.all())
    class Meta:
        model = Empresa
        fields = [
            'id',
            'identificacion', 
            'numero_identificacion',
            'digito_verificacion',
            'nombre_corto',
            'direccion',
            'ciudad',
            'telefono',
            'correo',
            'tipo_persona',
            'regimen',
            'imagen',
            'contenedor_id']  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'numero_identificacion': instance.numero_identificacion,
            'digito_verificacion': instance.digito_verificacion,
            'nombre_corto': instance.nombre_corto,
            'direccion': instance.direccion,
            'telefono': instance.telefono,
            'correo': instance.correo,
            'imagen': instance.imagen
        }            
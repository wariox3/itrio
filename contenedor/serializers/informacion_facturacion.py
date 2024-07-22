from rest_framework import serializers
from contenedor.models import InformacionFacturacion
    
class InformacionFacturacionSerializador(serializers.ModelSerializer):
    class Meta:
        model = InformacionFacturacion
        fields = ['numero_identificacion', 'digito_verificacion', 'nombre_corto', 'direccion', 'telefono', 'correo', 'identificacion', 'ciudad', 'usuario']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'numero_identificacion':instance.numero_identificacion,
            'digito_verificacion':instance.digito_verificacion,
            'nombre_corto': instance.nombre_corto,
            'direccion':instance.direccion,
            'telefono':instance.telefono,
            'correo':instance.correo,
            'identificacion_id':instance.identificacion_id,
            'ciudad_id':instance.ciudad_id,
            'usuario_id':instance.usuario_id
        }   
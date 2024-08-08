from rest_framework import serializers
from contenedor.models import CtnInformacionFacturacion
    
class CtnInformacionFacturacionSerializador(serializers.ModelSerializer):
    class Meta:
        model = CtnInformacionFacturacion
        fields = ['numero_identificacion', 'digito_verificacion', 'nombre_corto', 'direccion', 'telefono', 'correo', 'identificacion', 'ciudad', 'usuario']
    
    def to_representation(self, instance):
        ciudad_nombre = ""
        ciudad_estado_nombre = ""
        ciudad_estado_pais_nombre = ""
        if instance.ciudad:
            ciudad_nombre = instance.ciudad.nombre
            if instance.ciudad.estado:
                ciudad_estado_nombre = instance.ciudad.estado.nombre
                if instance.ciudad.estado.pais:
                    ciudad_estado_pais_nombre = instance.ciudad.estado.pais.nombre
        identificacion_nombre = ''
        if instance.identificacion:
            identificacion_nombre = instance.identificacion.nombre
        return {
            'id': instance.id,            
            'numero_identificacion':instance.numero_identificacion,
            'digito_verificacion':instance.digito_verificacion,
            'nombre_corto': instance.nombre_corto,
            'direccion':instance.direccion,
            'telefono':instance.telefono,
            'correo':instance.correo,
            'identificacion_id':instance.identificacion_id,
            'identificacion_nombre': identificacion_nombre,
            'ciudad_id':instance.ciudad_id,
            'ciudad_nombre': ciudad_nombre,
            'ciudad_estado_nombre': ciudad_estado_nombre,
            'ciudad_estado_pais_nombre': ciudad_estado_pais_nombre,
            'usuario_id':instance.usuario_id
        }   
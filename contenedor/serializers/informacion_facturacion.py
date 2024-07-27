from rest_framework import serializers
from contenedor.models import CtnInformacionFacturacion
    
class InformacionFacturacionSerializador(serializers.ModelSerializer):
    class Meta:
        model = CtnInformacionFacturacion
        fields = ['numero_identificacion', 'digito_verificacion', 'nombre_corto', 'direccion', 'telefono', 'correo', 'identificacion', 'ciudad', 'usuario']
    
    def to_representation(self, instance):
        ciudad_nombre = ""
        ciudad_nombre_mascara = ""
        if instance.ciudad:
            ciudad_nombre = instance.ciudad.nombre
            if instance.ciudad.estado:
                if instance.ciudad.estado.pais:
                    ciudad_nombre_mascara = instance.ciudad.nombre + ", " + instance.ciudad.estado.nombre + ", " + instance.ciudad.estado.pais.nombre
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
            'ciudad_nombre': ciudad_nombre,
            'ciudad_nombre_mascara': ciudad_nombre_mascara,
            'usuario_id':instance.usuario_id
        }   
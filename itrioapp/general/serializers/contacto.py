from general.models.contacto import Contacto
from rest_framework import serializers

class ContactoSerializador(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Contacto
        fields = [
            'identificacion', 
            'numero_identificacion',
            'digito_verificacion',
            'nombre_corto',
            'nombre1',
            'nombre2',
            'apellido1',
            'apellido2',
            'direccion',
            'ciudad',
            'codigo_postal',
            'telefono',
            'celular',
            'correo',
            'tipo_persona',
            'regimen'
            ]          
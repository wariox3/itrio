from general.models.contacto import Contacto, Ciudad, Identificacion, Regimen, TipoPersona
from rest_framework import serializers

class ContactoSerializador(serializers.HyperlinkedModelSerializer):
    identificacion = serializers.PrimaryKeyRelatedField(queryset=Identificacion.objects.all())
    ciudad = serializers.PrimaryKeyRelatedField(queryset=Ciudad.objects.all())    
    tipo_persona = serializers.PrimaryKeyRelatedField(queryset=TipoPersona.objects.all())
    regimen = serializers.PrimaryKeyRelatedField(queryset=Regimen.objects.all())
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
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'numero_identificacion': instance.numero_identificacion,
            'digito_verificacion': instance.digito_verificacion,
            'nombre_corto': instance.nombre_corto,
            'nombre1': instance.nombre1,
            'nombre2': instance.nombre2,
            'apellido1': instance.apellido1,
            'apellido2': instance.apellido2,
            'direccion': instance.direccion,
            'codigo_postal': instance.codigo_postal,
            'telefono': instance.telefono,
            'celular': instance.celular,
            'correo': instance.correo,
            'identificacion_id': instance.identificacion_id,
            'identificacion_nombre': instance.identificacion.nombre,
            'ciudad_id': instance.ciudad_id,
            'ciudad_nombre': instance.ciudad.nombre,
            'regimen_id': instance.regimen_id,
            'regimen_nombre': instance.regimen.nombre,
            'tipo_persona_id': instance.tipo_persona_id,
            'tipo_persona_nombre': instance.tipo_persona.nombre,
        }     

class ContactoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    identificacion = serializers.PrimaryKeyRelatedField(queryset=Identificacion.objects.all())
    ciudad = serializers.PrimaryKeyRelatedField(queryset=Ciudad.objects.all())    
    tipo_persona = serializers.PrimaryKeyRelatedField(queryset=TipoPersona.objects.all())
    regimen = serializers.PrimaryKeyRelatedField(queryset=Regimen.objects.all())
    class Meta:
        model = Contacto 
        
    def to_representation(self, instance):
        return {
            'contacto_id': instance.id,            
            'contacto_nombre_corto': instance.nombre_corto
        }        
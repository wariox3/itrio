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
            'regimen',
            'barrio',
            'codigo_ciuu'
            ]  
        
    def to_representation(self, instance):
        return {
            'id': instance.id,            
            'numero_identificacion': instance.numero_identificacion,
            'identificacion_nombre': instance.identificacion.nombre,            
            'nombre_corto': instance.nombre_corto,            
            'correo': instance.correo,
            'telefono': instance.telefono,
            'celular': instance.celular,
            'direccion': instance.direccion,        
            'ciudad_nombre': instance.ciudad.nombre,
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
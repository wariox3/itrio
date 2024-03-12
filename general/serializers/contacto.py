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
            'id',
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
            'identificacion_id': instance.identificacion_id, 
            'identificacion_abreviatura': instance.identificacion.abreviatura, 
            'numero_identificacion': instance.numero_identificacion,
            'digito_verificacion': instance.digito_verificacion,
            'nombre_corto': instance.nombre_corto,
            'nombre1': instance.nombre1,
            'nombre2': instance.nombre2,
            'apellido1': instance.apellido1,
            'apellido2': instance.apellido2,
            'correo': instance.correo,
            'telefono': instance.telefono,
            'celular': instance.celular,
            'direccion': instance.direccion,  
            'ciudad': instance.ciudad.nombre,
            'barrio': instance.barrio,
            'codigo_postal': instance.codigo_postal,
            'tipo_persona_id': instance.tipo_persona_id,
            'tipo_persona': instance.tipo_persona.nombre,
            'regimen_id': instance.regimen_id,
            'regimen_nombre': instance.regimen.nombre,  
            'codigo_ciuu': instance.codigo_ciuu

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

'''#Esto fue una prueba para retornar solo los campos de la peticion, se puede borrar
class ContactoSerializadorV2(serializers.ModelSerializer):
    identificacion = serializers.PrimaryKeyRelatedField(queryset=Identificacion.objects.all())
    class Meta:
        model = Contacto
        fields = '__all__'   

    def __init__(self, *args, fields=None, **kwargs):
        super(ContactoSerializadorV2, self).__init__(*args, **kwargs)
        if fields:
            allowed = set(fields)
            existing = set(self.fields.keys())
            for field_name in existing - allowed:
                self.fields.pop(field_name)                   '''
from general.models.empresa import Empresa, Ciudad, Identificacion, Regimen, TipoPersona
from rest_framework import serializers
from decouple import config

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
            'contenedor_id',
            'suscriptor']  
        
    def to_representation(self, instance):
        nombre_ciudad = instance.ciudad.nombre
        nombre_estado = instance.ciudad.estado.nombre

        nombre_completo = f"{nombre_ciudad} - {nombre_estado}"
        region = config('DO_REGION')
        bucket = config('DO_BUCKET')
        return {
            'id': instance.id,            
            'numero_identificacion': instance.numero_identificacion,
            'identificacion_id': instance.identificacion.id,
            'ciudad_id': instance.ciudad.id,
            'ciudad_nombre': nombre_completo,
            'digito_verificacion': instance.digito_verificacion,
            'nombre_corto': instance.nombre_corto,
            'direccion': instance.direccion,
            'telefono': instance.telefono,
            'correo': instance.correo,
            'regimen': instance.regimen.id,
            'tipo_persona': instance.tipo_persona.id,
            'suscriptor': instance.suscriptor,
            'imagen': f"https://{bucket}.{region}.digitaloceanspaces.com/{instance.imagen}"
        }   

class EmpresaActualizarSerializador(serializers.HyperlinkedModelSerializer):
    ciudad = serializers.PrimaryKeyRelatedField(queryset=Ciudad.objects.all())
    identificacion = serializers.PrimaryKeyRelatedField(queryset=Identificacion.objects.all())
    class Meta:
        model = Empresa
        fields = ['nombre_corto', 'direccion', 'correo', 'numero_identificacion', 'digito_verificacion', 'telefono','ciudad', 'identificacion']
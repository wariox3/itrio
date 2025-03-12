from rest_framework import serializers
from contabilidad.models.activo import ConActivo
from contabilidad.models.activo_grupo import ConActivoGrupo
from contabilidad.models.metodo_depreciacion import ConMetodoDepreciacion
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.grupo import ConGrupo

class ConActivoSerializador(serializers.HyperlinkedModelSerializer):
    activo_grupo = serializers.PrimaryKeyRelatedField(queryset=ConActivoGrupo.objects.all())
    metodo_depreciacion = serializers.PrimaryKeyRelatedField(queryset=ConMetodoDepreciacion.objects.all())
    grupo = serializers.PrimaryKeyRelatedField(queryset=ConGrupo.objects.all())
    cuenta_gasto = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all())
    cuenta_depreciacion = serializers.PrimaryKeyRelatedField(queryset=ConCuenta.objects.all())

    class Meta:
        model = ConActivo
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)    
        representation['activo_grupo_nombre'] = instance.activo_grupo.nombre if instance.activo_grupo else ""        
        representation['grupo_nombre'] = instance.grupo.nombre if instance.grupo else ""        
        representation['metodo_depreciacion_nombre'] = instance.metodo_depreciacion.nombre if instance.metodo_depreciacion else "" 
        representation['cuenta_gasto_nombre'] = instance.cuenta_gasto.nombre if instance.cuenta_gasto else ""        
        representation['cuenta_depreciacion_nombre'] = instance.cuenta_depreciacion.nombre if instance.cuenta_depreciacion else ""        
        return representation 


class ConActivoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConActivo

    def to_representation(self, instance):
        return {
            'activo_id': instance.id,
            'activo_nombre': instance.nombre,
            'activo_codigo': instance.codigo
        }         
        
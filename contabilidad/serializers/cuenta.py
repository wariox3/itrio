from rest_framework import serializers
from contabilidad.models.cuenta import ConCuenta
from contabilidad.models.cuenta_clase import ConCuentaClase
from contabilidad.models.cuenta_grupo import ConCuentaGrupo
from contabilidad.models.cuenta_cuenta import ConCuentaCuenta
from contabilidad.models.cuenta_subcuenta import ConCuentaSubcuenta

class ConCuentaListaSerializador(serializers.ModelSerializer):          
    class Meta:
        model = ConCuenta
        fields = ['id', 
                  'nombre',
                  'codigo']

#Deprecated
class ConCuentaSerializador(serializers.HyperlinkedModelSerializer):
    cuenta_clase = serializers.PrimaryKeyRelatedField(queryset=ConCuentaClase.objects.all(), allow_null=True)
    cuenta_grupo = serializers.PrimaryKeyRelatedField(queryset=ConCuentaGrupo.objects.all(), allow_null=True)
    cuenta_cuenta = serializers.PrimaryKeyRelatedField(queryset=ConCuentaCuenta.objects.all(), allow_null=True)

    class Meta:
        model = ConCuenta
        fields = ['id', 'codigo', 'nombre', 'exige_base', 'exige_contacto', 'exige_grupo', 'permite_movimiento', 'nivel',
                  'cuenta_clase', 'cuenta_grupo', 'cuenta_cuenta', 'cuenta_subcuenta']

    def to_representation(self, instance):
        cuenta_clase_nombre = ""
        if instance.cuenta_clase:
            cuenta_clase_nombre = instance.cuenta_clase.nombre
        cuenta_grupo_nombre = ""
        if instance.cuenta_grupo:
            cuenta_grupo_nombre = instance.cuenta_grupo.nombre
        cuenta_cuenta_nombre = ""
        if instance.cuenta_cuenta:
            cuenta_cuenta_nombre = instance.cuenta_cuenta.nombre
        return {
            'id': instance.id,
            'codigo': instance.codigo,
            'nombre': instance.nombre,
            'cuenta_clase_id': instance.cuenta_clase_id,
            'cuenta_clase_nombre': cuenta_clase_nombre,
            'cuenta_grupo_id': instance.cuenta_grupo_id,
            'cuenta_grupo_nombre': cuenta_grupo_nombre,
            'cuenta_cuenta_id': instance.cuenta_cuenta_id,
            'cuenta_cuenta_nombre': cuenta_cuenta_nombre,
            'exige_base': instance.exige_base,
            'exige_contacto': instance.exige_contacto,
            'exige_grupo': instance.exige_grupo,
            'permite_movimiento': instance.permite_movimiento          
        } 



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
        fields = ['id', 'codigo', 'nombre', 'marca', 'serie', 'modelo', 'fecha_compra', 
                  'fecha_activacion', 'fecha_baja', 'duracion', 'valor_compra', 'depreciacion_inicial', 
                  'activo_grupo', 'metodo_depreciacion', 'cuenta_gasto', 'cuenta_depreciacion',
                  'grupo', 'depreciacion_periodo', 'depreciacion_saldo']


    def to_representation(self, instance):

        return {
            'id': instance.id,
            'codigo':instance.codigo,
            'nombre':instance.nombre,
            'marca':instance.marca,
            'serie':instance.serie,
            'modelo':instance.modelo,
            'fecha_compra':instance.fecha_compra,
            'fecha_activacion':instance.fecha_activacion,
            'fecha_baja':instance.fecha_baja,
            'duracion':instance.duracion,
            'valor_compra':instance.valor_compra,
            'depreciacion_inicial':instance.depreciacion_inicial,
            'depreciacion_periodo':instance.depreciacion_periodo,
            'depreciacion_saldo':instance.depreciacion_saldo,
            'activo_grupo_id':instance.activo_grupo_id,
            'metodo_depreciacion':instance.metodo_depreciacion_id,
            'cuenta_gasto':instance.cuenta_gasto_id,
            'cuenta_depreciacion':instance.cuenta_depreciacion_id,
            'grupo':instance.grupo_id,
            'activo_grupo_nombre': instance.activo_grupo.nombre if instance.activo_grupo else "",
            'grupo_nombre':instance.grupo.nombre if instance.grupo else "",
            'metodo_depreciacion_nombre':instance.metodo_depreciacion.nombre if instance.metodo_depreciacion else "",
            'cuenta_gasto_codigo':instance.cuenta_gasto.codigo if instance.cuenta_gasto else "",
            'cuenta_gasto_nombre':instance.cuenta_gasto.nombre if instance.cuenta_gasto else "",
            'cuenta_depreciacion_codigo':instance.cuenta_depreciacion.codigo if instance.cuenta_depreciacion else "",
            'cuenta_depreciacion_nombre':instance.cuenta_depreciacion.nombre if instance.cuenta_depreciacion else ""
        }     


class ConActivoListaAutocompletarSerializador(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = ConActivo

    def to_representation(self, instance):
        return {
            'activo_id': instance.id,
            'activo_nombre': instance.nombre,
            'activo_codigo': instance.codigo
        }         
        
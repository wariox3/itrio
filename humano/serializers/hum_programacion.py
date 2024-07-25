from rest_framework import serializers
from humano.models.hum_programacion import HumProgramacion
from humano.models.hum_grupo import HumGrupo
from humano.models.hum_pago_tipo import HumPagoTipo

class HumProgramacionSerializador(serializers.HyperlinkedModelSerializer):
    pago_horas = serializers.BooleanField(required=True)
    pago_auxilio_transporte = serializers.BooleanField(required=True)
    pago_incapacidad = serializers.BooleanField(required=True)
    pago_licencia = serializers.BooleanField(required=True)   
    pago_vacacion = serializers.BooleanField(required=True)
    descuento_salud = serializers.BooleanField(required=True)
    descuento_pension = serializers.BooleanField(required=True)
    descuento_fondo_solidaridad = serializers.BooleanField(required=True)
    descuento_retencion_fuente = serializers.BooleanField(required=True)
    descuento_adicional_permanente = serializers.BooleanField(required=True)
    descuento_adicional_programacion = serializers.BooleanField(required=True)
    descuento_credito = serializers.BooleanField(required=True)
    descuento_embargo = serializers.BooleanField(required=True)


    pago_tipo = serializers.PrimaryKeyRelatedField(queryset=HumPagoTipo.objects.all())
    grupo = serializers.PrimaryKeyRelatedField(queryset=HumGrupo.objects.all())

    class Meta:
        model = HumProgramacion
        fields = ['id', 'fecha_desde', 'fecha_hasta', 'fecha_hasta_periodo', 'nombre', 'grupo', 'pago_tipo', 
                  'pago_horas', 'pago_auxilio_transporte', 'pago_incapacidad', 'pago_licencia', 'pago_vacacion', 
                  'descuento_salud', 'descuento_pension', 'descuento_fondo_solidaridad', 'descuento_retencion_fuente', 
                  'descuento_adicional_permanente', 'descuento_adicional_programacion', 'descuento_credito', 'descuento_embargo']
        
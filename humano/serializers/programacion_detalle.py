from rest_framework import serializers
from humano.models.programacion import HumProgramacion
from humano.models.programacion_detalle import HumProgramacionDetalle
from humano.models.contrato import HumContrato

class HumProgramacionDetalleSerializador(serializers.HyperlinkedModelSerializer):
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
    programacion = serializers.PrimaryKeyRelatedField(queryset=HumProgramacion.objects.all())
    contrato = serializers.PrimaryKeyRelatedField(queryset=HumContrato.objects.all())

    class Meta:
        model = HumProgramacionDetalle
        fields = ['id', 'pago_horas', 'pago_auxilio_transporte', 'pago_incapacidad', 'pago_licencia', 'pago_vacacion', 
                  'descuento_salud', 'descuento_pension', 'descuento_fondo_solidaridad', 'descuento_retencion_fuente', 
                  'descuento_adicional_permanente', 'descuento_adicional_programacion', 'descuento_credito', 'descuento_embargo', 'programacion',
                  'contrato']
        
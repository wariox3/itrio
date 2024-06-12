from rest_framework import serializers
from contenedor.models import ContenedorMovimiento

class ContenedorMovimientoSerializador(serializers.ModelSerializer):
    class Meta:
        model = ContenedorMovimiento
        fields = ['fecha']
    
    def to_representation(self, instance):
        total_enmascarado = "{:.2f}".format(instance.vr_saldo).replace('.', '').replace(',', '')
        return {
            'id': instance.id,   
            'tipo': instance.tipo,         
            'fecha': instance.fecha,
            'fecha_vence': instance.fecha_vence,
            'vr_total': instance.vr_total,
            'vr_afectado': instance.vr_afectado,
            'vr_saldo': instance.vr_saldo,
            'vr_saldo_enmascarado': total_enmascarado
        }         
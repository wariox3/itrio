from rest_framework import serializers
from inquilino.models import InquilinoMovimiento

class InquilinoMovimientoSerializador(serializers.ModelSerializer):
    class Meta:
        model = InquilinoMovimiento
        fields = ['fecha']
    
    def to_representation(self, instance):
        return {
            'id': instance.id,   
            'tipo': instance.tipo,         
            'fecha': instance.fecha,
            'vr_total': instance.vr_total,
            'vr_afectado': instance.vr_afectado,
            'vr_saldo': instance.vr_saldo
        }         
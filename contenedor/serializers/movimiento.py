from rest_framework import serializers
from contenedor.models import CtnMovimiento, CtnSocio

class CtnMovimientoSerializador(serializers.ModelSerializer):
    class Meta:
        model = CtnMovimiento
        fields = ['fecha']
    
    def to_representation(self, instance):
        usuario_username = ''
        if instance.usuario:
            usuario_username = instance.usuario.username
        total_enmascarado = "{:.2f}".format(instance.vr_saldo).replace('.', '').replace(',', '')
        return {
            'id': instance.id,   
            'tipo': instance.tipo,         
            'fecha': instance.fecha,
            'fecha_vence': instance.fecha_vence,
            'vr_total': instance.vr_total,
            'vr_afectado': instance.vr_afectado,
            'vr_saldo': instance.vr_saldo,
            'vr_saldo_enmascarado': total_enmascarado,
            'documento_fisico': instance.documento_fisico,
            'usuario_id': instance.usuario_id,
            'usuario_username': usuario_username
        }         
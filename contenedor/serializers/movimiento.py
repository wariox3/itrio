from rest_framework import serializers
from contenedor.models import CtnMovimiento


class CtnMovimientoSerializador(serializers.ModelSerializer):  
    usuario__username = serializers.CharField(source='usuario.username', read_only=True)
    movimiento_referencia__usuario__username = serializers.CharField(source='movimiento_referencia.usuario.username', read_only=True)
    
    class Meta:
        model = CtnMovimiento
        fields = [            
            'id',   
            'tipo',         
            'fecha',
            'descripcion',
            'vr_total',
            'vr_total_operado',
            'vr_afectado',
            'vr_saldo',            
            'documento_fisico',
            'contenedor_movimiento_id',
            'movimiento_referencia_id',
            'movimiento_referencia__usuario__username',
            'usuario_id',
            'usuario__username',
            'socio_id'
        ]
        select_related_fields = ['usuario', 'movimiento_referencia']      
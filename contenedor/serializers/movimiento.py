from rest_framework import serializers
from contenedor.models import CtnMovimiento


class CtnMovimientoSerializador(serializers.ModelSerializer):  
    usuario__username = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = CtnMovimiento
        fields = [            
            'id',   
            'tipo',         
            'fecha',
            'fecha_vence',
            'descripcion',
            'vr_total',
            'vr_afectado',
            'vr_saldo',            
            'documento_fisico',
            'contenedor_movimiento_id',
            'usuario_id',
            'usuario__username'
        ]
        select_related_fields = ['usuario']      
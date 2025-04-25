from rest_framework import serializers
from ruteo.models.despacho import RutDespacho
from datetime import datetime
from django.utils.timezone import now
from decimal import Decimal

class RutDespachoSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = RutDespacho
        fields = ['id', 'fecha', 'fecha_salida', 'fecha_ubicacion', 'peso', 'volumen', 'tiempo', 'tiempo_servicio', 'tiempo_trayecto',
                  'visitas', 'visitas_entregadas', 'visitas_liberadas', 'vehiculo', 'entrega_id', 'estado_aprobado', 'estado_terminado']

    def to_representation(self, instance):      
        vehiculo_placa = ""
        if instance.vehiculo:
            vehiculo_placa = instance.vehiculo.placa
        return {
            'id': instance.id,  
            'fecha': instance.fecha,
            'fecha_salida': instance.fecha_salida,
            'fecha_ubicacion': instance.fecha_ubicacion,
            'peso': instance.peso,
            'volumen': instance.volumen,
            'tiempo': instance.tiempo,
            'tiempo_servicio': instance.tiempo_servicio,
            'tiempo_trayecto': instance.tiempo_trayecto,
            'visitas': instance.visitas,
            'visitas_entregadas': instance.visitas_entregadas,
            'visitas_liberadas': instance.visitas_liberadas,
            'vehiculo_id': instance.vehiculo_id,
            'vehiculo_placa': vehiculo_placa,
            'entrega_id': instance.entrega_id,
            'estado_aprobado': instance.estado_aprobado,
            'estado_terminado': instance.estado_terminado
        }
    
class RutDespachoTraficoSerializador(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = RutDespacho
        fields = ['id', 'fecha', 'fecha_salida', 'fecha_ubicacion', 'peso', 'volumen', 'tiempo', 'tiempo_servicio', 'tiempo_trayecto',
                  'visitas', 'visitas_entregadas', 'visitas_liberadas', 'vehiculo', 'entrega_id', 'estado_aprobado', 'estado_terminado', 
                  'estado_anulado', 'latitud', 'longitud']

    def to_representation(self, instance):      
        vehiculo_placa = ""
        if instance.vehiculo:
            vehiculo_placa = instance.vehiculo.placa        
        tiempo_trafico = 0
        if instance.fecha_salida:
            fecha_actual = now()
            diferencia = fecha_actual - instance.fecha_salida
            tiempo_trafico = int(diferencia.total_seconds() / 60)
        
        tiempo_promedio_visita = 0
        if instance.visitas > 0:            
            tiempo_promedio_visita = Decimal(instance.tiempo) / Decimal(instance.visitas)
        tiempo_entrega = Decimal(instance.visitas_entregadas) * tiempo_promedio_visita        
        visitas_entregadas_esperadas = round(tiempo_trafico / tiempo_promedio_visita)
        if visitas_entregadas_esperadas > instance.visitas:
            visitas_entregadas_esperadas = instance.visitas
        estado = 'tiempo'
        if visitas_entregadas_esperadas > instance.visitas_entregadas:
            estado = 'retrazado'

        return {
            'id': instance.id,  
            'fecha': instance.fecha,
            'fecha_salida': instance.fecha_salida,
            'fecha_ubicacion': instance.fecha_ubicacion,
            'peso': instance.peso,
            'volumen': instance.volumen,
            'tiempo': instance.tiempo,
            'tiempo_servicio': instance.tiempo_servicio,
            'tiempo_trayecto': instance.tiempo_trayecto,
            'visitas': instance.visitas,
            'visitas_entregadas': instance.visitas_entregadas,
            'visitas_liberadas': instance.visitas_liberadas,
            'visitas_entregadas_esperadas': visitas_entregadas_esperadas,
            'vehiculo_id': instance.vehiculo_id,
            'vehiculo_placa': vehiculo_placa,
            'entrega_id': instance.entrega_id,
            'estado_aprobado': instance.estado_aprobado,
            'estado_terminado': instance.estado_terminado, 
            'estado_anulado': instance.estado_anulado, 
            'tiempo_trafico': tiempo_trafico,
            'estado': estado,
            'latitud' : instance.latitud,
            'longitud' : instance.longitud
        }    
    

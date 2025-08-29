from ruteo.models.visita import RutVisita
from ruteo.models.despacho import RutDespacho
from transporte.models.vehiculo import TteVehiculo
from transporte.serializers.vehiculo import TteVehiculoSerializador
from vertical.models.viaje import VerViaje
from django.db import transaction

class TteDespachoServicio():

    @staticmethod
    def validar_vehiculo_vertical(viaje: VerViaje):    
        if viaje.vehiculo:
            vehiculo = TteVehiculo.objects.filter(placa=viaje.vehiculo.placa).first()
            if vehiculo:
                return vehiculo            
            else:
                if viaje.vehiculo.verificado:
                    data = {
                        'placa': viaje.vehiculo.placa,                        
                        'modelo': viaje.vehiculo.modelo,                                                                        
                        'ejes': viaje.vehiculo.ejes,
                        'peso_vacio': viaje.vehiculo.peso_vacio,
                        "capacidad": viaje.vehiculo.capacidad,
                        "vence_poliza": viaje.vehiculo.vence_poliza,
                        "vence_tecnicomecanica": viaje.vehiculo.vence_tecnicomecanica,
                        "poseedor":1,
                        "propietario":1,
                        "aseguradora": 1,
                        "color":viaje.vehiculo.color_id,
                        "marca": viaje.vehiculo.marca_id,
                        "linea":viaje.vehiculo.linea_id,
                        "combustible":viaje.vehiculo.combustible_id,
                        "carroceria":viaje.vehiculo.carroceria_id,
                        "configuracion":viaje.vehiculo.configuracion_id,                         
                    }
                    serializador_vehiculo = TteVehiculoSerializador(data=data)
                    if serializador_vehiculo.is_valid():
                        vehiculo = serializador_vehiculo.save()
                        return vehiculo
                    else:
                        raise ValueError('Se presentaron errores en el vehiculo: ' + str(serializador_vehiculo.errors))
                else:                    
                    raise ValueError('El vehiculo no existe')
        else:
            raise ValueError('El viaje no tiene vehiculo asignado')        

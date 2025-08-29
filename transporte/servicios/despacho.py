from ruteo.models.despacho import RutDespacho
from transporte.models.vehiculo import TteVehiculo
from general.models.contacto import GenContacto
from transporte.serializers.vehiculo import TteVehiculoSerializador
from general.serializers.contacto import GenContactoSerializador
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
                        'capacidad': viaje.vehiculo.capacidad,
                        'vence_poliza': viaje.vehiculo.vence_poliza,
                        'vence_tecnicomecanica': viaje.vehiculo.vence_tecnicomecanica,
                        'poseedor':1,
                        'propietario':1,
                        'aseguradora': 1,
                        'color':viaje.vehiculo.color_id,
                        'marca': viaje.vehiculo.marca_id,
                        'linea':viaje.vehiculo.linea_id,
                        'combustible':viaje.vehiculo.combustible_id,
                        'carroceria':viaje.vehiculo.carroceria_id,
                        'configuracion':viaje.vehiculo.configuracion_id,                         
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

    @staticmethod
    def validar_conductor_vertical(viaje: VerViaje):    
        if viaje.conductor:
            conductor = GenContacto.objects.filter(identificacion_id=viaje.conductor.identificacion_id, numero_identificacion=viaje.conductor.numero_identificacion).first()
            if conductor:
                return conductor            
            else:
                if viaje.conductor.verificado:
                    data = {
                        'identificacion':viaje.conductor.identificacion_id,
                        'numero_identificacion':viaje.conductor.numero_identificacion,
                        'nombre_corto':viaje.conductor.nombre_corto,
                        'nombre1':viaje.conductor.nombre1,
                        'nombre2':viaje.conductor.nombre2,
                        'apellido1':viaje.conductor.apellido1,
                        'apellido2':viaje.conductor.apellido2,
                        'direccion':viaje.conductor.direccion,
                        'telefono':viaje.conductor.telefono,
                        'ciudad':viaje.conductor.ciudad_id,
                        'correo':viaje.conductor.correo,
                        'tipo_persona':2,
                        'regimen': 2                        
                    }
                    serializador_conductor = GenContactoSerializador(data=data)
                    if serializador_conductor.is_valid():
                        conductor = serializador_conductor.save()
                        return conductor
                    else:
                        raise ValueError('Se presentaron errores en el conductor: ' + str(serializador_conductor.errors))
                else:                    
                    raise ValueError('El conductor no existe')
        else:
            raise ValueError('El viaje no tiene conductor asignado')              

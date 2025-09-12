from transporte.models.negocio import TteNegocio
from transporte.models.despacho_detalle import TteDespachoDetalle
from transporte.models.guia import TteGuia
from transporte.models.vehiculo import TteVehiculo
from general.models.contacto import GenContacto
from transporte.serializers.vehiculo import TteVehiculoSerializador
from transporte.serializers.despacho_detalle import TteDespachoDetalleSerializador
from general.serializers.contacto import GenContactoSerializador
from vertical.models.viaje import VerViaje
from django.db.models import F

class TteNegocioServicio():

    @staticmethod
    def aprobar(negocio: TteNegocio, contenedor_id, schema_name):
        if negocio.estado_aprobado == False:
            if negocio.publicar:
                if negocio.pago > 0 and negocio.contacto is not None and negocio.operacion is not None:                
                    viaje = VerViaje()
                    viaje.servicio_id = negocio.servicio_id
                    viaje.producto_id = negocio.producto_id
                    viaje.empaque_id = negocio.empaque_id
                    viaje.negocio_id = negocio.id   
                    viaje.pago = negocio.pago                         
                    viaje.unidades = negocio.unidades
                    viaje.peso = negocio.peso
                    viaje.volumen = negocio.volumen    
                    viaje.puntos_entrega = negocio.puntos_entrega
                    viaje.ciudad_origen_id = negocio.ciudad_origen_id
                    viaje.ciudad_destino_id = negocio.ciudad_destino_id                       
                    viaje.contenedor_id = contenedor_id
                    viaje.schema_name = schema_name
                    viaje.solicitud_transporte = True                            
                    viaje.save()
            negocio.estado_aprobado = True
            negocio.save()
            return {'error':False}
        else:
            return {'error':True, 'mensaje':'El negocio ya se encuentra aprobado'}  



                 

                 

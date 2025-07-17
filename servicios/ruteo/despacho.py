from ruteo.models.visita import RutVisita
from ruteo.models.despacho import RutDespacho

class DespachoServicio():

    @staticmethod
    def regenerar_valores(despacho: RutDespacho):    
        visitas = RutVisita.objects.filter(despacho_id=despacho.id)
        despacho.peso=0
        despacho.volumen=0
        despacho.tiempo=0
        despacho.tiempo_servicio=0
        despacho.tiempo_trayecto=0
        despacho.visitas=0
        for visita in visitas:
            despacho.peso+=visita.peso
            despacho.volumen+=visita.volumen
            despacho.tiempo+=visita.tiempo
            despacho.tiempo_servicio+=visita.tiempo_servicio
            despacho.tiempo_trayecto+=visita.tiempo_trayecto
            despacho.visitas +=1
        despacho.save()
        
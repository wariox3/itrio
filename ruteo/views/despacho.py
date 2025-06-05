from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ruteo.models.despacho import RutDespacho
from ruteo.models.visita import RutVisita
from ruteo.models.vehiculo import RutVehiculo
from vertical.models.entrega import VerEntrega
from seguridad.models import User
from ruteo.serializers.despacho import RutDespachoSerializador
from django.http import HttpResponse
from openpyxl import Workbook
from utilidades.workbook_estilos import WorkbookEstilos
from datetime import datetime
from django.db import transaction

class RutDespachoViewSet(viewsets.ModelViewSet):
    queryset = RutDespacho.objects.all()
    serializer_class = RutDespachoSerializador
    permission_classes = [permissions.IsAuthenticated]      

    def destroy(self, request, *args, **kwargs):        
        instance = self.get_object()
        if instance.estado_aprobado:
                return Response({'mensaje': 'No se puede eliminar un despacho aprobado.'}, status=status.HTTP_400_BAD_REQUEST)        
        RutVisita.objects.filter(despacho_id=instance.id).update(despacho=None, estado_despacho=False)
        if instance.vehiculo_id:
            RutVehiculo.objects.filter(id=instance.vehiculo_id).update(estado_asignado=False)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
    @action(detail=False, methods=["post"], url_path=r'aprobar',)
    def aprobar(self, request):             
        raw = request.data
        id = raw.get('id')
        if id:
            try:                
                with transaction.atomic():               
                    despacho = RutDespacho.objects.get(pk=id)  
                    if despacho.estado_aprobado == False: 
                        entrega = VerEntrega()
                        entrega.despacho_id = despacho.id
                        entrega.fecha = despacho.fecha
                        entrega.peso = despacho.peso
                        entrega.volumen = despacho.volumen
                        entrega.tiempo_servicio = despacho.tiempo_servicio
                        entrega.tiempo_trayecto = despacho.tiempo_trayecto
                        entrega.tiempo = despacho.tiempo
                        entrega.visitas = despacho.visitas
                        entrega.visitas_entregadas = despacho.visitas_entregadas
                        entrega.contenedor_id = request.tenant.id
                        entrega.schema_name = request.tenant.schema_name
                        entrega.save()                   
                        despacho.estado_aprobado = True
                        despacho.fecha_salida = datetime.now()
                        despacho.entrega_id = entrega.id             
                        despacho.save()                             
                        return Response({'mensaje': 'Se aprobo el despacho'}, status=status.HTTP_200_OK)                
                    else:
                        return Response({'mensaje':'El despacho ya esta aprobado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                        
            except RutDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)     

    @action(detail=False, methods=["post"], url_path=r'terminar',)
    def terminar(self, request):             
        raw = request.data
        id = raw.get('id')
        if id:
            try:                
                despacho = RutDespacho.objects.get(pk=id)  
                if despacho.estado_aprobado == True:
                    if despacho.estado_terminado == False:
                        visitas = RutVisita.objects.filter(despacho_id=id, estado_entregado=False).first()
                        if visitas:
                            return Response({'mensaje':'El despacho tiene visitas sin entregar', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                        despacho.estado_terminado = True                
                        despacho.save()              
                        vehiculo = RutVehiculo.objects.get(pk=despacho.vehiculo_id)
                        vehiculo.estado_asignado = False
                        vehiculo.save() 
                        return Response({'mensaje': 'Se termino el despacho'}, status=status.HTTP_200_OK)                
                    else:
                        return Response({'mensaje':'El despacho ya esta terminado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                                                
                else:
                    return Response({'mensaje':'El despacho no esta aprobado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                        
            except RutDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=["post"], url_path=r'anular',)
    def anular(self, request):             
        raw = request.data
        id = raw.get('id')
        if id:
            try:                
                despacho = RutDespacho.objects.get(pk=id)  
                if despacho.estado_aprobado == True and despacho.estado_anulado == False and despacho.estado_terminado == False:
                    visitas = RutVisita.objects.filter(despacho_id=id, estado_entregado=True).first()
                    if visitas:
                        return Response({'mensaje':'El despacho tiene visitas entregadas', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                    visitas = RutVisita.objects.filter(despacho_id=id)
                    for visita in visitas:
                        visita.estado_despacho = False
                        visita.despacho = None
                        visita.save()
                    despacho.estado_anulado = True
                    despacho.estado_terminado = True                                    
                    despacho.save()   
                    vehiculo = RutVehiculo.objects.get(pk=despacho.vehiculo_id)
                    vehiculo.estado_asignado = False
                    vehiculo.save() 

                    return Response({'mensaje': 'Se anulo el despacho'}, status=status.HTTP_200_OK)                                                              
                else:
                    return Response({'mensaje':'El despacho debe estar aprobado, sin terminar y sin anular', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                        
            except RutDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST) 

    @action(detail=False, methods=["post"], url_path=r'visita-adicionar',)
    def visita_adicionar(self, request):             
        raw = request.data
        id = raw.get('id')
        visita_id = raw.get('visita_id')
        trafico = raw.get('trafico', False)
        if id and visita_id:
            try:                
                despacho = RutDespacho.objects.get(pk=id)  
                if despacho.estado_terminado == False:
                    visita = RutVisita.objects.get(pk=visita_id)
                    if visita.estado_despacho == True: 
                        if trafico == False:
                            return Response({'mensaje':'La visita esta en otro despacho', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            despacho_origen = RutDespacho.objects.get(pk=visita.despacho_id)
                            despacho_origen.peso = despacho_origen.peso - visita.peso
                            despacho_origen.volumen = despacho_origen.volumen - visita.volumen
                            despacho_origen.tiempo = despacho_origen.tiempo - visita.tiempo
                            despacho_origen.tiempo_servicio = despacho_origen.tiempo_servicio - visita.tiempo_servicio
                            despacho_origen.tiempo_trayecto = despacho_origen.tiempo_trayecto - visita.tiempo_trayecto
                            despacho_origen.visitas = despacho_origen.visitas - 1                                   
                            despacho_origen.save()                                
                    visita.despacho = despacho
                    visita.estado_despacho = True
                    visita.save()                            
                    despacho.peso = despacho.peso + visita.peso
                    despacho.volumen = despacho.volumen + visita.volumen
                    despacho.tiempo = despacho.tiempo + visita.tiempo
                    despacho.tiempo_servicio = despacho.tiempo_servicio + visita.tiempo_servicio
                    despacho.tiempo_trayecto = despacho.tiempo_trayecto + visita.tiempo_trayecto
                    despacho.visitas = despacho.visitas + 1                                   
                    despacho.save()               
                    return Response({'mensaje': 'Se adiciono la visita'}, status=status.HTTP_200_OK)                              
                else:
                    return Response({'mensaje':'El despacho esta terminado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                        
            except RutDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
            except RutVisita.DoesNotExist:
                return Response({'mensaje':'La visita no existe', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)            
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'trasbordar',)
    def trasbordar(self, request):             
        raw = request.data
        id = raw.get('id')
        despacho_origen_id = raw.get('despacho_origen_id')        
        if id and despacho_origen_id:
            try:                
                despacho = RutDespacho.objects.get(pk=id)
                despacho_origen = RutDespacho.objects.get(pk=despacho_origen_id)  
                if despacho.estado_aprobado == False:
                    if despacho_origen.estado_terminado == False:
                        visitas = RutVisita.objects.filter(despacho_id=despacho_origen_id, estado_entregado=False)
                        for visita in visitas:                                                                                
                            despacho_origen.peso = despacho_origen.peso - visita.peso
                            despacho_origen.volumen = despacho_origen.volumen - visita.volumen
                            despacho_origen.tiempo = despacho_origen.tiempo - visita.tiempo
                            despacho_origen.tiempo_servicio = despacho_origen.tiempo_servicio - visita.tiempo_servicio
                            despacho_origen.tiempo_trayecto = despacho_origen.tiempo_trayecto - visita.tiempo_trayecto
                            despacho_origen.visitas = despacho_origen.visitas - 1                                   
                            despacho_origen.save()                                

                            despacho.peso = despacho.peso + visita.peso
                            despacho.volumen = despacho.volumen + visita.volumen
                            despacho.tiempo = despacho.tiempo + visita.tiempo
                            despacho.tiempo_servicio = despacho.tiempo_servicio + visita.tiempo_servicio
                            despacho.tiempo_trayecto = despacho.tiempo_trayecto + visita.tiempo_trayecto
                            despacho.visitas = despacho.visitas + 1                                   
                            despacho.save()               

                            visita.despacho = despacho
                            visita.save()
                        return Response({'mensaje': 'Se trasbordaron las visitas pendientes por entrega'}, status=status.HTTP_200_OK)                            
                    else:                          
                        return Response({'mensaje':'El despacho origen no puede estar terminado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'mensaje':'El despacho no puede estar aprobado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                        
            except RutDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], url_path=r'plano-semantica',)
    def plano_semantica(self, request):             
        raw = request.data
        id = raw.get('id')
        if id:
            try:                
                despacho = RutDespacho.objects.get(pk=id)    
                visitas = RutVisita.objects.filter(despacho_id=id).values('numero').order_by('orden')                
                field_names = list(visitas[0].keys()) if visitas else []
                field_names.append('orden')
                orden = 0
                wb = Workbook()
                ws = wb.active
                ws.append(field_names)
                for row in visitas:
                    orden += 1                    
                    row_data = []
                    # -1 para que no tome orden
                    for field in field_names[:-1]:
                        value = row.get(field)
                        if value is None:
                            row_data.append("")
                        elif isinstance(value, datetime) and value.tzinfo is not None:
                            row_data.append(value.replace(tzinfo=None))
                        else:
                            row_data.append(value) 
                    row_data.append(orden)                       
                    ws.append(row_data)
                estilos_excel = WorkbookEstilos(wb)
                estilos_excel.aplicar_estilos()         
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Access-Control-Expose-Headers'] = 'Content-Disposition'
                response['Content-Disposition'] = f'attachment; filename=visitas.xlsx'
                wb.save(response)
                return response
            except RutDespacho.DoesNotExist:
                return Response({'mensaje':'El despacho no existe', 'codigo':15}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'mensaje':'Faltan parametros', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)  

    @action(detail=False, methods=["post"], url_path=r'tablero-trafico',)
    def tablero_trafico(self, request): 
        despachos = RutDespacho.objects.filter(
                        estado_aprobado=True, estado_terminado=False                                               
                    )           
        return Response({'mensaje': 'Se aprobo el despacho'}, status=status.HTTP_200_OK)  
               
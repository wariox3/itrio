from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ruteo.models.despacho import RutDespacho
from ruteo.models.visita import RutVisita
from ruteo.serializers.despacho import RutDespachoSerializador
from django.http import HttpResponse
from openpyxl import Workbook
from utilidades.excel import WorkbookEstilos
from datetime import datetime

class RutDespachoViewSet(viewsets.ModelViewSet):
    queryset = RutDespacho.objects.all()
    serializer_class = RutDespachoSerializador
    permission_classes = [permissions.IsAuthenticated]      

    def destroy(self, request, *args, **kwargs):        
        instance = self.get_object()
        if instance.estado_aprobado:
                return Response({'mensaje': 'No se puede eliminar un despacho aprobado.'}, status=status.HTTP_400_BAD_REQUEST)        
        RutVisita.objects.filter(despacho_id=instance.id).update(despacho=None, estado_despacho=False)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)    
    
    @action(detail=False, methods=["post"], url_path=r'aprobar',)
    def aprobar(self, request):             
        raw = request.data
        id = raw.get('id')
        if id:
            try:                
                despacho = RutDespacho.objects.get(pk=id)  
                if despacho.estado_aprobado == False:
                    despacho.estado_aprobado = True                
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
                        despacho.estado_terminado = True                
                        despacho.save()               
                        return Response({'mensaje': 'Se termino el despacho'}, status=status.HTTP_200_OK)                
                    else:
                        return Response({'mensaje':'El despacho ya esta terminado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                                                
                else:
                    return Response({'mensaje':'El despacho no esta aprobado', 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)                        
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
             
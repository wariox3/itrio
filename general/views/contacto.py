from rest_framework import viewsets, permissions, status
from general.models.contacto import GenContacto
from general.serializers.contacto import GenContactoSerializador, GenContactoExcelSerializador
from rest_framework.response import Response
from rest_framework.decorators import action
from openpyxl import Workbook
from django.http import HttpResponse

class ContactoViewSet(viewsets.ModelViewSet):
    queryset = GenContacto.objects.all()
    serializer_class = GenContactoSerializador    
    permission_classes = [permissions.IsAuthenticated]               

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        relaciones = instance.contactos_rel.first()
        if relaciones:
            modelo_asociado = relaciones.__class__.__name__           
            return Response({'mensaje':f"El registro no se puede eliminar porque tiene registros asociados en {modelo_asociado}", 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=["post"], url_path=r'excel',)
    def excel(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 5000)    
        limiteTotal = raw.get('limite_total', 5000)                
        filtros = raw.get('filtros', [])        
        ordenamientos = raw.get('ordenamientos', [])    
        ordenamientos.append('-id')                 
        respuesta = ContactoViewSet.listar(desplazar, limite, limiteTotal, filtros, ordenamientos)
        serializador = GenContactoExcelSerializador(respuesta['contactos'], many=True)
        contactos = serializador.data
        if contactos:
            field_names = list(contactos[0].keys())
        else:
            field_names = []

        wb = Workbook()
        ws = wb.active
        ws.append(field_names)
        for row in contactos:
            row_data = [row[field] for field in field_names]
            ws.append(row_data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        response['Content-Disposition'] = 'attachment; filename=contactos.xlsx'
        wb.save(response)
        return response

        
    @staticmethod
    def listar(desplazar, limite, limiteTotal, filtros, ordenamientos):
        contactos = GenContacto.objects.all()
        if filtros:
            for filtro in filtros:
                contactos = contactos.filter(**{filtro['propiedad']: filtro['valor1']})
        if ordenamientos:
            contactos = contactos.order_by(*ordenamientos)              
        contactos = contactos[desplazar:limite+desplazar]
        itemsCantidad = GenContacto.objects.all()[:limiteTotal].count()                   
        respuesta = {'contactos': contactos, "cantidad_registros": itemsCantidad}
        return respuesta     
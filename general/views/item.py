from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from general.models.documento_detalle import GenDocumentoDetalle
from general.models.item import GenItem
from general.models.item_impuesto import GenItemImpuesto
from general.serializers.item import GenItemSerializador, GenItemExcelSerializador
from general.serializers.item_impuesto import GenItemImpuestoSerializador, GenItemImpuestoDetalleSerializador
from rest_framework.decorators import action
from openpyxl import Workbook
from django.http import HttpResponse

class ItemViewSet(viewsets.ModelViewSet):
    queryset = GenItem.objects.all()
    serializer_class = GenItemSerializador
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, pk=None, venta=False):
        raw = request.data
        venta = raw.get('venta')
        queryset = GenItem.objects.all()
        item = get_object_or_404(queryset, pk=pk)
        itemSerializador = GenItemSerializador(item)
        itemImpuestos = GenItemImpuesto.objects.filter(item=pk)
        if venta:
            itemImpuestos = itemImpuestos.filter(impuesto__venta=True)
        itemImpuestosSerializador = GenItemImpuestoDetalleSerializador(itemImpuestos, many=True)
        itemRespuesta = itemSerializador.data
        itemRespuesta['impuestos'] = itemImpuestosSerializador.data
        return Response({'item':itemRespuesta}, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        itemSerializador = GenItemSerializador(data=request.data)
        if itemSerializador.is_valid():
            item = itemSerializador.save()            
            impuestos = data.get('impuestos')
            if impuestos is not None:
                for impuesto in impuestos:                
                    datosImpuestoItem = {"item":item.id,"impuesto":impuesto['impuesto']}
                    itemImpuestoSerializador = GenItemImpuestoSerializador(data=datosImpuestoItem)
                    if itemImpuestoSerializador.is_valid():
                        itemImpuestoSerializador.save()                
            itemImpuestos = GenItemImpuesto.objects.filter(item=item.id)
            itemImpuestosSerializador = GenItemImpuestoDetalleSerializador(itemImpuestos, many=True)
            itemRespuesta = itemSerializador.data
            itemRespuesta['impuestos'] = itemImpuestosSerializador.data
            return Response({'item':itemRespuesta}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': itemSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        raw = request.data
        item = self.get_object()    
        itemSerializador = self.serializer_class(instance=item, data=raw, partial=True)
        if itemSerializador.is_valid():
            itemSerializador.save()
            impuestosNuevos = raw.get('impuestos')
            if impuestosNuevos is not None:
                for impuesto in impuestosNuevos:                
                    impuesto['item'] = item.id
                    itemImpuestoSerializador = GenItemImpuestoSerializador(data=impuesto)
                    if itemImpuestoSerializador.is_valid():
                        itemImpuestoSerializador.save() 
            impuestosEliminados = raw.get('impuestos_eliminados')
            if impuestosEliminados is not None:
                for itemImpuestoEliminado in impuestosEliminados:                                
                    itemImpuesto = GenItemImpuesto.objects.get(pk=itemImpuestoEliminado)
                    itemImpuesto.delete()
            itemImpuestos = GenItemImpuesto.objects.filter(item=item.id)
            itemImpuestosSerializador = GenItemImpuestoDetalleSerializador(itemImpuestos, many=True)
            itemRespuesta = itemSerializador.data
            itemRespuesta['impuestos'] = itemImpuestosSerializador.data                    
            return Response({'item':itemRespuesta}, status=status.HTTP_200_OK)
        return Response({'mensaje':'Errores de validacion', 'codigo':14, 'validaciones': itemSerializador.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        relaciones = instance.itemes_rel.first()
        if relaciones:
            modelo_asociado = relaciones.__class__.__name__           
            return Response({'mensaje':f"El registro no se puede eliminar porque tiene registros asociados en {modelo_asociado}", 'codigo':1}, status=status.HTTP_400_BAD_REQUEST)        
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=["post"], url_path=r'lista',)
    def lista(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 50)    
        cantidadLimite = raw.get('cantidad_limite', 5000)    
        filtros = raw.get('filtros')
        ordenamientos = raw.get('ordenamientos')
        items = GenItem.objects.all()
        if filtros:
            for filtro in filtros:
                items = items.filter(**{filtro['propiedad']: filtro['valor1']})
        if ordenamientos:
            items = items.order_by(*ordenamientos)              
        items = items[desplazar:limite+desplazar]
        itemsCantidad = GenItem.objects.all()[:cantidadLimite].count()
        #consumos = Item.objects.aggregate(cantidad=Count('id'))
        #consulta_sql = str(items.query)
        #print(consulta_sql)
        ItemSerializador = ItemSerializador(items, many=True)
        return Response({"registros": ItemSerializador.data, "cantidad_registros": itemsCantidad}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["post"], url_path=r'detalle',)
    def detalle(self, request):
        raw = request.data
        id = raw.get('id')
        venta = raw.get('venta')
        compra = raw.get('compra')
        if(id):
            queryset = GenItem.objects.all()
            item = get_object_or_404(queryset, pk=id)
            itemSerializador = GenItemSerializador(item)
            itemImpuestos = GenItemImpuesto.objects.filter(item=id)
            if venta:
                itemImpuestos = itemImpuestos.filter(impuesto__venta=True)
            if compra:
                itemImpuestos = itemImpuestos.filter(impuesto__compra=True)
            itemImpuestosSerializador = GenItemImpuestoDetalleSerializador(itemImpuestos, many=True)
            itemRespuesta = itemSerializador.data
            itemRespuesta['impuestos'] = itemImpuestosSerializador.data
            return Response({'item':itemRespuesta}, status=status.HTTP_200_OK)
        else:
            return Response({'mensaje': 'Faltan parámetros', 'codigo': 1}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=False, methods=["post"], url_path=r'excel',)
    def excel(self, request):
        raw = request.data
        desplazar = raw.get('desplazar', 0)
        limite = raw.get('limite', 5000)    
        limiteTotal = raw.get('limite_total', 5000)                
        filtros = raw.get('filtros', [])        
        ordenamientos = raw.get('ordenamientos', [])    
        ordenamientos.append('-id')                 
        respuesta = ItemViewSet.listar(desplazar, limite, limiteTotal, filtros, ordenamientos)
        serializador = GenItemExcelSerializador(respuesta['items'], many=True)
        items = serializador.data
        if items:
            field_names = list(items[0].keys())
        else:
            field_names = []

        wb = Workbook()
        ws = wb.active
        ws.append(field_names)
        for row in items:
            row_data = [row[field] for field in field_names]
            ws.append(row_data)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Access-Control-Expose-Headers'] = 'Content-Disposition'
        response['Content-Disposition'] = 'attachment; filename=items.xlsx'
        wb.save(response)
        return response

        
    @staticmethod
    def listar(desplazar, limite, limiteTotal, filtros, ordenamientos):
        items = GenItem.objects.all()
        if filtros:
            for filtro in filtros:
                items = items.filter(**{filtro['propiedad']: filtro['valor1']})
        if ordenamientos:
            items = items.order_by(*ordenamientos)              
        items = items[desplazar:limite+desplazar]
        itemsCantidad = GenItem.objects.all()[:limiteTotal].count()                   
        respuesta = {'items': items, "cantidad_registros": itemsCantidad}
        return respuesta     